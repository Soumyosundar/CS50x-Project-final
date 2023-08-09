# Stock Manager
#### Video Demo: https://drive.google.com/file/d/1mx1DVDL-xtNKUmzwOelPgyWdpzsFZImS/view?usp=drive_link
#### Description:
# Layout.html- The layout.html file is in place so that all the other html files can follow a certain layout of the entire webpage. My layout.html files allows their to be a tab for each file that is being called in the layout.html file. The layout file is basically the entire webpage and contains the title, all the html files, layouts, designs, and etc.

# Add cash.html- This file is mainly there to add cash to a certain user's cash. This file uses the Select * function in which it calls the users table and adds the cash the user wants to add. This function once you have added the cash it will redirect you to the index.html page. The add cash file also has a separate html file which holds the main body of the buttons and text boxes.

# Change password.html- This file is mainly there to change your password and hash the password in the users table. This file uses the Select * function in which it calls the users table and changes the password whilst also showing a hashed version of this password on the actual users table. This function once you have added the cash it will redirect you to the index.html page. The add cash file also has a separate html file which holds the main body of the buttons and text boxes.

# Apology.html- This file is used to give error messages or “apologies” when they have done something when inputting a value. It gets called in helpers.py and the html file has a link which generates the apology with the error codes.

# Login.html- This file contains the code for a person to be able to log into the website. The login.html file contains the code for the input fields and log in button. Login calls the users table and unhashes the password so that it can verify if you have inputted the values correctly.

# Buy.html- this file contains the code for the tab Buy. Buy.html contains the code for the input fields and buy button. The input fields are the stock symbol and how many shares do you want to buy for that stock.

# Sell.html-this file contains the code for the tab Sell. Sell.html contains the code for the input fields and Sell button. The input fields are the stock symbol and how many shares do you want to buy for that stock.

# Portfolio analysis.html- This file contains the code for the tab portfolio analysis. In this file it contains the code for the table in which it calls the API IEX and displays the stock symbol and stock price. It also displays the amount of shares you own for that particular stock, the investment price or (shares*stock price), and the sell price which is what you would get if you sold the stock at that current moment.

# Index.html- This file contains the code for the mainpage of the entire stock website. This file also contains the info from the IEX API, in which on the table it calls the stock price, stock symbol. It also has the amount of shares you own for a particular stock. It only displays any new stocks you buy, if you bought any old ones twice or thrice it will only add to the original amount of shares.

# History.html- this file contains the code for the history page of the stock website. This file also contains the info from the IEX API and from the users table, in which on the table it calls the stock price, stock symbol. It shows how many times you have bought a stock by displaying the stock symbol, the amount of shares you bought, and how much one share cost. It will also display if it was a purchase or if you sold a stock with the words “BUY” and “SELL”.


# Register.html- This file contains the code for the Register page. This file contains the code for the input fields and Register button. The file also calls the users table and adds a new user with a new id every time a new user has registered on the page.

# Quote.html- This file contains the code for the quote page of the stock website. In this file it has the code of the input field and quote button. The quote.html file when you click quote, it will scour the IEX API, for the Stock symbol you input and display how much that particular stock costs, its name, and who it's under.

# Finance.db- This file contains all the tables that I used for this code. Finance.db has the users table which contains the users information like username, password, and how much money they have. Finance.db also has the Transactions table which shows all the transactions made by any user. Finally it contains the user_shar table which shows all the shared data related to a user.

# App.py- This is the main file that controls all the functionalities of the entire stock webpage. App.py controls the functions of Buy and sell, it calls all three tables in finance.db and updates them every time a person buys or sells a stock. App.py also controls the register, login, changepassword, addcash, and logout functions allowing them to update the users, transactions, and user_share table and change their relative rows and columns. App.py also controls quotes and when you click the button it calls the IEX API and gets the relative information to display the price of the stock and the name of the company. App.py controls index, history, and portfolio analysis and helps display the information on the tables in each of these tabs.

# By: Soumyosundar Dutta

