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
    savings_data (list): A list of tuples containing (year, month, total_savings, profit_this_month).
    total_savings (float): The final savings amount after all years.
    """
    total_savings = 0
    monthly_profit_rate = (annual_profit_percentage / 100) / 12  # Convert annual rate to monthly

    savings_data = []  # To store savings details for each month
    
    for year in range(1, years + 1):
        yearly_profit = 0  # Track profit for the current year
        for month in range(1, 13):
            total_savings += monthly_saving  # Add monthly saving
            profit_this_month = total_savings * monthly_profit_rate  # Calculate profit for this month
            total_savings += profit_this_month  # Add profit to total savings
            yearly_profit += profit_this_month  # Add to yearly profit
            savings_data.append((year, month, total_savings, profit_this_month))  # Store data for reference
        savings_data.append((year, "Yearly Total", total_savings, yearly_profit))  # Add yearly summary
    
    return savings_data, total_savings

# Function to calculate loan installments
def calculate_loan_installments(total_amount, down_payment, annual_interest_rate, years):
    """
    This function calculates the monthly and yearly loan installments based on:
    - Total loan amount.
    - Down payment.
    - Annual interest rate.
    - Number of years.

    Parameters:
    total_amount (float): Total loan amount.
    down_payment (float): Down payment made upfront.
    annual_interest_rate (float): Annual interest rate.
    years (int): Loan tenure in years.

    Returns:
    monthly_installment (float): Monthly installment amount.
    yearly_installment (float): Yearly installment amount.
    """
    loan_amount = total_amount - down_payment  # Calculate the principal amount
    monthly_interest_rate = (annual_interest_rate / 100) / 12  # Convert annual rate to monthly
    num_payments = years * 12  # Total number of monthly payments

    # Calculate monthly installment using the loan formula
    if monthly_interest_rate == 0:  # Handle zero interest case
        monthly_installment = loan_amount / num_payments
    else:
        monthly_installment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** (-num_payments))
    
    yearly_installment = monthly_installment * 12  # Calculate yearly installment
    return monthly_installment, yearly_installment

# Function to convert number to words (e.g., 1,500,000 -> "1.5 million")
def number_to_words(number):
    """
    Converts a number into words representation (e.g., 1,500,000 -> "1.5 million").
    
    Parameters:
    number (float): The number to convert.

    Returns:
    str: The number in words.
    """
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f} million"
    elif number >= 1_000:
        return f"{number / 1_000:.1f} thousand"
    else:
        return f"{number:.2f}"

# Streamlit App
st.sidebar.title("Navigation")
app_choice = st.sidebar.radio("Choose an app:", ["Compounded Savings Calculator", "Loan Calculator"])

if app_choice == "Compounded Savings Calculator":
    # Compounded Savings Calculator UI
    st.title("Compounded Savings Calculator")  # App title

    # User input fields in Streamlit UI
    monthly_saving = st.number_input("Enter monthly saving amount:", min_value=0.0, value=10000.0)
    annual_profit_percentage = st.number_input("Enter annual profit percentage:", min_value=0.0, value=15.0)
    years = st.number_input("Enter number of years:", min_value=1, value=20)  # Default to 20 years for better demonstration

    # Button to trigger savings calculation
    if st.button("Calculate Savings"):
        savings_data, total_savings = calculate_compounded_savings(monthly_saving, annual_profit_percentage, years)

        # Convert total savings to words
        total_savings_words = number_to_words(total_savings)

        # Display final total savings
        st.write(f"### Total savings after {years} years: **{total_savings:,.2f}** ({total_savings_words})")

        # Display year-wise breakdown of savings in dropdowns for every 5 years
        for start_year in range(1, years + 1, 5):
            end_year = min(start_year + 4, years)  # Ensure we don't exceed the total years
            with st.expander(f"Years {start_year} to {end_year}"):
                for year in range(start_year, end_year + 1):
                    # Filter data for the current year
                    year_data = [s for s in savings_data if s[0] == year]
                    yearly_total = year_data[-1]  # Get the yearly summary (last entry for the year)
                    total_savings_year = yearly_total[2]  # Total savings at the end of the year
                    total_profit_year = yearly_total[3]  # Total profit for the year

                    # Convert to words
                    total_savings_year_words = number_to_words(total_savings_year)
                    total_profit_year_words = number_to_words(total_profit_year)

                    # Display year-wise results
                    st.write(f"#### Year {year}")
                    st.write(f"- **Total Savings:** {total_savings_year:,.2f} ({total_savings_year_words})")
                    st.write(f"- **Total Profit:** {total_profit_year:,.2f} ({total_profit_year_words})")
                    st.write("---")

elif app_choice == "Loan Calculator":
    # Loan Calculator UI
    st.title("Loan Calculator")  # App title

    # User input fields in Streamlit UI
    total_amount = st.number_input("Enter total loan amount:", min_value=0.0, value=1000000.0)
    down_payment = st.number_input("Enter down payment:", min_value=0.0, value=200000.0)
    annual_interest_rate = st.number_input("Enter annual interest rate (%):", min_value=0.0, value=8.0)
    years = st.number_input("Enter loan tenure (years):", min_value=1, value=20)

    # Button to trigger loan calculation
    if st.button("Calculate Loan"):
        monthly_installment, yearly_installment = calculate_loan_installments(total_amount, down_payment, annual_interest_rate, years)

        # Display results
        st.write(f"### Loan Details:")
        st.write(f"- **Loan Amount:** {total_amount - down_payment:,.2f}")
        st.write(f"- **Monthly Installment:** {monthly_installment:,.2f}")
        st.write(f"- **Yearly Installment:** {yearly_installment:,.2f}")