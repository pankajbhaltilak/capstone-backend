from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Sales
from datetime import date


class BaseTestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client = APIClient()
        # Authenticate the client
        self.client.force_authenticate(user=self.user)

        # Sample sales data
        Sales.objects.create(
            order_id="O1",
            order_date=date.today(),
            status="delivered",
            qty=2,
            currency="INR",
            amount=1000,
            ship_state="Maharashtra",
            ship_city="Mumbai",
            ship_country="India",
        )
        Sales.objects.create(
            order_id="O2",
            order_date=date.today(),
            status="pending",
            qty=1,
            currency="INR",
            amount=500,
            ship_state="Karnataka",
            ship_city="Bangalore",
            ship_country="India",
        )


class SalesByRegionTest(BaseTestCase):
    def test_sales_by_state(self):
        url = reverse("sales-by-region")  
        response = self.client.get(url + "?level=state")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  

    def test_sales_by_country(self):
        url = reverse("sales-by-region")
        response = self.client.get(url + "?level=country")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["region"], "India")

class TopCitiesTest(BaseTestCase):
    def test_top_cities(self):
        url = reverse("top-cities")
        response = self.client.get(url + "?limit=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["city"], "Mumbai")

