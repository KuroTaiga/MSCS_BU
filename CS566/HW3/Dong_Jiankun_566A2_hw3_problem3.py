import numpy as np
import math
import sys
import random
#idea of this sort is that we splite the array based on the max size we can store: N
#we merge sort each of the segments O（NlogN)
#then take the first element of each sorted segments and merge it into a sorted array
#repeat that until all elements of each segments have been poped off and sorted

class listNode:
    """ min heap
        value is the value being sorted
        segIndex is the segment that contains this value
    """
    def __init__(
            self,
            value,
            segIndex
    ):
        self.value = value
        self.segIndex = segIndex

# inputArray is the unsorted array, N is the largest number of elements we can store in each segment
# N should be larger than the segments
def externalSort(inputArray, N):
    segCount = math.ceil((len(inputArray)/N)) # find number of segments needed
    result = []
    #print(segCount)
    segArray = []
    # spliting the array into segments, each with N elements
    for i in range (0,segCount-1):
        curr = inputArray[N*i : N*i+N]
        segArray.append(curr)
    segArray.append(inputArray[N*(segCount-1):len(inputArray)])
    # sort each segments
    for curr in segArray:
        curr.sort()
    
    #first we take the sorted segments' first element, to form a sorted storage buffer
    bufferArray = []
    #size of the element from each seg to form the buffer
    for i in range(0,segCount):
        currNode = listNode(segArray[i][0],i); #take first element of each sorted segment
        #print("value",segArray[i][0], "in",i)
        bufferArray.append(currNode)
        segArray[i] = segArray[i][1:]
    bufferArray.sort(key= lambda listNode: listNode.value)
    for i in range(0, len(inputArray)):
        currMin = bufferArray[0].value
        popSeg = bufferArray[0].segIndex
        result.append(currMin)
        bufferArray = bufferArray[1:]
        if (len(segArray[popSeg])>0):
            #then we append the next element
            bufferArray.append(listNode(segArray[popSeg][0],popSeg))
            segArray[popSeg] = segArray[popSeg][1:]
        else:
            bufferArray.append(listNode(sys.maxsize, popSeg))
        bufferArray.sort(key= lambda listNode: listNode.value)
    #now we need to clear the remaining buffer
    #i = 0
    #while (bufferArray[i].value!=sys.maxsize) and (i<len(bufferArray)):
     #   result.append(bufferArray[i].value)
      #  i += 1
    return result



# TEST CASES:
# create an array using np.array()
testN = 10
testArr1 = random.sample(range(1,101),100)
golden1 = sorted(testArr1)
#print("testArray", testArr1)

splitTest = externalSort(testArr1,testN)
#print("result: ",splitTest[0:30])
#print("golden: ",golden1[0:30])
testPassed1 = splitTest==golden1
print("test 1")
print("test size: ",len(testArr1))
print("test 1 passed: ",testPassed1)

testN = 100
testArr2 = random.sample(range(1,1001),1000)
golden2 = sorted(testArr2)
#print("testArray", testArr2)

splitTest = externalSort(testArr2,testN)
#print("result: ",splitTest[0:10])
#print("golden: ",golden2[0:10])
testPassed2 = splitTest==golden2
print("test 2")
print("test size: ",len(testArr2))
print("test 2 passed: ",testPassed2)

testN = 1000
testArr3 = random.sample(range(1,10001),10000)
golden3 = sorted(testArr3)
#print("testArray", testArr3)

splitTest = externalSort(testArr3,testN)
#print("result: ",splitTest[0:10])
#print("golden: ",golden3[0:10])
testPassed3 = splitTest==golden3
print("test 3")
print("test size: ",len(testArr3))
print("test 3 passed: ",testPassed3)
print("All test has passed? ", testPassed3 and testPassed1 and testPassed2)

