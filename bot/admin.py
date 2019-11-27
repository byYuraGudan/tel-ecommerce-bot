from django.contrib import admin

from bot.models import TelegramUser, TypeBook, File, Author, Book, Basket, ListBasket, Like, Purchase


class ListBasketInLine(admin.TabularInline):
    model = ListBasket
    fk_name = 'basket_id'


class BookInLineTypeBook(admin.TabularInline):
    model = Book
    fk_name = 'type_id'


class BookInLineTypeAuthor(admin.TabularInline):
    model = Book
    fk_name = 'author_id'


class BasketInLine(admin.TabularInline):
    model = Basket
    fk_name = 'basket_id'


class BasketAdmin(admin.ModelAdmin):
    inlines = [ListBasketInLine]


class TypeBookAdmin(admin.ModelAdmin):
    inlines = [BookInLineTypeBook]


class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInLineTypeAuthor]


admin.site.register(TelegramUser)
admin.site.register(TypeBook, TypeBookAdmin)
admin.site.register(File)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book)
admin.site.register(Basket, BasketAdmin)
admin.site.register(ListBasket)
admin.site.register(Like)
admin.site.register(Purchase)
