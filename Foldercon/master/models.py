from django.db import models
from django.utils.text import slugify

class Type(models.Model):
    title = models.CharField(max_length=200)
    ico = models.FileField(upload_to='type_icons/', blank=True, null=True)

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"

    def __str__(self):
        return self.title

class Category(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

class FolderCon(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foldercons')
    title = models.CharField(max_length=200)
    ico = models.FileField(upload_to='foldercon/ico/', blank=True, null=True)
    png = models.FileField(upload_to='foldercon/png/', blank=True, null=True)
    icns = models.FileField(upload_to='foldercon/icns/', blank=True, null=True)
    zip = models.FileField(upload_to='foldercon/zip/', blank=True, null=True)
    webp = models.FileField(upload_to='foldercon/webp/', blank=True, null=True)
    is_visible = models.BooleanField(default=True, verbose_name="Visible")

    class Meta:
        verbose_name = "FolderCon"
        verbose_name_plural = "FolderCons"

    def __str__(self):
        return self.title
