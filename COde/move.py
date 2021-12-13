def printcurr(curr):
    if curr.left:
        print(curr.left.val,end=' ') 
    else :
        print('-',end=' ')
    print(curr.val,end=' ')
    if curr.right:
        print(curr.right.val)
    else :
        print('-')
nmove = 0
def moveLeft(curr):
    global nmove
    nmove+=1
    print('left',nmove)
    if curr.left is not None:
        curr = curr.left
    printcurr(curr)
    return curr
def moveRight(curr):
    global nmove
    nmove+=1
    print('right',nmove)
    if curr.right is not None:
        curr = curr.right
    printcurr(curr)
    return curr
def moveBack(curr):
    global nmove
    nmove+=1
    print('down',nmove)
    if curr.parent is not None:
        curr = curr.parent
    printcurr(curr)
    return curr
def accurage(nmove,ansmove):
    return ['Your move : '+str(nmove),'Minimum move : '+str(ansmove),'Accuracy : '+str(round(ansmove/nmove*100,2))+'%']
def score(nmove,ansmove):
    return round(ansmove/nmove*100,2)