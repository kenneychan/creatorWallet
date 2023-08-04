from datetime import date
from django.db import models
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Platform(models.Model):
  name = models.CharField(max_length=50)
  url = models.URLField(max_length=100)
  platform_username = models.CharField(max_length=50, blank=True, null=True)

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('platforms_detail', kwargs={'pk': self.id})


class Deal(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, default=0.00)
    details = models.TextField(max_length=500, blank=True, default='')
    due_date = models.DateField(blank=True, null=True)
    url = models.URLField(max_length=100, blank=True, default='')
    promo_code = models.CharField(max_length=100, blank=True, default='')
    done = models.BooleanField(blank=True, default=False)
    created_date = models.DateField(default=date.today)
    platforms = models.ManyToManyField(Platform)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse("index")
    
    
class Attachment(models.Model):
    filename = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)

    def __str__(self):
        # return f"Contract for my_deal_id: {self.my_deal_id} @{self.url}"
        return f"Attachment {self.filename} {self.url}"
    

class Activity(models.Model):
    date = models.DateField()
    notes = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_activity_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']