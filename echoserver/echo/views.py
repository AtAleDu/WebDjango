import json
from django.shortcuts import  get_object_or_404
from .models import Book, CartItem
from .forms import BookForm, SignUpForm, LoginForm
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import  user_passes_test
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .forms import UserProfileForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cart
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def create_order(request):
    # Получаем корзину пользователя
    cart = get_object_or_404(Cart, user=request.user)

    # Создаем новый заказ
    order = Order.objects.create(
        user=request.user,
        total_price=cart.total_price
    )

    # Переносим товары из корзины в заказ
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            book=cart_item.book,
            quantity=cart_item.quantity,
            price=cart_item.book.price
        )

    # Очищаем корзину после создания заказа
    cart.items.all().delete()

    # Перенаправляем пользователя на страницу с деталями заказа
    return redirect('order_detail', order_id=order.id)


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/view_cart.html', {'cart': cart})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('book_list')

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('book_list')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        User = get_user_model()  # Получаем кастомную модель пользователя
        exists = User.objects.filter(username=username).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def user_logout(request):
    logout(request)
    return redirect('book_list')

def is_admin(user):
    return user.role == 'admin'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # Аутентифицируем пользователя
            if user is not None:
                login(request, user)  # Входим в систему
                return redirect('book_list')  # Перенаправляем на главную страницу
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('book_list')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

# Отображение списка книг
def book_list(request):
    books = Book.objects.all()

    # Фильтрация по автору
    author = request.GET.get('author')
    if author:
        books = books.filter(author__icontains=author)

    # Фильтрация по названию
    title = request.GET.get('title')
    if title:
        books = books.filter(title__icontains=title)

    # Сортировка по цене
    sort = request.GET.get('sort')
    if sort == 'price_desc':
        books = books.order_by('-price')  # Сортировка по убыванию цены
    elif sort == 'price_asc':
        books = books.order_by('price')  # Сортировка по возрастанию цены

    # Пагинация
    paginator = Paginator(books, 10)  # 10 книг на странице
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    return render(request, 'books/book_list.html', {'books': books})

# Отображение деталей книги
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Получаем книгу по её ID
    return render(request, 'books/book_detail.html', {'book': book})

# Добавление новой книги
@login_required
def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_edit.html', {'form': form})

# Редактирование существующей книги
@user_passes_test(is_admin)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_edit.html', {'form': form})

# Удаление книги
@user_passes_test(is_admin)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')
