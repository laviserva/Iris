from django.db import models

class CssFile(models.Model):
    file = models.FileField(upload_to='css_files/')