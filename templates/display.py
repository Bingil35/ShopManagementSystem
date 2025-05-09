def display_main_menu():
    """Displays the main menu options."""
    print("\n===== HỆ THỐNG QUẢN LÝ KHÁCH HÀNG SIÊU THỊ =====")
    print("1. Thêm mới khách hàng")
    print("2. Sửa thông tin khách hàng")
    print("3. Xoá khách hàng")
    print("4. Tìm kiếm khách hàng (theo Mã KH, Tên)") # Requirement only mentions Mã KH, Tên
    print("5. Hiển thị danh sách khách hàng (theo phân loại)")
    print("6. Tính tổng doanh thu")
    print("7. Hiển thị 3 khách hàng mua hàng nhiều nhất")
    print("8. Thống kê khách hàng thân thiết nhận quà Tết")
    print("9. Thêm giao dịch mua hàng cho khách hàng") # Added for interaction with purchase_history
    print("0. Thoát chương trình")
    print("================================================")

def get_user_choice():
    """Gets the user's menu choice."""
    return input("Nhập lựa chọn của bạn: ").strip()

def display_message(message, is_error=False):
    """Displays a generic message or an error message."""
    prefix = "LỖI: " if is_error else "THÔNG BÁO: "
    print(f"{prefix}{message}")

def display_customer_details(customer):
    """Displays the details of a single customer using its __str__ method."""
    if customer:
        print("-" * 20)
        print(customer) # Relies on the __str__ methods in your customer classes
        print(f"  Tổng chi tiêu: {customer.total_spent():,.0f} VND")
        print(f"  Số lần mua: {customer.purchase_count()}")
        print(f"  Chi tiêu trung bình/lần: {customer.average_spent():,.2f} VND")
        print("-" * 20)
    else:
        display_message("Không tìm thấy thông tin khách hàng.", True)


def display_customer_list(customers, title="Danh sách khách hàng"):
    """Displays a list of customers."""
    print(f"\n--- {title} ---")
    if not customers:
        print("Không có khách hàng nào để hiển thị.")
        return
    for customer in customers:
        display_customer_details(customer) # Uses the detailed display

def display_revenue_report(total_revenue_all, total_revenue_loyal, total_revenue_casual,
                           avg_spent_loyal_type, avg_spent_casual_type):
    """Displays the revenue report."""
    print("\n--- Báo cáo doanh thu ---")
    print(f"Tổng doanh thu toàn bộ siêu thị: {total_revenue_all:,.0f} VND")
    print(f"Tổng doanh thu từ Khách hàng thân thiết: {total_revenue_loyal:,.0f} VND")
    print(f"Tổng doanh thu từ Khách hàng vãng lai: {total_revenue_casual:,.0f} VND")
    print("\n--- Trung bình giá trị mua hàng theo loại khách hàng ---")
    print(f"Trung bình chi tiêu của loại Khách hàng thân thiết: {avg_spent_loyal_type:,.0f} VND/khách")
    print(f"Trung bình chi tiêu của loại Khách hàng vãng lai: {avg_spent_casual_type:,.0f} VND/khách")
    print("-" * 20)

def display_top_spenders(customers):
    """Displays top spending customers."""
    print("\n--- Top khách hàng mua nhiều nhất ---")
    if not customers:
        print("Chưa có khách hàng nào để xếp hạng.")
        return
    for i, customer in enumerate(customers):
        print(f"{i+1}. {customer.name} (Mã: {customer.customer_id}) - Tổng mua: {customer.total_spent():,.0f} VND")
    print("-" * 20)

def display_tet_gift_candidates(candidates):
    """Displays customers eligible for Tet gifts."""
    print("\n--- Khách hàng thân thiết đủ điều kiện nhận quà Tết ---")
    if not candidates:
        print("Không có khách hàng nào đủ điều kiện.")
        return
    for customer in candidates:
        print(f"- {customer.name} (Mã: {customer.customer_id}), Điểm: {customer.loyalty_points}, TB mua hàng: {customer.average_spent():,.0f} VND")
    print("-" * 20)

def get_customer_base_info(is_update=False, existing_customer=None):
    """Gets base customer information (ID, name, phone, email)."""
    customer_id = None
    if not is_update:
        while True:
            customer_id = input("Nhập Mã khách hàng (bắt buộc): ").strip()
            if customer_id:
                break
            display_message("Mã khách hàng không được để trống.", True)
    else: # For updates, ID is typically fixed or pre-fetched
        customer_id = existing_customer.customer_id if existing_customer else input("Nhập Mã khách hàng cần sửa: ").strip()


    default_name = existing_customer.name if existing_customer and is_update else ""
    name = input(f"Nhập Tên khách hàng (hiện tại: '{default_name}', bỏ trống nếu không đổi): ").strip() or default_name

    while True:
        default_phone = existing_customer.phone if existing_customer and is_update else ""
        phone = input(f"Nhập Số điện thoại (bắt buộc, hiện tại: '{default_phone}', bỏ trống nếu không đổi): ").strip() or default_phone
        if phone:
            break
        display_message("Số điện thoại không được để trống.", True)

    default_email = existing_customer.email if existing_customer and is_update else ""
    email = input(f"Nhập Email (hiện tại: '{default_email}', bỏ trống nếu không đổi): ").strip() or default_email

    return customer_id, name, phone, email

def get_purchase_amount():
    """Gets the purchase amount from the user."""
    while True:
        try:
            amount = float(input("Nhập số tiền mua hàng: "))
            if amount > 0:
                return amount
            else:
                display_message("Số tiền mua hàng phải là số dương.", True)
        except ValueError:
            display_message("Vui lòng nhập một số hợp lệ cho số tiền mua hàng.", True)

def get_loyalty_points_to_add_or_redeem(action="thêm"):
    """Gets loyalty points from user for adding or redeeming."""
    while True:
        try:
            points_str = input(f"Nhập số điểm tích lũy muốn {action} (hoặc bỏ trống): ").strip()
            if not points_str:
                return None # User chose not to change
            points = int(points_str)
            if points > 0:
                return points
            else:
                display_message(f"Số điểm {action} phải là số dương.", True)
        except ValueError:
            display_message("Vui lòng nhập một số nguyên hợp lệ cho điểm.", True)