from django.db import models
from django.urls import reverse
from datetime import date
# Import the User
from django.contrib.auth.models import User

# Create your models here.

class Platform(models.Model):
  name = models.CharField(max_length=50)
  url = models.URLField(max_length=100)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('platforms_detail', kwargs={'pk': self.id})


class Deal(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, default=0.00)
    details = models.TextField(max_length=500, blank=True, default='')
    due_date = models.DateField(blank=True, default=date.today)
    url = models.URLField(max_length=100, blank=True, default='')
    promo_code = models.CharField(max_length=100, blank=True, default='')
    done = models.BooleanField(blank=True, default=False)
    create_date = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} ({self.id})"

    def get_absolute_url(self):
        return reverse("detail", kwargs={"deal_id": self.id})