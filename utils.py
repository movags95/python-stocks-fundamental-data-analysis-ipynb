import os
import pandas as pd
import yfinance as yf

yearly_dir = 'data/yearly'

quarterly_dir = 'data/quarterly'

# Function to fetch S&P 500 tickers
def get_sp500_tickers():
    table = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    return table[0]['Symbol'].tolist()

# Function to fetch quarterly financials data
def fetch_qtrly_financials_data(ticker: yf.Ticker):
    financials = ticker.quarterly_financials.T
    financials.sort_index(ascending=False, inplace=True)
    return financials

# Function to fetch quarterly cash flow data
def fetch_qtrly_cashflow_data(ticker: yf.Ticker):
    cashflow = ticker.quarterly_cashflow.T
    cashflow.sort_index(ascending=False, inplace=True)
    return cashflow

# Function to fetch quarterly income data
def fetch_qtrly_income_data(ticker: yf.Ticker):
    income = ticker.quarterly_income_stmt.T
    income.sort_index(ascending=False, inplace=True)
    return income

# Function to fetch quarterly balance sheet data
def fetch_qtrly_balance_data(ticker: yf.Ticker):
    balance = ticker.quarterly_balancesheet.T
    balance.sort_index(ascending=False, inplace=True)
    return balance

# Function to fetch yearly financials data
def fetch_financials_data(ticker: yf.Ticker):
    financials = ticker.financials.T
    financials.sort_index(ascending=False, inplace=True)
    return financials

# Function to fetch yearly cash flow data
def fetch_cashflow_data(ticker: yf.Ticker):
    cashflow = ticker.cashflow.T
    cashflow.sort_index(ascending=False, inplace=True)
    return cashflow

# Function to fetch yearly income data
def fetch_income_data(ticker: yf.Ticker):
    income = ticker.income_stmt.T
    income.sort_index(ascending=False, inplace=True)
    return income

# Function to fetch yearly balance sheet data
def fetch_balance_data(ticker: yf.Ticker):
    balance = ticker.balance_sheet.T
    balance.sort_index(ascending=False, inplace=True)
    return balance

# Main function to fetch and save data
def fetch_qtrly_data(tickers):
    base_dir = quarterly_dir

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for ticker_symbol in tickers:
        ticker = yf.Ticker(ticker_symbol)
        print(
            f'Fetching quarterly data for {ticker_symbol}: {ticker.info["shortName"]}')

        ticker_dir = os.path.join(base_dir, ticker_symbol)
        if not os.path.exists(ticker_dir):
            os.makedirs(ticker_dir)

        try:
            financials = fetch_qtrly_financials_data(ticker)
            financials.to_csv(os.path.join(
                base_dir, ticker_symbol, 'financials.csv'))

            cashflow = fetch_qtrly_cashflow_data(ticker)
            cashflow.to_csv(os.path.join(
                base_dir, ticker_symbol, 'cashflow.csv'))

            income = fetch_qtrly_income_data(ticker)
            income.to_csv(os.path.join(base_dir, ticker_symbol, 'income.csv'))

            balance = fetch_qtrly_balance_data(ticker)
            balance.to_csv(os.path.join(
                base_dir, ticker_symbol, 'balance.csv'))

        except Exception as e:
            print(f'Could not fetch data for {ticker_symbol}: {e}')


def fetch_yearly_data(tickers):
    base_dir = yearly_dir

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for ticker_symbol in tickers:
        ticker = yf.Ticker(ticker_symbol)
        print(
            f'Fetching yearly data for {ticker_symbol}: {ticker.info["shortName"]}')

        ticker_dir = os.path.join(base_dir, ticker_symbol)
        if not os.path.exists(ticker_dir):
            os.makedirs(ticker_dir)

        try:
            financials = fetch_financials_data(ticker)
            financials.to_csv(os.path.join(
                base_dir, ticker_symbol, 'financials.csv'))

            cashflow = fetch_cashflow_data(ticker)
            cashflow.to_csv(os.path.join(
                base_dir, ticker_symbol, 'cashflow.csv'))

            income = fetch_income_data(ticker)
            income.to_csv(os.path.join(base_dir, ticker_symbol, 'income.csv'))

            balance = fetch_balance_data(ticker)
            balance.to_csv(os.path.join(
                base_dir, ticker_symbol, 'balance.csv'))

        except Exception as e:
            print(f'Could not fetch data for {ticker_symbol}: {e}')


def load_data(ticker, quarterly=False):
    if quarterly:
        basedir = quarterly_dir
    else:
        basedir = yearly_dir

    finance_path = os.path.join(basedir, ticker, 'financials.csv')
    cashflow_path = os.path.join(basedir, ticker, 'cashflow.csv')
    income_path = os.path.join(basedir, ticker, 'income.csv')
    balance_path = os.path.join(basedir, ticker, 'balance.csv')
    splt = '_'

    try:
        finance_data = pd.read_csv(finance_path)
        finance_data.set_index(finance_data.columns[0], inplace=True)
        print(f'Financials loaded for {ticker}')
    except Exception as e:
        print(
            f"Could not fetch {basedir.split(splt)[0]} financials for {ticker}: ", e)
        finance_data = None

    try:
        cashflow_data = pd.read_csv(cashflow_path)
        cashflow_data.set_index(cashflow_data.columns[0], inplace=True)
        print(f'Cashflows loaded for {ticker}')
    except Exception as e:
        print(
            f'Could not fetch {basedir.split(splt)[0]} cashflow for {ticker}: ', e)
        cashflow_data = None

    try:
        income_data = pd.read_csv(income_path)
        income_data.set_index(income_data.columns[0], inplace=True)
        print(f'Income stmt loaded for {ticker}')
    except Exception as e:
        print(
            f'Could not fetch {basedir.split(splt)[0]} income for {ticker}: ', e)
        income_data = None

    try:
        balance_data = pd.read_csv(balance_path)
        balance_data.set_index(balance_data.columns[0], inplace=True)
        print(f'Balance sheet loaded for {ticker}')
    except Exception as e:
        print(
            f"Could not fetch {basedir.split(splt)[0]} balancesheet for {ticker}: ", e)
        balance_data = None

    return finance_data, cashflow_data, income_data, balance_data
