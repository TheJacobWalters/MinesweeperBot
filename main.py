'''
id = "row_column" I would expect it to be "column_row"
1_1  -  1_30  
 |       |
16_1 - 16_30

Notes
am going to have a list of class instances not going to have
multiple lists like lists of squares that have 1 lists of squares that 
have 2

need to change list to dictionary
'''

''' Expert Mode settings '''
#width = 30
#height = 16

''' begginer mode settings '''
width = 9
height = 9

class square:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.label = 'square blank'
        self.id = f"{self.row}_{self.column}"
        self.isHintSquare = False
        self.isFlagged = False
        self.isBlank = True
        self.touchingSquares = list()
        
        '''
        create list of touching ids
        '''
        if (row - 1 > 0) and (column - 1 > 0):
            self.touchingSquares.append(f"{row -1}_{column - 1}")
        if (column - 1 > 0):
            self.touchingSquares.append(f"{row}_{column - 1}")
        if (row + 1 < height + 1 ) and (column - 1 > 0):
            self.touchingSquares.append(f"{row + 1}_{column - 1}")
        
        if (row - 1 > 0) :
            self.touchingSquares.append(f"{row - 1}_{column}")
        if (row + 1 < height + 1) :
            self.touchingSquares.append(f"{row + 1}_{column}")
        
        if (row - 1 > 0) and (column + 1 < width + 1):
            self.touchingSquares.append(f"{row -1}_{column + 1}")
        if (column + 1 < width + 1):
            self.touchingSquares.append(f"{row}_{column + 1}")
        if (row + 1 < width + 1) and (column + 1 < width + 1):
            self.touchingSquares.append(f"{row + 1}_{column + 1}")

    def __str__ (self):
        return f"{self.row}_{self.column} -- {self.label} -- {self.id} -- {self.isHintSquare} -- touching Squares:{' '.join(self.touchingSquares)} -- isHintSquare {self.isHintSquare} -- isBlank {self.isBlank} -- isFlagged {self.isFlagged}"
'''
Setup game
'''
from selenium import webdriver
from selenium.webdriver import ActionChains
driver = webdriver.Firefox()
actions = ActionChains(driver)
driver.get('http://www.minesweeperonline.com/#beginner')
elem = driver.find_element_by_id("1_1")
elem.click()

def clickSquares(squares, currentSquare):
    clickTheseSquares = list()
    for potentialClick in currentSquare.touchingSquares:
        if squares[potentialClick].label == "square blank":
            clickTheseSquares.append(f"{potentialClick}")

    for clickSquare in clickTheseSquares:
        driver.find_element_by_id(clickSquare).click()
    
    


'''
create list of square instances
'''
squares = dict()
for column in range(1, width + 1):
    for row in range(1, height + 1):
        squares[f"{row}_{column}"] = square(row,column)

'''
for each square, if it is not a hint square, 
try and update it

if a square has been converted to a hint square,
then add the hint to the instance and change hint 
square to True
'''

for key, square in squares.items():
    # skip hint squares these dont change
    if (square.isHintSquare is True):
        continue

    # try and update non hint squares because these will change according to clicks
    if(square.isHintSquare is False):
        elem = driver.find_element_by_id(square.id)
        if (elem.get_attribute("class") != "square blank"):
            square.label = elem.get_attribute("class")
            square.isHintSquare = True
            square.isBlank = False

'''
for each square open1 go to that square and check if only 
one non hint square or marked mine is touching it. Mark that nonhint square 
if it hasnt been marked already
'''
for _ , square in squares.items():
    if square.label != "square open1":
        continue

    # need to see how many of the touching squares are open squares
    # or are squares that have been flagged. 
    touchingOpensAndFlags = list()
    for potentialOpen in square.touchingSquares:
        if squares[potentialOpen].isBlank or squares[potentialOpen].isFlagged :
            touchingOpensAndFlags.append(potentialOpen)

    # have found how many open squares are touching the ones
    # now i need to right click on the square if the len of 
    # touching opens is one AND the square hasnt already been marked
    
    if 1 == len(touchingOpensAndFlags):
        index = touchingOpensAndFlags[0]
        if True == squares[index].isFlagged:
            print(f'skipped clicking {index} because bomb is already flagged')
            continue
        else:
            print(f"right clicking {index} ---")
            elem = driver.find_element_by_id(f"{index}")
            actions.context_click(elem).perform()
            # update the right clicked square in memory
            rightClickSquare = squares[f"{index}"]
            rightClickSquare.isFlagged = True
            rightClickSquare.isBlank = False
            rightClickSquare.label = "square bombflagged"



'''
i am clicking square but not updating the programs understanding of the board
go through each square and 
'''
    
'''
have marked bombs found because they are near 1squares. Now I need to check every 1square
if it is touching a bomb, then click all other non-hint squares.
'''
for _ , square in squares.items():
    # skip squares that dont have a 1 on them
    if square.label != "square open1":
        continue

    # create a list of squares that are flagged that are touching our focused square
    touchingBombs = list()
    for potentialBomb in square.touchingSquares:
        if squares[potentialBomb].label == "square bombflagged":
            touchingBombs.append(potentialBomb)
    

    

    
    # if the len of touchingBombs is 0 then continue
    # if the len of touchingBombs is 1 then click
    # if the len of touchingBombs is greater than 1 then there is an error
    if 0 == len(touchingBombs):
        print(f"{square.id} is not touching any bombs")
        continue
    if len(touchingBombs) > 1:
        print("error: {square.id} is touching {len(touchingBombs)} but its label is {square.label}")
        continue
    if 1 == len(touchingBombs):
        # this is getting and clicking the bomb but that is wrong it needs to be getting all of the non
        # hint squares and non bomb squares touching squares[square.id]


        clickSquares(squares, square)
    
   
'''
begin
    update squares
click 1s
    if successful go to begin
click 2s
    if successful go to begin
mark 1s
    if successful go to begin
mark 2s
    if succesful go to begin

'''






#driver.close()