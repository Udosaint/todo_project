from django.db import models

from api.models import User

# Create your models here.

class Todo(models.Model):
    name = models.CharField("Todo Name", max_length=50)
    description = models.TextField("Descriptions", max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    status = models.BooleanField(default=False)
    created = models.DateField("Date", auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name