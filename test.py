from pybit.unified_trading import HTTP
session = HTTP(testnet=False)
res = session.get_tickers(category="spot")
l = []
for symbol in res['result']['list']:
    l.append(symbol['symbol'])
l.sort()
print(l)