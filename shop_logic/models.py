from django.db import models
from slugify import slugify
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model


User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=30, primary_key=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, primary_key=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Наличие')
    available = models.BooleanField(default=True, verbose_name='Товар включен')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()

    def __str__(self):
        return self.name



class Article(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='articles', verbose_name='Товар')
    title = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=256, primary_key=True, blank=True)
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение' )

    class Meta:
        verbose_name = 'Артикул'
        verbose_name_plural = 'Артикли'


    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

class Orders(models.Model):
    date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', verbose_name='Товар')
    quantities = ArrayField(models.PositiveIntegerField(), default=list, verbose_name='Количество')
    delivery_method = models.CharField(max_length=30, default='Доставка на дом')
    payment_method = models.CharField(max_length=30, default='Картой')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self) -> str:
        return f'Заказ от пользователя {self.owner}'

class Comment(models.Model):
    body = models.CharField(max_length=30)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.body

    class Meta:
        ordering = ['-created_at']


class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')

    def __str__(self) -> str:
        return f'{self.rating} -> {self.product}'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='liked')
    is_liked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.product}Liked by{self.author.name}'

class Favorites(models.Model):
    product = models.ForeignKey(Product,
                             on_delete=models.CASCADE,
                             related_name='favorites')
    author = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorite')
    is_favorite = models.BooleanField(default=False)

    class Meta:
        unique_together = ['product', 'author']
