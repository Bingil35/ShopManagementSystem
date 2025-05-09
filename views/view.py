from models.customer import Customer # ABC, not directly instantiated
from models.loyal_customer import LoyalCustomer
from models.casual_customer import CasualCustomer
from templates import display # Import the display module

class ShopView:
    PROMOTION_THRESHOLD = 2000000.0 # 2 triệu VND

    def __init__(self):
        self.customers = [] # List to store customer objects

    def _find_customer_by_id(self, customer_id):
        """Finds a customer by ID and returns the customer object and its index."""
        for i, customer in enumerate(self.customers):
            if customer.customer_id == customer_id:
                return customer, i
        return None, -1

    def _check_and_promote_customer(self, customer_index):
        """Checks if a CasualCustomer should be promoted to LoyalCustomer."""
        customer = self.customers[customer_index]
        if isinstance(customer, CasualCustomer) and customer.total_spent() > self.PROMOTION_THRESHOLD:
            display.display_message(f"Khách hàng {customer.name} ({customer.customer_id}) "
                                    f"với tổng chi tiêu {customer.total_spent():,.0f} VND đủ điều kiện nâng cấp.")
            # Create a new LoyalCustomer, preserving data
            promoted_customer = LoyalCustomer(
                customer_id=customer.customer_id,
                name=customer.name,
                phone=customer.phone,
                email=customer.email
            )
            # Transfer purchase history
            for purchase in customer.purchase_history:
                promoted_customer.add_purchase(purchase)
            # Assuming new loyal customers start with 0 points unless earned
            # promoted_customer.add_loyalty_points(0) # or some initial points

            self.customers[customer_index] = promoted_customer
            display.display_message(f"Đã nâng cấp khách hàng {promoted_customer.name} thành Khách hàng thân thiết.")
            return True
        return False

    def add_customer(self):
        """Adds a new customer to the system."""
        display.display_message("--- Thêm khách hàng mới ---")
        customer_id, name, phone, email = display.get_customer_base_info()

        # Check for duplicate ID
        existing_customer, _ = self._find_customer_by_id(customer_id)
        if existing_customer:
            display.display_message(f"Mã khách hàng '{customer_id}' đã tồn tại.", True)
            return

        while True:
            type_choice = input("Loại khách hàng (1: Thân thiết, 2: Vãng lai, mặc định là Vãng lai): ").strip()
            if type_choice == '1':
                customer = LoyalCustomer(customer_id, name, phone, email)
                # Optionally ask for initial loyalty points
                points_to_add = display.get_loyalty_points_to_add_or_redeem("thêm ban đầu")
                if points_to_add is not None:
                    customer.add_loyalty_points(points_to_add)
                break
            elif type_choice == '2' or not type_choice: # Default to Casual
                customer = CasualCustomer(customer_id, name, phone, email)
                break
            else:
                display.display_message("Lựa chọn không hợp lệ. Vui lòng chọn 1 hoặc 2.", True)

        self.customers.append(customer)
        display.display_message(f"Đã thêm khách hàng '{name}' ({customer.get_type()}) thành công.")
        # For CasualCustomer, initial total_spent is 0, so no immediate promotion.
        # Promotion happens after adding purchases.

    def add_purchase_to_customer(self):
        """Adds a purchase transaction for a customer."""
        display.display_message("--- Thêm giao dịch mua hàng ---")
        customer_id = input("Nhập Mã khách hàng để thêm giao dịch: ").strip()
        customer, index = self._find_customer_by_id(customer_id)

        if not customer:
            display.display_message(f"Không tìm thấy khách hàng với mã '{customer_id}'.", True)
            return

        amount = display.get_purchase_amount()
        customer.add_purchase(amount)
        display.display_message(f"Đã thêm giao dịch {amount:,.0f} VND cho khách hàng {customer.name}.")

        # Optional: Award loyalty points for LoyalCustomers after purchase
        if isinstance(customer, LoyalCustomer):
            # Example: 1 point for every 100,000 VND spent in this transaction
            points_earned = int(amount // 100000)
            if points_earned > 0:
                customer.add_loyalty_points(points_earned)
                display.display_message(f"Khách hàng {customer.name} được cộng {points_earned} điểm tích lũy.")

        # Check for promotion if CasualCustomer
        if isinstance(customer, CasualCustomer):
            self._check_and_promote_customer(index)


    def edit_customer_info(self):
        """Edits an existing customer's information."""
        display.display_message("--- Sửa thông tin khách hàng ---")
        customer_id_to_edit = input("Nhập Mã khách hàng cần sửa: ").strip()
        customer, index = self._find_customer_by_id(customer_id_to_edit)

        if not customer:
            display.display_message(f"Không tìm thấy khách hàng với mã '{customer_id_to_edit}'.", True)
            return

        display.display_message("Thông tin hiện tại của khách hàng:")
        display.display_customer_details(customer)

        _, name, phone, email = display.get_customer_base_info(is_update=True, existing_customer=customer)
        
        customer.name = name
        customer.phone = phone
        customer.email = email

        if isinstance(customer, LoyalCustomer):
            action_choice = input("Bạn có muốn (1) Thêm điểm, (2) Trừ điểm tích lũy không? (bỏ trống nếu không): ").strip()
            if action_choice == '1':
                points = display.get_loyalty_points_to_add_or_redeem("thêm")
                if points: customer.add_loyalty_points(points)
            elif action_choice == '2':
                points = display.get_loyalty_points_to_add_or_redeem("trừ")
                if points:
                    try:
                        customer.redeem_loyalty_points(points)
                    except ValueError as e: # Assuming redeem_loyalty_points might raise ValueError
                        display.display_message(str(e), True)


        display.display_message(f"Đã cập nhật thông tin cho khách hàng '{customer_id_to_edit}'.")
        # Note: Editing basic info doesn't trigger promotion check.
        # Promotion is tied to `total_spent` which changes via `add_purchase_to_customer`.

    def delete_customer(self):
        """Deletes a customer from the system."""
        display.display_message("--- Xoá khách hàng ---")
        customer_id = input("Nhập Mã khách hàng cần xoá: ").strip()
        customer, index = self._find_customer_by_id(customer_id)

        if not customer:
            display.display_message(f"Không tìm thấy khách hàng với mã '{customer_id}'.", True)
            return

        confirm = input(f"Bạn có chắc chắn muốn xoá khách hàng {customer.name} (Mã: {customer_id})? (y/n): ").strip().lower()
        if confirm == 'y':
            del self.customers[index]
            display.display_message(f"Đã xoá khách hàng '{customer_id}'.")
        else:
            display.display_message("Hủy thao tác xoá.")

    def search_customers(self):
        """Searches for customers by ID or Name."""
        display.display_message("--- Tìm kiếm khách hàng ---")
        if not self.customers:
            display.display_message("Chưa có khách hàng nào trong hệ thống.")
            return

        keyword = input("Nhập từ khoá tìm kiếm (Mã KH hoặc Tên KH): ").strip().lower()
        if not keyword:
            display.display_message("Vui lòng nhập từ khoá.", True)
            return

        results = [
            customer for customer in self.customers
            if keyword in customer.customer_id.lower() or keyword in customer.name.lower()
        ]

        if results:
            display.display_customer_list(results, f"Kết quả tìm kiếm cho '{keyword}'")
        else:
            display.display_message(f"Không tìm thấy khách hàng nào phù hợp với từ khoá '{keyword}'.")

    def display_all_customers_by_type(self):
        """Displays all customers, categorized by type."""
        display.display_message("\n--- Danh sách khách hàng ---")
        if not self.customers:
            display.display_message("Chưa có khách hàng nào trong hệ thống.")
            return

        loyal_customers = [c for c in self.customers if isinstance(c, LoyalCustomer)]
        casual_customers = [c for c in self.customers if isinstance(c, CasualCustomer)]

        if loyal_customers:
            display.display_customer_list(loyal_customers, "Khách hàng thân thiết")
        else:
            display.display_message("Không có khách hàng thân thiết nào.")

        if casual_customers:
            display.display_customer_list(casual_customers, "Khách hàng vãng lai")
        else:
            display.display_message("Không có khách hàng vãng lai nào.")

    def calculate_and_display_revenue(self):
        """Calculates and displays total revenue and revenue by customer type."""
        if not self.customers:
            display.display_message("Chưa có dữ liệu khách hàng để tính doanh thu.", True)
            return

        total_revenue_all = sum(c.total_spent() for c in self.customers)
        
        loyal_customers = [c for c in self.customers if isinstance(c, LoyalCustomer)]
        casual_customers = [c for c in self.customers if isinstance(c, CasualCustomer)]

        total_revenue_loyal = sum(c.total_spent() for c in loyal_customers)
        total_revenue_casual = sum(c.total_spent() for c in casual_customers)
        
        avg_spent_loyal_type = (total_revenue_loyal / len(loyal_customers)) if loyal_customers else 0
        avg_spent_casual_type = (total_revenue_casual / len(casual_customers)) if casual_customers else 0
        
        display.display_revenue_report(total_revenue_all, total_revenue_loyal, total_revenue_casual,
                                       avg_spent_loyal_type, avg_spent_casual_type)
        
        # Yêu cầu cũng có "Tính trung bình giá trị mua hàng của từng khách hàng"
        # This is already part of display_customer_details which is used by display_customer_list
        print("\n--- Chi tiêu trung bình của từng khách hàng ---")
        if self.customers:
            for cust in self.customers:
                print(f"  {cust.name} (Mã: {cust.customer_id}): {cust.average_spent():,.2f} VND/lần mua")
        else:
            print("  Không có khách hàng nào.")
        print("-" * 20)


    def display_top_3_spenders(self):
        """Displays the top 3 customers by total spending."""
        if not self.customers:
            display.display_message("Chưa có khách hàng nào trong hệ thống.", True)
            return

        # Sort customers by total_spent in descending order
        sorted_customers = sorted(self.customers, key=lambda c: c.total_spent(), reverse=True)
        display.display_top_spenders(sorted_customers[:3])


    def display_tet_gift_candidates(self):
        """Displays LoyalCustomers eligible for Tet gifts."""
        if not self.customers:
            display.display_message("Chưa có khách hàng nào trong hệ thống.", True)
            return

        # 1. Filter LoyalCustomers with loyalty_points > 500
        eligible_by_points = [
            lc for lc in self.customers
            if isinstance(lc, LoyalCustomer) and lc.loyalty_points > 500
        ]

        if not eligible_by_points:
            display.display_message("Không có Khách hàng thân thiết nào có > 500 điểm tích lũy.")
            return

        # 2. Get top 10 customers by average_spent() from ALL customers
        all_customers_sorted_by_avg_spent = sorted(
            self.customers,
            key=lambda c: c.average_spent(),
            reverse=True
        )
        top_10_avg_spenders_ids = {c.customer_id for c in all_customers_sorted_by_avg_spent[:10]}

        if not top_10_avg_spenders_ids:
            display.display_message("Không có đủ dữ liệu khách hàng để xác định top 10 theo chi tiêu trung bình.")
            return
            
        # 3. Find the intersection: LoyalCustomers who are in eligible_by_points AND in top_10_avg_spenders_ids
        final_candidates = [
            lc for lc in eligible_by_points if lc.customer_id in top_10_avg_spenders_ids
        ]
        display.display_tet_gift_candidates(final_candidates)

    def run(self):
        """Main loop for the application."""
        # Sample Data (Optional - for quick testing)
        # c1 = LoyalCustomer("TT001", "Nguyen Van A", "0901234567", "a@test.com")
        # c1.add_purchase(1000000)
        # c1.add_purchase(1500000) # Total 2.5M, Avg 1.25M
        # c1.add_loyalty_points(600)
        # self.customers.append(c1)

        # c2 = CasualCustomer("VL001", "Tran Thi B", "0912223333", "b@test.com")
        # c2.add_purchase(500000) # Total 0.5M
        # self.customers.append(c2)

        # c3 = CasualCustomer("VL002", "Le Van C", "0923334444", "c@test.com")
        # c3.add_purchase(1000000)
        # c3.add_purchase(1200000) # Total 2.2M -> should promote
        # self.customers.append(c3)
        # # Manually trigger check for sample data if added like this
        # for i, cust in enumerate(self.customers):
        #     if cust.customer_id == "VL002":
        #         self._check_and_promote_customer(i)
        #         break
        
        # c4 = LoyalCustomer("TT002", "Pham Thi D", "0987654321", "d@test.com")
        # c4.add_purchase(3000000) # Total 3M, Avg 3M
        # c4.add_loyalty_points(400)
        # self.customers.append(c4)

        # c5 = LoyalCustomer("TT003", "Hoang Van E", "0911111111", "e@test.com")
        # c5.add_purchase(2000000) # Total 2M, Avg 2M
        # c5.add_loyalty_points(550)
        # self.customers.append(c5)


        while True:
            display.display_main_menu()
            choice = display.get_user_choice()

            if choice == '1':
                self.add_customer()
            elif choice == '2':
                self.edit_customer_info()
            elif choice == '3':
                self.delete_customer()
            elif choice == '4':
                self.search_customers()
            elif choice == '5':
                self.display_all_customers_by_type()
            elif choice == '6':
                self.calculate_and_display_revenue()
            elif choice == '7':
                self.display_top_3_spenders()
            elif choice == '8':
                self.display_tet_gift_candidates()
            elif choice == '9':
                self.add_purchase_to_customer()
            elif choice == '0':
                display.display_message("Đã thoát chương trình. Tạm biệt!")
                break
            else:
                display.display_message("Lựa chọn không hợp lệ. Vui lòng thử lại.", True)
            
            if choice != '0': # Don't pause if exiting
                input("\nNhấn Enter để tiếp tục...")


if __name__ == "__main__":
    app_view = ShopView()
    app_view.run()