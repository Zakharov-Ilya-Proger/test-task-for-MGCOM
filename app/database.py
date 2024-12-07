from tinydb import TinyDB, Query

db = TinyDB('db.json')

def get_db():
    return db

def initialize_db():
    db.drop_tables()  # Очистка базы данных
    db.insert_multiple([
        {
            "name": "Order Form",
            "fields": {
                "user_email": "email",
                "user_phone": "phone",
                "order_date": "date"
            }
        },
        {
            "name": "Contact Form",
            "fields": {
                "contact_email": "email",
                "contact_phone": "phone",
                "contact_date": "date"
            }
        }
    ])

initialize_db()
