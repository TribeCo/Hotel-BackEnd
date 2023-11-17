from django.db import models
# ----------------------------------------------------------------------------------------------------------------------------
class Room(models.Model):
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
    has_Resev = models.BooleanField(default=False)

    #

    code = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return str(self.type) + "-" + str(self.bed_count)

    
    def n_night(self,n):
        return n * self.price_one_night

# ----------------------------------------------------------------------------------------------------------------------------
