from django.urls import path
from . import views


urlpatterns = [
    path('', views.books, name='books'),
    path('category/<slug:category_slug>/', views.books, name='category_wise_books'),
    path('book_details/<int:id>/', views.bookDetails, name='book_details'),
    path('borrow_book/<int:book_id>/', views.borrowBook, name='borrow_book'),
    path('return_book/<int:borrow_id>/', views.returnBook, name='return_book'),
    path('books/borrowed/', views.borrowedBooks, name='borrowed_books'),
]
