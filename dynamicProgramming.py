import numpy as np
import math

moneyNeedToWin = 100
probabilityToGetEagle = 0.55
gamma = 0.5
precision = 0.00001

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
    if currentMoney + nextMoney > moneyNeedToWin:
        return 1
    return 0

def needToStopFunc(prevValues, newValues):
    for i in range(0, len(prevValues)):
        if abs(prevValues[i] - newValues[i]) > precision:
            return False
    return True
    
def startSimulation():
    # 0 means 1
    stateValues = np.zeros(moneyNeedToWin - 1)
    needToStop = False
    while needToStop != True:
        # 0 means 1
        currStateValues = np.zeros(moneyNeedToWin - 1)
        for s in range(1, moneyNeedToWin):
            stateValue = 0
            
            for a in range(0, min(s, moneyNeedToWin - s)):
                aVal = a + 1
                strategyRes = throwCoin(aVal)                
                secondSum = 0
                for sNext in range (1, moneyNeedToWin):
                    p = probabilityToGetMoney(s, sNext, aVal)
                    r = valuesYouWillGet(s, sNext, a)
                    secondSum = secondSum + p * (r + gamma * stateValues[s - 1])
                
                stateValue = stateValue + strategyRes * secondSum
            currStateValues[s - 1] = stateValue
        needToStop = needToStopFunc(stateValues, currStateValues)
        stateValues = currStateValues
        print(stateValues)

startSimulation()