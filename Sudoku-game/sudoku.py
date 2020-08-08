

board = [
        [0, 0, 0, 0, 0, 0, 4, 7, 0],
        [9, 3, 0, 0, 2, 4, 0, 5, 6],
        [0, 0, 0, 0, 7, 0, 0, 0, 0],
        [5, 0, 6, 0, 9, 0, 0, 1, 0],
        [3, 2, 0, 0, 6, 0, 0, 9, 7],
        [0, 7, 0, 0, 5, 0, 6, 0, 2],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [7, 9, 0, 2, 1, 0, 0, 3, 4],
        [0, 1, 2, 0, 0, 0, 0, 0, 0]
]

r = len(board)
c = len(board[0])

def findEmpty(board):
    for i in range(r):
        for j in range(c):
            if board[i][j] == 0:
                return (i,j)
    
    return False

def printBoard(board):
    print()
    for i in range(r):
        if i % 3 == 0 and i != 0:
            print('- - -   - - -   - - -')
        
        for j in range(c):
            if j % 3 == 0 and j != 0:
                print('| ',end='')
            print('{} '.format(board[i][j]),end='')
        
        print()
    print()

def notPresentInRow(board,row,col,key):
    for i in range(c):
        if board[row][i] == key and i != col:
            return False
    
    return True

def notPresentInCol(board,row,col,key):
    for i in range(r):
        if board[i][col] == key and i != row:
            return False

    return True

def notPresentInSquare(board,row,col,key):
    row_start = row - row % 3
    col_start = col - col % 3

    for i in range(row_start,row_start + 3):
        for j in range(col_start,col_start + 3):
            if board[i][j] == key and (i,j) != (row,col):
                return False

    return True
    
def solveSudoko(board):
    search_empty = findEmpty(board)
    if not search_empty: # if empty box not found
        # handling the base case 
        # print('Congrats, Sudoko successfully solved...!')
        # printBoard(board)
        return True
    else:
        row,col = search_empty # row and column of empty box   

    for i in range(1,10):
        a = notPresentInRow(board,row,col,i) 
        b = notPresentInCol(board,row,col,i)
        c = notPresentInSquare(board,row,col,i)

        if a and b and c:
            board[row][col] = i
            next = solveSudoko(board)

            # if my move is ok 
            if next:
                return True
            else: # if my move not found to be ok
                board[row][col] = 0 # unfill the current filled box and check for other possibilities

    return False

printBoard(board)
solveSudoko(board)
printBoard(board)




