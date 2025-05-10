def display_customer(customer):
    """Hiển thị thông tin khách hàng."""
    print(str(customer))

def display_customer_list(customers, title="Danh sách khách hàng"):
    """Hiển thị danh sách khách hàng."""
    print(f"\n--- {title} ---")
    if not customers:
        print("Không tìm thấy khách hàng.")
        return
    for i, customer in enumerate(customers):
        print(f"{i+1}. {str(customer)}")
    print("--------------------")

def display_menu(options):
    """
    Hiển thị menu với các lựa chọn được đánh số.
    
    """
    print("\n===== MENU QUẢN LÝ CỬA HÀNG =====")
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    print("0. Thoát")
    print("==============================")

def display_message(message, is_error=False):
    """Hiển thị thông báo chung hoặc thông báo lỗi."""
    prefix = "THÔNG BÁO: "
    if is_error:
        prefix = "LỖI: "
    print(f"{prefix}{message}")

def display_revenue_report(manager):
    """Hiển thị báo cáo doanh thu."""
    print("\n--- Báo cáo doanh thu ---")
    print(f"Tổng doanh thu (Tất cả khách hàng): {manager.report_total_revenue():,.0f} VND")
    print(f"Chi tiêu trung bình mỗi khách hàng: {manager.report_average_spending_per_customer():,.0f} VND")
    
    print(f"\nTổng doanh thu (Khách hàng thân thiết): {manager.report_total_revenue_by_type('Loyal'):,.0f} VND")
    print(f"Chi tiêu trung bình (Khách hàng thân thiết): {manager.report_average_spending_by_type('Loyal'):,.0f} VND")

    print(f"\nTổng doanh thu (Khách hàng vãng lai): {manager.report_total_revenue_by_type('Casual'):,.0f} VND")
    print(f"Chi tiêu trung bình (Khách hàng vãng lai): {manager.report_average_spending_by_type('Casual'):,.0f} VND")
    print("----------------------")

def display_top_customers(customers, count):
    """Hiển thị top N khách hàng theo tổng chi tiêu."""
    title = f"Top {count} khách hàng chi tiêu nhiều nhất"
    display_customer_list(customers, title)

def display_tet_promotion_list(customers):
    """Hiển thị danh sách khách hàng đủ điều kiện khuyến mãi Tết."""
    title = "Ứng viên khuyến mãi Tết (Thân thiết > 500 điểm, sắp xếp theo chi tiêu trung bình)"
    if not customers:
        print(f"\n--- {title} ---")
        print("Không có khách hàng nào đủ điều kiện khuyến mãi Tết.")
        print("--------------------")
        return
    
    print(f"\n--- {title} ---")
    for i, customer in enumerate(customers):
        print(f"{i+1}. Mã KH: {customer.customer_id}, Tên: {customer.name}, "
              f"Điểm tích lũy: {customer.loyalty_points}, Chi tiêu TB: {customer.average_spent():,.0f} VND")
    print("--------------------")