import random
import move

class TreeNode(object): 
    def __init__(self, val): 
        self.val = val 
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1
        

    def __str__(self):
        return str(self.val)
  
class AVL_Tree(object):
    def insert(self, root, key):
        if not root:
            return TreeNode(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        root.height = 1 + max(self.getHeight(root.left),
						self.getHeight(root.right))
        b = self.getBal(root)
        if b > 1 and key < root.left.val:
            return self.rRotate(root)
        if b < -1 and key > root.right.val:
            return self.lRotate(root)
        if b > 1 and key > root.left.val:
            root.left = self.lRotate(root.left)
            return self.rRotate(root)
        if b < -1 and key < root.right.val:
            root.right = self.rRotate(root.right)
            return self.lRotate(root)
        root.parent = None
        self.findPar(root)
        return root

    def lRotate(self, z):   
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
						self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
						self.getHeight(y.right))
        return y

    def rRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
						self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
						self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBal(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)
    
    def findPar(self, root):
        if root.left is not None:
            root.left.parent = root
            self.findPar(root.left)
        if root.right is not None:
            root.right.parent = root
            self.findPar(root.right)

    def search(self,root,key):
        return self._search(root,key) 

    def _search(self,root,key):
        if root.val == key:
            return root
        if root.val < key:
            return self._search(root.right,key)
        return self._search(root.left,key)

    def findlevel(self,curr,level = 0):
        if curr.parent is not None:
            return self.findlevel(curr.parent,level+1)  
        else:
            return level
    
def printTree90(node, level = 0):
    if node != None:
        printTree90(node.right, level + 1)
        print('     ' * level, node)
        printTree90(node.left, level + 1)

def equal(scurr,dcurr):
    global ansmove
    myTree = AVL_Tree()
    ls = []
    ld = []
    spath = []
    dpath = []
    while scurr.val != dcurr.val:
        if myTree.findlevel(scurr) < myTree.findlevel(dcurr):
            ld.append(dcurr.val)
            if dcurr.val > dcurr.parent.val:
                dpath.append('r')
            else:
                dpath.append('l')
            dcurr = dcurr.parent
        

        elif myTree.findlevel(scurr) > myTree.findlevel(dcurr):
            ls.append(scurr.val)
            spath.append('b')
            scurr = scurr.parent  
        else:
            ld.append(dcurr.val)
            if dcurr.val > dcurr.parent.val:
                dpath.append('r')
            else:
                dpath.append('l')
            dcurr = dcurr.parent
            ls.append(scurr.val)
            scurr = scurr.parent
            spath.append('b')

    ansmove = len(spath+dpath)
    return spath+dpath[::-1],ls+[scurr.val]+ld[::-1],ansmove
    
class GameTree():
    def __init__(self):
        self.myTree = AVL_Tree() 
        self.root = None
        self.data = []
        self.x = int(random.randint(0,1000))
        for i in range(100):
            while self.x in self.data:
                self.x = int(random.randint(0,1000))
            self.data.append(self.x)
        self.srand = self.data[random.randint(0,99)]
        self.drand = self.data[random.randint(0,99)]
        while self.drand == self.srand:
            self.drand = self.data[random.randint(0,99)]
        for e in self.data:
            self.root = self.myTree.insert(self.root, int(e))

        self.scurr = self.myTree.search(self.root,self.srand)
        self.dcurr = self.myTree.search(self.root,self.drand)
        self.current = self.scurr

        printTree90(self.root)
        print("===============")

        print('source = ',str(self.srand))
        print('destination = ',str(self.drand))

    #print('now = ',scurr.val,'level = ',myTree.findlevel(scurr))
    #print(myTree.findlevel(scurr))
        
        print(equal(self.scurr,self.dcurr))
        self.ansmove = equal(self.scurr,self.dcurr)[2]
        move.printcurr(self.current)