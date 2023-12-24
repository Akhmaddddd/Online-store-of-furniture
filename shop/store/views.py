from random import randint

from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import LoginForm, RegisterForm, CustomerForm, ShippingForm,EditProfileForm,EditAccountFrom
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import CartForAuthenticatedUser, get_cart_data
from shop import settings
import stripe


# Create your views here.

class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    extra_context = {
        'title': 'Главная страница'

    }
    template_name = 'store/product_list.html'

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)

        return categories


class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/category_page.html'

    def get_queryset(self):
        main_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategory = main_category.subcategories.all()
        products = Product.objects.filter(category__in=subcategory)
        print(products)
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        main_category = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'Категория: {main_category.title}'
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'{product.category}: {product.title}'
        fav = len(FavoriteProduct.objects.filter(product=product))
        context['fav'] =fav
        images = product.images.all()
        if images:
            context['product_image_1'] = images[0]

        products = Product.objects.all()
        data = []
        for i in range(4):
            random_index = randint(0, len(products) - 1)
            p = products[random_index]
            if p not in data:
                data.append(p)
        context['products'] = data
        colors = product.colors.all()
        for i in colors:
            i = i.color
        context['colors'] = i
        return context


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            profile = Profile.objects.create(user=user)
            order = Customer.objects.create(user=user)
            profile.save()
            order.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('product_list')
        else:
            for field in register_form.errors:
                messages.error(request, register_form.errors[field].as_text())
                return redirect('register')


    else:
        register_form = RegisterForm()
    context = {
        'title': 'Авторизация',

        'register_form': register_form,
    }
    return render(request, 'store/register.html', context)


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            if user:
                login(request, user)  # Вызвали функцию для логина
                messages.success(request, 'Вы вошли в Аккаунт')
                return redirect('product_list')
            else:
                messages.error(request, 'Не верный логин или пароль')
                return redirect('login')
        else:
            messages.error(request, 'Не верный логин или пароль')
            return redirect('login')

    else:
        login_form = LoginForm()

    context = {
        'title': 'Авторизация',
        'login_form': login_form,

    }

    return render(request, 'store/login.html', context)


def user_logout(request):
    logout(request)
    page = request.META.get('HTTP_REFERER', 'product_list')
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect(page)


# class SearchResults(ListView):
#     model = Product
#     context_object_name = 'categories'
#     extra_context = {
#         'title': 'Главная страница'
#
#     }
#     template_name = 'store/search.html'
#     def get_queryset(self):
#         categories = Category.objects.filter(parent=None)
#         return categories


class SearchResults(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/search.html'

    def get_queryset(self):
        word = self.request.GET.get('q')
        products = Product.objects.filter(title__icontains=word)
        for i in products:
            print(i.price)
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        word = self.request.GET.get('q')
        context['q_name'] = word
        return context


# def search(request):
#     word = request.GET.get('q')
#     products = Product.objects.filter(title__icontains=word)
#     for i in products:
#         print(i.price)
#     return render(request,'store/search.html',products)


def save_favorite_products(request, slug):
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(slug=slug)
        favorite_products = FavoriteProduct.objects.filter(user=user)
        if user:
            if product in [i.product for i in favorite_products]:
                fav_product = FavoriteProduct.objects.get(user=user, product=product)
                fav_product.delete()
                messages.error(request, 'Товар удалён из Избранного')
            else:
                FavoriteProduct.objects.create(user=user, product=product)
                messages.success(request, 'Товар добавлен в Избранное')
    else:
        messages.error(request, 'Авторизуйтесь чтобы добавить в избранное')
    page = request.META.get('HTTP_REFERER', 'product_list')

    return redirect(page)


class FavoriteProductView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    context_object_name = 'products'
    template_name = 'store/favorite.html'
    login_url = 'product_list'

    def get_queryset(self):
        user = self.request.user
        fav = FavoriteProduct.objects.filter(user=user)
        products = [i.product for i in fav]
        return products


def save_mail_customer(request):
    if request.user.is_authenticated:
        email = request.POST.get('email')
        user = request.user
        if email:
            try:
                MailCustomer.objects.create(user=user, mail=email)
                messages.success(request, 'Ваша почта сохранена')
            except:
                page = request.META.get('HTTP_REFERER', 'product_list')
                messages.error(request, 'Ваша почта уже сохранена')
                return redirect(page)

    else:
        messages.error(request, 'Авторизуйтесь чтобы оставить почту')
    page = request.META.get('HTTP_REFERER', 'product_list')
    return redirect(page)


def mail_view(request):
    context = {
        'title': 'Как связаться с нами'
    }
    return render(request, 'store/mail.html', context)


from shop import settings
from django.core.mail import send_mail


def send_mail_to_customer(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            text = request.POST.get('text')
            mail_list = MailCustomer.objects.all()
            for email in mail_list:
                mail = send_mail(
                    subject='Взможно вас заинтересует',
                    message=text,
                    from_email=settings.EMAIL_HOST_USER,  # От кого отправлять
                    recipient_list=[email],  # Кому отправлять
                    fail_silently=False  # Если почта не сущ избегу ошибки
                )
                print(f'Сообщения были отправлены на почты {email}? - {bool(mail)}')

        else:
            pass
    else:
        return redirect('product_list')

    return render(request, 'store/send_mail_customer.html')


def cart(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Моя корзина',
            'order': cart_info['order'],
            'products': cart_info['products']
        }
        return render(request, 'store/cart.html', context)
    else:
        messages.error(request, 'Авторизуйтесь чтобы зайти в корзину')
        return redirect('product_list')


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)

        page = request.META.get('HTTP_REFERER', 'product_list')
        return redirect(page)
    else:
        messages.success(request, 'Авторизуйтесь чтобы посмотреть корзину')
        page = request.META.get('HTTP_REFERER', 'product_list')
        return redirect(page)


def checkout(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Оформление заказа',
            'order': cart_info['order'],
            'items': cart_info['products'],

            'customer_form': CustomerForm,
            'shipping_form': ShippingForm
        }
        return render(request, 'store/checkout.html', context)

    else:
        return redirect('product_list')


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()

        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data['first_name']
            customer.last_name = customer_form.cleaned_data['last_name']
            customer.save()

        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()

        total_price = cart_info['cart_total_price']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Покупка на сайте LOFT MEBEL'
                    },
                    'unit_amount': int(total_price * 100)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('checkout'))
        )
        return redirect(session.url, 303)


def success_payment(request):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        order = cart_info['order']
        order_save = SaveOrder.objects.create(customer=order.customer, total_price=order.get_cart_total_price)
        order_save.save()
        order_products = order.orderproduct_set.all()
        for item in order_products:
            save_order_product = SaveOrderProducts.objects.create(order_id=order_save.pk,
                                                                  product=str(item),
                                                                  quantity=item.quantity,
                                                                  product_price=item.product.price,
                                                                  final_price=item.get_total_price,
                                                                  photo=item.product.get_image_product())
            print(f'Заказаннный продукт {item} сохранен')
            save_order_product.save()

        user_cart.clear()
        messages.success(request, 'Ваша оплата прошла успешно')
        return render(request, 'store/success.html')
    else:
        messages.error(request, 'Авторизуйтесь чтобы зайти туда')
        return redirect('product_list')


def clear_cart(request):
    user_cart = CartForAuthenticatedUser(request)
    order = user_cart.get_cart_info()['order']
    order_products = order.orderproduct_set.all()
    for order_product in order_products:
        quantity = order_product.quantity
        product = order_product.product
        order_product.delete()
        product.quantity += quantity
        product.save()

    return redirect('my_cart')


def about(request):
    context = {
        'title': 'О сайте'
    }
    return render(request, 'store/about.html', context)


def profile_view(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        user_orders = SaveOrderProducts.objects.filter(order__customer=request.user.customer).order_by('-added_at')[:5]

        context = {
            'title': f'Профиль пользователя : {profile.user.username}',
            'profile': profile,
            'user_orders':user_orders
        }
        return render(request, 'store/profile.html', context)
    else:
        return redirect('product_list')


def edit_account_view(request):
    if request.method == 'POST':
        edit_account_form = EditAccountFrom(request.POST,instance=request.user)
        if edit_account_form.is_valid():
            data = edit_account_form.cleaned_data
            user = User.objects.get(id=request.user.id)
            if user.check_password(data['old_password']):
                if data['old_password'] and data['new_password'] == data['confirm_password']:
                    user.set_password(data['new_password'])
                    user.save()
                    update_session_auth_hash(request,user)
                    messages.success(request,'Данные акаунта изменены')
                    return redirect('profile',user.pk)
                else:
                    for field in edit_account_form.errors:
                        messages.error(request, edit_account_form.errors[field].as_text())
                        return redirect('change_account')
            else:
                for field in edit_account_form.errors:
                    messages.error(request, edit_account_form.errors[field].as_text())
                    return redirect('change_account')
            edit_account_form.save()
            return redirect('profile',user.pk)

    else:
        edit_account_form = EditAccountFrom(instance=request.user)

    context ={
        'title':'Изменение аккаунта',
        'edit_account_form':edit_account_form
    }
    return render(request,'store/change.html',context)


def edit_profile_view(request):
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            messages.success(request,'Данные профиля изменены')
            return redirect('profile',request.user.pk)
        else:
            for field in edit_profile_form.errors:
                messages.error(request, edit_profile_form.errors[field].as_text())
                return redirect('change_profile')
    else:
        edit_profile_form = EditProfileForm(instance=request.user.profile)

    context = {
        'title': 'Изменение профиля',
        'edit_profile_form': edit_profile_form
    }
    return render(request, 'store/change.html', context)



