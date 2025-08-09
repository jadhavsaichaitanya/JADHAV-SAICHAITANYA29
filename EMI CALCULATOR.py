import math
import pandas as pd

def calculate_emi(principal, annual_rate, tenure_months):
    monthly_rate = annual_rate / (12 * 100)
    emi = principal * monthly_rate * (math.pow(1 + monthly_rate, tenure_months)) / (math.pow(1 + monthly_rate, tenure_months) - 1)
    return emi

def generate_schedule(principal, annual_rate, tenure_months):
    emi = calculate_emi(principal, annual_rate, tenure_months)
    balance = principal
    schedule = []

    for month in range(1, tenure_months + 1):
        interest = balance * (annual_rate / (12 * 100))
        principal_component = emi - interest
        balance -= principal_component
        schedule.append({
            "Month": month,
            "EMI": round(emi, 2),
            "Interest Paid": round(interest, 2),
            "Principal Paid": round(principal_component, 2),
            "Remaining Balance": round(balance if balance > 0 else 0, 2)
        })
    
    return pd.DataFrame(schedule)

if __name__ == "__main__":
    print("📊 Loan EMI & Interest Calculator")
    principal = float(input("Enter loan amount: "))
    annual_rate = float(input("Enter annual interest rate (%): "))
    tenure_months = int(input("Enter loan tenure (months): "))

    emi = calculate_emi(principal, annual_rate, tenure_months)
    print(f"\nYour monthly EMI is: ₹{emi:.2f}\n")

    df = generate_schedule(principal, annual_rate, tenure_months)
    print(df.to_string(index=False))

    # Optional: Save to Excel
    save = input("\nDo you want to save the schedule to 'emi_schedule.xlsx'? (y/n): ")
    if save.lower() == 'y':
        df.to_excel("emi_schedule.xlsx", index=False)
        print("✅ EMI schedule saved to 'emi_schedule.xlsx'")