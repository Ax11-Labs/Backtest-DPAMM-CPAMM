import matplotlib.pyplot as plt

import pandas as pd
file_path = "./content/ETH_Price202124.csv"
eth_data = pd.read_csv(file_path)

close_prices_list = eth_data['priceClose'].tolist()

# Iniitialize pool balances 
# K = 484084355000.00075
ethBalance = 25000 #neutral: 25000 | directionX: 50000 | directionY: 12500
usdBalance = 19363374.200000003 #neutral:19363374.200000003 | directionX:9681687.100000001 | directionY:38726748.400000006
fee_rate = 0.003
k=ethBalance*usdBalance # k remains constant entirely, no compound fees in this test
currentPrice = close_prices_list[-1] # 774.534968 # use the price of x (y/x)
hodlValueEth = ethBalance
hodlValueUSD = usdBalance

totalETH_fees = 0
totalUSD_fees = 0
eth_reserve = []
usd_reserve = []
eth_fees = []
usd_fees = []


def resetValue(ethBal, usdBal):
    global ethBalance, usdBalance, k, currentPrice, hodlValueEth,hodlValueUSD, totalETH_fees, totalUSD_fees
    ethBalance = ethBal
    usdBalance =usdBal
    k = ethBalance*usdBalance
    currentPrice = close_prices_list[-1]
    hodlValueEth = ethBal
    hodlValueUSD = usdBal
    totalUSD_fees =0
    totalETH_fees =0

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
        feeEarned = ethOut*fee_rate
        totalETH_fees+=feeEarned
        eth_fees.append(feeEarned)
        usd_fees.append(0)
        currentPrice = nextPrice

    elif nextPrice < currentPrice: # eth-in, usd-out
        # ethIn = newEthBalance - ethBalance
        ethBalance = newEthBalance
        newUsdBalance = k/ethBalance
        usdOut = usdBalance - newUsdBalance
        usdBalance = newUsdBalance
        # totalETH_fees += ethIn * fee_rate
        feeEarned = usdOut * fee_rate
        totalUSD_fees += feeEarned
        eth_fees.append(0)
        usd_fees.append(feeEarned)
        currentPrice = nextPrice
    eth_reserve.append(ethBalance)
    usd_reserve.append(usdBalance)

plt.figure(figsize=(14,6))


def runTest():
    resetValue(25000,19363374.200000003) # neutral, the same as CPAMM
    eth_reserve.append(ethBalance)
    usd_reserve.append(usdBalance)                   
    for i in reversed(range(len(close_prices_list)-1)):
        startDPAMM(close_prices_list[i])
    
    plt.subplot(2,2,1)
    plt.ylabel('ETH Reserve Amount')
    plt.xlabel('Days')
    plt.plot(eth_reserve, label='ETH Reserve Neutral', color="blue")
    plt.grid(True)
    plt.legend()


    plt.subplot(2,2,2)
    plt.ylabel('USD Reserve Amount')
    plt.xlabel('Days')
    plt.plot(usd_reserve, label='USD Reserve Neurtral', color="green")
    plt.grid(True)
    plt.legend()

    plt.subplot(2,2,3)
    plt.ylabel('ETH fees Amount')
    plt.xlabel('Days')
    plt.plot(eth_fees, label='ETH fees Neutral', color='blue')
    plt.grid(False)
    plt.legend()

    plt.subplot(2,2,4)
    plt.ylabel('USD fees Amount')
    plt.xlabel('Days')
    plt.plot(usd_fees, label='USD fees Neutral', color='green')
    plt.grid(False)
    plt.legend()
    eth_fees.clear()
    usd_fees.clear()
    eth_reserve.clear()
    usd_reserve.clear()
    
    resetValue(50000,9681687.100000001) # directional towards ETH by 2x
    eth_reserve.append(ethBalance)
    usd_reserve.append(usdBalance) 
    for i in reversed(range(len(close_prices_list)-1)):
        startDPAMM(close_prices_list[i])
    plt.subplot(2,2,1)
    plt.plot(eth_reserve, label='ETH Reserve Directional ETH 2x', color="red")
    plt.grid(True)
    plt.legend()

    plt.subplot(2,2,2)
    plt.plot(usd_reserve, label='USD Reserve Directional USD 0.5x', color="turquoise")
    plt.grid(True)
    plt.legend()

    plt.subplot(2,2,3)
    plt.ylabel('ETH fees Amount')
    plt.xlabel('Days')
    plt.plot(eth_fees, label='ETH fees Directional ETH 2x', color='red')
    plt.grid(False)
    plt.legend()

    plt.subplot(2,2,4)
    plt.ylabel('USD fees Amount')
    plt.xlabel('Days')
    plt.plot(usd_fees, label='USD fees Directional USD 0.5x', color='turquoise')
    plt.grid(False)
    plt.legend()
    eth_fees.clear()
    usd_fees.clear()
    eth_reserve.clear()
    usd_reserve.clear()
    
    resetValue(12500,38726748.400000006) # directional towards USD by 2x
    eth_reserve.append(ethBalance)
    usd_reserve.append(usdBalance) 
    for i in reversed(range(len(close_prices_list)-1)):
        startDPAMM(close_prices_list[i])
    plt.subplot(2,2,1)
    plt.plot(eth_reserve, label='ETH Reserve Directional ETH 0.5x', color="orange")
    plt.grid(True)
    plt.legend()

    plt.subplot(2,2,2)
    plt.plot(usd_reserve, label='USD Reserve Directional USD 2x', color="violet")
    plt.grid(True)
    plt.legend()

    plt.subplot(2,2,3)
    plt.ylabel('ETH fees Amount')
    plt.xlabel('Days')
    plt.plot(eth_fees, label='ETH fees Directional ETH 0.5x', color='orange')
    plt.grid(False)
    plt.legend()

    plt.subplot(2,2,4)
    plt.ylabel('USD fees Amount')
    plt.xlabel('Days')
    plt.plot(usd_fees, label='USD fees Directional USD 2x', color='violet')
    plt.grid(False)
    plt.legend()    
    eth_fees.clear()
    usd_fees.clear()
    eth_reserve.clear()
    usd_reserve.clear()

    # plt.tight_layout()
    plt.show()

runTest()

# for i in reversed(range(len(close_prices_list)-1)):
#     startDPAMM(close_prices_list[i])
# print("---------------------------")
# print("Current ETH Price: ", currentPrice)
# print("ETH Balance: ", ethBalance)
# print("USD Balance", usdBalance)
# print("ETH Fees: ", totalETH_fees)
# print("USD Fees: ", totalUSD_fees)
# balValue = (ethBalance*currentPrice)+usdBalance
# feeValue = (totalETH_fees*currentPrice)+totalUSD_fees
# print("Total Balance Value: ", balValue)
# print("Total Fees Value:     ", feeValue)
# # print("Fees in {%} Gain: ", (feeValue/balValue) *100)
# print()
# print("---------------------------")
# sumVal = balValue+feeValue
# print("Value Sum: ", sumVal)
# holdStillVal = (hodlValueEth*currentPrice)+hodlValueUSD
# print("Holding Still Value: ", holdStillVal)
# print()
# print("---------------------------")
# print("Testing for impermanent loss: Negative = IL, Positive = IG")
# impermaLoss = (1-(holdStillVal/sumVal))*100
# if impermaLoss > 0:
#     des = "Impermanent Gain(+): "
# else:
#     des = "Impermanent Loss(-): "
# print(des,impermaLoss,"percent")






