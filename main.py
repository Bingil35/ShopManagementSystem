from models.manage_customer import ManageCustomer
from views import view
from templates import display

DATA_FILE = "data/shop_data.pkl" # Define data file path

def main():
    customer_manager = ManageCustomer()
    customer_manager.load_data(DATA_FILE) # Load data at startup

    menu_options = [
        "Add New Customer",
        "Add Purchase to Customer",
        "Update Customer Information",
        "Delete Customer",
        "Search Customer",
        "List All Customers",
        "List Customers by Type (Casual/Loyal)",
        "Display Revenue Reports",
        "Display Top 3 Customers (by total spent)",
        "Display Customers Sorted by Total Spent (Descending)", # Added based on YC3
        "Display Tet Promotion Candidates",
        "Add Loyalty Points to Loyal Customer" # Added for YC1 LoyalCustomer
    ]

    while True:
        display.display_menu(menu_options)
        try:
            choice = view.get_int_input("Enter your choice (0-12): ", 0, len(menu_options))

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
            elif choice == 10: # Display Customers Sorted by Total Spent
                all_customers_sorted = customer_manager.sort_by_total_spent(reverse=True)
                display.display_customer_list(all_customers_sorted, "Customers Sorted by Total Spent (Descending)")
            elif choice == 11:
                view.display_tet_promotion_view(customer_manager)
            elif choice == 12:
                view.add_loyalty_points_view(customer_manager)
            elif choice == 0:
                customer_manager.save_data(DATA_FILE) # Save data on exit
                display.display_message("Exiting program. Goodbye!")
                break
            else:
                display.display_message("Invalid choice. Please try again.", is_error=True)
            
            # Optionally save after every significant operation
            # customer_manager.save_data(DATA_FILE) 

        except ValueError:
            display.display_message("Invalid input. Please enter a number for choice.", is_error=True)
        except Exception as e:
            display.display_message(f"An unexpected error occurred: {e}", is_error=True)

if __name__ == "__main__":
    main()