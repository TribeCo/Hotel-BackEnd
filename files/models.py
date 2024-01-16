from django.db import models
#--------------------------------------------------------
class FrontImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='front/',default ='front/image.jpg')

    def __str__(self):
        return str(self.name) + "-"
#--------------------------------------------------------