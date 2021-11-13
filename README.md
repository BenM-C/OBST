# OBST
This repository contains the code 


```python
import numpy as np
import sys
from collections import deque
from binarytree import bst, build
# from BSTclass import*
```


```python
def OBST(p,q,n):
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

p = [5,3,2,1]
q = [5,1,1,1,1]
dp = OBST(p,q,len(p))
print(dp)
```

    [[[5.0 1.0 1.0 1.0 1.0]
      [11.0 5.0 4.0 3.0 nan]
      [15.0 8.0 6.0 nan nan]
      [18.0 10.0 nan nan nan]
      [20.0 nan nan nan nan]]
    
     [[0.0 0.0 0.0 0.0 0.0]
      [11.0 5.0 4.0 3.0 nan]
      [20.0 12.0 9.0 nan nan]
      [30.0 18.0 nan nan nan]
      [38.0 nan nan nan nan]]
    
     [[nan nan nan nan nan]
      [1.0 2.0 3.0 4.0 nan]
      [1.0 2.0 3.0 nan nan]
      [1.0 3.0 nan nan nan]
      [1.0 nan nan nan nan]]]


Given movies $M_1...M_4$ and null searches $q_0...q_4$ we can arange them as such: 
$$q_0,M_1,q_1, M_2, q_2, M_3, q_3, M_4,q_4$$
This can be indexed into an array of size 9(indicies 0 through 8) where if the index of an element in the array is odd, it refers to a movie and even it refers to a null space, and can be translated by $M_n$ can be found at index 2n+1 and $q_n$ can be found at 2n.  


```python
def OBST_constructor(dp,tree = (2,-1,0)):
    x,y= np.shape(dp)[2],np.shape(dp)[1]
    if dp[tree]!=None:
        root = BST(value = dp[tree])
        root.right = OBST_constructor(dp,tree = (2,0,0))
        root.right = OBST_constructor(dp,tree = (2,0,0))
    else: root = None      

```

def OBST_constructor(roots, subtree) 
$4+3z$
    if the root of the subtree is null\
        set root to the null node of the x inded
    if the root of the sub-tree is non-null, 
        set right to the root of the right sub-tree
        set left to the root of the left sub-tree


```python
class BST:
    def __init__(self, value = None,left = None, right = None):
        self.left = left
        self.right = right
        self.value = value
        if value:
            self.size=1
            self.depth = 1
        else:
            self.size = 0
            self.depth = 0
            
    def stats(self):
        print('Tree with root: ', self.value, 'containing', self.size, 'nodes with a maximum depth of: ', self.depth)
        
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
                #deals with duplicates, and subtracts them from size
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
        try:
            leftDepth = self.left.maxDepth()
        except AttributeError:
            leftDepth = 0
        try:
            rightDepth = self.right.maxDepth()
        except AttributeError:
            rightDepth = 0
            
        if leftDepth > rightDepth:
            return leftDepth + 1
        else:
            return rightDepth + 1

    def BFS(self, filtered = True):
        BFS = []
        if self.value==None:
            return None
        q = deque()
        q.append(self)
        i=0
        while i<2**self.depth:
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
tree = BST(50)
tree.insert(random.sample(range(100), 20))
tree.insert(random.sample(range(100), 20))
print(tree.inorderTraversal())
tree.visualize()
# tree.BFS()
```

    [3, 5, 7, 8, 12, 13, 18, 19, 22, 23, 24, 27, 30, 33, 34, 35, 41, 42, 50, 51, 53, 54, 57, 60, 62, 65, 68, 69, 73, 75, 78, 81, 87, 88, 89, 97]
    
                             _________________________50___________________________
                            /                                                      \
        ___________________23___                                    ________________73____________
       /                        \                                  /                              \
      5__________               _27____________               ____57______                        _88___
     /           \             /               \             /            \                      /      \
    3         ____18___       24            ____41         _53            _65                  _87      _97
             /         \                   /      \       /   \          /   \                /        /
          __12         _22               _34       42    51    54      _62    68            _81       89
         /    \       /                 /   \                         /         \          /
        7      13    19               _33    35                      60          69      _78
         \                           /                                                  /
          8                         30                                                 75
    



```python
import random
randomlist = random.sample(range(10, 100), 20)
```
