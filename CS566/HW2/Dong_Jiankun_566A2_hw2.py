import numpy as np

def findMax(inputArray, endIndex):
    result = 0
    for curr in range(1,endIndex+1): #index 1 to endIndex, no need to compare
                                     #with self(inputArray[result])
        if (inputArray[curr]>=inputArray[result]):
            result = curr
    return result

def MAXSORT(inputArray): #inputArray is E
    count = 0;
    if len(inputArray)<=1:
        return inputArray
    currSorted = len(inputArray)-1
    result = inputArray
    while(currSorted>0):
        # print("currSorted: ", currSorted)
        currMaxIndex = findMax(result,currSorted)
        # print("currMaxIndex: ",currMaxIndex)
        currMax = result[currMaxIndex]
        # print("currMax: ",currMax)
        result[currMaxIndex] = result[currSorted]
        result[currSorted] = currMax
        # print("result: ", result)
        currSorted = currSorted-1
    return result

# TEST CASES:
# create an array using np.array()
array1 = np.array([4, 1, 3, 5])
array2 = np.array([1])
array3 = np.array([5,4,3,7,8,6,2,1])
array4 = np.array([])

print("Result for Array: ",array1," is: ",MAXSORT(np.copy(array1)))
print("Result for Array: ",array2," is: ",MAXSORT(np.copy(array2)))
print("Result for Array: ",array3," is: ",MAXSORT(np.copy(array3)))
print("Result for Array: ",array4," is: ",MAXSORT(np.copy(array4)))