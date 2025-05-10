from models.customer_manager import CustomerManager
from models.loyal_customer import LoyalCustomer
from models.casual_customer import CasualCustomer
import os


def menu():
    print("\n====== HỆ THỐNG QUẢN LÝ KHÁCH HÀNG SIÊU THỊ ======")
    print("1. Thêm khách hàng")
    print("2. Sửa thông tin khách hàng")
    print("3. Cập nhật khách hàng thân thiết")
    print("4. Xóa khách hàng")
    print("5. Tìm kiếm khách hàng")
    print("6. Hiển thị danh sách khách hàng")
    print("7. Tính tổng doanh thu")
    print("8. Tính trung bình giá trị mua hàng")
    print("9. Liệt kê 3 khách hàng mua nhiều nhất")
    print("10. Hiển thị khách hàng nhận quà Tết")
    print("0. Thoát chương trình")
    print("===============================================\n")


def main():
    manager = CustomerManager()

    if os.path.exists("data/customer_info.json"):
        manager.load_from_file("data/customer_info.json")

    while True:
        menu()
        choice = input("Nhập lựa chọn của bạn: ").strip()

        if choice == "1":
            id = input("Mã KH: ")
            name = input("Tên KH: ")
            phone = input("SĐT: ")
            email = input("Email: ")
            type_cus = input("Loại (Thân thiết/Vãng lai): ")

            if type_cus == "Thân thiết":
                c = LoyalCustomer(id, name, phone, email)
            elif type_cus == "Vãng lai":
                c = CasualCustomer(id, name, phone, email)
            else:
                print("Loại không hợp lệ.")
                continue

            try:
                while True:
                    total_spent = input("Nhập tổng giá trị giao dịch (để trống nếu xong): ")

                    if total_spent == "":
                        break

                    try:
                        total_spent_value = float(total_spent)
                        if total_spent_value <= 0:
                            print("Giá trị giao dịch phải là số dương.")
                            continue
                        c.add_purchase(total_spent_value)
                    except ValueError:
                        print("Giá trị giao dịch không hợp lệ. Vui lòng nhập lại.")
                        continue

                manager.add_customer(c)
                print("Thêm thành công.")
            except Exception as e:
                print("Lỗi:", e)



        elif choice == "2":
            id = input("Nhập mã KH cần sửa: ")
            name = input("Tên mới: ")
            phone = input("SĐT mới: ")
            email = input("Email mới: ")
            manager.update_customer(id, name, phone, email)

        elif choice == "3":
            manager.upgrade_loyal_customers()

        elif choice == "4":
            id = input("Nhập mã KH cần xóa: ")
            try:
                manager.remove_customer_by_id(id)
            except ValueError as e:
                print(e)

        elif choice == "5":
            keyword = input("Nhập mã / tên: ")
            manager.search_customer(keyword)

        elif choice == "6":
            manager.display_all()

        elif choice == "7":
            manager.total_revenue()

        elif choice == "8":
            manager.avg_purchases()

        elif choice == "9":
            manager.top_3_customers_by_total_spent()

        elif choice == "10":
            manager.display_gift_customers()

        elif choice == "0":
            manager.save_to_file("data/customer_info.json")
            print("Đã lưu và thoát chương trình.")
            break

        else:
            print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()
