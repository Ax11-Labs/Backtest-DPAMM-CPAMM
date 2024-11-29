import matplotlib as plt

import pandas as pd
file_path = "./content/ETH_Price202124.csv"
eth_data = pd.read_csv(file_path)

close_prices_list = eth_data['priceClose'].tolist()

# Iniitialize pool balances 
# K = 484084355000.00075
ethBalance = 25000
usdBalance = 19363374.200000003
fee_rate = 0.003
k=ethBalance*usdBalance # k remains constant entirely, no compound fees in this test
currentPrice = close_prices_list[-1] # 774.534968 # use the price of x (y/x)
hodlValueEth = ethBalance
hodlValueUSD = usdBalance

totalETH_fees = 0
totalUSD_fees = 0

def startCPAMM(nextPrice):
    global ethBalance, usdBalance,currentPrice,totalETH_fees, totalUSD_fees 
    DeltaPrice = nextPrice/currentPrice
    newEthBalance=ethBalance/DeltaPrice

    # We assume the worst case where there is no trade that not changing the price,
    # so DeltaPrice = 0 is skipped
    #Eth price increases
    if DeltaPrice > 1: # eth-out, usd-in
        ethOut = ethBalance - newEthBalance 
        ethBalance = newEthBalance
        newUsdBalance = k/ethBalance
        # usdIn = newUsdBalance - usdBalance
        # totalUSD_fees += usdIn*fee_rate
        totalETH_fees += ethOut*fee_rate
        usdBalance = newUsdBalance
        currentPrice  = nextPrice
    #Eth price decreases
    elif DeltaPrice < 1: #eth-in, usd-out
        # ethIn =  newEthBalance - ethBalance
        ethBalance = newEthBalance
        newUsdBalance = k/ethBalance
        usdOut = usdBalance - newUsdBalance 
        usdBalance=newUsdBalance
        totalUSD_fees+=usdOut*fee_rate
        # totalETH_fees += ethIn*fee_rate
        currentPrice  = nextPrice

for i in reversed(range(len(close_prices_list)-1)):
    startCPAMM(close_prices_list[i])
    
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

        



        

        
        
    

    


