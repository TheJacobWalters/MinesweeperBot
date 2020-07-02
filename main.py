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
currentNumber = 0

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


def update():
    '''
    for each square, if it is not a hint square, 
    try and update it

    if a square has been converted to a hint square,
    then add the hint to the instance and change hint 
    square to True
    '''

    for _, square in squares.items():
        # skip hint squares these dont change
        if (square.isHintSquare is True):
            continue

        # try and update non hint squares because these will change according to clicks
        elif(square.isHintSquare is False):
            elem = driver.find_element_by_id(square.id)
            if (elem.get_attribute("class") != "square blank"):
                square.label = elem.get_attribute("class")
                square.isHintSquare = True
                square.isBlank = False


def mark1s():
    '''
    for each square open1 go to that square and check if only 
    one non hint square or marked mine is touching it. Mark that nonhint square 
    if it hasnt been marked already
    '''
    wasAbleToMark = False
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
                # update wasAbleToMark so that I can make decisions about whether to restart
                wasAbleToMark = True
    if (True == wasAbleToMark):
        global currentNumber
        currentNumber = 0
    return wasAbleToMark
def mark2s():
    '''
    for each square open2 go to that square and check if only 
    two non hint square or marked mine is touching it. Mark that nonhint square 
    if it hasnt been marked already
    '''
    for _ , square in squares.items():
        if square.label != "square open2":
            continue

        # need to see how many of the touching squares are open squares
        # or are squares that have been flagged. 
        touchingOpensAndFlags = list()
        for potentialOpen in square.touchingSquares:
            if squares[potentialOpen].isBlank or squares[potentialOpen].isFlagged :
                touchingOpensAndFlags.append(potentialOpen)

        # have found how many open squares are touching the twos
        # now i need to right click on the square if the len of 
        # touching opens is one AND the square hasnt already been marked
        
        if 2 == len(touchingOpensAndFlags):
            index1 = touchingOpensAndFlags[0]
            index2 = touchingOpensAndFlags[1]
            if True == squares[index1].isFlagged and True ==squares[index2].isFlagged:
                print(f'skipped clicking {index1} and {index2} because bomb is already flagged')
                continue
            else:
                print(f"right clicking {index1} and {index2} ---")

                elem = driver.find_element_by_id(f"{index1}")
                actions.context_click(elem).perform()
                # update the right clicked square in memory
                rightClickSquare = squares[f"{index1}"]
                rightClickSquare.isFlagged = True
                rightClickSquare.isBlank = False
                rightClickSquare.label = "square bombflagged"

                elem = driver.find_element_by_id(f"{index2}")
                actions.context_click(elem).perform()
                # update the right clicked square in memory
                rightClickSquare = squares[f"{index2}"]
                rightClickSquare.isFlagged = True
                rightClickSquare.isBlank = False
                rightClickSquare.label = "square bombflagged"
                wasAbleToMark = True
    
    if (True == wasAbleToMark):
        global currentNumber
        currentNumber = 0
    return wasAbleToMark

def allBlanksOrFlags(indexList):
    '''
    True: all indexs in this list are blank or Flagged
    False: one of these indexs are 
    '''
    for index in indexList:
        if (False == squares[index].isFlagged) or (False == squares[index].isBlank):
            return False
    return True

def allFlagged (indexList):
    for index in indexList:
        if False == squares[index].isFlagged:
            return False
    return True

def markXs( focusedNumber ):
    '''
    for each square open2 go to that square and check if only 
    two non hint square or marked mine is touching it. Mark that nonhint square 
    if it hasnt been marked already
    '''
    wasAbleToMark = False
    for _ , square in squares.items():
        if square.label != f"square open{focusedNumber}":
            continue

        # need to see how many of the touching squares are open squares
        # or are squares that have been flagged. 
        touchingOpensAndFlags = list()
        for potentialOpen in square.touchingSquares:
            if squares[potentialOpen].isBlank or squares[potentialOpen].isFlagged :
                touchingOpensAndFlags.append(potentialOpen)

        # have found how many open squares are touching the twos
        # now i need to right click on the square if the len of 
        # touching opens is one AND the square hasnt already been marked
        
        if focusedNumber == len(touchingOpensAndFlags):
            '''
                # if True == squares[index1].isFlagged and True ==squares[index2].isFlagged:
                # this needs to be changed so that it checks isFlagged or isBlank
                # going to make a function that returns True if all indexes are isFlagged or isBlank
            '''
            if allFlagged(touchingOpensAndFlags):
                print(f'skipped clicking {touchingOpensAndFlags} because bomb is already flagged')
                continue
            else:
                print(f"right clicking {touchingOpensAndFlags} ---")

                for index in touchingOpensAndFlags:
                    elem = driver.find_element_by_id(f"{index}")
                    actions.context_click(elem).perform()
                    # update the right clicked square in memory
                    rightClickSquare = squares[f"{index}"]
                    rightClickSquare.isFlagged = True
                    rightClickSquare.isBlank = False
                    rightClickSquare.label = "square bombflagged"
    
    if (True == wasAbleToMark):
        global currentNumber 
        currentNumber = 0
    return wasAbleToMark


def clickXs(label):
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
        if square.label != f"square open{label}":
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
        elif len(touchingBombs) == label:
            print(f"clicking {label} number of bombs at {square.id}")
            clickSquares(squares, square)
            continue

   
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

for x in range(20):
    print(f"beggining iteration {x}")
    currentNumber += 1
    update()
    if (markXs(1)):
        continue
    elif (clickXs(1)):
        continue
    elif (markXs(2)):
        continue
    elif (clickXs(2)):
        continue
    elif (markXs(3)):
        continue
    elif (clickXs(3)):
        continue
    elif (markXs(4)):
        continue
    elif (clickXs(4)):
        continue
    
    print(f"ending iteration {x}")

## DEBUG ###################
''' print out bomb positions'''
for _, square in squares.items():
    if (square.isFlagged == True):
        print("bomb is at:" + square.id)
###########################






#driver.close()