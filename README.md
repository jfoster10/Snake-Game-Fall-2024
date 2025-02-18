# Snake-Game-Fall-2024
A simple snake game. Initial template by Alyssa Kubota. Snake functionality, AI, and various customizations by Zeke Foster (me).

There are several directories with different purposes in this project:
-boardCell.py contains the BoardCell class, which creates a single cell block on the screen.

-boardDisplay.py updates the screen with every single BoardCell. This includes empty cells, food cells, and cells containing part of the snake's body.

-gameData.py contains all of the data related to the operations of the game, whether it includes methods related to adding food, placing and modifying the position and direction of the snake's movement, as well as recognizing when the game is over.
      
-controller.py uses the class from gameData.py and gives the player a way to play the game through user controls. It also contains methods for how the snake interacts with the game in AI mode, which can be activated using the 'A' key. 
(Note: controller.py is the script you must run to play the game.)

-preferences.py is a smaller script which contains many different custom settings such as the game speed, colors of tiles, etc. I personally integrated my own randomized color palettes for the background and the snake, while also adjusting the game speed to increase when food cells are eaten.
