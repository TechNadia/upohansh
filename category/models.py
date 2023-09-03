from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length= 30, unique = True)
    slug = models.SlugField(max_length=50, unique = True)
    description = models.TextField(max_length = 255, blank = True)
    category_image = models.ImageField(upload_to = 'photos/categories', blank=True)
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self) -> str:
        return f'{self.category_name}';