import requests
from decimal import Decimal
from django.conf import settings
import logging
import json

logger = logging.getLogger(__name__)
BASE_URL = "http://django_product:8000/api"


class ProductService:
    def __init__(self):
        self.email     = 'admin@admin.com'
        self.password  = '@dmin12345'
        self.base_url  = 'http://127.0.0.1:8000/api'
        self.jwt_token = None

    def _get_headers(self):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        if self.jwt_token is not None:
            headers |= {
                'Authorization': f'Bearer {self.jwt_token}'
            }
        return headers

    def login(self):
        url = f"{self.base_url}/auth/jwt/login/"
        data = {
            "email": self.email,
            "password": self.password
        }
        response = requests.post(url=url, headers=self._get_headers(), data=json.dumps(data))
        response = response.json()
        print(f"Response: {response}")
        self.jwt_token = response['access']
        return response

    def get_product(self, product_id):
        self.login()

        try:
            url = f"{self.base_url}/products/{product_id}/"
            headers = self._get_headers()
            print("headers: ", headers)
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            product_data = response.json()
            return product_data

        except requests.RequestException as e:
            logger.error(f"Error fetching product price: {e}")
            return None

