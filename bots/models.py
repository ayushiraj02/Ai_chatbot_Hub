from django.db import models

# Create your bots/model.py here.
from django.db import models
from accounts.models import User

class Bot(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    apikey = models.CharField(max_length=50)
    vector_path = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} owned by {self.owner}"
