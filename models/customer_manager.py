import json
import pandas as pd
from models.customer import Customer
from models.loyal_customer import LoyalCustomer
from models.casual_customer import CasualCustomer
from views.view import display_customers

def save_customer_info(customers, filename="./data/customer_info.json"):
    data = [customer.to_dict() for customer in customers]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_customers(filename="./data/customer_info.json"):
    customers = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                customer_type = item.get("Loại")
                if customer_type == "Thân thiết":
                    customer = LoyalCustomer(item["ID"], item["Tên"], item["SĐT"], item["Email"])
                elif customer_type == "Vãng lai":
                    customer = CasualCustomer(item["ID"], item["Tên"], item["SĐT"], item["Email"])
                else:
                    continue

                total = item.get("Tổng giao dịch", 0)
                count = item.get("Số lần giao dịch", 0)
                if count > 0:
                    avg = total / count
                    for _ in range(count):
                        customer.add_purchase(avg)

                customers.append(customer)
    except FileNotFoundError:
        print(f"File {filename} không tồn tại!")
    except json.JSONDecodeError:
        print(f"File {filename} không đúng định dạng JSON.")
    return customers

class CustomerManager:
    def __init__(self):
        self.customers = []

    def add_customer(self, customer):
        if any(c.customer_id == customer.customer_id for c in self.customers):
            raise ValueError(f"Khách hàng có ID - {customer.customer_id} đã tồn tại.")
        self.customers.append(customer)
        self.save_to_file()

    def remove_customer_by_id(self, customer_id, filename="./data/customer_info.json"):
        customer_id = str(customer_id).strip()
        before = len(self.customers)

        self.customers = [c for c in self.customers if str(c.customer_id) != customer_id]

        if len(self.customers) == before:
            raise ValueError(f"Không tìm thấy khách hàng có ID - {customer_id}.")
        else:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump([c.to_dict() for c in self.customers], f, ensure_ascii=False, indent=4)
                print(f"Đã xóa khách hàng có ID - {customer_id} và cập nhật file.")
            except Exception as e:
                print(f"Đã xóa khách hàng nhưng gặp lỗi khi ghi file: {e}")

        
    
    def find_by_id(self, customer_id):
        return next((c for c in self.customers if c.customer_id == customer_id), None)
    
    def find_customer(self, keyword):
        keyword = keyword.strip()
        
        if keyword.isdigit():
            return next((c for c in self.customers if c.customer_id == keyword), None)
        else:
            return [c for c in self.customers if keyword.lower() in c.name.lower()]


    def display_all(self):
        if not self.customers:
            print("Danh sách khách hàng trống!")
        else:
            display_customers(self.customers)

    def save_to_file(self, filename="./data/customer_info.json"):
        save_customer_info(self.customers, filename)

    def load_from_file(self, filename="./data/customer_info.json"):
        self.customers = load_customers(filename)

    import json

    def update_customer(self, customer_id, new_name, new_phone, new_email, filename="data/customer_info.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Không thể đọc file {filename}.")
            return

        updated = False

        for customer in data:
            if str(customer.get("ID")) == str(customer_id):
                if new_name.strip():
                    customer["Tên"] = new_name
                if new_phone.strip():
                    customer["SĐT"] = new_phone
                if new_email.strip():
                    customer["Email"] = new_email
                updated = True
                print(f"Đã cập nhật thông tin cho KH: {customer_id}")
                break

        if not updated:
            print(f"Không tìm thấy KH với ID: {customer_id}")
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi khi ghi file: {e}")



    def upgrade_loyal_customers(self):
        upgraded = False  

        for c in self.customers:
            if isinstance(c, CasualCustomer):  
                if c.total_spent() >= 2000000:
                    c.__class__ = LoyalCustomer  
                    print(f"Khách hàng {c.name} đã được nâng cấp thành khách hàng thân thiết.")
                    upgraded = True  

        if not upgraded:
            print("Không có khách hàng nào có thể nâng lên khách hàng thân thiết.")
        else:
            self.save_customer_info()


    def search_customer(self, keyword, filename="./data/customer_info.json"):
        keyword = keyword.strip()

        if not keyword:
            print("Vui lòng nhập từ khóa tìm kiếm!")
            return

        customers = load_customers(filename)

        if not customers:
            print("Không có khách hàng nào trong hệ thống!")
            return

        results = [c for c in customers if
                   keyword in str(c.customer_id) or
                   keyword in c.name]

        if results:
            display_customers(results)
        else:
            print("Không tìm thấy khách hàng nào phù hợp!")





    def total_revenue(self):
        total = sum(c.total_spent() for c in self.customers)
        casual_total = sum(c.total_spent() for c in self.customers if isinstance(c, CasualCustomer))
        loyal_total = sum(c.total_spent() for c in self.customers if isinstance(c, LoyalCustomer))

        print("Thống kê Doanh thu:")
        print(f"- Tổng doanh thu toàn cửa hàng: {total:,.0f} VND")
        print(f"- Doanh thu từ KH vãng lai:      {casual_total:,.0f} VND")
        print(f"- Doanh thu từ KH thân thiết:    {loyal_total:,.0f} VND")

    def avg_purchases(self):
        if not self.customers:
            print("Danh sách khách hàng trống!")
            return

        data = []
        for c in self.customers:
            data.append({
                "ID": c.customer_id,
                "Tên": c.name,
                "Loại": c.get_type(),
                "Trung bình giao dịch": round(c.average_spent(), 2)
            })

        df = pd.DataFrame(data)

        print("\nGIÁ TRỊ TRUNG BÌNH GIAO DỊCH CỦA TỪNG KHÁCH HÀNG:")
        print(df.to_string(index=False))

        avg_all = df["Trung bình giao dịch"].mean()
        avg_loyal = df[df["Loại"] == "Thân thiết"]["Trung bình giao dịch"].mean()
        avg_casual = df[df["Loại"] == "Vãng lai"]["Trung bình giao dịch"].mean()

        print("\nTRUNG BÌNH CHUNG THEO LOẠI KHÁCH HÀNG:")
        print(f"- Trung bình toàn bộ: {round(avg_all, 2):,.0f} VND")
        print(f"- Khách hàng thân thiết: {round(avg_loyal, 2):,.0f} VND")
        print(f"- Khách hàng vãng lai: {round(avg_casual, 2):,.0f} VND")


    def top_3_customers_by_total_spent(self):
        top = sorted(self.customers, key=lambda c: c.total_spent(), reverse=True)[:3]
        print("Top 3 KH chi tiêu nhiều nhất:")
        display_customers(top)

    def display_gift_customers(self):
        eligible_loyal_customers = [
            c for c in self.customers
            if isinstance(c, LoyalCustomer) and c.purchase_count() > 500
        ]

        top_customers = sorted(
            eligible_loyal_customers,
            key=lambda c: c.average_spent(),
            reverse=True
        )[:10]

        print("Top 10 KH thân thiết có điểm tích lũy > 500 và trung bình giao dịch cao nhất:")
        if top_customers:
            display_customers(top_customers)
        else:
            print("Không có khách hàng nào đủ điều kiện nhận quà.")

