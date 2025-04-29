from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Transaction


class TransactionAPITest(APITestCase):
    def setUp(self):
        self.valid = {
            "transaction_type": "DEPOSIT",
            "amount": 100.00,
            "description": "Initial deposit"
        }
        self.neg_amount = {
            "transaction_type": "DEPOSIT",
            "amount": -50,
            "description": "Negative"
        }
        self.bad_type = {
            "transaction_type": "TRANSFER",
            "amount": 50,
            "description": "Bad type"
        }

    def test_create_valid(self):
        r = self.client.post(
            reverse('transaction-list-create'),
            self.valid,
            format='json'
            )
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_create_negative_amount(self):
        r = self.client.post(
            reverse('transaction-list-create'),
            self.neg_amount,
            format='json'
            )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_type(self):
        r = self.client.post(
            reverse('transaction-list-create'),
            self.bad_type,
            format='json'
            )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        Transaction.objects.create(
            transaction_type="DEPOSIT",
            amount=10,
            description="T1"
            )
        r = self.client.get(reverse('transaction-list-create'))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIsInstance(r.data, list)

    def test_detail(self):
        tx = Transaction.objects.create(
            transaction_type="DEPOSIT",
            amount=10,
            description="T2"
            )
        r = self.client.get(reverse(
            'transaction-detail',
            kwargs={'pk': tx.pk}
            ))
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['id'], tx.pk)
