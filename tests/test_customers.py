# tests/test_customers.py

import json
import pytest

@pytest.mark.parametrize("method, url, data, expected_status", [
    ("GET", "/check-db", None, 200),
    ("GET", "/customers", None, 200),
    ("POST", "/customers", {"name": "John Doe", "email": "john@example.com"}, 201),
    ("GET", "/customers/1", None, 200),  # Ganti 1 dengan ID pelanggan yang ada
    ("PUT", "/customers/1", {"name": "John Doe Updated"}, 200),  # Ganti 1 dengan ID pelanggan yang ada
    ("DELETE", "/customers/1", None, 200)  # Ganti 1 dengan ID pelanggan yang ada
])
def test_routes(client, method, url, data, expected_status):
    if method == "POST":
        response = client.post(url, data=json.dumps(data), content_type='application/json')
    elif method == "PUT":
        response = client.put(url, data=json.dumps(data), content_type='application/json')
    elif method == "DELETE":
        response = client.delete(url)
    else:  # GET
        response = client.get(url)

    assert response.status_code == expected_status


def test_create_customer_email_exists(client):
    # Menguji untuk membuat customer dengan email yang sudah ada
    client.post("/customers", data=json.dumps({"name": "Jane Doe", "email": "jane@example.com"}), content_type='application/json')
    response = client.post("/customers", data=json.dumps({"name": "Jane Doe", "email": "jane@example.com"}), content_type='application/json')

    assert response.status_code == 409
    assert b"Customer with this email already exists." in response.data
