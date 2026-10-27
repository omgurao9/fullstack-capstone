from django.conf import settings
from django.db import models

class Dealer(models.Model):
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, db_index=True)
    address = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    website = models.URLField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.city}, {self.state})"

class Review(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    review = models.TextField()
    purchase = models.CharField(max_length=160, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    sentiment = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def display_name(self):
        if self.author:
            return self.author.username
        return self.name or "Guest"

    def __str__(self):
        return f"Review for {self.dealer_id} by {self.display_name()}"

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField(default=2025)
    class Meta:
        unique_together = ("make", "name", "year")
    def __str__(self):
        return f"{self.year} {self.make.name} {self.name}"
