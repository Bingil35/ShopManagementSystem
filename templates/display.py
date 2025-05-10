def display_customer(customer):
    """Displays a single customer's details."""
    print(str(customer))

def display_customer_list(customers, title="Customer List"):
    """Displays a list of customers."""
    print(f"\n--- {title} ---")
    if not customers:
        print("No customers found.")
        return
    for i, customer in enumerate(customers):
        print(f"{i+1}. {str(customer)}")
    print("--------------------")

def display_menu(options):
    """
    Displays a menu with numbered options.
    options: A list of strings, where each string is a menu item.
    """
    print("\n===== SHOP MANAGEMENT MENU =====")
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    print("0. Exit")
    print("==============================")

def display_message(message, is_error=False):
    """Displays a generic message or an error message."""
    prefix = "INFO: "
    if is_error:
        prefix = "ERROR: "
    print(f"{prefix}{message}")

def display_revenue_report(manager):
    """Displays various revenue statistics."""
    print("\n--- Revenue Report ---")
    print(f"Total Revenue (All Customers): {manager.report_total_revenue():,.0f} VND")
    print(f"Average Spending per Customer (All): {manager.report_average_spending_per_customer():,.0f} VND")
    
    print(f"\nTotal Revenue (Loyal Customers): {manager.report_total_revenue_by_type('Loyal'):,.0f} VND")
    print(f"Average Spending (Loyal Customers): {manager.report_average_spending_by_type('Loyal'):,.0f} VND")

    print(f"\nTotal Revenue (Casual Customers): {manager.report_total_revenue_by_type('Casual'):,.0f} VND")
    print(f"Average Spending (Casual Customers): {manager.report_average_spending_by_type('Casual'):,.0f} VND")
    print("----------------------")

def display_top_customers(customers, count):
    """Displays top N customers."""
    title = f"Top {count} Customers by Total Spent"
    display_customer_list(customers, title)

def display_tet_promotion_list(customers):
    """Displays customers eligible for Tet promotion."""
    title = "Tet Promotion Candidates (Loyal > 500 points, sorted by Avg. Purchase)"
    if not customers:
        print(f"\n--- {title} ---")
        print("No customers eligible for Tet promotion.")
        print("--------------------")
        return
    
    print(f"\n--- {title} ---")
    for i, customer in enumerate(customers):
        print(f"{i+1}. ID: {customer.customer_id}, Name: {customer.name}, "
              f"Loyalty Points: {customer.loyalty_points}, Avg. Spent: {customer.average_spent():,.0f} VND")
    print("--------------------")