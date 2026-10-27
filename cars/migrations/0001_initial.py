from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="CarMake",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Dealer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(db_index=True, max_length=100)),
                ("address", models.CharField(blank=True, max_length=255)),
                ("zip_code", models.CharField(blank=True, max_length=15)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("website", models.URLField(blank=True)),
                ("image_url", models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="CarModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("year", models.PositiveIntegerField(default=2025)),
                ("make", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="models", to="cars.carmake")),
            ],
            options={"unique_together": {("make", "name", "year")}},
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=100)),
                ("review", models.TextField()),
                ("purchase", models.CharField(blank=True, max_length=160)),
                ("purchase_date", models.DateField(blank=True, null=True)),
                ("sentiment", models.CharField(blank=True, max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("author", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("dealer", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="cars.dealer")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
