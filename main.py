from models.manage_customer import ManageCustomer
from views import view
from templates import display

DATA_FILE = "data/shop_data.pkl" 

def main():
    customer_manager = ManageCustomer()
    customer_manager.load_data(DATA_FILE) 

    menu_options = [
        "Thêm khách hàng mới",
        "Thêm đơn hàng cho khách hàng",
        "Cập nhật thông tin khách hàng",
        "Xoá khách hàng",
        "Tìm kiếm khách hàng",
        "Hiển thị tất cả khách hàng",
        "Liệt kê khách hàng theo loại (Vãng lai/Thân thiết)",
        "Hiển thị báo cáo doanh thu",
        "Hiển thị 3 khách hàng chi tiêu nhiều nhất",
        "Hiển thị danh sách khách hàng theo tổng chi tiêu (giảm dần)", 
        "Hiển thị khách hàng đủ điều kiện khuyến mãi Tết",
        "Thêm điểm tích lũy cho khách hàng thân thiết" 
    ]

    while True:
        display.display_menu(menu_options)
        try:
            choice = view.get_int_input("Nhập lựa chọn của bạn (0-12): ", 0, len(menu_options))

            if choice == 1:
                view.add_new_customer_view(customer_manager)
            elif choice == 2:
                view.add_purchase_view(customer_manager)
            elif choice == 3:
                view.update_customer_view(customer_manager)
            elif choice == 4:
                view.delete_customer_view(customer_manager)
            elif choice == 5:
                view.search_customer_view(customer_manager)
            elif choice == 6:
                view.list_all_customers_view(customer_manager)
            elif choice == 7:
                view.list_customers_by_type_view(customer_manager)
            elif choice == 8:
                view.display_revenue_reports_view(customer_manager)
            elif choice == 9:
                view.display_top_customers_view(customer_manager)
            elif choice == 10: 
                all_customers_sorted = customer_manager.sort_by_total_spent(reverse=True)
                display.display_customer_list(all_customers_sorted, "Khách hàng theo tổng chi tiêu (giảm dần)")
            elif choice == 11:
                view.display_tet_promotion_view(customer_manager)
            elif choice == 12:
                view.add_loyalty_points_view(customer_manager)
            elif choice == 0:
                customer_manager.save_data(DATA_FILE) 
                display.display_message("Đang thoát chương trình. Tạm biệt!")
                break
            else:
                display.display_message("Lựa chọn không hợp lệ. Vui lòng thử lại.", is_error=True)
            
            

        except ValueError:
            display.display_message("Dữ liệu không hợp lệ. Vui lòng nhập một số.", is_error=True)
        except Exception as e:
            display.display_message(f"Đã xảy ra lỗi: {e}", is_error=True)

if __name__ == "__main__":
    main()