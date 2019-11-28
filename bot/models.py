from django.db import models


class TelegramUser(models.Model):
    full_name = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=100)
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.id, self.full_name)


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


class Basket(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    telegram_user_id = models.ForeignKey(TelegramUser, on_delete=models.PROTECT)
    tolal_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.telegram_user_id)


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