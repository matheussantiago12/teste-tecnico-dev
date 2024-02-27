from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=50)
    card_id = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name