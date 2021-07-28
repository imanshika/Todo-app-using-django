from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    descr = models.TextField()
    updateDate = models.DateField()
    doneDate = models.DateField(null=True)
    isDone = models.BooleanField(default=False)
    def __str__(self):
        return self.title