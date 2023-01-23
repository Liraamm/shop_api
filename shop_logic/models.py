from django.db import models
from slugify import slugify

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, primary_key=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Наличие')
    available = models.BooleanField(default=True, verbose_name='Товар включен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    
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
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
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

