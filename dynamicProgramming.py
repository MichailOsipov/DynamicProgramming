import numpy as np
import matplotlib.pyplot as plt

moneyNeedToWin = 100
probabilityToGetEagle = 0.25
gamma = 1
precision = 1e-3

def throwCoin(moneyToBet):
    randomNumber = np.random.uniform(0, 1)
    if randomNumber < probabilityToGetEagle:
        return moneyToBet
    return -moneyToBet
    
def probabilityToGetMoney(currentMoney, nextMoney, moneyToBet):
    if currentMoney < moneyToBet:
        return 0
    if currentMoney + moneyToBet == nextMoney:
        return probabilityToGetEagle
    if currentMoney - moneyToBet == nextMoney:
        return 1 - probabilityToGetEagle
    return 0

def valuesYouWillGet(currentMoney, nextMoney, moneyToBet):
    if currentMoney < moneyToBet:
        return 0
    if currentMoney + moneyToBet != nextMoney:
        return 0
    if currentMoney + moneyToBet >= moneyNeedToWin:
        return 1
    return 0

def needToStopFunc(prevValues, newValues):
    maxDiff = np.amax(np.absolute(prevValues - newValues))
    if (maxDiff < precision):
        return True
    return False

def calculateValues():
    stateValues = np.zeros(moneyNeedToWin + 1)
    needToStop = False
    while needToStop != True:
        currStateValues = np.zeros(moneyNeedToWin + 1)
        for s in range(1, moneyNeedToWin):
            stateValue = -1
            
            for a in range(1, min(s, moneyNeedToWin - s) + 1):
                sNext1 = s + a
                sNext2 = s - a

                p1 = probabilityToGetMoney(s, sNext1, a)
                r1 = valuesYouWillGet(s, sNext1, a)
                nextStateValue1 = stateValues[sNext1]
                curr1 = p1 * (r1 + gamma * nextStateValue1)
                
                p2 = probabilityToGetMoney(s, sNext2, a)
                r2 = valuesYouWillGet(s, sNext2, a)
                nextStateValue2 = stateValues[sNext2]
                curr2 = p2 * (r2 + gamma * nextStateValue2)

                curr = curr1 + curr2
                if curr > stateValue:
                    stateValue = curr

            currStateValues[s] = stateValue
        needToStop = needToStopFunc(stateValues, currStateValues)
        stateValues = currStateValues
    return stateValues

def calculateStrategy(strategyValues):
    strategy = np.zeros(moneyNeedToWin + 1)
    for s in range (1, moneyNeedToWin):
        stateValue = -1
        currA = 0
        for a in range(1, min(s, moneyNeedToWin - s) + 1):
            sNext1 = s + a
            sNext2 = s - a
            
            p1 = probabilityToGetMoney(s, sNext1, a)
            r1 = valuesYouWillGet(s, sNext1, a)
            nextStateValue1 = strategyValues[sNext1]
            curr1 = p1 * (r1 + gamma * nextStateValue1)
            
            p2 = probabilityToGetMoney(s, sNext2, a)
            r2 = valuesYouWillGet(s, sNext2, a)
            nextStateValue2 = strategyValues[sNext2]
            curr2 = p2 * (r2 + gamma * nextStateValue2)

            curr = curr1 + curr2
            if curr > stateValue:
                stateValue = curr
                currA = a
        strategy[s] = currA
    return strategy
        
strategyValues = calculateValues()
strategy = calculateStrategy(strategyValues)

#plt.plot(np.arange(len(strategyValues)), strategyValues)
plt.plot(np.arange(len(strategy)), strategy)
plt.show()