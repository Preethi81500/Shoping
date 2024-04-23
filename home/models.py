from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

class Category(models.Model):
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('K','Kids')
    ]
    category = models.CharField(max_length=100, default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.category

class Product(models.Model):
    name_validator = RegexValidator(
    regex=r'^[A-Za-z0-9?!,.\'\s-]+$',
    message="Product name can only contain letters, numbers, spaces, '?', '!', ',', '.', hyphens, and apostrophe characters."
    )

    name = models.CharField(
        max_length=255,
        validators=[name_validator],
        default=False,
    )
    description = models.TextField()
    image = models.ImageField(upload_to="Product", default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', default=None)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_product_price(self):
        return self.price
    
class CartItem(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True , blank = True)
    price = models.IntegerField(default = False)
    quantity = models.IntegerField(default = 0)
    total_price = models.DecimalField(max_digits = 10 , decimal_places = 2, default = 0)

    class Meta:
        unique_together  = ('name','product')
    
    def __str__(self):
        return f"{self.name} - {self.product}"
    
class Recommended(models.Model):
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('W', 'Women'),
        ('K','Kids')
    ]
    name_validator = RegexValidator(
    regex=r'^[A-Za-z0-9?!,.\'\s-]+$',
    message="Product name can only contain letters, numbers, spaces, '?','&', '!', '^','-','_','.', hyphens, and apostrophe characters."
    )

    name = models.CharField(
        max_length=255,
        validators=[name_validator],
        default=False,
    )
    description = models.TextField()
    image_1 = models.ImageField(upload_to="Recommended", default="")
    image_2 = models.ImageField(upload_to="Recommended", default="")
    image_3 = models.ImageField(upload_to="Recommended", default="")
    image_4 = models.ImageField(upload_to="Recommended", default="")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    price = models.IntegerField(default=0)

    def _str_(self):
        return self.name

    def get_product_price(self):
        return self.price