from django.db import models
from django.urls import reverse
# Import the User
from django.contrib.auth.models import User

# Create your models here.
class Deal(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    details = models.TextField(max_length=500)
    due_date = models.DateField()
    url = models.URLField(max_length=100)
    promo_code = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
  
    create_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.id})"

    def get_absolute_url(self):
        return reverse("detail", kwargs={"deal_id": self.id})