import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Dealer, Review, CarMake, CarModel

class DealershipTests(TestCase):
    def setUp(self):
        self.dealer = Dealer.objects.create(name="Kansas Auto", city="Wichita", state="Kansas")
        self.user = User.objects.create_user(username="tester", password="TestPass123!", email="tester@example.com")
        CarMake.objects.create(name="TestMake")

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kansas Auto")

    def test_all_dealers_api(self):
        response = self.client.get("/api/dealers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["dealers"][0]["name"], "Kansas Auto")

    def test_dealers_by_state(self):
        response = self.client.get("/api/dealers/state/Kansas/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["dealers"]), 1)

    def test_reviews_api(self):
        Review.objects.create(dealer=self.dealer, author=self.user, review="Fantastic services")
        response = self.client.get(f"/api/dealers/{self.dealer.id}/reviews/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["reviews"]), 1)

    def test_sentiment(self):
        response = self.client.post("/api/analyze-review/", data=json.dumps({"review": "Fantastic services"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sentiment_analysis"]["label"], "positive")

    def test_register_requires_all_fields(self):
        response = self.client.post("/api/register/", data=json.dumps({"username": "new"}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
