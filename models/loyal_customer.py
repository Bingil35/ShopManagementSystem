from models.customer import Customer

class LoyalCustomer(Customer):
    def __init__(self, customer_id, name, phone, email):
        super().__init__(customer_id, name, phone, email)
        self.loyalty_points = 0

    def add_loyalty_points(self, points):
        if points > 0:
            self.loyalty_points += points
        # else:
        #     raise ValueError("Loyalty points must be positive")

    def redeem_loyalty_points(self, points):
        if 0 < points <= self.loyalty_points:
            self.loyalty_points -= points
        # else:
        #     raise ValueError("Invalid number of loyalty points to redeem")

    def get_type(self):
        return "Thân thiết"
    def __str__(self):
        return f"{super().__str__()}| Điểm thành viên: {self.loyalty_points}| Loại khách hàng: {self.get_type()}"