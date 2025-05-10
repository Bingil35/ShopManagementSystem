import json

from models.customer import Customer, LoyalCustomer, CasualCustomer

def save_customer_info(customers, filename="./data/customer.json"):
    data = [customer.to_dict() for customer in customers]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
def load_customers(filename="./data/customer.json"):
    customers = []
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            if item["Type"] == "Loyal":
                customer = LoyalCustomer(item["ID"], item["Name"], item["Phone"], item["Email"])
            elif item["Type"] == "Casual":
                customer = CasualCustomer(item["ID"], item["Name"], item["Phone"], item["Email"])
            else:
                continue  # Bỏ qua nếu Type không hợp lệ

            # Gán lại dữ liệu mua hàng
            total = item.get("Total Spent", 0)
            count = item.get("Purchases", 0)
            if count > 0:
                avg = total / count
                for _ in range(count):
                    customer.add_purchase(avg)  # Ước lượng lại danh sách mua hàng

            customers.append(customer)
    return customers

