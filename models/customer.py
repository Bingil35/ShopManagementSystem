from abc import ABC, abstractmethod

class Customer(ABC):
    def __init__(self, customer_id, name, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email
        self.purchase_history = []
        
    def add_purchase(self, amount):
        if amount > 0:
            self.purchase_history.append(amount)
        # else:
        #     raise ValueError("Purchase amount must be positive")
    
    def total_spent(self):
        return sum(self.purchase_history)
    
    def purchase_count(self):
        return len(self.purchase_history)
    
    def average_spent(self):
        if self.purchase_count() > 0:
            return self.total_spent() / len(self.purchase_history)
        return 0
    
    @abstractmethod
    def get_type(self):
        pass
    
    def __str__(self):
        return f"ID: {self.customer_id}| Name: {self.name}| Phone: {self.phone}| Email: {self.email}| Type: {self.get_type()}"