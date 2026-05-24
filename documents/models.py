from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    file = models.FileField(upload_to='documents/', verbose_name='فایل')
    content = models.TextField(blank=True, verbose_name='متن کامل')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_indexed = models.BooleanField(default=False, verbose_name='ایندکس شده')

    class Meta:
        verbose_name = 'سند'
        verbose_name_plural = 'اسناد'

    def __str__(self):
        return self.title
