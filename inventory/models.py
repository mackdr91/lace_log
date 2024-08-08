from django.db import models
from core.models import Profile
from .utils import generate_qr_code


class Sneaker(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    is_new = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def get_qr_code(self):
        return generate_qr_code(self)

    def save(self, *args, **kwargs):
        super(Sneaker, self).save(*args, **kwargs)
        generate_qr_code(self)

    def __str__(self):
        return self.name

class SneakerVariation(models.Model):
    sneaker = models.ForeignKey(Sneaker, related_name='variations', on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.sneaker.name} - Size: {self.size} - Quantity: {self.quantity}"

class Collection(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    date_added = models.DateField(auto_now=True)
    sneaker = models.ManyToManyField('Sneaker', related_name='collections')

    def __str__(self):
        return self.description
