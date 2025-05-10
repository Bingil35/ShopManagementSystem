from models.manage_customer import ManageCustomer, CasualCustomer # For type hints if needed
from templates import display

def get_string_input(prompt, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if value or allow_empty:
            return value
        display.display_message("Input cannot be empty.", is_error=True)

def get_id_input(prompt="Enter Customer ID: "):
    return get_string_input(prompt)

def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                display.display_message("Amount must be positive.", is_error=True)
        except ValueError:
            display.display_message("Invalid input. Please enter a number.", is_error=True)

def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if (min_val is None or value >= min_val) and \
               (max_val is None or value <= max_val):
                return value
            else:
                display.display_message(f"Input must be between {min_val} and {max_val}.", is_error=True)
        except ValueError:
            display.display_message("Invalid input. Please enter an integer.", is_error=True)


def get_customer_details_from_user():
    customer_id = get_id_input("Enter Customer ID: ")
    name = get_string_input("Enter Customer Name: ")
    phone = get_string_input("Enter Customer Phone: ")
    email = get_string_input("Enter Customer Email: ")
    return customer_id, name, phone, email

# --- Action Functions ---

def add_new_customer_view(manager: ManageCustomer):
    display.display_message("--- Add New Customer ---")
    customer_id, name, phone, email = get_customer_details_from_user()
    if manager.add_customer(customer_id, name, phone, email):
        # display.display_message(f"Customer {name} added successfully.") # Manager method already prints
        pass
    # else:
        # display.display_message(f"Failed to add customer.", is_error=True) # Manager method already prints

def add_purchase_view(manager: ManageCustomer):
    display.display_message("--- Add Purchase to Customer ---")
    customer_id = get_id_input("Enter Customer ID to add purchase to: ")
    amount = get_float_input("Enter purchase amount: ")
    manager.add_purchase_to_customer(customer_id, amount)

def update_customer_view(manager: ManageCustomer):
    display.display_message("--- Update Customer Information ---")
    customer_id = get_id_input("Enter Customer ID to update: ")
    
    customer_index = manager._find_customer_index(customer_id)
    if customer_index == -1:
        display.display_message(f"Customer with ID {customer_id} not found.", is_error=True)
        return

    customer = manager.customers[customer_index]
    display.display_message(f"Current details: {str(customer)}")

    new_name = get_string_input(f"Enter new name (current: {customer.name}) or press Enter to keep: ", allow_empty=True)
    new_phone = get_string_input(f"Enter new phone (current: {customer.phone}) or press Enter to keep: ", allow_empty=True)
    new_email = get_string_input(f"Enter new email (current: {customer.email}) or press Enter to keep: ", allow_empty=True)
    
    updated_something = False
    _new_name = new_name if new_name else None
    _new_phone = new_phone if new_phone else None
    _new_email = new_email if new_email else None

    if _new_name or _new_phone or _new_email:
        manager.update_customer_info(customer_id, _new_name, _new_phone, _new_email)
        updated_something = True
    
    if not updated_something:
        display.display_message("No changes made.")


def delete_customer_view(manager: ManageCustomer):
    display.display_message("--- Delete Customer ---")
    customer_id = get_id_input("Enter Customer ID to delete: ")
    manager.delete_customer(customer_id)

def search_customer_view(manager: ManageCustomer):
    display.display_message("--- Search Customer ---")
    keyword = get_string_input("Enter search keyword (ID, Name, or Phone): ")
    results = manager.search_customer(keyword)
    display.display_customer_list(results, f"Search Results for '{keyword}'")

def list_all_customers_view(manager: ManageCustomer):
    display.display_customer_list(manager.get_all_customers(), "All Customers")

def list_customers_by_type_view(manager: ManageCustomer):
    display.display_message("--- List Customers by Type ---")
    type_choice = get_string_input("Enter customer type (Casual/Loyal): ").capitalize()
    if type_choice not in ["Casual", "Loyal"]:
        display.display_message("Invalid type. Please enter 'Casual' or 'Loyal'.", is_error=True)
        return
    customers = manager.list_customers_by_type(type_choice)
    display.display_customer_list(customers, f"{type_choice} Customers")

def display_revenue_reports_view(manager: ManageCustomer):
    display.display_revenue_report(manager)

def display_top_customers_view(manager: ManageCustomer):
    n = 3 # As per requirement "3 khách hàng mua nhiều nhất"
    top_customers = manager.report_top_customers(n)
    display.display_top_customers(top_customers, n)
    
    # Additional: Hiển thị 3 khách hàng mua hàng nhiều nhất (sắp xếp danh sách theo giá trị mua hàng giảm dần).
    # This is essentially the same as report_top_customers.
    # If it means 'most purchase count', we'd need another sorting key.
    # The term "giá trị mua hàng" strongly suggests total_spent.
    sorted_by_spent_desc = manager.sort_by_total_spent(reverse=True)
    display.display_customer_list(sorted_by_spent_desc, "Customers Sorted by Total Spent (Descending)")


def display_tet_promotion_view(manager: ManageCustomer):
    candidates = manager.get_tet_promotion_candidates()
    display.display_tet_promotion_list(candidates)

def add_loyalty_points_view(manager: ManageCustomer):
    display.display_message("--- Add Loyalty Points ---")
    customer_id = get_id_input("Enter Loyal Customer ID: ")
    points = get_int_input("Enter loyalty points to add: ", min_val=1)
    manager.add_loyalty_points_to_customer(customer_id, points)