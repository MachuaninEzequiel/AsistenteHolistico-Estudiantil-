from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class EstresAcademico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nivel_de_estres = models.IntegerField()
    emociones = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True,)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Nivel de estrés: {self.nivel_de_estres}, Emociones: {self.emociones}"
    

class Icon(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='icon_images/', default='path/to/default/image.jpg')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class Product(models.Model):

    PRODUCT_TYPES = [
        ('producto', 'Producto'),
        ('cabeza', 'Cabeza'),
        ('torso', 'Torso'),
        ('pierna', 'Pierna'),
        ('pie', 'Pie'),
        ('background', 'Background'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    gif = models.FileField(upload_to='product_gifs/', default='default.gif')
    price = models.IntegerField()
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='producto')

    def __str__(self):
        return self.name
    


class Avatar(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    background_image = models.ImageField(upload_to='avatar_images/backgrounds/', default='path/to/default/background.jpg')
    head_image = models.ImageField(upload_to='avatar_images/heads/', default='path/to/default/head.jpg')
    torso_image = models.ImageField(upload_to='avatar_images/torsos/', default='path/to/default/torso.jpg')
    legs_image = models.ImageField(upload_to='avatar_images/legs/', default='path/to/default/legs.jpg')
    feet_image = models.ImageField(upload_to='avatar_images/feet/', default='path/to/default/feet.jpg')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    purchased_products = models.ManyToManyField(Product, related_name='purchased_by')
    tokens = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ForeignKey(Avatar, on_delete=models.SET_NULL, null=True, blank=True)
    selected_background = models.ImageField(upload_to='avatar_images/backgrounds', null=True, blank=True)
    selected_head = models.ImageField(upload_to='avatar_images/heads/', null=True, blank=True)
    selected_torso = models.ImageField(upload_to='avatar_images/torsos/', null=True, blank=True)
    selected_legs = models.ImageField(upload_to='avatar_images/legs/', null=True, blank=True)
    selected_feet = models.ImageField(upload_to='avatar_images/feet/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Tokens: {self.tokens}"
    




