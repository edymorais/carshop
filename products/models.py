from django.db import models
from time import strftime


def foto(instance, filename):
    return 'images/{datetime}.jpg'.format(datetime=strftime('%Y%m%d%H%M%S'))


class Product(models.Model):
    type = models.CharField(max_length=20)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=250)
    year = models.IntegerField()
    fabrication = models.IntegerField()
    version = models.CharField(max_length=250)
    color = models.CharField(max_length=20)
    is_new = models.BooleanField(default=False)
    fuel_type = models.CharField(max_length=20)
    exchange = models.CharField(max_length=20)
    distance_round = models.CharField(max_length=30)
    motor = models.CharField(max_length=30)
    observation = models.CharField(max_length=250, null=True, blank=True)
    price_sale = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.model} - {self.brand} - {self.version} - {self.year}'


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    foto = models.ImageField(upload_to=foto, null=True, blank=True, default='')

    def __str__(self):
        return f'{self.product}'


class Specification(models.Model):
    name = models.CharField(max_length=100)
    categories = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.categories}'


class ProductSpecifications(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    specification = models.ForeignKey(Specification, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.product} - {self.specification}'
