from django.db import models
from django.db import models
from django.utils.text import slugify

class ProductoCatalogo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    imagen_principal = models.ImageField(upload_to='imagenes/')
    imagen_extra1 = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    imagen_extra2 = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    imagen_extra3 = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    visible = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super(ProductoCatalogo, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre