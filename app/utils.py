import re
from datetime import datetime
from typing import Any

from app.models import FormData
from database import get_db


def validate_fields(fields: dict) -> dict:
    validated_fields = {}
    for field_name, value in fields.items():
        if is_valid_date(value):
            validated_fields[field_name] = "date"
        elif is_valid_phone(value):
            validated_fields[field_name] = "phone"
        elif is_valid_email(value):
            validated_fields[field_name] = "email"
        elif isinstance(value, int) or isinstance(value, float):
            validated_fields[field_name] = "num"
        else:
            validated_fields[field_name] = "text"
    return validated_fields

def is_valid_email(value: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, value) is not None

def is_valid_phone(value: str) -> bool:
    phone_regex = r'^\+7 \d{3} \d{3} \d{2} \d{2}$'
    return re.match(phone_regex, value) is not None

def is_valid_date(value: str) -> bool:
    date_formats = ["%d.%m.%Y", "%Y-%m-%d"]
    for fmt in date_formats:
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            continue
    return False

def match_fields(input_fields: list, template_fields: list) -> bool:
    count_valid_fields = 0
    for field in template_fields:
        if field in input_fields:
            count_valid_fields += 1
    if count_valid_fields == len(template_fields):
        return True
    return False

def find_matching_template(validated_fields: dict) -> Any | None:
    db = get_db()
    templates = db.all()
    for template in templates:
        template_fields = template["fields"].keys()
        if match_fields(validated_fields.keys(), template_fields):
            return template
    return None


def match_validated_template_and_matched_template(validated_fields, matching_template):
    response = {'Template name': matching_template["name"]}
    for field in validated_fields.keys():
        if field in matching_template["fields"].keys():
            if validated_fields[field] != matching_template["fields"][field]:
                response[field] = "Mask or type error"
            else:
                response[field] = matching_template["fields"][field]
        else:
            response[field] = validated_fields[field]
        if "Mask or type error" not in response.values():
            return matching_template["name"]
        return response


def response_fields(form_data: FormData):
    validated_fields = validate_fields(form_data.fields)
    matching_template = find_matching_template(validated_fields)
    if matching_template is None:
        return validated_fields
    final_result = match_validated_template_and_matched_template(validated_fields, matching_template)
    return final_result

