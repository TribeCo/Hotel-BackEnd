from django.db import models
from accounts.models import User
# ----------------------------------------------------------------------------------------------------------------------------
class Food(models.Model):
    """
        Foods Model.

    """
    meal_choice = (
        ('m','صبحانه'),
        ('d','ناهار'),
        ('n','شام'),
    )
    price = models.IntegerField()
    name = models.CharField(max_length=100)
    meal = models.CharField(max_length=1,choices=meal_choice)
    reserve = models.ManyToManyField(User)
    type = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    # day = models.CharField(max_length=1,choices=day_choice)
    


    def __str__(self):
        return str(self.name) + "-"

# ----------------------------------------------------------------------------------------------------------------------------
