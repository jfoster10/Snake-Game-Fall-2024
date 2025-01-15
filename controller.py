"""
Author: Prof. Alyssa
The Controller of the game, including handling key presses
(and AI in the next assignment). You will update this file.

Adapted from HMC CS60

Updated by: Zeke Foster
Date: 11/13/24
Finished methods: 
    -advanceSnake()
    -CheckKeypress()

Date: 11/18/24
Finished methods:
    -unlabelHead()
    -reverseBody()
    -relabelHead()
    -redirectSnake()

Date: 12/2/24
Updated methods:
    -CheckKeypress(): Prevented key presses from killing the snake instantly
    -AdvanceSnake(): When food is eaten, the snake changes to a random color and the game speed inreases to 1.05 times the previous speed.

Date: 12/4/24
Finished methods:
    -getNextCellFromBFS()
    -getFirstCellInPath(foodCell)
    -manhattan(a, b)
"""

from preferences import Preferences
from gameData import GameData
from boardDisplay import BoardDisplay

import pygame
from enum import Enum
from queue import Queue
import random

class Controller():
    def __init__(self):
        # The current state of the board
        self.__data = GameData()
        # The display
        self.__display = BoardDisplay()
        # How many frames have passed
        self.__numCycles = 0

        # Attempt to load any sounds and images
        try:
            pygame.mixer.init()
            self.__audioEat = pygame.mixer.Sound(Preferences.EAT_SOUND)
            self.__display.headImage = pygame.image.load(Preferences.HEAD_IMAGE)
        except:
            print("Problem error loading audio / images")
            self.__audioEat = None

        # Initialize the board for a new game
        self.startNewGame()
        
    def startNewGame(self):
        """ Initializes the board for a new game """

        # Place the snake on the board
        self.__data.placeSnakeAtStartLocation()

    def gameOver(self):
        """ Indicate that the player has lost """
        self.__data.setGameOver()

    def run(self):
        """ The main loop of the game """

        # Keep track of the time that's passed in the game 
        clock = pygame.time.Clock()

        # Loop until the game ends
        while not self.__data.getGameOver():
            # Run the main behavior
            self.cycle() 
            # Sleep
            clock.tick(Preferences.SLEEP_TIME)

    def cycle(self):
        """ The main behavior of each time step """

        # Check for user input
        self.checkKeypress()
        # Update the snake state
        self.updateSnake()
        # Update the food state
        self.updateFood()
        # Increment the number of cycles
        self.__numCycles += 1
        # Update the display based on the new state
        self.__display.updateGraphics(self.__data)

    def checkKeypress(self):
        """ Update the game based on user input """
        # Check for keyboard input
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT:
                self.gameOver()
            # Change the snake's direction based on the keypress
            elif event.type == pygame.KEYDOWN:
                # Reverse direction of snake
                if event.key in self.Keypress.REVERSE.value:
                    self.reverseSnake()
                # Enter AI mode
                elif event.key in self.Keypress.AI.value:
                    self.__data.setAIMode()
                # Change directions
                    
                # Change the direction of the snake based on keyboard inputs.
                elif event.key in self.Keypress.UP.value:
                    if self.__data.getHeadNorthNeighbor()!= self.__data.getSnakeNeck():
                        self.__data.setDirectionNorth()
                elif event.key in self.Keypress.DOWN.value:
                    if self.__data.getHeadSouthNeighbor()!= self.__data.getSnakeNeck():
                        self.__data.setDirectionSouth()
                elif event.key in self.Keypress.RIGHT.value:
                    if self.__data.getHeadEastNeighbor()!= self.__data.getSnakeNeck():
                        self.__data.setDirectionEast()
                elif event.key in self.Keypress.LEFT.value:
                    if self.__data.getHeadWestNeighbor()!= self.__data.getSnakeNeck():
                        self.__data.setDirectionWest()

    def updateSnake(self):
        """ Move the snake forward one step, either in the current 
            direction, or as directed by the AI """

        # Move the snake once every REFRESH_RATE cycles
        if self.__numCycles % Preferences.REFRESH_RATE == 0:
            # Find the next place the snake should move
            if self.__data.inAIMode():
                nextCell = self.getNextCellFromBFS()
            else:
                nextCell = self.__data.getNextCellInDir()
            try:
                # Move the snake to the next cell
                self.advanceSnake(nextCell)
            except:
                print("Failed to advance snake")

    def advanceSnake(self, nextCell):
        """ Update the state of the world to move the snake's head to the given cell """

        # If we run into a wall or the snake, it's game over
        if nextCell.isWall() or nextCell.isBody():
            self.gameOver()
        
        # If we eat food, update the state of the board
        elif nextCell.isFood():
            self.playSound_eat()
            # Tell __data that we ate food! (The snake eats the food and grows in size)
            self.__data.becomeBody(self.__data.getSnakeHead())
            self.__data.becomeHead(nextCell)

            #Update the speed of the game upon eating the food
            Preferences.SLEEP_TIME *= 1.05

            #Update the color of the snake upon eating the food, to a random color, without repetitions.
            self.storageUnit = Preferences.RANDOM_CHOICE
            Preferences.RANDOM_CHOICE = random.choice(Preferences.SNAKE_LIST)
            Preferences.COLOR_HEAD = pygame.Color(Preferences.RANDOM_CHOICE[1])
            Preferences.COLOR_BODY = pygame.Color(Preferences.RANDOM_CHOICE[0])
            Preferences.SNAKE_LIST.append(self.storageUnit)
            Preferences.SNAKE_LIST.remove(Preferences.RANDOM_CHOICE)

            #Remove the food from the list if it was eaten
            self.__data.getFood().remove(nextCell)
            

            

        # If the next space is empty, the snake moves forwards without growing.
        else:
            self.__data.becomeBody(self.__data.getSnakeHead())
            self.__data.becomeHead(nextCell)
            self.__data.becomeEmpty(self.__data.getSnakeTail())

    def updateFood(self):
        """ Add food every FOOD_ADD_RATE cycles or if there is no food """
        if self.__data.noFood() or (self.__numCycles % Preferences.FOOD_ADD_RATE == 0):
            self.__data.addFood()

    def getNextCellFromBFS(self):
        """ Searches for the food closest to the head of the snake.
            Returns the *next* step the snake should take to get closer 
            to the closest food cell. """
        
        # Parepare all the tiles to search
        #self.__data.resetCellsForSearch()

        # Initialize a queue to hold the tiles to search
        #cellsToSearch = Queue()

        # Add the head to the queue and mark it as added
        #head = self.__data.getSnakeHead()
        #head.setAddedToSearchList()
        #cellsToSearch.put(head)

        # Search!
        # TODO implement BFS here (I didn't do this)



        """NOTE: I AM USING A DIFFERENT METHOD FOR SEARCH."""

        #Initialize an empty list for food distances
        __distanceList = []

        #Initialize variables for the snake head's row and column
        head = self.__data.getSnakeHead()
        HeadA = self.__data.getSnakeHead().getRow()
        HeadB = self.__data.getSnakeHead().getCol()

        #A for loop which checks the whole list of food spaces in gameData
        for i in range(0, len(self.__data.getFood())):
    
            #Get the row and column of the current food space
            FoodA = self.__data.getFood()[i].getRow()
            FoodB = self.__data.getFood()[i].getCol()

            # Take the Manhattan distance between the snake head and the current food space,
            # and insert that distance, as well as the current food's row and column, into the distanceList.
            __distanceList.append([self.manhattan([HeadA, HeadB], [FoodA, FoodB]), FoodA, FoodB])
    
        #Sort the distanceList by the first index (the distance)
        __distanceList.sort()

        #If there is food, call getFirstCellInPath, with the closest food as an input.
        if __distanceList != []:
            nextCell = self.getFirstCellInPath(__distanceList[0])

        #If there is no food, move the snake in an acceptable direction (hopefully)...
        else:
            if self.__data.getNorthNeighbor(head) == self.__data.getSnakeNeck():
                    nextCell = self.__data.getHeadSouthNeighbor()
            elif self.__data.getSouthNeighbor(head) == self.__data.getSnakeNeck():
                nextCell = self.__data.getHeadNorthNeighbor()
            elif self.__data.getEastNeighbor(head) == self.__data.getSnakeNeck():
                nextCell = self.__data.getWestNeighbor()
            elif self.__data.getWestNeighbor(head) == self.__data.getSnakeNeck():
                nextCell = self.__data.getHeadEastNeighbor()


        return nextCell

    # Add any other helper functions you might want here

    def manhattan(self, a, b):
        """Returns the manhattan distance between two lists. Inputs: a (list) and b (list)"""

        return sum(abs(val1-val2) for val1, val2 in zip(a,b))

    
    
    def getFirstCellInPath(self, foodCell):
        """ A helper function to find the next space the snake should move when in AI mode.
            Inputs: foodCell (the closest food cell to the snake)
            Returns: the next space the snake should move to """

        head = self.__data.getSnakeHead()

        nextCell = None

        if head != foodCell:
            #If there isn't a space, there isn't a solution.
            if head == None:
                return None
            
            # If the space up/down/left/right from the snake's head is available, 
            # then: If the food cell is up/down/left/right, determine the next cell accordingly.
            if self.__data.getHeadSouthNeighbor().isBody() == False:
                if foodCell[1] > head.getRow():
                    nextCell = self.__data.getHeadSouthNeighbor()
            if self.__data.getHeadNorthNeighbor().isBody() == False:
                if foodCell[1] < head.getRow():
                    nextCell = self.__data.getHeadNorthNeighbor()
            if self.__data.getHeadEastNeighbor().isBody() == False:
                if foodCell[2] > head.getCol():
                    nextCell = self.__data.getHeadEastNeighbor()
            if self.__data.getHeadWestNeighbor().isBody() == False:
                if foodCell[2] < head.getCol():
                    nextCell = self.__data.getHeadWestNeighbor()

            #If there is still not a next cell chosen (there may not be food)
            if nextCell == None:

                #Move the snake anywhere which is acceptable (away from its body)
                if self.__data.getNorthNeighbor(head) == self.__data.getSnakeNeck():
                    nextCell = self.__data.getHeadSouthNeighbor()
                if self.__data.getSouthNeighbor(head) == self.__data.getSnakeNeck():
                    nextCell = self.__data.getHeadNorthNeighbor()
                if self.__data.getEastNeighbor(head) == self.__data.getSnakeNeck():
                    nextCell = self.__data.getWestNeighbor()
                if self.__data.getWestNeighbor(head) == self.__data.getSnakeNeck():
                    nextCell = self.__data.getHeadEastNeighbor()

        return nextCell
    
    def reverseSnake(self):
        """ Reverses the snake such that the head is on the opposite side of its body. 
            Inputs: None
            Returns: None
        """
        self.__data.unlabelHead()
        self.__data.reverseBody()
        self.__data.relabelHead()
        self.__data.redirectSnake()
        


    def playSound_eat(self):
        """ Plays an eating sound """
        if self.__audioEat:
            pygame.mixer.Sound.play(self.__audioEat)
            pygame.mixer.music.stop()

    class Keypress(Enum):
        """ An enumeration (enum) defining the valid keyboard inputs 
            to ensure that we do not accidentally assign an invalid value.
        """
        UP = pygame.K_i, pygame.K_UP        # i and up arrow key
        DOWN = pygame.K_k, pygame.K_DOWN    # k and down arrow key
        LEFT = pygame.K_j, pygame.K_LEFT    # j and left arrow key
        RIGHT = pygame.K_l, pygame.K_RIGHT  # l and right arrow key
        REVERSE = pygame.K_r,               # r
        AI = pygame.K_a,                    # a


if __name__ == "__main__":
    Controller().run()