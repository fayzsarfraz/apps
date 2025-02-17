import streamlit as st
import pandas as pd

# Function to calculate compounded savings
def calculate_compounded_savings(monthly_saving, annual_profit_percentage, years):
    total_savings = 0
    monthly_profit_rate = (annual_profit_percentage / 100) / 12
    savings_data = []
    
    for year in range(1, years + 1):
        yearly_savings = 0
        yearly_profit = 0
        
        for month in range(1, 13):
            total_savings += monthly_saving
            profit_this_month = total_savings * monthly_profit_rate
            total_savings += profit_this_month
            yearly_savings += monthly_saving
            yearly_profit += profit_this_month
        
        savings_data.append((year, yearly_savings, yearly_profit, total_savings))
    
    return savings_data, total_savings

# Function to convert number to words
def number_to_words(number):
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f} million"
    elif number >= 1_000:
        return f"{number / 1_000:.1f} thousand"
    else:
        return f"{number:.2f}"

# Streamlit App
st.sidebar.title("Navigation")
app_choice = st.sidebar.radio("Choose an app:", ["Compounded Savings Calculator"])

if app_choice == "Compounded Savings Calculator":
    st.title("Compounded Savings Calculator")
    
    monthly_saving = st.number_input("Enter monthly saving amount:", min_value=0.0, value=10000.0)
    annual_profit_percentage = st.number_input("Enter annual profit percentage:", min_value=0.0, value=15.0)
    years = st.number_input("Enter number of years:", min_value=1, value=20)
    
    if st.button("Calculate Savings"):
        savings_data, total_savings = calculate_compounded_savings(monthly_saving, annual_profit_percentage, years)
        total_savings_words = number_to_words(total_savings)
        
        st.write(f"### Total savings after {years} years: **{total_savings:,.2f}** ({total_savings_words})")
        
        # Convert data to DataFrame and display as a table
        df = pd.DataFrame(savings_data, columns=["Year", "Amount Saved", "Profit", "Total Amount"])
        df["Amount Saved"] = df["Amount Saved"].apply(lambda x: f"{x:,.2f}")
        df["Profit"] = df["Profit"].apply(lambda x: f"{x:,.2f}")
        df["Total Amount"] = df["Total Amount"].apply(lambda x: f"{x:,.2f}")
        
        st.write("### Savings Table")
        st.dataframe(df)

