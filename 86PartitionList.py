# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        #store the last node that is less than target
        #store the first node that is greater than target
        last_node_lessThanTarget = head
        first_node_greaterThanTarget = head
        last_GTT = None
        currNode = head
        result = head
        if currNode == None:
            return None
        if currNode.val < x:
            result = head
            last_node_lessThanTarget = currNode
            first_node_greaterThanTarget = None
            last_GTT = None
            currNode = currNode.next
        elif currNode.val > x:
            first_node_greaterThanTarget = currNode
            last_GTT = currNode
            last_node_lessThanTarget = None
            currNode = currNode.next
            result = currNode
        else:
            # ==x
            first_node_greaterThanTarget = None
            last_node_lessThanTarget = currNode
            currNode = currNode.next
            result = head
        while(currNode.next != None):
            if currNode.val<x:
                #append curr node to the last node less than target,
                last_node_lessThanTarget.next = currNode
                temp = currNode.next
                currNode.next = first_node_greaterThanTarget
                currNode = temp
            elif currNode.val>x:
                temp = currNode.next
                if first_node_greaterThanTarget!=None:
                    first_node_greaterThanTarget.next = currNode
                last_GTT = currNode
                currNode = temp
            else:
                #==x just move the last bound of the current sesstion one over
                if last_node_lessThanTarget.next == currNode:
                    last_node_lessThanTarget = currNode
                if last_GTT.next = currNode:
                    last_GTT = currNode
        return result


        