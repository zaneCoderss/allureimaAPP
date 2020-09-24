from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True) # will auto aticaly input, cannot be changed
    datecompleted = models.DateTimeField(null=True, blank=True) # to be collected when the student marks it done
    important = models.BooleanField(default=False) # An option to mark the 'Importnat Stuff'
    artist = models.ForeignKey(User, on_delete=models.CASCADE) # getting unique id for each user (allureima studnets/artits in this case) so we cna maintain context.
    #foreign key is used for the one to many relationshps...one user can have multiple to-dos', and NOT the other way
