import matplotlib as plt

import pandas as pd
file_path = "./content/ETH_Price202124.csv"
eth_data = pd.read_csv(file_path)

close_prices_list = eth_data['priceClose'].tolist()

# Iniitialize pool balances 
# K = 484084355000.00075
ethBalance = 2500 #neutral: 25000 | directionX: 50000 | directionY: 12500
usdBalance = 193633742.00000003 #neutral:19363374.200000003 | directionX:9681687.100000001 | directionY:38726748.400000006
fee_rate = 0.003
k=ethBalance*usdBalance # k remains constant entirely, no compound fees in this test
currentPrice = close_prices_list[-1] # 774.534968 # use the price of x (y/x)
hodlValueEth = ethBalance
hodlValueUSD = usdBalance

totalETH_fees = 0
totalUSD_fees = 0

def startDPAMM(nextPrice):
    global ethBalance, usdBalance,currentPrice,totalETH_fees, totalUSD_fees 
    newEthBalance = (ethBalance*currentPrice)/nextPrice

    if nextPrice > currentPrice: # eth-out, usd-in
        ethOut = ethBalance-newEthBalance
        ethBalance = newEthBalance
        newUsdBalance = k /ethBalance
        # usdIn = newUsdBalance - usdBalance
        usdBalance = newUsdBalance
        # totalUSD_fees += usdIn*fee_rate
        totalETH_fees+=ethOut*fee_rate
        currentPrice = nextPrice

    elif nextPrice < currentPrice: # eth-in, usd-out
        # ethIn = newEthBalance - ethBalance
        ethBalance = newEthBalance
        newUsdBalance = k/ethBalance
        usdOut = usdBalance - newUsdBalance
        usdBalance = newUsdBalance
        # totalETH_fees += ethIn * fee_rate
        totalUSD_fees += usdOut * fee_rate
        currentPrice = nextPrice

for i in reversed(range(len(close_prices_list)-1)):
    startDPAMM(close_prices_list[i])

print("---------------------------")
print("Current ETH Price: ", currentPrice)
print("ETH Balance: ", ethBalance)
print("USD Balance", usdBalance)
print("ETH Fees: ", totalETH_fees)
print("USD Fees: ", totalUSD_fees)
balValue = (ethBalance*currentPrice)+usdBalance
feeValue = (totalETH_fees*currentPrice)+totalUSD_fees
print("Total Balance Value: ", balValue)
print("Total Fees Value:     ", feeValue)
# print("Fees in {%} Gain: ", (feeValue/balValue) *100)
print()
print("---------------------------")
sumVal = balValue+feeValue
print("Value Sum: ", sumVal)
holdStillVal = (hodlValueEth*currentPrice)+hodlValueUSD
print("Holding Still Value: ", holdStillVal)
print()
print("---------------------------")
print("Testing for impermanent loss: Negative = IL, Positive = IG")
impermaLoss = (1-(holdStillVal/sumVal))*100
if impermaLoss > 0:
    des = "Impermanent Gain(+): "
else:
    des = "Impermanent Loss(-): "
print(des,impermaLoss,"percent")


