import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from transactions_app.models import Transaction


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_valid_transaction(api_client):
    url = reverse('transaction-list-create')
    payload = {
        "transaction_type": "DEPOSIT",
        "amount": 100.00,
        "description": "Initial deposit"
    }
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    assert Transaction.objects.count() == 1
    tx = Transaction.objects.first()
    assert tx.transaction_type == "DEPOSIT"
    assert float(tx.amount) == 100.00
    assert tx.description == "Initial deposit"


@pytest.mark.django_db
def test_create_negative_amount(api_client):
    url = reverse('transaction-list-create')
    payload = {
        "transaction_type": "DEPOSIT",
        "amount": -50,
        "description": "Negative amount"
    }
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "amount" in resp.data
    assert resp.data["amount"][0] == "amount must be positive (> 0)"
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_create_invalid_type(api_client):
    url = reverse('transaction-list-create')
    payload = {
        "transaction_type": "TRANSFER",
        "amount": 50,
        "description": "Bad type"
    }
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "transaction_type" in resp.data
    assert resp.data["transaction_type"][0] == "transaction_type must be either DEPOSIT or WITHDRAWAL" # noqa
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_create_invalid_description(api_client):
    url = reverse('transaction-list-create')
    # non-string description
    payload = {
        "transaction_type": "DEPOSIT",
        "amount": 10,
        "description": 12345
    }
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "description" in resp.data
    assert resp.data["description"][0] == "description must be a string"
    # empty string
    payload["description"] = ""
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data["description"][0] == "description cannot be empty"


@pytest.mark.django_db
def test_list_transactions(api_client):
    # create two records
    Transaction.objects.create(transaction_type="DEPOSIT", amount=20, description="T1") # noqa
    Transaction.objects.create(transaction_type="WITHDRAWAL", amount=5, description="T2") # noqa
    url = reverse('transaction-list-create')
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert isinstance(resp.data, list)
    assert len(resp.data) == 2


@pytest.mark.django_db
def test_retrieve_transaction_detail(api_client):
    tx = Transaction.objects.create(transaction_type="DEPOSIT", amount=15, description="DetailTest") # noqa
    url = reverse('transaction-detail', kwargs={'pk': tx.pk})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["id"] == tx.pk
    assert resp.data["amount"] == "15.00"


@pytest.mark.django_db
def test_retrieve_invalid_id(api_client):
    url = reverse('transaction-detail', kwargs={'pk': 999})
    resp = api_client.get(url)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.data["detail"] == "Transaction with id=999 not found"
