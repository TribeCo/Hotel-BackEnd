from django.db import models
# ----------------------------------------------------------------------------------------------------------------------------
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
    

    #

    code = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return str(self.type) + "-" + str(self.bed_count)

    def __str__(self):
        if(self.type == 'o'): return f"تخته {str(self.bed_count)}"
        return f" {str(self.bed_count)} تخته"

    def n_night(self,n):
        return n * self.price_one_night

# ----------------------------------------------------------------------------------------------------------------------------
class Room(models.Model):

    number = models.IntegerField(unique=True)
    type = models.ForeignKey(RoomType,on_delete=models.CASCADE)
    has_Resev = models.BooleanField(default=False)


    def __str__(self):
        return str(self.type) + "-" + str(self.bed_count)

# ----------------------------------------------------------------------------------------------------------------------------
