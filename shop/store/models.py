from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название категории')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Категория',
                               related_name='subcategories')
    icon = models.FileField(upload_to='categories/', default='Нет фото', verbose_name='Изображение категорий')

    def get_absolute_url(self):
        return reverse('category_page', kwargs={'slug': self.slug})

    def get_image_category(self):
        if self.icon:
            return self.icon.url
        else:
            return ''

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Категория :pk={self.pk},title={self.title},'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название товара')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление')
    quantity = models.IntegerField(default=0, verbose_name='Колиество товара')
    description = models.TextField(default='Здесь скоро будет описание', verbose_name='Описание товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категоря товара',
                                 related_name='products')
    slug = models.SlugField(unique=True, null=True)

    length = models.CharField(max_length=100, default='100 CM', verbose_name='Длина')
    width = models.CharField(max_length=100, default='100 CM', verbose_name='Ширина')
    height = models.CharField(max_length=100, default='100 CM', verbose_name='Высота')

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_image_product(self):
        if self.images:
            try:
                return self.images.first().image.url

            except:
                return ''
        else:
            return ''

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Продукт :pk={self.pk},title={self.title}, price={self.price}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Изображение товаров')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Color(models.Model):
    color_name = models.CharField(max_length=50, default='Желтый', verbose_name='Цвет')
    color = models.ImageField(upload_to='color/', verbose_name='Цвет товаров')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')

    class Meta:
        verbose_name = 'Цвет товара'
        verbose_name_plural = 'Цвета товаров'


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class MailCustomer(models.Model):
    mail = models.EmailField(unique=True, verbose_name='Почта покупателя')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Покупатель')

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = 'Почта'
        verbose_name_plural = 'Почтовые адреса'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    first_name = models.CharField(max_length=250, default='', verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=250, default='', verbose_name='Фамилия пользователя')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнен ли заказ')
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество товара')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    address = models.CharField(max_length=300, verbose_name='Адрес доставки')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, verbose_name='Город')
    region = models.CharField(max_length=250, verbose_name='Регион')
    phone = models.CharField(max_length=250, verbose_name='Номер телефона')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата доставки')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставок'


class City(models.Model):
    city = models.CharField(max_length=300, verbose_name='Название города')

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_photo(self):
        try:
            return self.photo.url

        except:
            return ''

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class SaveOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    total_price = models.FloatField(default=0, verbose_name='Сумма заказа')

    def __str__(self):
        return f'Заказ номер : {self.pk}'

    class Meta:
        verbose_name = 'История заказа'
        verbose_name_plural = 'Истории заказа'


class SaveOrderProducts(models.Model):
    order = models.ForeignKey(SaveOrder, on_delete=models.CASCADE, null=True, related_name='products')
    product = models.CharField(max_length=300, verbose_name='Продукт')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    product_price = models.FloatField(verbose_name='Цена продукта')
    final_price = models.FloatField(verbose_name='На сумму')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')
    photo = models.ImageField(upload_to='images/', verbose_name='Фото товара')

    def get_photo(self):
        try:
            return self.photo.url

        except:
            return ''

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'История заказанного товара'
        verbose_name_plural = 'Истории заказаннфх товаров'
