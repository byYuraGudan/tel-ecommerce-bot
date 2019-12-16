from django.shortcuts import render

from bot.models import Book


def detail_book(request, book_id):
    fields = ['id', 'type_id__name', 'author_id__full_name', 'name', 'year', 'description', 'price', 'date',
              'language', 'page_count', 'publishing', 'image']
    book = Book.objects.filter(id=book_id).values(*fields).first()
    return render(request, 'book/detail.html', context={'book_detail': book})
