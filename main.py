import random
import math


def readInputFromFile(filePath):
    fileInput = open(filePath, "r")
    lines = fileInput.readlines()
    n = -1
    capacity = -1
    profits = []
    weights = []
    for i in range(len(lines)):
        line = lines[i]
        if i == 0:
            n = int(line.split(" ")[0])
            capacity = int(line.split(" ")[1])
        else:
            profits.append(int(line.split(" ")[0]))
            weights.append(int(line.split(" ")[1]))

    knapsack(n, profits, weights, capacity)


def printResultsToFile(profitsSum, itemsDic):
    result = str(profitsSum) + "\n"  # final string that will be written in txt file
    for item in itemsDic:
        if item.get("selected") == True:
            result += "1\n"
        else:
            result += "0\n"
    file = open("output.txt", "w")
    file.write(result)
    file.close()


def knapsack(n, profits, weights, capacity):
    """
    inputs:
    n => number of available items
    profits => list of items profits
    weights => corresponding profit item weight
    capacity => container's overall capacity
    -- items are turned into dictionaries (used dictionary types to be able to track items original place after sorting)
    """
    # Step 0: create a list of dictionaries based on inputs
    items = []  # will contain a list of dictionaries
    for i in range(n):
        items.append(
            {
                "original_index": i,
                "profit": profits[i],
                "weight": weights[i],
                "selected": False,
            }
        )

    # Step 1: for each item we get profit/weight ratio
    for i in range(n):
        ratio = items[i].get("profit") / items[i].get("weight")
        items[i]["ratio"] = ratio

    # Step 2: sort ratios list in a decreasing format
    items = sorted(items, key=lambda x: x["ratio"], reverse=True)

    # Step 3: start filling container (knapsack) as much as possible
    profitsSum = 0
    remainedCapacity = capacity
    numberOfSelectedNodes = 0
    for i in range(n):
        itemWeight = items[i].get("weight")
        if itemWeight > remainedCapacity:
            continue
        items[i]["selected"] = True  # select item
        numberOfSelectedNodes += 1
        remainedCapacity -= itemWeight  # update remained capacity
        profitsSum += items[i].get("profit")

    # output result
    # sort items based on their original order
    items = sorted(items, key=lambda x: x["original_index"])
    print("\n\n*** Process Completed ***")
    print("Number of nodes:", n)
    print("Number of selected nodes (in the knapsack):", numberOfSelectedNodes)
    print("Selected nodes profit:", profitsSum)
    for i in range(n):
        print(
            f"Item {i + 1} with (w/p) of ({items[i].get('weight')}, {items[i].get('profit')}) is selected? {items[i].get('selected')}"
        )

    printResultsToFile(profitsSum, items)


def generateRandomTests(numberOfInstances, m, n):
    """
    numberOfInstances => is v in the given document
    n => list of number of items in the given document
    m => normalization factor given in the document
    """
    for i in range(len(n)):
        numberOfItems = n[i]
        for j in range(numberOfInstances):
            weights = []
            profits = []
            for k in range(numberOfItems):
                # Step 1: genearate pairs of (weight, profit)
                weight = random.randint(1, 1000)
                profit = random.randint(weight + 95, weight + 105)
                # Step 2: normalization
                weight = math.ceil(weight / (m + 1))
                profit = math.ceil(profit / (m + 1))
                # save values
                weights.append(weight)
                profits.append(profit)

            # Step 3: get random item at previously genearated items and multiply it by a random number at range [1, m]
            finalWeights = []
            finalProfits = []
            overallWeight = 0
            for k in range(numberOfItems):
                selectedItemIndex = random.randint(0, numberOfItems - 1)
                multiplicationFactor = random.randint(1, m)
                curItemWeight = weights[selectedItemIndex] * multiplicationFactor
                finalWeights.append(curItemWeight)
                finalProfits.append(profits[selectedItemIndex] * multiplicationFactor)
                overallWeight += curItemWeight
            capacity = math.ceil(overallWeight / 3)

            knapsack(numberOfItems, finalProfits, finalWeights, capacity)


v = 5
m = 20
n = [50, 60, 70, 80, 90, 100]
generateRandomTests(v, m, n)

# uncomment this is you want to read input from file
#readInputFromFile("input.txt")
