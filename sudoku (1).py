
import os
import random
from abc import abstractclassmethod
from time import time, sleep
class sudoku:
    def __init__(self):# to initialize grid and initial grid (double array - size 9*9)
        self.__grid = [[0 for i in range(9)] for i in range(9)]
        self.__initgrid = [[0 for i in range(9)] for i in range(9)]
# setters and getters for grid and initial grid
    def getgrid(self):
        return self.__grid
    
    def getInitgrid(self):
        return self.__initgrid
    
    def setgrid(self, row, column, value):
        self.__grid[row][column] = value


    def setInitgrid(self, row, column, value):
        self.__initgrid[row][column] = value

    def setDifficulty(self, diff): # set difficulty level
        self.difficulty(diff) # call difficulty method then fill the gird according to difficulty level
        for i in range(9):
            for j in range(9):
                self.setgrid(i, j, self.__initgrid[i][j])


    def FillByFile(self, file):# method to read the grid from file
        input = open(file)
        lines = input.readlines()
        row_number = 0
        for rows in lines:# loop that read line by line(rows)
            row_elements = rows.replace('\n', '').split(',')
            print(row_elements)
            for i in range(9):#loop for each element from 0-9
                if len(row_elements) > i:
                    if row_elements[i] != '':
                        self.setgrid(row_number, i, int(row_elements[i]))
                        self.setInitgrid(row_number, i, int(row_elements[i]))
                else:# the element that does not exist is filled with a value of zero
                    self.setgrid(row_number, i, 0)
                    self.setInitgrid(row_number, i, 0)
            row_number+=1
    

    def valid_location(self, grid, row, col, number):# to check if the element valid or not
        if number < 0 or number > 9: # check if numbers between 1-9
            return False
        # check if the number exist before
        else:
            for value in grid[row]:
                if value == number:
                    return False
            for i in range(9):
                if grid[i][col] == number:
                    return False
            i = row//3
            j = col//3
            for row in range(i * 3, i * 3 + 3):
                for column in range (j * 3, j * 3 + 3):
                    if grid[row][column]==number:
                        return False
        return True

    def find_empty(self, grid): #this finds empty spaces.
        for i in range(len(grid)):
            for j in range(len(grid[0])):
              if grid[i][j] == 0:
                return (i, j) # row, then column of empty spaces.
        return (-1, -1)

    def display(self, grid): # to display the grid in special form
        for i in range(len(grid)):
            if i % 3 == 0:
                if i == 0:
                    print(" ┎─────────────────────────────┒")
                else:
                    print(" ┠─────────────────────────────┨")

            for j in range(len(grid[0])):
                if j % 3 == 0:
                    print(" ┃ ", end=" ")

                if j == 8:
                    print(grid[i][j], " ┃")
                else:
                    print(grid[i][j], end=" ")

        print(" ┖─────────────────────────────┚")

    
    def make(self):# make initial grid from method make_grid()
        self.__initgrid = self.make_grid()

    def make_grid(self, m=3):# made a random grid every time we call this method using backtraking algorithem
        """Return a random filled m**2 x m**2 Sudoku grid."""
        n = m**2
        grid = [[None for _ in range(n)] for _ in range(n)]
        def search(c=0):
            "Recursively search for a solution starting at position c."
            i, j = divmod(c, n)
            i0, j0 = i - i % m, j - j % m # Origin of mxm block
            numbers = list(range(1, n + 1))
            random.shuffle(numbers)
            for x in numbers:
                if (x not in grid[i]                     # row
                    and all(row[j] != x for row in grid) # column
                    and all(x not in row[j0:j0+m]         # block
                            for row in grid[i0:i])): 
                    grid[i][j] = x
                    if c + 1 >= n**2 or search(c + 1):
                        return grid
            else:
                # No number is valid in this cell: backtrack and try again.
                grid[i][j] = None
                return None
        return search()
    
    def solve(self, i=0, j=0): # solve the grid using backtracking algorithem
        i, j = self.find_empty(self.getInitgrid()) # to get the empty index in grid
        if i == -1:
            return True
        for e in range(1, 10): # to find the valid solution for empty index
            if self.valid_location(self.__initgrid,i, j, e):
                self.__initgrid[i][j] = e
                if self.solve(i, j):
                    return True
                self.__initgrid[i][j] = 0
        return False
    
    def solved(self, grid): # check if grid sloved or not
        for row in grid:
            for val in row: # if there index in grid that value =0 then the grid not solved
                if val == 0:
                    return False
        return True


    def get_hint(self):# to give hint for player by solve index in grid
        for row in range(9):
            for col in range(9):
                if self.getgrid()[row][col] == 0:
                    for i in range(1, 10):
                        if self.valid_location(self.getgrid(), row, col, i):
                            print("value "+str(i)+" in row: "+str(row)+" column: "+ str(col))
                            self.setgrid(row, col, i)
                            return True
        print("There is no hints for the empty slots.")# if there is no solution this sentence appears

    
    def difficulty(self, difficulty): # Depending on the level of difficulty a certain number of items are set to zero
        assert 0 < difficulty < 1, 'Difficulty must be between 0 and 1'
        for p in random.sample(range(81), int(81*difficulty)): # using sample method to get numbers from [1-81] , and choose how many numbers we need depend on the level of difficulty
            self.__initgrid[p//9][p%9] = 0
   # defintion of abstract method
    @abstractclassmethod
    def prompt(self):
        pass

    @abstractclassmethod
    def start(self):
        pass

    @abstractclassmethod
    def getScore(self):
        pass

class firstMode(sudoku):
    def __init__(self):
        self.__score = 0
        self.__t = 0
        self.__t1 = 0
        self.__t2 = 0
        super().__init__()
        if self.prompt(): # call the prompt method
            print("The game is starting, please wait.. ")
            sleep(2)
            os.system("cls") # clear the screen
            self.start() # call the start method
            self.__t2 = time() # Store the end time of the game
            self.__t = self.__t2-self.__t1 # Calculate the total time of the game
            total = self.getScore() # call the score method that return the score of player
            print("Your total score is: " + str(total))

    def prompt(self):# initilize the abstract method
        game = input("Do you want to load the game from file or generate a random (F, R)?\n>> ")
        try:# to check if game value is true
            assert(game == 'f' or game == 'F' or game == 'r' or game == 'R')
        except:
            while game != 'f' and game != 'F' and game != 'r' and game != 'R':
                game = input(">> ") # if the input from user not valid , then ask user again

        if game == 'f' or game == 'F':
            os.system("cls")# clear the screen
            file = input("File name\n>> ")# ask user to enter file name
            self.FillByFile(file)#call method(file by file) to insert the grid from this file
            return True
        else:
            
            os.system("cls")

            gameLevel = input("Choose difficulty level: \n1- Easy\n2- Medium\n3- Hard\n>> ")# ask user to choose difficulty level
            try:#to check if gamelevel value is true
                assert(gameLevel == '1' or gameLevel == '2' or gameLevel =='3')
            except:
                while gameLevel != '1' and gameLevel != '2' and gameLevel != 3:
                    gameLevel = input(">> ")# if the input from user not valid , then ask user again
            
            if gameLevel == '1':
                self.make()# call make method that make the grid
                self.setDifficulty(0.6) # set the difficulty level (easy)
                return True
            elif gameLevel == '2':
                self.make()
                self.setDifficulty(0.75)# set the difficulty level (medium)
                return True
            else:
                self.make()
                self.setDifficulty(0.9)# set the difficulty level (hard)
                return True
    
    def start(self):# initilize the abstract method
        self.__t1 = time()# store the start time of game
        while not self.solved(self.getgrid()):
            os.system("cls")
            print("Your Score number is: "+ str(self.__score))
            self.display(self.getgrid()) # display the grid
            answer = tuple(input("(row, column, number) ,(h) hint, (s) solve ,(q) quit\n>> ").replace(' ','').split(','))#ask the user to choose from this tuble
            try:
                assert len(answer) == 3 # that mean the user entered solution for any index in grid
                if self.valid_location(self.getgrid(),int(answer[0])-1,int(answer[1])-1,int(answer[2])) and self.getInitgrid()[int(answer[0])-1][int(answer[1])-1] == 0:#chek if the solution is valid
                    self.setgrid(int(answer[0])-1, int(answer[1])-1, int(answer[2])) # set the solution to grid
                    self.__score += 1 # increase the score of player
                else:
                    self.__score -= 2 # decrease the score of player if the solution not true
                    print("Wrong !!")
            except AssertionError:
                if answer[0] == 'h' or answer[0] == 'H':
                    if self.get_hint():# call hint method if the user enter hint option and decrease the score of player
                        self.__score -= 2
                elif answer[0] == 's' or answer[0] == 'S':
                    self.solve()# call slove method if the user enter solve option
                    print("Solution is: ")
                    self.display(self.getInitgrid()) # display the solution of grid
                    return 
                elif answer[0] == 'q' or answer[0] == 'Q': # quit the game if the user enter quit option
                    return
    # initilize the abstract method
    def getScore(self):# Calculate the score of player
        if self.__score <= 0:
            return 0
        else:
            time = 3600/self.__t
            score = self.__score/81
            return time * score

class secondMode(sudoku):
    def __init__(self):
        super().__init__()# initialize dictionary for 2 player then set them in list
        self.__player1Dict = { "name" : "Player 1" ,"score" : 0 , "total time" : 0 , "points" : 0}
        self.__player2Dict = { "name" : "Player 2" , "score" : 0 , "total time" : 0 , "points" : 0}
        self.players = [self.__player1Dict, self.__player2Dict]
        if self.prompt():
            print("Game is starting, please wait")
            sleep(2)
            self.start() # call start method to start the game
          # store the score of 2 player using getScore method
            self.players[0]["score"] , self.players[1]["score"] = self.getScore(self.players[0]["points"], self.players[1]["points"], self.players[0]["total time"], self.players[1]["total time"])

            for i in self.players:
                print(str(i["name"])+" score is: "+ str(i["score"]))# print name and score for each player

    def prompt(self):# initilize the abstract method
        game = input("Do you want to load the game from file or generate a random (F, R)?\n>> ")
        try:# to check if game value is true
            assert(game == 'f' or game == 'F' or game == 'r' or game == 'R')
        except:
            while game != 'f' and game != 'F' and game != 'r' and game != 'R':
                game = input(">> ")# if the input from user not valid , then ask user again

        if game == 'f' or game == 'F':
            os.system("cls")# clear the screen
            file = input("File name\n>> ")# ask user to enter file name
            self.FillByFile(file)#call method(file by file) to insert the grid from this file
            return True
        else:
            self.make()
            os.system("cls")
            gameLevel = input("Choose difficulty level: \n1- Easy\n2- Medium\n3- Hard\n>> ")
            try:#to check if gamelevel value is true
                assert(gameLevel == '1' or gameLevel == '2' or gameLevel =='3')
            except:
                while gameLevel != '1' and gameLevel != '2' and gameLevel != 3:
                    gameLevel = input(">> ")# if the input from user not valid , then ask user again
            
            if gameLevel == '1':
                self.make()# call make method that make the grid
                self.setDifficulty(0.6)# set the difficulty level (easy)
                return True
            elif gameLevel == '2':
                self.make()
                self.setDifficulty(0.75)# set the difficulty level (medium)
                return True
            else:
                self.make()
                self.setDifficulty(0.9)# set the difficulty level (hard)
                return True
    
    def start(self):# initilize the abstract method
        self.player = 0 # This element was used to turn roles
        numberofPasses = 0 # store number of passes that user used
        while not self.solved(self.getgrid()):
            t1 = time()#store the start time of game
            os.system("cls")
            self.display(self.getgrid())# display the grid
            print(str(self.players[self.player]["name"]) +", Your Score number is: "+ str(self.players[self.player]['points']))# to display the active player and his score
            answer = tuple(input("(row, column, number) ,(p) pass, (s) solve ,(q) quit\n>> ").replace(' ','').split(','))#ask the user to choose from this tuble
            try:
                assert len(answer) == 3 # that mean the user entered solution for any index in grid
                if self.valid_location(self.getgrid(),int(answer[0])-1,int(answer[1])-1,int(answer[2])) and self.getInitgrid()[int(answer[0])-1][int(answer[1])-1] == 0:#chek if the solution is valid
                    numberofPasses = 0
                    self.setgrid(int(answer[0])-1, int(answer[1])-1, int(answer[2]))# set the solution of grid
                    self.players[self.player]['points'] += 1# increase the score of active player
                else:
                    self.players[self.player]['points'] -= 2# decrease the points of active player if the solution not true
                    print("Wrong !!")
            except AssertionError:
                if answer[0] == 'p' or answer[0] == 'p':
                    numberofPasses+=1 # turn the roles and increase the number of passes by 1
                    self.players[self.player]['points'] -= 1 # decrease the points of player that pass there role
                    if numberofPasses == 4: # if number of passes = 4 , then give hint to player
                        numberofPasses = 0
                        self.get_hint()# call hint method
                elif answer[0] == 's' or answer[0] == 'S':
                    numberofPasses = 0
                    self.solve()# call slove method if the user enter solve option
                    print("Solution is: ")
                    self.display(self.getInitgrid())# display the solution of grid
                    return 
                elif answer[0] == 'q' or answer[0] == 'Q':# quit the game if the user enter quit option
                    numberofPasses = 0
                    return
            self.players[self.player]['total time'] += (time()-t1)# calculate the total time for game for active player
            self.player = not self.player# turn the roles

    # initilize the abstract method
    def getScore(self, p1, p2, tp1, tp2):# Calculate the score of player
        if p1 < 0 and p2 < 0:
            return (0, 0)
        elif p1 > 0 and p2 < 0:
            score1 = p1/81
            score1 *= ((tp1 + tp2)/tp1)
            return (score1 , 0)
        elif p2 > 0 and p1 < 0:
            score2 = p2/81
            score2 *= ((tp1 + tp2)/tp2)
            return (0 , score2)
        else:
            score1 = p1/81
            score1 *= ((tp1+tp2)/tp1)
            score2 = p2/81
            score2 *= ((tp1 + tp2)/tp2)
            return (score1, score2)
        
if __name__ == "__main__":

    while 1:
        print("--- Wellcome to the sudoku game ---")
        print("What is your mode ? \n1- one palyer mode \n2- two players mode")# ask user to choose mode of game;1 player or 2 player
        mode = input(">> ")
        try:
            assert(mode == '1' or mode == '2')
        except:
            while mode != '1' and mode != '2':
                mode = input(">> ")# # if the input from user not valid , then ask user again
        
        if mode == '1':# this mean 1 player
            os.system("cls")
            start_game = firstMode() # creat an object from class firstmode()
        else:
            os.system("cls")
            start_game = secondMode()# creat an object from class firstmode()

        del start_game # delete the object after end each game

        choice = input("Do you want to play again? (Y, N) ")# ask the user if he want to play onther game
        if choice != 'Y' and choice != 'y':
            exit("Thank you for playing sudoku, good bye")
