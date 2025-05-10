from abc import ABC, abstractmethod

class Customer(ABC):
    def __init__(self, customer_id, name, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email
        self.purchase_history = []
        
    def add_purchase(self, amount):
        if isinstance(amount, (int, float)) and amount > 0:
            self.purchase_history.append(amount)
        else:
            raise ValueError("Số lần giao dịch là số nguyên dương!")
    
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
    
    def to_dict(self):
        return {
            "ID": self.customer_id,
            "Tên": self.name,
            "SĐT": self.phone,
            "Email": self.email,
            "Loại": self.get_type(),
            "Tổng giao dịch": self.total_spent(),
            "Số lần giao dịch": self.purchase_count(),
            "Trung bình giao dịch": round(self.average_spent(), 2)
        }
