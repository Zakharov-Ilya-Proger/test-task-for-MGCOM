import requests

url = "http://localhost:8000/get_form"

def test_form():
    data = {
        "fields": {
            "user_email": "test@example.com",
            "user_phone": "+7 123 456 78 90",
            "order_date": "2023-10-01"
        }
    }
    response = requests.post(url, json=data)
    print("Form Found Response:", response.json())

def test_invalid_form():
    data = {
        "fields": {
            "contact_email": "invalid_email",
            "contact_phone": "+7 123 456 78 90",
            "contact_date": "2023-10-01"
        }
    }
    response = requests.post(url, json=data)
    print("Form Invalid Response:", response.json())


def test_form_not_found():
    data = {
        "fields": {
            "unknown_field": "some_text",
            "another_field": "2023-10-01"
        }
    }
    response = requests.post(url, json=data)
    print("Form Not Found Response:", response.json())

if __name__ == "__main__":
    test_form()
    test_invalid_form()
    test_form_not_found()