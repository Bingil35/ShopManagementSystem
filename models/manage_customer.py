import pickle
from models.customer import Customer
from models.loyal_customer import LoyalCustomer
from models.casual_customer import CasualCustomer

LOYALTY_THRESHOLD = 2000000

class ManageCustomer:
    def __init__(self):
        self.customers = [] # List[Customer]

    def _find_customer_index(self, customer_id):
        for i, customer in enumerate(self.customers):
            if customer.customer_id == customer_id:
                return i
        return -1

    def add_customer(self, customer_id, name, phone, email):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                print(f"Lỗi: Mã khách hàng '{customer_id}' đã tồn tại.")
                return None
            if customer.phone == phone:
                print(f"Lỗi: Số điện thoại '{phone}' đã tồn tại.")
                return None
            if customer.email.lower() == email.lower():
                print(f"Lỗi: Email '{email}' đã tồn tại.")
                return None

        new_customer = CasualCustomer(customer_id, name, phone, email)
        self.customers.append(new_customer)
        print(f"Khách hàng '{name}' đã được thêm thành công.")
        return new_customer

    def delete_customer(self, customer_id):
        index = self._find_customer_index(customer_id)
        if index != -1:
            removed_customer = self.customers.pop(index)
            print(f"Customer {removed_customer.name} (ID: {customer_id}) deleted successfully.")
            return True
        else:
            print(f"Error: Customer with ID {customer_id} not found.")
            return False

    def update_customer_info(self, customer_id, new_name=None, new_phone=None, new_email=None):
        index = self._find_customer_index(customer_id)
        if index != -1:
            customer = self.customers[index]
            if new_name:
                customer.name = new_name
            if new_phone:
                customer.phone = new_phone
            if new_email:
                customer.email = new_email
            print(f"Customer {customer.name} (ID: {customer_id}) updated successfully.")
            return True
        else:
            print(f"Error: Customer with ID {customer_id} not found for update.")
            return False

    def add_purchase_to_customer(self, customer_id, amount):
        index = self._find_customer_index(customer_id)
        if index != -1:
            customer = self.customers[index]
            customer.add_purchase(amount)
            print(f"Purchase of {amount} added for customer {customer.name}.")
            self.update_customer_type(customer) # Check if type needs to change
            return True
        else:
            print(f"Error: Customer with ID {customer_id} not found to add purchase.")
            return False
            
    def add_loyalty_points_to_customer(self, customer_id, points):
        index = self._find_customer_index(customer_id)
        if index != -1:
            customer = self.customers[index]
            if isinstance(customer, LoyalCustomer):
                customer.add_loyalty_points(points)
                print(f"{points} loyalty points added to {customer.name}.")
                return True
            else:
                print(f"Error: Customer {customer.name} is not a Loyal Customer.")
                return False
        else:
            print(f"Error: Customer with ID {customer_id} not found.")
            return False


    def update_customer_type(self, customer):
        """
        Updates the customer type based on total spending.
        If a CasualCustomer's total_spent >= LOYALTY_THRESHOLD, they become Loyal.
        """
        index = self._find_customer_index(customer.customer_id)
        if index == -1:
            return # Should not happen if customer is managed

        current_customer = self.customers[index]

        if isinstance(current_customer, CasualCustomer) and current_customer.total_spent() >= LOYALTY_THRESHOLD:
            # Upgrade to LoyalCustomer
            loyal_cust = LoyalCustomer(
                customer_id=current_customer.customer_id,
                name=current_customer.name,
                phone=current_customer.phone,
                email=current_customer.email
            )
            # Transfer purchase history and potentially initial loyalty points
            loyal_cust.purchase_history = list(current_customer.purchase_history)
            # loyal_cust.loyalty_points = 0 # Or some initial points
            
            self.customers[index] = loyal_cust
            print(f"Customer {loyal_cust.name} (ID: {loyal_cust.customer_id}) has been upgraded to Loyal Customer.")
        
        # Downgrade (Optional, not explicitly in requirements but good to consider)
        # elif isinstance(current_customer, LoyalCustomer) and current_customer.total_spent() < LOYALTY_THRESHOLD:
        #     casual_cust = CasualCustomer(
        #         customer_id=current_customer.customer_id,
        #         name=current_customer.name,
        #         phone=current_customer.phone,
        #         email=current_customer.email
        #     )
        #     casual_cust.purchase_history = list(current_customer.purchase_history)
        #     self.customers[index] = casual_cust
        #     print(f"Customer {casual_cust.name} has been downgraded to Casual Customer.")


    def search_customer(self, keyword):
        keyword = keyword.lower()
        results = []
        for customer in self.customers:
            if (keyword in customer.customer_id.lower() or
                keyword in customer.name.lower() or
                keyword in customer.phone.lower()):
                results.append(customer)
        return results

    def list_customers_by_type(self, type_name):
        type_name = type_name.lower()
        results = []
        for customer in self.customers:
            if customer.get_type().lower() == type_name:
                results.append(customer)
        return results
    
    def get_all_customers(self):
        return self.customers

    def sort_by_total_spent(self, reverse=True):
        return sorted(self.customers, key=lambda c: c.total_spent(), reverse=reverse)

    def report_top_customers(self, n=3):
        sorted_customers = self.sort_by_total_spent(reverse=True)
        return sorted_customers[:n]

    def report_total_revenue(self):
        return sum(customer.total_spent() for customer in self.customers)

    def report_average_spending_per_customer(self):
        if not self.customers:
            return 0
        return self.report_total_revenue() / len(self.customers)

    def report_total_revenue_by_type(self, customer_type):
        """Calculates total revenue for a specific customer type ('Loyal' or 'Casual')."""
        type_customers = self.list_customers_by_type(customer_type)
        return sum(customer.total_spent() for customer in type_customers)

    def report_average_spending_by_type(self, customer_type):
        """Calculates average spending for a specific customer type."""
        type_customers = self.list_customers_by_type(customer_type)
        if not type_customers:
            return 0
        total_spent_by_type = sum(customer.total_spent() for customer in type_customers)
        return total_spent_by_type / len(type_customers)
    
    def get_tet_promotion_candidates(self):
        """
        Returns top 10 loyal customers with > 500 loyalty points,
        sorted by average purchase value (descending).
        """
        candidates = []
        for customer in self.customers:
            if isinstance(customer, LoyalCustomer) and customer.loyalty_points > 500:
                candidates.append(customer)
        
        # Sort by average_spent in descending order
        candidates.sort(key=lambda c: c.average_spent(), reverse=True)
        return candidates[:10]

    def save_data(self, filename="data/shop_data.pkl"):
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        try:
            with open(filename, "wb") as f:
                pickle.dump(self.customers, f)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self, filename="data/shop_data.pkl"):
        try:
            with open(filename, "rb") as f:
                self.customers = pickle.load(f)
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No saved data found. Starting with an empty customer list.")
            self.customers = []
        except Exception as e:
            print(f"Error loading data: {e}. Starting with an empty list.")
            self.customers = []