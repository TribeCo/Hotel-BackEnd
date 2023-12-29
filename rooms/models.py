import numbers
from django.db import models
from accounts.models import User
from config.utils import jalali_create
from django.db.models import Max
from datetime import timedelta
#--------------------------------------------------------
class RoomType(models.Model):
    """
        Rooms Model.

    """
    type_choice = (
        ('o','معمولی'),
        ('v','vip'),
    )
    
    type = models.CharField(max_length=1,choices=type_choice)
    bed_count = models.IntegerField()
    features = models.TextField()
    price_one_night = models.IntegerField()
    image = models.ImageField(upload_to='rooms/',default ='rooms/image.jpg')
    number = models.IntegerField(blank=True, null=True)

    code = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return str(self.type) + "-" + str(self.bed_count)

    def __str__(self):
        if(self.type == 'o'): return f"تخته {str(self.bed_count)}"
        return f" {str(self.bed_count)} تخته"

    def n_night(self,n):
        return n * self.price_one_night

    def save(self, *args, **kwargs):
        if not self.number:
            if self.pk is None:  # Object is being created
                max_id = RoomType.objects.aggregate(Max('id'))['id__max']
                self.number = max_id + 1 if max_id else 1
        super().save(*args, **kwargs)
#--------------------------------------------------------
class Room(models.Model):
    number = models.IntegerField(unique=True)
    type = models.ForeignKey(RoomType,on_delete=models.CASCADE,related_name="rooms")
    has_Resev = models.BooleanField(default=False)


    def __str__(self):
        return str(self.type) + "-" + str(self.number)
#--------------------------------------------------------
class RoomReservation(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name="reservations")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reservations")
    night_count = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    check_in = models.DateField()
    paid = models.BooleanField(default=False)
    been_paid = models.IntegerField(default=0)



    def __str__(self):
        return str(self.room) + "-" + str(self.user) + "-" + str(self.created)

    def price(self):
        return self.night_count * self.room.type.price_one_night

    def remaining(self):
        return self.price() - self.been_paid

    # def shamsi_date(self):
    #     temp = jalali_create(self.check_in)
    #     return f"{temp[0]}-{temp[1]}-{temp[2]}"

    def end_date(self):
        return self.check_in + timedelta(days=self.night_count)

    def payed(self):
        self.paid = True
        self.been_paid = self.price()
        self.save()
#--------------------------------------------------------