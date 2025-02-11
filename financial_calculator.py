import streamlit as st

# Function to calculate compounded savings
def calculate_compounded_savings(monthly_saving, annual_profit_percentage, years):
    """
    This function calculates the compounded savings based on:
    - A fixed monthly saving amount.
    - A yearly interest/profit percentage applied monthly.
    
    Parameters:
    monthly_saving (float): The amount saved each month.
    annual_profit_percentage (float): The annual profit percentage applied.
    years (int): The total number of years to calculate.

    Returns:
    savings_data (list): A list of tuples containing (year, month, total_savings).
    total_savings (float): The final savings amount after all years.
    """
    total_savings = 0
    monthly_profit_rate = (annual_profit_percentage / 100) / 12  # Convert annual rate to monthly

    savings_data = []  # To store savings details for each month
    
    for year in range(1, years + 1):
        for month in range(1, 13):
            total_savings += monthly_saving  # Add monthly saving
            total_savings += total_savings * monthly_profit_rate  # Apply monthly profit percentage
            savings_data.append((year, month, total_savings))  # Store data for reference
    
    return savings_data, total_savings

# Streamlit UI for the savings calculator
st.title("Compounded Savings Calculator")  # App title

# User input fields in Streamlit UI
monthly_saving = st.number_input("Enter monthly saving amount:", min_value=0.0, value=10000.0)
annual_profit_percentage = st.number_input("Enter annual profit percentage:", min_value=0.0, value=15.0)
years = st.number_input("Enter number of years:", min_value=1, value=5)

# Button to trigger savings calculation
if st.button("Calculate Savings"):
    savings_data, total_savings = calculate_compounded_savings(monthly_saving, annual_profit_percentage, years)

    # Display final total savings
    st.write(f"### Total savings after {years} years: **{total_savings:,.2f}**")
    
    # Display year-wise breakdown of savings
    for year in range(1, years + 1):
        year_savings = [s for y, m, s in savings_data if y == year]
        st.write(f"Year {year}: **{year_savings[-1]:,.2f}**")
