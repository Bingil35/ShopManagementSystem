from models.manage_customer import ManageCustomer, CasualCustomer # For type hints if needed
from templates import display

def get_string_input(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        display.display_message("Dữ liệu không được để trống.", is_error=True)

def get_id_input(prompt="Nhập mã khách hàng: "):
    return get_string_input(prompt)

def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                display.display_message("Số tiền phải lớn hơn 0.", is_error=True)
        except ValueError:
            display.display_message("Dữ liệu không hợp lệ. Vui lòng nhập một số.", is_error=True)

def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if (min_val is None or value >= min_val) and \
               (max_val is None or value <= max_val):
                return value
            else:
                display.display_message(f"Giá trị phải nằm trong khoảng từ {min_val} đến {max_val}.", is_error=True)
        except ValueError:
            display.display_message("Dữ liệu không hợp lệ. Vui lòng nhập một số nguyên..", is_error=True)


def get_customer_details_from_user():
    customer_id = get_id_input("Nhập mã khách hàng: ")
    name = get_string_input("Nhập tên khách hàng: ")
    phone = get_string_input("Nhập số điện thoại: ")
    email = get_string_input("Nhập email: ")
    return customer_id, name, phone, email

# --- Các hàm xử lý hành động ---

def add_new_customer_view(manager: ManageCustomer):
    display.display_message("--- Thêm khách hàng mới ---")
    customer_id, name, phone, email = get_customer_details_from_user()
    if manager.add_customer(customer_id, name, phone, email):
        # display.display_message(f"Customer {name} added successfully.") # Manager method already prints
        pass
    # else:
        # display.display_message(f"Failed to add customer.", is_error=True) # Manager method already prints

def add_purchase_view(manager: ManageCustomer):
    display.display_message("--- Thêm đơn hàng cho khách hàng ---")
    customer_id = get_id_input("Nhập mã khách hàng: ")
    amount = get_float_input("Nhập số tiền mua hàng: ")
    manager.add_purchase_to_customer(customer_id, amount)

def update_customer_view(manager: ManageCustomer):
    display.display_message("--- Cập nhật thông tin khách hàng ---")
    customer_id = get_id_input("Nhập mã khách hàng cần cập nhật: ")
    
    customer_index = manager._find_customer_index(customer_id)
    if customer_index == -1:
        display.display_message(f"Không tìm thấy khách hàng với mã {customer_id}.", is_error=True)
        return

    customer = manager.customers[customer_index]
    display.display_message(f"Thông tin hiện tại: {str(customer)}")

    new_name = get_string_input(f"Nhập tên mới (hiện tại: {customer.name}) hoặc Enter để giữ nguyên: ", allow_empty=True)
    new_phone = get_string_input(f"Nhập số điện thoại mới (hiện tại: {customer.phone}) hoặc Enter để giữ nguyên: ", allow_empty=True)
    new_email = get_string_input(f"Nhập email mới (hiện tại: {customer.email}) hoặc Enter để giữ nguyên: ", allow_empty=True)
    
    updated_something = False
    _new_name = new_name if new_name else None
    _new_phone = new_phone if new_phone else None
    _new_email = new_email if new_email else None

    if _new_name or _new_phone or _new_email:
        manager.update_customer_info(customer_id, _new_name, _new_phone, _new_email)
        updated_something = True
    
    if not updated_something:
        display.display_message("Không có thay đổi nào được thực hiện.")


def delete_customer_view(manager: ManageCustomer):
    display.display_message("--- Xoá khách hàng ---")
    customer_id = get_id_input("Nhập mã khách hàng cần xoá: ")
    manager.delete_customer(customer_id)

def search_customer_view(manager: ManageCustomer):
    display.display_message("--- Tìm kiếm khách hàng ---")
    keyword = get_string_input("Nhập từ khoá tìm kiếm (Mã, Tên hoặc SĐT): ")
    results = manager.search_customer(keyword)
    display.display_customer_list(results, f"Kết quả tìm kiếm cho '{keyword}'")

def list_all_customers_view(manager: ManageCustomer):
    display.display_customer_list(manager.get_all_customers(), "Danh sách tất cả khách hàng")

def list_customers_by_type_view(manager: ManageCustomer):
    display.display_message("--- Liệt kê khách hàng theo loại ---")
    type_choice = get_string_input("Nhập loại khách hàng (Casual/Loyal): ").capitalize()
    if type_choice not in ["Casual", "Loyal"]:
        display.display_message("Loại không hợp lệ. Vui lòng nhập 'Casual' hoặc 'Loyal'.", is_error=True)
        return
    customers = manager.list_customers_by_type(type_choice)
    
    display.display_customer_list(customers, f"Khách hàng {type_choice}")

def display_revenue_reports_view(manager: ManageCustomer):
    display.display_revenue_report(manager)

def display_top_customers_view(manager: ManageCustomer):
    n = 3 # Hiển thị 3 khách hàng mua nhiều nhất
    top_customers = manager.report_top_customers(n)
    display.display_top_customers(top_customers, n)
    
    # Additional: Hiển thị 3 khách hàng mua hàng nhiều nhất (sắp xếp danh sách theo giá trị mua hàng giảm dần).
    # This is essentially the same as report_top_customers.
    # If it means 'most purchase count', we'd need another sorting key.
    # The term "giá trị mua hàng" strongly suggests total_spent.
    sorted_by_spent_desc = manager.sort_by_total_spent(reverse=True)
    display.display_customer_list(sorted_by_spent_desc, "Khách hàng theo tổng chi tiêu (giảm dần)")


def display_tet_promotion_view(manager: ManageCustomer):
    candidates = manager.get_tet_promotion_candidates()
    display.display_tet_promotion_list(candidates)

def add_loyalty_points_view(manager: ManageCustomer):
    display.display_message("--- Thêm điểm tích lũy ---")
    customer_id = get_id_input("Nhập mã khách hàng thân thiết: ")
    points = get_int_input("Nhập số điểm cần thêm: ", min_val=1)
    manager.add_loyalty_points_to_customer(customer_id, points)