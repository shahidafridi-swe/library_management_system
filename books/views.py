from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from .models import Book, Category,Borrow


from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def books(request, category_slug=None):
    books = Book.objects.all()
    categories = Category.objects.all()
    
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        books = Book.objects.filter(category=category)
    
    context= {
        'books':books,
        'categories':categories,
    }
    # print(books)
    return render(request, 'books/books.html', context)


def bookDetails(request, id):
    book = Book.objects.get(pk=id)
    commentable = False
    if request.user.is_authenticated:
        commentable = Borrow.objects.filter(book=book, user=request.user).exists()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.name = request.user.username
            comment.email = request.user.email
            comment.save()    
            messages.success(request, 'Review successfull !!!')
            return redirect('book_details', id =id)
    else:
        form = ReviewForm()
        
    
    context = {
        'book' : book,
        'comment_form': form,
        'commentable': commentable
    }
    return render(request, 'books/book_details.html', context)

@login_required(login_url='login')
def borrowBook(request, book_id):
    book = Book.objects.get(id=book_id)
    user = request.user
    
    existing_borrow = Borrow.objects.filter(book=book, user=user, book_returned=False).exists()

    if existing_borrow:
        messages.error(request, "You have already borrowed this book and have not returned it yet.")
        return redirect('book_details', id=book_id)

    if user.account.balance < book.borrow_price:
        messages.error(request, "Sorry, you do not have enough money to borrow this book!")
        return redirect('book_details', id=book_id)

    user.account.balance -= book.borrow_price
    user.account.save()
    borrow = Borrow.objects.create(book=book, user=user)
    messages.success(request, "You have successfully borrowed the book!")
    #email
    email_message  = render_to_string('books/borrow_book_email.html', {
        'user' : request.user,
        'borrow' : borrow,
    })
    send_email = EmailMultiAlternatives('Boorrow Book', '', to=[request.user.email])
    send_email.attach_alternative(email_message , 'text/html')
    send_email.send()

    return redirect('book_details', id=book_id)

@login_required(login_url='login')
def returnBook(request, borrow_id):
    user = request.user
    borrow = Borrow.objects.get(id=borrow_id)    
    borrow.book_returned = True
    borrow.save()
    
    user.account.balance += borrow.book.borrow_price
    user.account.save()
    messages.success(request, "You have successfully return the book!")
    
    #email
    email_message  = render_to_string('books/return_book_email.html', {
        'user' : request.user,
        'borrow' : borrow,
    })
    send_email = EmailMultiAlternatives('Return Book', '', to=[request.user.email])
    send_email.attach_alternative(email_message , 'text/html')
    send_email.send()
    return redirect('borrowed_books')



@login_required(login_url='login')
def borrowedBooks(request):
    user = request.user
    borrows = Borrow.objects.filter(user=user)
    return render(request, 'books/borrow_history.html', {'borrows': borrows})