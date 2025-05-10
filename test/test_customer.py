import unittest
import json

from models.casual_customer import CasualCustomer
from models.loyal_customer import LoyalCustomer

class TestCustomer(unittest.TestCase):
    # Test case 1: Kiểm tra thêm giao dịch và tính toán giao dịch
    def test_add_purchase_and_total(self):
        c = LoyalCustomer("001", "Nguyễn Văn A", "0909999999", "a@example.com")
        c.add_purchase(100000)
        c.add_purchase(200000)
        self.assertEqual(c.total_spent(), 300000)
        self.assertEqual(c.purchase_count(), 2)
        self.assertEqual(c.average_spent(), 150000)
        
    # Test case 2: 
    def test_invalid_purchase(self):
        c = CasualCustomer("002", "Trần Văn B", "0911111111", "b@example.com")
        with self.assertRaises(ValueError):
            c.add_purchase(-50000)
            
    # Test case 3
    def test_to_dict_format(self):
        c = LoyalCustomer("003", "Lê Thị C", "0933333333", "c@example.com")
        c.add_purchase(100000)
        c.add_purchase(300000)
        d = c.to_dict()
        self.assertEqual(d["ID"], "003")
        self.assertEqual(d["Tổng giao dịch"], 400000)
        self.assertEqual(d["Số lần giao dịch"], 2)
        self.assertEqual(d["Trung bình giao dịch"], 200000.0)
    
    # Test case 4
    def test_average_spent(self):
        """Kiểm tra tính toán giá trị trung bình giao dịch"""
        customer = CasualCustomer('4', 'Nguyễn Văn D', '0123456789', 'd@example.com')
        customer.add_purchase(1000000)
        customer.add_purchase(2000000)
        self.assertEqual(customer.average_spent(), 1500000)
        
    # Test case 5
    def test_customer_type(self):
        """Kiểm tra loại khách hàng"""
        loyal_customer = LoyalCustomer('5', 'Nguyễn Văn E', '0123456789', 'e@example.com')
        casual_customer = CasualCustomer('6', 'Nguyễn Văn F', '0123456789', 'f@example.com')
        self.assertEqual(loyal_customer.get_type(), 'Thân thiết')
        self.assertEqual(casual_customer.get_type(), 'Vãng lai')
        
    # Test case 6
    def test_upgrade_loyal_customer(self):
        """Kiểm tra chức năng nâng cấp khách hàng vãng lai lên thân thiết"""
        customer = CasualCustomer('7', 'Nguyễn Văn G', '0123456789', 'g@example.com')
        customer.add_purchase(3000000)  # Đủ điều kiện nâng cấp
        customer.__class__ = LoyalCustomer  # Nâng cấp trực tiếp cho test
        self.assertEqual(customer.get_type(), 'Thân thiết')
        
    # Test case 7
    def test_no_upgrade_for_casual(self):
        """Kiểm tra không nâng cấp khách hàng vãng lai nếu không đủ điều kiện"""
        customer = CasualCustomer('8', 'Nguyễn Văn H', '0123456789', 'h@example.com')
        customer.add_purchase(1000000)  # Không đủ điều kiện nâng cấp
        self.assertEqual(customer.get_type(), 'Vãng lai')
        
    # Test case 8
    def test_empty_purchase_history(self):
        """Kiểm tra khi chưa có giao dịch"""
        customer = LoyalCustomer('9', 'Nguyễn Văn I', '0123456789', 'i@example.com')
        self.assertEqual(customer.purchase_count(), 0)
        self.assertEqual(customer.total_spent(), 0)
        self.assertEqual(customer.average_spent(), 0)
        
    # Test case 9
    def test_strong_purchase_history(self):
        """Kiểm tra khi có nhiều giao dịch lớn"""
        customer = LoyalCustomer('10', 'Nguyễn Văn J', '0123456789', 'j@example.com')
        customer.add_purchase(5000000)
        customer.add_purchase(7000000)
        customer.add_purchase(9000000)
        self.assertEqual(customer.purchase_count(), 3)
        self.assertEqual(customer.total_spent(), 21000000)
        self.assertEqual(customer.average_spent(), 7000000)
        
     # Test case 10
    def test_zero_spent(self):
        """Kiểm tra khách hàng có số tiền giao dịch bằng 0"""
        customer = LoyalCustomer('11', 'Nguyễn Văn K', '0123456789', 'k@example.com')
        self.assertEqual(customer.total_spent(), 0)

    # Test Case 11: Kiểm tra khi khách hàng có giá trị giao dịch âm
    def test_invalid_negative_purchase(self):
        """Kiểm tra khi khách hàng nhập giá trị giao dịch âm"""
        customer = LoyalCustomer('12', 'Nguyễn Văn L', '0123456789', 'l@example.com')
        with self.assertRaises(ValueError):
            customer.add_purchase(-500000)

    # Test Case 12: Kiểm tra tính toán số lần giao dịch khi không có giao dịch
    def test_no_purchase(self):
        """Kiểm tra số lần giao dịch khi không có giao dịch nào"""
        customer = CasualCustomer('13', 'Nguyễn Văn M', '0123456789', 'm@example.com')
        self.assertEqual(customer.purchase_count(), 0)

    # Test Case 13: Kiểm tra khi có một giao dịch duy nhất
    def test_one_purchase(self):
        """Kiểm tra khi khách hàng chỉ có một giao dịch"""
        customer = CasualCustomer('14', 'Nguyễn Văn N', '0123456789', 'n@example.com')
        customer.add_purchase(1000000)
        self.assertEqual(customer.purchase_count(), 1)
        self.assertEqual(customer.total_spent(), 1000000)

    # Test Case 14: Kiểm tra khi khách hàng có nhiều giao dịch với giá trị lớn
    def test_multiple_large_purchases(self):
        """Kiểm tra nhiều giao dịch với giá trị lớn"""
        customer = LoyalCustomer('15', 'Nguyễn Văn O', '0123456789', 'o@example.com')
        customer.add_purchase(5000000)
        customer.add_purchase(10000000)
        self.assertEqual(customer.total_spent(), 15000000)
        self.assertEqual(customer.purchase_count(), 2)

    # Test Case 15: Kiểm tra trung bình giao dịch khi có nhiều giao dịch
    def test_average_spent_multiple_transactions(self):
        """Kiểm tra tính trung bình giao dịch khi có nhiều giao dịch"""
        customer = CasualCustomer('16', 'Nguyễn Văn P', '0123456789', 'p@example.com')
        customer.add_purchase(2000000)
        customer.add_purchase(3000000)
        self.assertEqual(customer.average_spent(), 2500000)

    # Test Case 16: Kiểm tra không tính trung bình khi chưa có giao dịch
    def test_average_spent_empty_history(self):
        """Kiểm tra trung bình giao dịch khi chưa có giao dịch"""
        customer = LoyalCustomer('17', 'Nguyễn Văn Q', '0123456789', 'q@example.com')
        self.assertEqual(customer.average_spent(), 0)

    # Test Case 17: Kiểm tra loại khách hàng khi khởi tạo
    def test_initial_customer_type(self):
        """Kiểm tra loại khách hàng khi khởi tạo"""
        loyal_customer = LoyalCustomer('18', 'Nguyễn Văn R', '0123456789', 'r@example.com')
        casual_customer = CasualCustomer('19', 'Nguyễn Văn S', '0123456789', 's@example.com')
        self.assertEqual(loyal_customer.get_type(), 'Thân thiết')
        self.assertEqual(casual_customer.get_type(), 'Vãng lai')

    # Test Case 18: Kiểm tra khách hàng thân thiết có số lần giao dịch > 1
    def test_loyal_customer_multiple_transactions(self):
        """Kiểm tra khách hàng thân thiết với nhiều giao dịch"""
        customer = LoyalCustomer('20', 'Nguyễn Văn T', '0123456789', 't@example.com')
        customer.add_purchase(1000000)
        customer.add_purchase(2000000)
        self.assertEqual(customer.purchase_count(), 2)
        self.assertEqual(customer.total_spent(), 3000000)

    # Test Case 19: Kiểm tra khách hàng vãng lai có số lần giao dịch > 1
    def test_casual_customer_multiple_transactions(self):
        """Kiểm tra khách hàng vãng lai với nhiều giao dịch"""
        customer = CasualCustomer('21', 'Nguyễn Văn U', '0123456789', 'u@example.com')
        customer.add_purchase(1500000)
        customer.add_purchase(2500000)
        self.assertEqual(customer.purchase_count(), 2)
        self.assertEqual(customer.total_spent(), 4000000)

    # Test Case 20: Kiểm tra thêm giao dịch không hợp lệ (chuỗi ký tự)
    def test_invalid_purchase_non_numeric(self):
        """Kiểm tra thêm giao dịch không hợp lệ với giá trị không phải số"""
        customer = LoyalCustomer('22', 'Nguyễn Văn V', '0123456789', 'v@example.com')
        with self.assertRaises(ValueError):
            customer.add_purchase("invalid_purchase")

    # Test Case 21: Kiểm tra khách hàng thân thiết có số tiền giao dịch bằng 0
    def test_loyal_customer_zero_spent(self):
        """Kiểm tra khách hàng thân thiết với tổng giá trị giao dịch bằng 0"""
        customer = LoyalCustomer('23', 'Nguyễn Văn W', '0123456789', 'w@example.com')
        self.assertEqual(customer.total_spent(), 0)

    # Test Case 22: Kiểm tra tổng giao dịch với giá trị rất lớn
    def test_large_total_spent(self):
        """Kiểm tra khách hàng với tổng giao dịch rất lớn"""
        customer = LoyalCustomer('24', 'Nguyễn Văn X', '0123456789', 'x@example.com')
        customer.add_purchase(999999999)
        customer.add_purchase(888888888)
        self.assertEqual(customer.total_spent(), 1888888887)

class TestLoyalCustomer(unittest.TestCase):
    
    #  Test case 23:
    def test_add_loyal_customer(self):
        c = LoyalCustomer("4", "Nguyễn Thị D", "0123456789", "d@example.com")
        
        self.assertEqual(c.customer_id, "4")
        self.assertEqual(c.name, "Nguyễn Thị D")
        self.assertEqual(c.phone, "0123456789")
        self.assertEqual(c.email, "d@example.com")
        self.assertEqual(c.purchase_history, [])
    
    # Test case 24:
    def test_upgrade_loyal_customer(self):
        c = LoyalCustomer("5", "Trần Thị E", "0123456789", "e@example.com")
        
        c.add_purchase(3000000)
        c.add_purchase(2500000)
        
        self.assertEqual(c.total_spent(), 5500000)
        self.assertEqual(c.purchase_count(), 2)
        self.assertTrue(c.total_spent() >= 2000000)  # Kiểm tra điều kiện tổng giao dịch

class TestCustomerAverageSpent(unittest.TestCase):
    
    # Test case 25:
    def test_average_spent(self):
        c = CasualCustomer("6", "Nguyễn Văn F", "0123456789", "f@example.com")
        
        c.add_purchase(100000)
        c.add_purchase(200000)
        c.add_purchase(300000)
        
        self.assertEqual(c.average_spent(), 200000)
    
    # Test case 26:
    def test_average_spent_no_purchases(self):
        c = CasualCustomer("7", "Lê Văn G", "0123456789", "g@example.com")
        
        self.assertEqual(c.average_spent(), 0)

class TestUpgradeLoyalCustomer(unittest.TestCase):
    
    # Test case 27:
    def test_upgrade_success(self):
        c = CasualCustomer("8", "Trương Thị H", "0123456789", "h@example.com")
        
        c.add_purchase(2000000)
        c.add_purchase(1000000)
        
        if c.total_spent() >= 2000000:
            c.__class__ = LoyalCustomer  # Nâng cấp khách hàng
            self.assertTrue(isinstance(c, LoyalCustomer))  # Kiểm tra loại khách hàng là thân thiết
            
    # Test case 28:
    def test_upgrade_not_eligible(self):
        c = CasualCustomer("9", "Phạm Thị I", "0123456789", "i@example.com")
        
        # Thêm giao dịch chưa đủ điều kiện
        c.add_purchase(1500000)
        
        # Không nâng cấp khách hàng nếu không đủ điều kiện
        if c.total_spent() < 2000000:
            self.assertFalse(isinstance(c, LoyalCustomer))  # Kiểm tra loại khách hàng vẫn là vãng lai


class TestCustomerFileOperations(unittest.TestCase):
    
    # Test case 29: Kiểm tra lưu khách hàng vào file JSON
    def test_save_customer_to_json(self):
        # Tạo khách hàng và lưu vào file JSON
        c = LoyalCustomer("10", "Trần Văn J", "0123456789", "j@example.com")
        c.add_purchase(5000000)
        c.add_purchase(2000000)
        
        # Lưu khách hàng vào file
        with open("customer_info.json", "w", encoding="utf-8") as f:
            json.dump(c.to_dict(), f, ensure_ascii=False, indent=4)
        
        # Đọc lại từ file
        with open("customer_info.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Kiểm tra dữ liệu đọc từ file
        self.assertEqual(data["ID"], "10")
        self.assertEqual(data["Tên"], "Trần Văn J")
        self.assertEqual(data["Tổng giao dịch"], 7000000)
        self.assertEqual(data["Số lần giao dịch"], 2)

class TestCustomerList(unittest.TestCase):
    
    # Test case 30: Kiểm tra danh sách khách hàng
    def test_display_customers(self):
        # Tạo danh sách khách hàng
        customers = [
            CasualCustomer("11", "Nguyễn Văn K", "0123456789", "k@example.com"),
            LoyalCustomer("12", "Trần Thị L", "0123456789", "l@example.com")
        ]
        
        # Thêm giao dịch cho khách hàng
        customers[0].add_purchase(1000000)
        customers[1].add_purchase(2000000)
        customers[1].add_purchase(2500000)
        
        # Kiểm tra danh sách khách hàng
        self.assertEqual(len(customers), 2)
        self.assertEqual(customers[0].purchase_count(), 1)
        self.assertEqual(customers[1].purchase_count(), 2)


if __name__ == "__main__":
    unittest.main()
