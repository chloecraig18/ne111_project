# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 13:52:02 2021

@author: Chloe
"""
## Erika Bechtel-Becker - EB
## Chloe Craig - CC
## Gaty Kazimi - GK
import pygame
# Reversegam general gameplay: placing an x or o changes your opponent's tiles that lie between the new places x or o and any other to your tile. 
# The game ends when the board is full or a player cannot make a move that flips any tiles. The winner is the player with more of their tiles CC
import random
import sys
#Board is 8 by 8 CC
WIDTH = 8 
HEIGHT = 8 

def drawBoard(board):                                                    ## print board of given width and height with coordinate values on all sides CC
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print('%s|' % (y+1), end='')
        for x in range(WIDTH):
            print(board[x][y], end='')
        print('|%s' % (y+1))
    print(' +--------+')
    print('  12345678')

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
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1],      ## returning which tiles to flip
           [0, -1], [-1, -1], [-1, 0], [-1, 1]]:                         ## iterate over all of the possible directions on the board, think NE100 2D direction vectors CC
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

def whoGoesFirst():                                                     ## function that decides which player starts first in the game 
                                                                        ## system that either selects 1 or 0 as a method of randomly choosing who goes first
    if random.randint(0, 1) == 0:                                       ## using the sub module random to create condition if the random integer returned is equal to 0 
        return 'computer'                                               ## returns string indicating that the computer starts first 
    else:                                                               ## 
        return 'player'                                                 ##

def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart and flip any of the opponent's pieces.
    # Return False if this is an invalid move; True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    # Make a duplicate of the board list and return it.
    boardCopy = getNewBoard()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]

    return boardCopy

def isOnCorner(x, y):
    # Return True if the position is in one of the four corners.
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)

def getPlayerMove(board, playerTile):
    # Let the player enter their move.
    # Return the move as [x, y] (or return the strings 'hints' or
           #'quit').
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, "quit" to end the game, or "hints" to toggle hints.')
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Enter the column (1-8) and then the row (1-8).')
            print('For example, 81 will move on the top-right corner.')

    return [x, y]

def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as an [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves) # Randomize the order of the moves.
    
    # Always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Find the highest-scoring move possible.
    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('You: %s points. Computer: %s points.' % (scores[playerTile],scores[computerTile]))

def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    # Clear the board and place starting pieces.
    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)

        if playerValidMoves == [] and computerValidMoves == []:
            return board # No one can move, so end the game.

        elif turn == 'player': # Player's turn
            if playerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board, playerTile, computerTile)

                move = getPlayerMove(board, playerTile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit() # Terminate the program.
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, playerTile, move[0], move[1])
            turn = 'computer'

        elif turn == 'computer': # Computer's turn
            if computerValidMoves != []:
                drawBoard(board)
                printScore(board, playerTile, computerTile)

                input('Press Enter to see the computer\'s move.')
                move = getComputerMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            turn = 'player'



print('Welcome to Reversegam!')

playerTile, computerTile = enterPlayerTile()

while True:
    finalBoard = playGame(playerTile, computerTile)

    # Display the final score.
    drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('X scored %s points. O scored %s points.' % (scores['X'],
           scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tie!')
        
    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        break
