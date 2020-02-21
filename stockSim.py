import yfinance as yf 
import matplotlib.pyplot as plt

# Assuming an initial capital of 100 money, compare the following strategies
# Every morning, invest the previous day's capital evenly
# Split it evenly between the stocks, leave it there
# Fixed Interest

stocks = ["AMD", "TSLA", "AAPL", "GOOGL"]
#Note: instead of stock names, currency names like "JPY=X" work

years = 5

#download stock data
datas = {}
for stock in stocks:
	data = yf.download(stock, period=str(years)+"y", interval="1d")#, interval="5m")
	
	datas[stock] = data
	print(data)
	
#profit += ( row["High"]-row["Low"] ) / (row["Close"]+row["Open"]) * 2
dc = datas[stocks[0]].shape[0] #daycount


#starting values
money = [0 for i in range(dc)] #redistribute strategy
money[0] = 100

pm = {} #buy&hold
for stock in stocks:
	pm[stock] = [0 for i in range(dc)]
	pm[stock][0] = 100/len(stocks)

for i in range(dc-1):
	split = money[i]/len(stocks)
	
	for stock in stocks:
		money[i+1] += (datas[stock].iloc[i+1,:].loc["Open"])/(datas[stock].iloc[i,:].loc["Close"])*split #redistribute
		
		pm[stock][i+1] = datas[stock].iloc[i+1,:].loc["Open"]/datas[stock].iloc[0,:].loc["Open"]*pm[stock][0] #buy&hold

tl = [0 for i in range(dc)]
for stock in stocks:
	for i in range(dc):
		tl[i] += pm[stock][i]


DAYPEARYEAR = dc//years #not all days are trading days

plt.plot(range(dc), money, label="redistribute")
plt.plot(range(dc), tl, label="buy&hold")
plt.plot(range(dc), [100*(1+0.1/DAYPEARYEAR)**(i+1) for i in range(dc)], label="10%")
plt.plot(range(dc), [100*(1+0.23/DAYPEARYEAR)**(i+1) for i in range(dc)],  label="23%")
plt.legend()
plt.show()

money = [int(x) for x in money]