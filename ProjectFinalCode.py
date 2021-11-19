
import numpy as np
import sys
from collections import deque
from binarytree import bst, build

def calc_OBST(p,q):
    '''
    calculates the optimal solution for a binary search tree using dynamic programing
    ==================
    Arguments:

        p:   List, np.ndarray--coresponding the probabilites a node is visited

        q:   List, np.ndarray--coresponding the probabilites of null nodes, size |p|+1

    Returns:

        dp:   np.ndarray--3 dimensional array of size (3,n+1,n+1), indexing (depth, row, col). 
              dp[0::]coresponds to the weights of tree(i,i+j), 
              dp[1::] coresponds to the cost of tree(i,i+j), 
              and dp[2::] coresponds to the root of tree(i,i+j). 
    '''
    n = len(q) #number of fail nodes
    dp = np.zeros((3,n,n))#z index: 0=w, 1=c 2 = r
    dp[:,:,:],dp[1,0,:]= None,0 #set initial costs to 0, else NaN
    
    for i in range(n): #initialize weights first row of trees with no nodes
        dp[0,0,i] = q[i] #first row weights are just the weight of the fail node

    for i in range(1,n): #iterate through rows(size of the tree)
        for j in range(n-i):#iterate through columns(starting fail node of tree of size i)
            #update weights, two different methods work
            #   dp[0,i,j]= dp[0,i-1,j]+p[i+j-1]+q[i+j]
            #alternitavely
            dp[0,i,j] = sum(p[j:j+i])+sum(q[j:j+i+1]) 
            dp[1,i,j] = sys.maxsize #set costs to max int
            for r in range(j,j+i):
                #cost of first tree contains root-start elements starting at j
                #cost of second tree contains end-root-1 elements starting at root+1
                #this is a little bit weird compared to alg becuase nodes indexed at 0 not 1
                c = dp[0,i,j]+dp[1,r-j,j]+dp[1,i+j-r-1,r+1]
                if c < dp[1,i,j]: #check if it is a new optimal cost and update apropriately
                    dp[1,i,j] = c
                    dp[2,i,j] = r+1
    return dp   

def OBST_constructor(A,i,j):
    '''
    based on the DP array of roots of each subtree T(i,j+i), this reconstructs a BST
    ==================
    Arguments:

        A:   (n+1,n+1)np.ndarray--coresponding roots of each optimal sub-tree

        i,j: int-- coresponding to the start location in the DP array of the sub-tree 
             containing all nodes, typically, (0, len(p))

    Returns:

        st:   BST object--Custom BST class containing the optimal binary search tree

    Note: this is not designed to include the null nodes in the tree coresponding to q as they are implied
          by the ordering of the nodes...ie q0 needs to be the left child of p1.  
    '''
    #establish root from A and check if it is a null node.  
    r = A[i,j]
    if np.isnan(r):
        return None
    #if if the root is another node, recursively call OBST_constructor on each of its 
    #children to get the optimal sub-trees and construct a new tree with the value of root, 
    #and its two optimal sub-trees
    else:
        st = BST(value = int(r))
        st.left = OBST_constructor(A,int(r)-j-1, j)
        st.right = OBST_constructor(A,i+j-int(r),int(r))
        return st
    
def OBST(p,q, output = True):
    '''
    Optimal Binary search trees
    ==================
    Arguments:
    
        P:   List, np.ndarray--coresponding the probabilites a node is visited

        M:   List, np.ndarray--coresponding the probabilites of null nodes, size |p|+1
    
    Returns:
    
        tree:   BST--instance of a binaary search tree object coresponding to custom class BST
    '''
    #if p and q are the right length use helper functions to return the obst
    if len(q) == len(p)+1:
        dp = calc_OBST(p,q)
        print(dp)
        tree = OBST_constructor(dp[2,:,:],len(p),0)
        if output: tree.visualize()
        return tree
    else:
        print('incorrrect number of nodes')





#===============================================================================================#
class BST:
    '''
    Custom Binary search tree class
    ==================
    Arguments:
    
        P:   List, np.ndarray--coresponding the probabilites a node is visited

        M:   List, np.ndarray--coresponding the probabilites of null nodes, size |p|+1
    
    Returns:
    '''
        
    def __init__(self, value = None,left = None, right = None):
        '''
        Each tree contains three atributes, a value and a pointer to left and right child 
        all initialized to None, meaning an empty tree can exist
        '''
        self.left = left
        self.right = right
        self.value = value
            
    def stats(self):
        '''
        basic to_string option
        '''
        print('Tree with root: ', self.value, 'containing', len(self.inorderTraversal()), 
              'nodes with a maximum depth of: ', self.maxDepth())
        
    def insert_1(self,v):
        '''
        Inserts a single value into BST, 
        checks if the value of the root is none and if not insert_1 recursively into 
        the right or left sub-tree
        ==================
        Arguments:
    
            v:   int, float--a singular value to be inserted into itself BST
    
        Returns: None
        '''
        if self.value!=None:
            if v < self.value:
                if self.left is None:
                    self.left = BST(value = v)
                else:
                    self.left.insert_1(v)
                    
            elif v > self.value:
                if self.right is None:
                    self.right = BST(value = v)
                else:
                    self.right.insert_1(v)
            else:
                self.value = v
        else:
            self.value = v
                    
    def insert(self,data):
        '''
        Inserts a single, or an array-like set of values into BST
        checks the type, and calls insert_1
        ==================
        Arguments:
    
            data:   int, float, list, np.ndarray--value(s) to be inserted into tree
    
        Returns: None
        '''
        if isinstance(data,(str,int,float)):
            self.insert_1(data)
        elif isinstance(data, (np.ndarray,list)):
            for i in data:
                self.insert_1(i)
        else:
            raise TypeError
        self.depth = self.maxDepth()
        self.size = len(self.inorderTraversal())
            
    def maxDepth(self):
        '''
        calculates the maximum depth for the tree, implemented to find the maximum 
        number of iterations on BFS
        ==================
        Arguments:
            
            self--BST
    
        Returns: 
            
            int--maximum depth of the tree
        '''
        if self.value==None:
            return 0
        else:
            try:
                leftDepth = self.left.maxDepth()
            except:
                leftDepth = 0
            try:
                rightDepth = self.right.maxDepth()
            except:
                rightDepth = 0
            if leftDepth > rightDepth:
                return leftDepth + 1
            else:
                return rightDepth + 1

    def BFS(self, filtered = True):
        BFS = []
        if np.isnan(self.value):
            return None
        q = deque()
        q.append(self)
        i=0
        while i<2**self.maxDepth():
            n = q.popleft()
            BFS.append(n.value)
            if n.left!=None:
                q.append(n.left)
            else: q.append(BST())
            if n.right!=None:
                q.append(n.right)
            else: q.append(BST())
            i+=1
                
                
        if filtered:
            return list(filter(None,BFS))
        else: 
            return BFS
    
    def inorderTraversal(self, p = True):
        l = []
        if self.left:
            l = l+self.left.inorderTraversal()
        l.append(self.value)
        if self.right:
            l=l+self.right.inorderTraversal()
        if p:
            return l
        else:
            return l
    
    def visualize(self):
        '''
        calls on BFS to generate a level order array of the tree containing null nodes, 
        and builds the tree
        '''
        print(build(self.BFS(filtered = False)))    
        
    def search(self, key):
        '''
        maybe i'll implement this one day
        '''
        return None
    
# testing examples! taken from the homework to show that this method works.  
# class/recitation 6
p=[2,1,4,1]
q = [1,2,1,1,3]
#homework 6
m = [5,3,2,1]
d = [5,1,1,1,1]

OBST(m,d)
OBST(p,q)
