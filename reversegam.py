## Erika Bechtel-Becker - EB
## Chloe Craig - CC
## Gaty Kazimi - GK
import pygame
# Reversegam general gameplay: placing an x or o changes your opponent's tiles that lie between the new places x or o and any other to your tile. 
# The game ends when the board is full or a player cannot make a move that flips any tiles. The winner is the player with more of their tiles CC
import random
import sys
#Board is 8 by 8 CC
def sizeBoard(h,w):
    print("How large would you like the board to be?")
    while(h != "6" or h != "8"):
        h = (input("Enter '6' for 6x6 or '8' for 8x8: "))
        print(h)
        if (h == "6" or h == "8"):
            break
        else:
            print("Please enter a valid response")
            
    h = int(h)
    w = h*2
    return(h,w)

h = 0
w = 0
(h,w) = sizeBoard(h,w)
HEIGHT = h
WIDTH = w

def drawBoard(board):                                                    ## print board of given width and height with coordinate values on all sides CC
    if (HEIGHT == 8):
        print('  1 2 3 4 5 6 7 8')
        print(' +---------------+')
        for y in range(HEIGHT):
            print('%s|' % (y+1), end='')
            for x in range(WIDTH):
                print(board[x][y], end='')
            print('|%s' % (y+1))
        print(' +---------------+')
        print('  1 2 3 4 5 6 7 8')
    elif (HEIGHT == 6):
        print('  1 2 3 4 5 6')
        print(' +-----------+')
        for y in range(HEIGHT):
            print('%s|' % (y+1), end='')
            for x in range(WIDTH):
                print(board[x][y], end='')
            print('|%s' % (y+1))
        print(' +-----------+')
        print('  1 2 3 4 5 6')

def getNewBoard():                                                       ##prints new board with spaces in all spots CC
    board = []                                                           ##defining board as empty collection
    for i in range(WIDTH):                                               ## WHY WIDTH AND NOT HEIGHT??
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])           ## adding a new row for either iteration
    return board                                                         ##


def isValidMove(board, tile, xstart, ystart):                            ## Returns false if move is invalid, returns the list of tiles to be flipped if valid CC  
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):    ## xstart, ystart is the player's move, tile is what the player chose to be i.e. the tile not to flip CC 
        return False                                                     ## if there is already an X or O in the spot OR if it is not on the board at all, return False CC
    if tile == 'X':                                                      ##
        otherTile = 'O'                                                  ## Defines 'othertile' as the tile the player is NOT playing as CC
    else:                                                                ##
        otherTile = 'X'                                                  ##
    tilesToFlip = []                                                     ##
    for xdirection, ydirection in [[0, 1], [2, 1], [2, 0], [2, -1],      ## returning which tiles to flip
           [0, -1], [-2, -1], [-2, 0], [-2, 1]]:                         ## iterate over all of the possible directions on the board, think NE100 2D direction vectors CC
        x, y = xstart, ystart                                            ## defining varibles x and y as the x and y the player input CC
        x += xdirection                                                  ## redefine x and y as the coordinates once you move a specific direction CC
        y += ydirection                                                  ## ex. the player input x=5 and y=5 and we were on [1, -1], it would be redefined as x = 6 and y = 4 CC
        while isOnBoard(x, y) and board[x][y] == otherTile:              ## while the xy coordinates are on the board the value at them is NOT the player's tile CC
            x += xdirection                                              ## we're going to flip that tile but keep moving until we hit the player's tile CC
            y += ydirection                                              ##
            if isOnBoard(x, y) and board[x][y] == tile:                  ## this is when we hit the player's tile i.e. the end of where we're flipping tiles CC    
                while True:                                              ##
                    x -= xdirection                                      ## go back in the opposite direction by subtracting the direction vector values CC
                    y -= ydirection                                      ## until you hit the space the player entered CC
                    if x == xstart and y == ystart:                      ##
                        break                                            ##
                    tilesToFlip.append([x, y])                           ## add the coordinates of each tile that needs to be flipped to the tilesToFlip collection CC
                                                                         ##
    if len(tilesToFlip) == 0:                                            ## means no tiles were flipped in any direction so this is not a valid move CC
        return False                                                     ##
    return tilesToFlip                                                   ## move was valid, return the list of coordinates of tiles that will be flipped CC


def isOnBoard(x, y):
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1     ## returns True if the coordinates the player enters are actually on the board CC 
      
    
def getBoardWithValidMoves(board, tile):                                ## returns version of board with periods in place of all valid moves for given tile CC
    boardCopy = getBoardCopy(board)                                     ## sets boardcopy as an a copy of the game board CC
                                                                        ##
    for x, y in getValidMoves(boardCopy, tile):                         ## for each xy pair deemed as a valid move, change the entry there to a period CC
        boardCopy[x][y] = '.'                                           ##
    return boardCopy                                                    ## return the new board with periods in the spots of valid moves CC


def getValidMoves(board, tile):                                         ## returns list of x,y coordinates that are valid moves for the given tile on the board at the time CC
    validMoves = []                                                     ##
    for x in range(WIDTH):                                              ##
        for y in range(HEIGHT):                                         ## check at every x,y spot
            if isValidMove(board, tile, x, y) != False:                 ## when isValidMove does not return False i.e. the move at that x,y pair is valid
                validMoves.append([x, y])                               ## add those coordinates to the validMoves collection
    return validMoves
 
    
def getScoreOfBoard(board):                                             ## finds score of game by counting Xs and Os 
    xscore = 0                                                          ## initializing both scores as 0
    oscore = 0                                                          ##
    for x in range(WIDTH):                                              ## check at every coordinate on board for Xs and Os
        for y in range(HEIGHT):                                         ##
            if board[x][y] == 'X':                                      ## for each X it finds
                xscore += 1                                             ## add one to the score of X
            if board[x][y] == 'O':                                      ## for each O it finds
                oscore += 1                                             ## add one to the score of O
    return {'X':xscore, 'O':oscore}                                     ## returns a dictionary with X being the key for xscore and O for oscore
 
def enterPlayerTile():                                                  ## function that prompts player to input desired name EB
                                                                        ## Let the player enter which tile they want to be computer's tile as the second
                                                                        ## 
    tile = ''                                                           ## assign the variable "tile" to be a string  
    while not (tile == 'X' or tile == 'O'):                             ## ensure that the condition that the player is not using the X or O tile is met
        print('Do you want to be X or O?')                              ## prompt player to choose a tile to play with
        tile = input().upper()                                          ## assigns an initial location to the tile to the upper side of the board 

                                                                        ## The first element in the list is the player's tile, and the second is the computer's tile 
                                                                        
    if tile == 'X':                                                     ## condition if the tile chosen is X   EB
        return ['X', 'O']                                               ## return chosen tile (X) first in a list              
    else:                                                               ## condition if tile chosen is not X
        return ['O', 'X']                                               ## return other tile (O) before X in a list   

def whoGoesFirst():                                                     ## function that decides which player starts first in the game EB
                                                                        ## system that either selects 1 or 0 as a method of randomly choosing who goes first
    if random.randint(0, 1) == 0:                                       ## using the sub module random to create condition if the random integer returned is equal to 0 
        return 'computer'                                               ## returns string indicating that the computer starts first 
    else:                                                               ## 
        return 'player'                                                 ## returns string indicating that the player starts first 

def makeMove(board, tile, xstart, ystart):                              ## function that allows player to move tile on board EB
                                                                        ## Place the tile on the board at xstart, ystart and flip any of the opponent's pieces.
                                                                        ## Return False if this is an invalid move; True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)              ## assigns list of coordinates where tiles are flipped to a previous function that ensures player's move is valid 
                                                                        ##
    if tilesToFlip == False:                                            ## if there are no tiles to flip (isValidMove returns False), function returns False
        return False                                                    ## 
                                                                        ##
    board[xstart][ystart] = tile                                        ## temporarily setting player's tile on the board 
    for x, y in tilesToFlip:                                            ## for loop 
        board[x][y] = tile                                              ## places tile on board for "x" and "y" coordinates in list of flipped tiles   
    return True                                                         ## True if "x" and "y" can be flipped                

def getBoardCopy(board):                                                ## Make a duplicate of the board list and return it EB
    boardCopy = getNewBoard()                                           ## assign variable to make a new board to the function of obtaining a new board 
                                                                        ##
    for x in range(WIDTH):                                              ## for loop of "x" when in the sequence of integers found in the WIDTH 
        for y in range(HEIGHT):                                         ## for loop of "y" when in the sequence of integers found in the HEIGHT, given "x" is in WIDTH
            boardCopy[x][y] = board[x][y]                               ## given both conditions are upheld, creates a copy of board 
                                                                        ##
    return boardCopy                                                    ## returns the copy of the board 

def isOnCorner(x, y):                                                   ## function if tile is on a corner of the board EB
                                                                        ## Return True if the position is in one of the four corners
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)   ## 

def getPlayerMove(board, playerTile):                                   ## function to prompt player to move
     if h == 6:                                                         ##
        DIGITS = '1 2 3 4 5 6'.split()                                  ## Assigns correct list to DIGITS depending on size of board input
     elif h == 8:                                                       ## 
        DIGITS = '1 2 3 4 5 6 7 8'.split()                              ##               
     while True:                                                        ##
        print('Enter your move, "quit" to end the game, "instructions" to see game instructions, or "hints" to toggle hints.')
        move = input().lower()                                          ## Let the player enter their move.
        if move == 'quit' or move == 'hints' or move == 'instructions': ## Return the move as [x, y] (or return the strings 'hints', 'instruction' or 'quit')
            return move                                                 ##
                                                                        ##
        if len(move) == 2 and move[0] in DIGITS and move[1] in DIGITS:  ## Check that the move that's entered is a valid form of input
            x = (int(move[0])*2) - 2                                    ## Assign input to x and y coordinates coresponding to 
            y = int(move[1]) - 1                                        ##
            if isValidMove(board, playerTile, x, y) == False:           ##
                continue                                                ##
            else:                                                       ##
                break                                                   ## Break while loop once move is confirmed valid, which stops game from asking for move again
        else:                                                           ##
            print('That is not a valid move. Enter the column (1-' + str(HEIGHT) + ') and then the row (1-' + str(h) + ').')
            print('For example, ' + str(HEIGHT) + '1 will move on the top-right corner.')
                                                                        ## Print message if move entered in invalid
     return [x, y]                                                      ##

def getComputerMove(board, computerTile):                               ## This function creates an algorithm for the computer's moves GK
                                                                        ## Given a board and the computer's tile, determine where to         
                                                                        ## move and return that move as an [x, y] list.                      
    possibleMoves = getValidMoves(board, computerTile)                  ## Find all possible move the computer can make
    random.shuffle(possibleMoves)                                       ## Randomize the order of the moves.   
                                                                        ##
                                                                        ## Always go for a corner if available.
    for x, y in possibleMoves:                                         
        if isOnCorner(x, y):                                               
            return [x, y]

                                                                        ## Find the highest-scoring move possible.
    bestScore = -1                                                      ##             
    for x, y in possibleMoves:                                          ##
        boardCopy = getBoardCopy(board)                                 ## Make a copy of the board and make moves there to determine
        makeMove(boardCopy, computerTile, x, y)                         ## which move will give the highest score
        score = getScoreOfBoard(boardCopy)[computerTile]                ##
        if score > bestScore:                                           ##
            bestMove = [x, y]                                           ##
            bestScore = score                                           ## Loop until all possible moves are played on the copy of the board
    return bestMove                                                     ## and the best move is found
                              
def printScore(board, playerTile, computerTile):                        ## Function to output the total scores
    scores = getScoreOfBoard(board)
    print('You: %s points. Computer: %s points.' % (scores[playerTile],scores[computerTile]))

def playGame(playerTile, computerTile):                                 ## Function for playing the game and putting all the previous functions toegther
    showHints = False
    turn = whoGoesFirst()                                               ## Use WhoGoesFirst() function
    print('The ' + turn + ' will go first.')                            
    print('')
                                                                        ## Clear the board and place starting pieces.
    board = getNewBoard()                                               ## Display the starting board using getNewBoard() function
    board[HEIGHT-2][HEIGHT//2 - 1] = 'X'
    board[HEIGHT-2][HEIGHT//2] = 'O'
    board[HEIGHT][HEIGHT//2 - 1] = 'O'
    board[HEIGHT][HEIGHT//2] = 'X'

    while True:                                                         ## Main loop for running the turns between the player and the computer
        playerValidMoves = getValidMoves(board, playerTile)             ## Gets a list of valid moves both the player and the computer can make
        computerValidMoves = getValidMoves(board, computerTile)

        if playerValidMoves == [] and computerValidMoves == []:
            return board # No one can move, so end the game.
        
        elif turn == 'player': # Player's turn                          
            if playerValidMoves != []:
                if showHints:                                           ## Show hints to the player if Hints mode is on
                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board, playerTile, computerTile)

                move = getPlayerMove(board, playerTile)
                if move == 'quit':                                      ## If the player quits the game, then end the program
                    print('Thanks for playing!')
                    sys.exit() # Terminate the program.
                elif move == 'hints':                                   ## If the player turns on Hints mode
                    showHints = not showHints
                    continue
                elif move == 'instructions':
                    game_instructions()
                    continue 
                else:
                    makeMove(board, playerTile, move[0], move[1])       ## Player makes the move
            else:
                print("You cannot play any moves, so the turn goes to the computer")
                print("")
            turn = 'computer'                                           ## Change the turn to the computer

        elif turn == 'computer': # Computer's turn
            if computerValidMoves != []:
                drawBoard(board)
                printScore(board, playerTile, computerTile)             ## Use the algorithm to get the computer's move

                input('Press Enter to see the computer\'s move.')       ## Output the computer's move
                move = getComputerMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            else:
                print("The computer cannot play any moves, so the turn goes to you")
                print("")
            turn = 'player'                                             ## Change the turn to the player

def game_instructions():                                                ## Runs at beginning of game and can be called at any point in game as a turn
        inst = input("Would you like to see the game instructions? Type Y/N for yes/no \n")
        if inst == "Y" or inst == "y" or inst == "Yes" or inst == "yes":
            print("Reversegam has a square board and two types of tiles, X and O. Each player starts with two tiles in the centre of the board.")
            print("For each turn, the player places a new tile by inputting the coordinates of the space they would like to play on.")
            print("For example if the player would like to play on the 4th column of the 1st row, the player would enter 41.")
            print("Once a tile is played, all of the opposing player's tiles that lie between the new tile and any of the current player's other tiles (including along diagonals) are changed.")
            print("For example, if an X is played, all O's that lie directly between the new X and any other X are changed to X's.")
            print("The players take turns until either the board is full or a player cannot make a move that changes any other tiles.")
            print("The player with the most tiles on the board wins. Good luck!")
            print("")

## MAIN PROGRAM
print('Welcome to Reversegam!')
game_instructions()

playerTile, computerTile = enterPlayerTile()                            ## Use the enterPlayerTile() function to determine both the player's 
                                                                        ## and computer's tiles
while True:
    finalBoard = playGame(playerTile, computerTile)                     ## Use the playGame function to get the final board

    # Display the final score.
    drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)                                ## Find the final score
    print('X scored %s points. O scored %s points.' % (scores['X'],
           scores['O']))
    print("")
    if scores[playerTile] > scores[computerTile]:                       ## Determine the winner of the game by finding who has the bigger score
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tie!')                                    ## If the scores are the same
        
    print('Do you want to play again? (yes or no)')                     ## Loops if player chooses 'yes'
    if not input().lower().startswith('y'):
        print ("Thank you for playing!")
        break
