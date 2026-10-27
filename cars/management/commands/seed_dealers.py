from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cars.models import Dealer, Review, CarMake, CarModel

class Command(BaseCommand):
    help = "Seed idempotent demo dealership, reviews, and car makes/models."

    def handle(self, *args, **options):
        dealer_rows = [
            ("Heartland Auto Center", "Wichita", "Kansas", "1200 East Central Ave", "67206", "316-555-0101"),
            ("Prairie Motors", "Topeka", "Kansas", "800 SW Topeka Blvd", "66603", "785-555-0102"),
            ("Lone Star Cars", "Dallas", "Texas", "500 Main Street", "75201", "214-555-0103"),
            ("Golden Gate Auto", "San Jose", "California", "240 Market Street", "95113", "408-555-0104"),
            ("Windy City Motors", "Chicago", "Illinois", "10 Lake Street", "60601", "312-555-0105"),
        ]
        dealers = []
        for name, city, state, address, zip_code, phone in dealer_rows:
            dealer, _ = Dealer.objects.get_or_create(
                name=name, defaults={"city": city, "state": state, "address": address, "zip_code": zip_code, "phone": phone}
            )
            dealers.append(dealer)
        demo, created = User.objects.get_or_create(username="demo_user", defaults={"email": "demo@example.com", "first_name": "Demo", "last_name": "User"})
        if created:
            demo.set_password("DemoPass123!")
            demo.save()
        sample_reviews = [
            (dealers[0], "Fantastic services", "positive"),
            (dealers[1], "Friendly staff and a great selection", "positive"),
            (dealers[2], "The wait was slow", "negative"),
        ]
        for dealer, review_text, sentiment in sample_reviews:
            Review.objects.get_or_create(dealer=dealer, review=review_text, defaults={"author": demo, "sentiment": sentiment})
        car_data = {
            "Toyota": [("Camry", 2025), ("Corolla", 2024), ("RAV4", 2025)],
            "Honda": [("Civic", 2025), ("Accord", 2024), ("CR-V", 2025)],
            "Ford": [("F-150", 2025), ("Escape", 2024)],
            "BMW": [("3 Series", 2025), ("X5", 2024)],
        }
        for make_name, models in car_data.items():
            make, _ = CarMake.objects.get_or_create(name=make_name)
            for model_name, year in models:
                CarModel.objects.get_or_create(make=make, name=model_name, year=year)
        self.stdout.write(self.style.SUCCESS(f"Seed complete: {Dealer.objects.count()} dealers, {Review.objects.count()} reviews, {CarMake.objects.count()} makes."))
