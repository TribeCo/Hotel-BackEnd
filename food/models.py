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
    # reserve = models.ManyToManyField(User)
    type = models.CharField(max_length=100)
    reserved = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    day = models.DateField()
    image = models.ImageField(upload_to='foods/',default ='foods/image.jpg')
    


    def __str__(self):
        return str(self.name) + "-"

    def remain(self):
        return self.count - self.reserved

# ----------------------------------------------------------------------------------------------------------------------------
class FoodReservation(models.Model):
    food = models.ForeignKey(Food,on_delete=models.CASCADE,related_name="reservations")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="food_reservations")
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    been_paid = models.IntegerField(default=0)

    def __str__(self):
        return str(self.food) + "-" + str(self.user.email) + "-" + str(self.created)

    def price(self):
        return self.food.price

    def remaining(self):
        return self.price() - self.been_paid

# ----------------------------------------------------------------------------------------------------------------------------
