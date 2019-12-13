from django.db import models


class TelegramUser(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=100)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.id, self.full_name)

    @classmethod
    def get_user(cls, user):
        try:
            user = TelegramUser.objects.get(id=user.id)
        except TelegramUser.DoesNotExist:
            user = TelegramUser.objects.create(id=user.id, full_name='{} {}'.format(user.first_name, user.last_name),
                                               username=user.username or ' ')
        return user


class TypeBook(models.Model):
    name = models.CharField(max_length=100, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)


class File(models.Model):
    name = models.CharField(max_length=100, null=False)
    file = models.BinaryField(null=True)
    type = models.CharField(max_length=15)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)


class Author(models.Model):
    full_name = models.CharField(max_length=100, null=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.id, self.full_name)


class Book(models.Model):
    type_id = models.ForeignKey(TypeBook, on_delete=models.PROTECT)
    file_id = models.OneToOneField(File, on_delete=models.PROTECT, blank=False)
    author_id = models.ForeignKey(Author, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, null=False)
    image = models.BinaryField(null=True)
    year = models.DateField()
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hidden = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)

    def show_details(self):
        details = "Назва книжки: {}\nКаталог: {}\nАвтор: {}\nРік видання:{} Ціна: {}".format(
            self.name, self.type_id.name, self.author_id.full_name, self.year, self.price)
        return details

    def check_book_in_basket(self, user):
        check_book = ListBasket.objects.filter(book_id=self, basket_id__telegram_user_id=user)
        if check_book.exists():
            check_book = ListBasket.objects.get(book_id=self, basket_id__telegram_user_id=user)
            if check_book.basket_id.is_active:
                return False
            return True
        return None

    def get_likes(self):
        return Like.objects.filter(book_id=self).count()

    def set_likes(self, user):
        book_likes = Like.objects.filter(book_id=self, telegram_user_id=user)
        if book_likes.exists():
            return book_likes.delete()
        return Like.objects.create(book_id=self, telegram_user_id=user)

    @classmethod
    def get_top_books(cls, limit=10):
        return Book.objects.exclude(hidden=True).annotate(likes=models.Count('like')).order_by('-likes')[:limit]

    @classmethod
    def get_top_purchase_books(cls, limit=10):
        return Book.objects.exclude(hidden=True).annotate(
            cnt=models.Count('listbasket', filter=models.Q(listbasket__basket_id__purchase__is_sold=True))
        ).filter(cnt__gt=0)[:limit]

    @classmethod
    def get_new_books(cls, limit=10):
        return Book.objects.exclude(hidden=True).order_by('-date')[:limit]

    @classmethod
    def get_user_books(cls, user):
        return Book.objects.filter(listbasket__basket_id__purchase__is_sold=True,
                                   listbasket__basket_id__telegram_user_id=user)


class Basket(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    telegram_user_id = models.ForeignKey(TelegramUser, on_delete=models.PROTECT)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.telegram_user_id)

    @classmethod
    def get_basket_user(cls, user):
        basket = Basket.objects.filter(telegram_user_id=user, is_active=True)
        if basket.exists():
            return Basket.objects.get(telegram_user_id=user, is_active=True)
        return Basket.objects.create(telegram_user_id=user, is_active=True)

    @classmethod
    def add_item_basket(cls, basket, book):
        if ListBasket.objects.filter(basket_id=basket, book_id=book).exists():
            return True
        ListBasket.objects.create(basket_id=basket, book_id=book, price=book.price)
        basket.total_price += book.price
        basket.save()

    @classmethod
    def delete_item_basket(cls, basket, book):
        if not ListBasket.objects.filter(basket_id=basket, book_id=book).exists():
            return True
        item = ListBasket.objects.get(basket_id=basket, book_id=book)
        basket.total_price -= item.price
        basket.save()
        item.delete()

    def clear_basket(self):
        self.total_price = 0
        self.save()
        return ListBasket.objects.filter(basket_id=self.id).delete()

    def get_list_basket(self):
        return ListBasket.objects.filter(basket_id=self.id)

    @classmethod
    def get_basket_by_id(cls, basket_id):
        basket = Basket.objects.filter(id=basket_id)
        if basket.exists():
            return Basket.objects.get(id=basket_id)
        return None


class ListBasket(models.Model):
    basket_id = models.ForeignKey(Basket, on_delete=models.PROTECT)
    book_id = models.ForeignKey(Book, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}.{} - {}'.format(self.basket_id, self.id, self.book_id)


class Like(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    telegram_user_id = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    rating = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return '{}.{} - {}'.format(self.telegram_user_id, self.book_id, self.rating)


class Purchase(models.Model):
    basket_id = models.ForeignKey(Basket, on_delete=models.PROTECT)
    datetime = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_id = models.CharField(max_length=100)
    is_sold = models.BooleanField(default=False)
