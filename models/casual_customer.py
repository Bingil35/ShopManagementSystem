from models.customer import Customer

class CasualCustomer(Customer):
    def __init__(self, customer_id, name, phone, email):
        super().__init__(customer_id, name, phone, email)
    
    def get_type(self):
        return "Vãng lai"