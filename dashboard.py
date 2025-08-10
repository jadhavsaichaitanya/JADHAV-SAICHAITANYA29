import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize session state for transactions
if 'transactions' not in st.session_state:
    st.session_state['transactions'] = []

def add_transaction(date, amount, t_type, category, description):
    st.session_state['transactions'].append({
        'date': date,
        'amount': amount,
        'type': t_type,
        'category': category,
        'description': description
    })

def load_data():
    if st.session_state['transactions']:
        return pd.DataFrame(st.session_state['transactions'])
    else:
        return pd.DataFrame(columns=['date', 'amount', 'type', 'category', 'description'])

def show_summary(df):
    total_income = df[df['type'] == 'Income']['amount'].sum()
    total_expense = df[df['type'] == 'Expense']['amount'].sum()
    balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{total_income:.2f}")
    col2.metric("Total Expense", f"₹{total_expense:.2f}")
    col3.metric("Balance", f"₹{balance:.2f}")

def plot_monthly_summary(df):
    if df.empty:
        st.write("No data to plot.")
        return

    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)

    monthly['Savings'] = monthly.get('Income', 0) - monthly.get('Expense', 0)
    monthly.index = monthly.index.astype(str)

    st.line_chart(monthly)

def main():
    st.title("Real-Time Personal Finance Dashboard")

    with st.form("add_transaction_form"):
        st.subheader("Add a Transaction")
        date = st.date_input("Date", datetime.today())
        t_type = st.selectbox("Type", ['Income', 'Expense'])
        amount = st.number_input("Amount (₹)", min_value=0.01, step=0.01)
        category = st.text_input("Category (e.g., Salary, Food, Rent)")
        description = st.text_input("Description (optional)")
        submitted = st.form_submit_button("Add Transaction")
        if submitted:
            if not category:
                st.error("Category is required.")
            else:
                add_transaction(date.strftime('%Y-%m-%d'), amount, t_type, category, description)
                st.success("Transaction added!")

    df = load_data()
    show_summary(df)
    st.subheader("Monthly Income, Expense, and Savings")
    plot_monthly_summary(df)

    st.subheader("All Transactions")
    st.dataframe(df)

if __name__ == "__main__":
    main()
