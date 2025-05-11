import yfinance as yf
import pandas as pd

Tickers = ['SIRI', 'GOOG']

all_tickers_data = [] # This list will hold dictionaries, one for each ticker
for ticker in Tickers:
    stock_ticker = yf.Ticker(ticker)

    income_statement = stock_ticker.income_stmt
    
    revenue_data = None # Initialize to None
    try:
        # Attempt to get 'Total Revenue' first using .loc[]
        revenue_data = income_statement.loc['Total Revenue']
    except KeyError:
        try:
            # If 'Total Revenue' is not found, try 'Revenues' using .loc[]
            revenue_data = income_statement.loc['Revenues']
        except KeyError:
            # If neither is found, print an error but allow script to continue
            print("Could not find 'Total Revenue' or 'Revenues' in the income statement.")
            print("Please check the available items using income_statement.index.tolist()")
    
    # Select the last 3 years of Revenue (first 3 columns) if data was found
    last_3_years_revenue = None
    if revenue_data is not None:
        last_3_years_revenue = revenue_data.iloc[:3]

    print(last_3_years_revenue)

    #create a dictionary to hold the data for the current ticker being looped
    current_ticker_data = {}

    #Add the ticker symbol to the dictinary 
    current_ticker_data['Ticker'] = ticker 

    #Check if we successfullly got revenue data before processing it
    if last_3_years_revenue is not None:
        for date, revenue in last_3_years_revenue.items():
            # The .items() method gives you the index (date) and value (revenue) for each item
            #Extract the year from the date
            year = pd.to_datetime(date).year 
            current_ticker_data[f'Revenue {year}'] = revenue

    
    # --- Get Free Cash Flow ---
    # Get the annual cash flow statement
    # Similar to income_statement, this returns a DataFrame with cash flow items as rows
    # and fiscal period end dates as columns.
    cashflow = stock_ticker.cashflow
    
    # Access the 'Free Cash Flow' row using .loc[] with error handling
    free_cashflow = None # Initialize to None
    try:
        free_cashflow = cashflow.loc['Free Cash Flow']
    
        # Select the last 3 years of Free Cash Flow (first 3 columns)
        last_3_free_cashflow = free_cashflow.iloc[:3]
    
        # Removed print statements as requested for combined export
    
    
    except KeyError:
        print("Could not find 'Free Cash Flow' in the cash flow statement.")
        print("Please check the available items using cashflow.index.tolist()")
    
    #Check if we successfullly got cashflow data before processing it
    if last_3_free_cashflow is not None:
        for date, cashflow in last_3_free_cashflow.items():
            # The .items() method gives you the index (date) and value (cashflow) for each item
            #Extract the year from the date
            year = pd.to_datetime(date).year 
            current_ticker_data[f'Free Cash Flow {year}'] = cashflow

    
    # --- Get Cash ---
    # Get the annual balance sheet
    # This returns a DataFrame with balance sheet items as rows
    # and fiscal period end dates as columns.
    balance_sheet = stock_ticker.balance_sheet
  
    # Access the 'Cash' row using .loc[] with error handling
    cash = None # Initialize to None
    try:
        cash = balance_sheet.loc['Cash And Cash Equivalents']
    
        # Select the last 3 years of cash (first 3 columns)
        last_3_cash = cash.iloc[:3]
    
        # Optional: Print Net Debt (removed for combined export, but can uncomment for debugging)
        # print(f"--- Net Debt for {SIRI.info.get('symbol', 'the ticker')} (last 3 years) ---")
        # for date, debt in last_3_net_debt.items():
        #     year = pd.to_datetime(date).year
        #     print(f"  {year}: ${debt:,.0f}")
        # print("-" * 40) # Separator
    
    except KeyError:
        print("Could not find 'Cash and Cash Equivalents' in the balance sheet.")
        print("Please check the available items using balance_sheet.index.tolist()")

    #Check if we successfullly got netdebt data before processing it
    if last_3_cash is not None:
        for date, cash in last_3_cash.items():
            # The .items() method gives you the index (date) and value (cashflow) for each item
            #Extract the year from the date
            year = pd.to_datetime(date).year 
            current_ticker_data[f'Cash {year}'] = cash
    
    #Pull Marketcap and Enterprise value for each ticker.
    info = stock_ticker.info
    
    # Safely get enterpriseValue and marketCap, as they might not always be present or might be None
    enterprise_value = info.get('enterpriseValue')
    market_cap = info.get('marketCap')
    total_debt = info.get('totalDebt')

    # Add Market Cap, Total Debt, Cash, Enterprise Value to the dictionary
    current_ticker_data['Market Cap'] = market_cap
    current_ticker_data['Enterprise Value'] = enterprise_value
    current_ticker_data['Total Debt'] = total_debt
    
    #print(current_ticker_data)
    all_tickers_data.append(current_ticker_data)

print(all_tickers_data)

# --- After the loop ---
# --- Step 4: Consolidate into a DataFrame ---
# Create a pandas DataFrame from the list of dictionaries
combined_data_df = pd.DataFrame(all_tickers_data)

# --- Step 5: Transpose (Optional, based on your preference) ---
# If you want financial metrics as index and years as columns
#combined_data_transposed = combined_data_df.set_index('Ticker').T

# For a screener, keeping tickers as rows and metrics/years as columns is often more useful.
# Let's keep the DataFrame with Ticker as a column for now.

# Optional: Print the combined data DataFrame
print("\n--- Combined Financial Data for All Tickers ---")
print(combined_data_df)
print("-" * 40)

# --- Step 6: Export to CSV ---
combined_data_df.to_csv('all_tickers_financial_data.csv', index=False)
# print("\nData exported to all_tickers_financial_data.csv")
