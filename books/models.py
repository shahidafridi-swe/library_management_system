from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    borrow_price = models.IntegerField()
    image = models.ImageField(upload_to='books/upload', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self) -> str:
        return self.title
    

    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    borrow_time = models.DateTimeField(auto_now_add=True)
    book_returned = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.book.title} - {self.user.username}"
    
    class Meta:
        ordering = ['-borrow_time']