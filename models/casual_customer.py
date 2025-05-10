from models.customer import Customer

class CasualCustomer(Customer):
    def __init__(self, customer_id, name, phone, email):
        super().__init__(customer_id, name, phone, email)
    
    def get_type(self):
        return "Vãng lai"
    
    def __str__(self):
        return f"{super().__str__()}| Loại khách hàng: {self.get_type()}"