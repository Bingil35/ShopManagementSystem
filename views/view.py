import json

def save_customer_info(customers, filename="customer.json"):
    data = [customer.to_dict() for customer in customers]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
