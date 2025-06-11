from django.contrib.auth.models import User
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folder_cons', blank=True, null=True, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foldercons')
    title = models.CharField(max_length=200)
    ico = models.FileField(upload_to='foldercon/ico/', blank=True, null=True)
    png = models.FileField(upload_to='foldercon/png/', blank=True, null=True)
    icns = models.FileField(upload_to='foldercon/icns/', blank=True, null=True)
    zip = models.FileField(upload_to='foldercon/zip/', blank=True, null=True)
    webp = models.FileField(upload_to='foldercon/webp/', blank=True, null=True)
    ico_downloads = models.PositiveIntegerField(default=0)
    png_downloads = models.PositiveIntegerField(default=0)
    icns_downloads = models.PositiveIntegerField(default=0)
    zip_downloads = models.PositiveIntegerField(default=0)

    is_visible = models.BooleanField(default=True, verbose_name="Visible")

    def total_downloads(self):
        return (
                self.ico_downloads +
                self.png_downloads +
                self.icns_downloads +
                self.zip_downloads
        )
    class Meta:
        verbose_name = "FolderCon"
        verbose_name_plural = "FolderCons"

    def __str__(self):
        return self.title

class ReportFile(models.Model):
    foldercon = models.ForeignKey(FolderCon, on_delete=models.CASCADE, related_name='report_files', blank=True, null=True, default=None)
    title = models.CharField(max_length=200)
    issue_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'issue {self.title} for {self.foldercon}'
