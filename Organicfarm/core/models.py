from django.db import models
from authapi.models import CustomUser
from django.shortcuts import reverse

# Create your models here.


class Contactinfo(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=16, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Contact Info'

    def __str__(self):
        return self.email


class Banner(models.Model):
    image = models.ImageField(upload_to='banner/')
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Banners'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:banner", kwargs={
            'slug': self.slug
        })


class Featured(models.Model):
    image = models.ImageField(upload_to='featured/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Featureds'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:featured", kwargs={
            'slug': self.slug
        })


class Aboutitem(models.Model):
    icon = models.ImageField(upload_to='about/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'About Item'

    def __str__(self):
        return self.title


class About(models.Model):
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    item = models.ManyToManyField(Aboutitem)
    experiance = models.CharField(max_length=10, blank=True, null=True)
    specialist = models.CharField(max_length=10, blank=True, null=True)
    projects = models.CharField(max_length=10, blank=True, null=True)
    clients = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'About'

    def __str__(self):
        return self.title


class Serviceitem(models.Model):
    icon = models.ImageField(upload_to='service/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Service Item'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:serviceitem", kwargs={
            'slug': self.slug
        })


class Service(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    item = models.ManyToManyField(Serviceitem)

    class Meta:
        verbose_name_plural = 'Service'

    def __str__(self):
        return self.title


class Whychooseitem(models.Model):
    image = models.ImageField(upload_to='whychoose/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Whychoose Item'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:whychoose", kwargs={
            'slug': self.slug
        })


class Whychoose(models.Model):
    image = models.ImageField(upload_to='whychoose/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    item = models.ManyToManyField(Whychooseitem)

    class Meta:
        verbose_name_plural = 'Whychoose'
        
    def __str__(self):
        return str(self.image)


class Clients(models.Model):
    image = models.ImageField(upload_to='testimonial/', blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Clients'
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:clients", kwargs={
            'slug': self.slug
        })
        

class Testimonial(models.Model):
    background = models.ImageField(upload_to='testimonial/', blank=True, null=True)
    item = models.ManyToManyField(Clients)

    class Meta:
        verbose_name_plural = 'testimonial'
    
    def __str__(self):
        return str(self.background)



class Team(models.Model):
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Team'
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:team", kwargs={
            'slug': self.slug
        })


class Contact(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Contact'

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("core:contact", kwargs={
            'slug': self.slug
        })
