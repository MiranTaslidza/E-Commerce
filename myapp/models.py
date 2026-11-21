from django.db import models
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100) # ime proizvoda
    price = models.FloatField() # cijena proizvoda
    description = models.TextField() # opis proizvoda
    image = models.ImageField(upload_to='images/') # slika proizvoda
    slug = models.SlugField(unique=True, blank=True) # slug služi za kreiranje URL-a proizvoda
    stock = models.IntegerField() # količina proizvoda
    active = models.BooleanField() # da li je proizvod dostupan
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            #self.slug = slugify(self.name)
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super(Product, self).save(*args, **kwargs)