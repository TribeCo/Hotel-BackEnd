from django.db import models
from accounts.models import User
from config.utils import jalali_create,persion_converter_number
#--------------------------------------------------------
class Food(models.Model):
    """The Food model defines a database table for storing food items."""
    price = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    reserved = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    day = models.DateField()
    image = models.ImageField(upload_to='foods/',default ='foods/image.jpg')
    


    def __str__(self):
        return str(self.name) + "-"

    def remain(self):
        """The number of dishes that can be reserved according to the reservations made."""
        return self.count - self.reserved

    def shamsi_date(self):
        """Date of serving food in Shamsi"""
        temp = jalali_create(self.day)
        return f"{temp[0]}-{temp[1]}-{temp[2]}"
#--------------------------------------------------------
class FoodReservation(models.Model):
    """The FoodReservation model represents a reservation made by a user for a specific food item."""
    meal_choice = (
        ('d','ناهار'),
        ('n','شام'),
    )
    place_choice = (
        ('r','رستوران'),
        ('a','اتاق'),
    )
    food = models.ForeignKey(Food,on_delete=models.CASCADE,related_name="reservations")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="food_reservations")
    created = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    been_paid = models.IntegerField(default=0)
    delivery = models.BooleanField(default=False)
    place = models.CharField(max_length=1,choices=place_choice,default='r')


    
    meal = models.CharField(max_length=1,choices=meal_choice)


    def __str__(self):
        return str(self.food) + "-" + str(self.user.email) + "-" + str(self.created)

    def price(self):
        return self.food.price

    def remaining(self):
        """The amount of unpaid food"""
        return self.price() - self.been_paid

    def shamsi_date(self):
        """Date of serving food in Shamsi"""
        # temp = jalali_create(self.created)
        # return f"{temp[0]}-{temp[1]}-{temp[2]}"
        return self.created
        

    def payed(self):
        self.paid = True
        self.been_paid = self.price()
        self.save()
#--------------------------------------------------------
