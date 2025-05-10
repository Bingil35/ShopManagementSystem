import pandas as pd

def display_customers(customers):
    if not customers:
        print("Danh sách khách hàng trống!")
        return

    df = pd.DataFrame([c.to_dict() for c in customers])
    
    df["Tổng giao dịch"] = df["Tổng giao dịch"].astype(int)
    print("\n=============== DANH SÁCH KHÁCH HÀNG ===============\n")
    print(df.to_string(index=False))
