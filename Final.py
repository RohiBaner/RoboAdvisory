# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 22:07:08 2019

@author: Rohini (MSBD6000E: Introduction to Financial Technology)
"""
from pathlib import Path
env_path = Path('.') / '.env'
import json
import os
import requests
import pandas as pd
import pickle

api_key = os.environ.get("KZSCEANOC0AZFNX5")


def SaveDictionary(dictionary,File):
    with open(File, "wb") as myFile:
        pickle.dump(dictionary, myFile)
        myFile.close()

def LoadDictionary(File):
    with open(File, "rb") as myFile:
        dict = pickle.load(myFile)
        myFile.close()
        return dict

def stock_info(ticker, tol):
    print("\nLet's see...")
    print("Printing out some data for you:")
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    tol1 = float((100+tol)/100) # Format the tolerance value to float
    tol = str(tol)
    # obtain the data from ALPHAVANTAGE for that ticker
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys())
    latest_day = dates[0]
    latest_close = tsd[latest_day]["4. close"]
    latest_close1 = "INR {0:,.2f}".format(float(latest_close)*60.0)
    high_prices = []
    low_prices = []
    for date in dates:
        high_price = tsd[date]["2. high"]
        low_price = tsd[date]["3. low"]
        high_prices.append(float(high_price))
        low_prices.append(float(low_price))
    recent_high = max(high_prices)
    recent_high1 = "INR {0:,.2f}".format(float(recent_high)*60.0)
    recent_low = min(low_prices)
    recent_low1 = "INR {0:,.2f}".format(float(recent_low)*60.0)
    print(f"Latest available data: {last_refreshed}")
    print(f"Latest closing price: {latest_close1} ")
    print(f"Recent avergae closing high price: {recent_high1}")
    print(f"Recent average closing low price: {recent_low1}")
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    threshold = tol1*(float(recent_low)*60.0)
    if (float(latest_close)*60.0) < threshold:
        print("Recommendation: BUY!")
        print("Reason: The latest closing price is not greater than",tol,"% of ")
        print("the recent low, indicating potential growth. Go for it!")
    else:
        print("Recommendation: DON'T BUY!")
        print("Reason: The latest closing price is greater than",tol,"% of the ")
        print("recent low, indicating potential decline. Umm, maybe next time?")
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")


def digi_crypto_info(frm, to):
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
    # obtain the data from ALPHAVANTAGE
    request_url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={frm}&to_currency={to}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    #Extract all necessary columns
    parsed_response = parsed_response["Realtime Currency Exchange Rate"]
    last_refreshed = parsed_response["6. Last Refreshed"]
    frm_code = parsed_response["1. From_Currency Code"]
    to_code = parsed_response["3. To_Currency Code"]
    frm_curr = parsed_response["2. From_Currency Name"]
    to_curr = parsed_response["4. To_Currency Name"]
    time_zone = parsed_response["7. Time Zone"]
    rate = parsed_response["5. Exchange Rate"]
    #Print out results
    print(f"Latest available data: {last_refreshed}({time_zone})")
    print(f"{frm_curr}({frm_code}) ---> {to_curr}({to_code}): {rate}")
    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")


def get_price_old(key):
    # obtain the data from ALPHAVANTAGE for that ticker
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={key}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys())
    latest_day = dates[1]
    return (float(tsd[latest_day]["2. high"])*60.0)


def get_price_new(key):
    # obtain the data from ALPHAVANTAGE for that ticker
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={key}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys())
    latest_day = dates[0] #latest price
    return (float(tsd[latest_day]["2. high"])*60.0)


def order_shares(item,prices,quant,portfolio ):
    """Change the quantity of owned stock if there is enough cash"""
    if item == 'CASH':
        return False
    if item not in prices:
        # Find new price
        get_price_new(item)
    if quant > 0:
        # Buy
        if portfolio['CASH'] < (prices[item] * quant):
            print("Not enough cash available to buy %s shares of %s!" % (quant, item))
            return False
    else:
        # Sell
        if portfolio[item] < (-1 * quant):
            print("You cannot sell more %s than you own!" % item)
            return False
    portfolio[item] += quant
    portfolio['CASH'] -= (prices[item] * quant)
    return True

def maintain_portfolio(req_portfolio, init_cash,tol):
#    trading_api = Trading(init_cash)
    portfolio = {'CASH': init_cash}
    counter = 1
#    keep_trading = True
    while counter == 1:
        print("\n-----------------------------------------------------------------")
        prices = dict()
        # Iterate over all stocks in our current portfolio
        total_value = 0
        for i in portfolio:
            # Calculate the total value of our portfolio (including cash)
            if i == 'CASH':
                total_value += portfolio[i]
                continue
            price = get_price_old(i)
            total_value += (price*portfolio[i])
            print("%s costs INR %s per share today" % (i, price))
            prices[i] = price
        # Record which stocks we need to rebalance
        to_rebalance = dict()
        for i in req_portfolio:
            # We don't need to rebalance cash
            if i == 'CASH':
                continue
            # If we don't already own this stock, we need to get it's price to use later
            if i not in prices:
                if i == "CASH":
                    return False
                if i not in portfolio:
                    portfolio[i] = 0
                prices[i] = get_price_old(i)
            # If the difference between what we own and what we want to own is greater than tolerance, we need to rebalance
            difference = ((prices[i] * portfolio[i]) / total_value) - req_portfolio[i]
            if abs(difference) > tol:
                print("%s needs rebalancing, it is %s percent off from our target percentage" % (i, round(difference * 100, 2)))
                to_rebalance[i] = difference
        # Rebalance the portfolio
        while to_rebalance:
            # Start with the stock that we need to sell the most of, so we don't run out of cash.
            ticker = max(to_rebalance, key=to_rebalance.get)
            # Calculate how many shares we need to purchase or sell - negative quantity indicates a sell order
            quantity = int((req_portfolio[ticker] * (total_value / prices[ticker])) - portfolio[ticker])
            print("Placing order for %s shares of %s" % (quantity, ticker))
            order_shares(ticker,prices,quantity,portfolio)
            del to_rebalance[ticker]
        # Print a summary of our portfolio
        print("\n----------------------------- RESULTS ---------------------------")
        print("Portfolio Starting Value: INR %s" % init_cash)
        print("Portfolio Value: INR %s" % round(total_value, 2))
        print("Portfolio Contents:")
#        portfolio = trading_api.get_portfolio()
        for i in portfolio:
            if i == 'CASH':
                print("CASH: INR %s (%s percent of portfolio)" % (
                    round(portfolio[i], 2), round((portfolio[i] / total_value) * 100, 2)))
            else:
                print("%s: %s shares (%s percent of portfolio)" % (
                    i, round(portfolio[i], 2), round(((portfolio[i] * prices[i] * 100) / total_value), 2)))
        counter += 1
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        print("Your portfolio is upto date! Check on it again tomorrow!")

# Initial welcome statements
print("\n\n+|---------------------------------------------------------------|+")
print("+|               HELLO! WELCOME TO SWIPE ADVISORY!               |+")
print("+|         What would you like me to help you with today?        |+")
print("+|---------------------------------------------------------------|+")
user = input("Please enter your username: ")
print("Welcome", user)
continued = 'y'
while continued == 'y':
    print("\n\n\n1. Quick advise about buying a particular stock.")
    print("2. Maintaining your portfolio.")
    print("3. Scan through current ForEx or cryptocurrency exchange rates.")
    # Get the task to be performed
    task = input()
    # Quick advice about a particular stock
    if task == '1':
        print("\n\n+|---------------------------------------------------------------|+")
        print("+|                 WELCOME TO THE STOCK ADVISORY!                |+")
        print("+|---------------------------------------------------------------|+")
        while True:
            symbol = input("Please type a valid stock symbol: ") #find the stock the user requires
            if not symbol.isalpha():
                print("Please try again, entering a valid stock ticker of 3-4 letters")
            else:
                data=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+str(symbol)+'&apikey='+str(api_key))
                if 'Error' in data.text:
                    print("There has been an error. Please type a different stock symbol: ")
                else:
                    break
        tol = float(input("How much is your tolerance level? (Usually 5-10%): "))
        stock_info(symbol, tol)
    # Get exchange advice about digital and cryptocurrencies
    if task == '3':
        print("\n\n+|---------------------------------------------------------------|+")
        print("+|           WELCOME TO DIGITAL AND CRYPTOCURRENCY HUB!          |+")
        print("+|---------------------------------------------------------------|+")
        while True:
            from_currency = input("Convert from: ") #starting currency
            to_currency = input("Convert to: ") #ending currency
            if not from_currency.isalpha():
                print("Please try again, entering a valid stock ticker of 3-4 letters")
            else:
                data=requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency='+str(from_currency)+'&to_currency='+str(to_currency)+'&apikey='+str(api_key))
                if 'Error' in data.text:
                    print("There has been an error. Please try after some time! ")
                else:
                    break
        digi_crypto_info(from_currency, to_currency)
    #Maintaining portfolio
    if task == '2':
        print("\n+|---------------------------------------------------------------|+")
        print("+|                    MAINTAIN YOUR PORTFOLIO!                   |+")
        print("+|---------------------------------------------------------------|+")
        exists = os.path.isfile(user+'.txt')
        if exists:
            req_portfolio = LoadDictionary(user+".txt")
#            print(req_portfolio)
            print("Retreived your target portfolio!")
        else:
            req_portfolio={} #desired portfolio
            print("Looks like your portfolio is empty!")
            print("Let's create a portfolio to get started..")
            print("NOTE 1: Make sure that the total percentage adds upto 100.")
            print("NOTE 2: Make sure your portfolio has some percentage for 'Cash'.\n\n")
            create = 'y'
            while create=='y':
                while True:
                    print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
                    symbol = input("Please type a valid stock symbol: ") #find the stock the user requires
                    if not symbol.isalpha():
                        print("Please try again, entering a valid stock ticker of 3-4 letters")
                    else:
                        data=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+str(symbol)+'&apikey='+str(api_key))
                        if 'Error' in data.text:
                            print("There has been an error. Please type a different stock symbol: ")
                        else:
                            break
                percent = input("What percentage of your portfolio should it cover? ")
                req_portfolio[symbol] = float("{:.2f}".format(float(percent)))
                create = input("Would you like to add another stock to your portfolio? (y/n): ")
            print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
            cash_per = input("What percentage amount should your portfolio keep aside for 'Cash'? ")
            req_portfolio['CASH'] = float("{:.2f}".format(float(cash_per)))
            print("\n\n-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
            print("Take a look at your portfolio!")
            print(pd.DataFrame.from_dict(req_portfolio, orient='index',columns=['Percentage']))
            print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-\n")
            #Saving portfolio
            save_port = input("Would you like to save your portfolio? (y/n): ")
            if save_port.lower() == 'y':
                SaveDictionary(req_portfolio, user+".txt")
                print("Portfolio saved!")
            else:
                print("Portfolio not saved! You will have to re-enter your requirements next time again!")
            print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-\n\n")
        #Convert to multipliers
        for i in req_portfolio:
            req_portfolio[i] /= 100
        # What percentage are we allowed to be off? (To save trading commissions in the real world)
        tol = float(input("What maintenance percentage am I allowed to be off by? (Usually 5-10% is optimal): "))
        init_cash = float(input("How much cash would you like me to start with? (INR): "))
        tol /= 100
        maintain_portfolio(req_portfolio, init_cash,tol)
            
    #Ask if user needs any other help
    continued = input("\n\nIs there any other task I can help you with? (y/n): ").lower()
print("\n+|---------------------------------------------------------------|+")
print("+|                       BYE, SEE YOU SOON!                      |+")
print("+|---------------------------------------------------------------|+")