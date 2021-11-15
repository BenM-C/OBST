```python
import numpy as np
import sys
from collections import deque
from binarytree import bst, build
```


```python
def OBST(p,q):
    def calc_OBST(p,q,n):
        dp = np.zeros((3,n+1,n+1))#z index: 0=w, 1=c 2 = r
        dp[:,:,:],dp[1,0,:]= None,0 #set initial costs to 0, else NaN
        for i in range(n+1): #initialize first row/base case of no elements
            dp[0,0,i] = q[i] #first row weights
        for j in range(1,n+1): #number of movies
            for i in range(n-j+1): #starting where
                dp[0,j,i]= dp[0,j-1,i]+p[i+j-1]+q[i+j]
                dp[1,j,i] = sys.maxsize
                for k in range(i+1,i+j+1):
                    t = dp[0,j,i]+dp[1,k-1-i,i]+dp[1,i+j-k,k]
                    if t< dp[1,j,i]:
                        dp[1,j,i] = t
                        dp[2,j,i] = k
        return dp
    
    def OBST_constructor(A,i,j):
        r = A[j-i,i]
        if np.isnan(r):
            return None
        else:
            st = myBST(value = int(r))
            st.left = OBST_constructor(A,i,int(r)-1)
            st.right = OBST_constructor(A,int(r), j)
            return st
    
    ##################################################################
    if len(q) == len(p)+1:
        dp = calc_OBST(p,q,len(p))
        tree = OBST_constructor(dp[2,:,:],0,len(p))
        return tree
    else:
        print('incorrrect number of nodes')
    
```


```python
class BST:
    def __init__(self, value = None,left = None, right = None):
        self.left = left
        self.right = right
        self.value = value
            
    def stats(self):
        print('Tree with root: ', self.value, 'containing', len(self.inorderTraversal()), 'nodes with a maximum depth of: ', self.maxDepth())
        
    def insert_1(self,v):
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
        print(build(self.BFS(filtered = False)))    
        
    def search(self, key):
        return None
    
```


```python
#testing examples!
#Movies
p=[2,1,4,1]
q = [1,2,1,1,3]
#homework
m = [5,3,2,1]
d = [5,1,1,1,1]
tree1 = OBST(p,q)
tree2 = OBST(m,d)
tree1.visualize(), tree2.visualize()
```

    
      __3
     /   \
    1     4
     \
      2
    
    
    1__
       \
        3
       / \
      2   4
    





    (None, None)


