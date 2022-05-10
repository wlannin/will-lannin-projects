class Sudoku():
    
    # sudstring (a sudoku-string) reads a sudoku left to right, from top-left
    # note1: "0" in sudstring represents an empty space in the sudoku
    # note2: sudstring can also be passed as a list of single string characters 
    def __init__(self,sudstring):
        # here we store sudstring in list-form as an attribute of our sudoku
        self.string = list(sudstring)
        # here we create a grid containing the numbers from sudstring
        self.grid = [list(self.string[(i*9):((i+1)*9)]) for i in range(0,9)]
        # make a version of the grid where the numbers are of type int
        self.numgrid = [[int(x) for x in ylist] for ylist in self.grid]
        # make a history attribute to record (if we need to) numbers we place 
        self.history = []
        # make a separate history for our backtracking solver, bhistory
        self.bhistory = []
        # make a notes attribute to record notes for each square of the sudoku
        self.notes = {(x,y):[] for x in range(0,9) for y in range(0,9)}
        # initialise a dict to store the previous iteration's notes
        self.oldnotes = {}
        # initialise a list to store the empty squares of our sudoku
        self.empties = []
        # initialise our backtracking notes dict, bnotes
        self.bnotes = {}
    
    # show() will print the sudoku grid in its current state
    def show(self):
        # first we define the rows we'll use to border the sudoku rows
        tb = "-------------------------------------"
        inn = "|   +   +   +   +   +   +   +   +   |"
        out = "|---+---+---+---+---+---+---+---+---|"
        # now make a dictionary where we'll store each row of our sudoku
        dic = {y:"" for y in range(0,9)}
        # now loop through each number in the sudoku
        for y in range(0,9):
            for x in range(0,9):
                # if our number is 0, we now replace it with a blankspace
                if self.grid[y][x] == "0":
                    mynumber = " "
                else:
                    mynumber = self.grid[y][x]
                # this logic simply makes the sudoku have border edges
                if x%3 == 0:
                    dic[y] += "| " + mynumber + " "
                else:
                    dic[y] += "  " + mynumber + " "
            # need to add one final border for the sudoku's right-side
            dic[y] += "|"
        # now make a list where rows are in their order of appearance
        sudlist = [tb,dic[0],inn,dic[1],inn,dic[2],out,
                   dic[3],inn,dic[4],inn,dic[5],out,
                   dic[6],inn,dic[7],inn,dic[8],tb]
        # now print our rows joined by newlines "\n"
        print("\n".join(sudlist))
    
    # getbox(x,y) returns a list of the numbers in the same box as (x,y)
    def getbox(self,x,y):
        # use // to round x & y down to their nearest multiple of 3
        xstart = x//3 * 3
        ystart = y//3 * 3
        # now make a list of lists, where each list is a row in our box
        list_of_lists = [
            [self.numgrid[i][x] for x in range(xstart,xstart+3)
             ] for i in range(ystart,ystart+3)]
        # now return the concatenation of these lists
        return [j for k in list_of_lists for j in k]
    
    # canplace(n,x,y) returns True if n can be placed in position (x,y) 
    def canplace(self, n, x, y):
        # first check if (x,y) is a free position (ie non-zero)
        if self.numgrid[y][x] != 0:
            return False
        # now check if placing n would break the sudoku row-rule
        if n in self.numgrid[y]:
            return False
        # now check if placing n would break the sudoku col-rule
        if n in [self.numgrid[i][x] for i in range(0,9)]:
            return False
        # now check if placing n would break the sudoku box-rule
        if n in self.getbox(x,y):
            return False
        else:
            return True
    
    # adds n at (x,y) with history (n can be 0 if we wish to undo something)  
    def bplace(self,n,x,y):
        # update all the relevant attributes with this information
        self.string[x+(9*y)] = str(n)
        self.grid[y][x] = str(n)
        self.numgrid[y][x] = n
        if n == 0:
            # if n is 0, we are correcting a mistake, so erase the last history
            self.bhistory = self.bhistory[:-1]
        else:
            # when n != 0, we're placing a new number so add (n,x,y) to history
            self.bhistory += [(n,x,y)]
    
    # iscompleted() returns True if the sudoku is completed correctly
    def iscomplete(self):
        # first, check if any digits in the sudoku are 0
        if '0' in self.string:
            return False
        # now, loop through every position and see if any break sudoku rules
        for y in range(0,9):
            for x in range(0,9):
                # call the value in this position n
                n = self.numgrid[y][x]
                # check row-rule
                if len([i for i in self.numgrid[y] if i==n]) != 1:
                    return False
                # check col-rule
                col = [self.numgrid[i][x] for i in range(0,9)]
                if len([i for i in col if i==n]) != 1:
                    return False
                # check box rule
                if len([i for i in self.getbox(x,y) if i==n]) != 1:
                    return False
        # if none of the earlier checks returned False, we know it is complete
        return True
    
    # bfunction is the function used in my backtracking solve method bsolve
    def bfunction(self):
        # find the first empty square (read left to right starting top left)
        (x,y) = [(xi,yi) for yi in range(9)
         for xi in range(9)
         if self.numgrid[yi][xi] == 0][0] #[0] chooses the first in the list
        # now iterate through the numbers in bnotes we can try in (x,y)
        for n in self.bnotes[(x,y)]:
            if self.canplace(n,x,y):
                # if we can place n in (x,y), we do it
                self.bplace(n,x,y)
                # now return control to the while loop in the method bsolve
                return
            else:
                # if this n can't be placed in (x,y), try the next possible n
                continue
        # we only reach this part of bfunction if no n can be placed in (x,y)
        # grab the last number we placed in the sudoku from bhistory
        (n1,x1,y1) = self.bhistory[-1]
        # erase this placement, since it directly leads to the sudoku breaking
        self.bplace(0,x1,y1)
        # remove n1 from x1,y1 bnotes, so its not placed again next while loop
        self.bnotes[(x1,y1)].remove(n1)
        # finally reset bnotes[(x,y)] ready for the next while loop on x1,y1
        self.bnotes[(x,y)] = list(range(1,10))
        # now return control to the while loop in bsolve
        return
    
    # method to solve the sudoku using backtracking
    def bsolve(self):
        # if the sudoku is already solved, stop the function
        if self.iscomplete():
            print("This sudoku is already solved!")
            return
        # now, find every square that isn't already filled in our sudoku
        self.empties = [(x,y) for x in range(9)
                   for y in range(9)
                   if self.numgrid[y][x] == 0]
        # initialise bnotes, the notes dict used by our backtracking solver
        self.bnotes = {(x,y):list(range(1,10)) for (x,y) in self.empties}
        # make a loop_count variable to count our number of loops
        loop_count = 0
        # now enter a while loop conditional on the sudoku being incomplete
        while self.iscomplete() == False:
            # add +1 to loop_count every time we loop
            loop_count += 1
            # now execute our backtracking function
            self.bfunction()
        # we only reach this point of the bsolve if we've solved our sudoku!
        if self.iscomplete():
            self.show()
            print("Sudoku solved in {0} iterations".format(loop_count))
            return
    
    # Below you'll find method smart_solve4() and its related methods
    
    # update_notes updates self.notes to reflect n being placed in (x,y)
    def update_notes(self,n,x,y):
        # set the notes for square (x,y) to be empty now we've placed n
        self.notes[(x,y)] = []
        # drop n from each square in notes which has x-coord == x
        for yi in range(0,9):
            # remove n from the notes for the square (x,yi) 
            try:
                self.notes[(x,yi)].remove(n)
            except ValueError:
                pass # if n isn't in the notes for this square, move on
        # next, drop n from each square in notes with y-coord == y
        for xi in range(0,9):
            # remove n from the notes for the square (xi,y) 
            try:
                self.notes[(xi,y)].remove(n)
            except ValueError:
                pass # if n isn't in the notes for this square, move on
        # finally, remove n from the notes in the same box as (x,y)
        for xi in range(x//3 * 3, x//3 * 3 + 3):
            for yi in range(y//3 * 3, y//3 * 3 + 3):
                # remove n from the notes for the square (xi,yi) 
                try:
                    self.notes[(xi,yi)].remove(n)
                except ValueError:
                    pass # if n isn't in the notes for this square, move on
    
    # add n at (x,y), update self.notes, and add to self.history with a code 
    def place(self,n,x,y,code):
        # update all the relevant attributes with this information
        self.string[x+(9*y)] = str(n)
        self.grid[y][x] = str(n)
        self.numgrid[y][x] = n
        # use our update_notes method to update the notes
        self.update_notes(n, x, y)
        # now store this info, with the code given, in self.history
        self.history += [(n,x,y,code)]
    
    # notfree(x,y) returns True if the position (x,y) isn't free, else False
    def notfree(self, x, y):
        return self.numgrid[y][x] != 0
    
    # v4 to ensure solver does an update in its entirety before it re-loops
    def smart_solve4(self):
        # firstly, if the sudoku is solved then stop the function
        if self.iscomplete():
            print("This sudoku is already solved!")
            return
        # make a list uniquely identifying each box by its top left coordinate
        boxlist = [(3*x,3*y) for x in range(0,3) for y in range(0,3)]
        
        # ---------------------------------------------------------------------
        # Part 1: Iterate through each square, making all notes in self.notes
        # ---------------------------------------------------------------------
        # 1.1: loop through every possible x and y coordinate
        for y in range(0,9):
            for x in range(0,9):
                xynote = [] #initialise an empty note
                # now loop through every number that could go in square (x,y)
                for n in range (1,10):
                    # check if n can be placed in square (x,y)
                    if self.canplace(n, x, y):
                        # if true then we add n to our (x,y) notes
                        xynote += [n] 
                # now store the note in self.notes
                self.notes[(x,y)] = xynote
                        
        # ---------------------------------------------------------------------
        # Part 2: While loop which tries to solve using only simple rules
        # ---------------------------------------------------------------------
        # initialise sudoku_updated as False
        sudoku_updated = False
        # enter a while loop conditional on the sudoku being unsolved
        while self.iscomplete() == False:
            
            # if we haven't changed anything since the last loop, stop!
            if sudoku_updated == False:
                # now see if notes have changed
                if self.oldnotes == self.notes:
                    print("Sudoku solve failed")
                    print(self.notes)
                    self.show()
                    return
            
            # now set old notes to be the current notes 
            self.oldnotes = self.notes
            # flag for if sudoku is updated in this iteration of the loop
            sudoku_updated = False
            
            # 2.1: find all the squares with only 1 possible number in notes
            ones = {xycoord:len(notelist) for xycoord,notelist in
                    self.notes.items() if len(notelist) == 1}
            # if ones is non-empty, then place numbers in the first ones square
            if ones != {}:
                # set x,y to be the first coordiante featured in ones
                (x,y) = list(ones.keys())[0]
                # collect n
                n = self.notes[(x,y)][0]
                # place n into the (x,y) square
                self.place(n, x, y,2.1)
                # sudoku_updated now True since we placed a new number
                sudoku_updated = True
                    
            # if sudoku updated outside a for-loop, goto next while iteration
            if sudoku_updated:
                continue
            
            # 2.2: check boxes for any numbers that have only 1 valid place
            for (xbox,ybox) in boxlist: # loop through all possible boxes
                # when sudoku updated within a for-loop, break
                if sudoku_updated:
                    break
                # make a list of all numbers missing from this box
                biglist = [self.notes[(x,y)] for x in range(xbox,xbox+3)
                           for y in range(ybox,ybox+3)]
                # now put these numbers in a list where each only appears once
                checklist = set([i for ls in biglist for i in ls])
                # now loop through each of these numbers
                for n in checklist:
                    # if there is only 1 place n can go, then place it
                    if len([i for ls in biglist for i in ls if i==n]) == 1:
                        # we must find the coordinate which n goes in
                        (x,y) = [(x,y) for x in range(xbox,xbox+3) for y in
                         range(ybox,ybox+3) if n in self.notes[(x,y)]][0]
                        # now place n in this coordinate
                        self.place(n, x, y,2.2)
                        # sudoku_updated now True since sudoku is updated
                        sudoku_updated = True
                        # if sudoku updated, break out of this loop
                        if sudoku_updated:
                            break
                        
            # if sudoku updated outside a for-loop, goto next while iteration
            if sudoku_updated:
                continue
            
            # 2.3: check columns for any numbers that have only 1 valid place
            for y in range(0,9): # loop through all possible y column values
                # when sudoku updated within a for-loop, break
                if sudoku_updated:
                    break
                # make a list of all numbers missing from this col
                biglist = [self.notes[(xi,y)] for xi in range(0,9)]
                # now put these numbers in a list where each only appears once
                checklist = set([i for ls in biglist for i in ls])
                # now loop through each of these numbers
                for n in checklist:
                    # if there is only 1 place n can go, then place it
                    if len([i for ls in biglist for i in ls if i==n]) == 1:
                        # we must find the coordinate which n goes in
                        (x,y) = [(xi,y) for xi in 
                                 range(0,9) if n in self.notes[(xi,y)]][0]
                        # now place n in this coordinate
                        self.place(n, x, y,2.3)
                        # sudoku_updated now True since sudoku is updated
                        sudoku_updated = True
                        # if sudoku updated, break out of this loop
                        if sudoku_updated:
                            break
            
            # if sudoku updated outside a for-loop, goto next while iteration
            if sudoku_updated:
                continue
            
            # 2.4: check rows for any numbers that have only 1 valid place
            for x in range(0,9): # loop through all possible x row values
                # when sudoku updated within a for-loop, break
                if sudoku_updated:
                    break
                # make a list of all numbers missing from this row
                biglist = [self.notes[(x,yi)] for yi in range(0,9)]
                # now put these numbers in a list where each only appears once
                checklist = set([i for ls in biglist for i in ls])
                # now loop through each of these numbers
                for n in checklist:
                    # if there is only 1 place n can go, then place it
                    if len([i for ls in biglist for i in ls if i==n]) == 1:
                        # we must find the coordinate which n goes in
                        (x,y) = [(x,yi) for yi in 
                                 range(0,9) if n in self.notes[(x,yi)]][0]
                        # now place n in this coordinate
                        self.place(n, x, y,2.4)
                        # sudoku_updated now True since sudoku is updated
                        sudoku_updated = True
                        # if sudoku updated in loop, break
                        if sudoku_updated:
                            break
            
            # if sudoku updated outside a for-loop, goto next while iteration
            if sudoku_updated:
                continue
        
            # -------------------------------------------------------------
            # Part 3: If sudoku not solved already, use pairs
            # -------------------------------------------------------------    
            
            # There are 2 types of pairs:
            
            # (1) pairs with ONLY n1,n2 in their notes
            # these (1) pairs lets us remove notes from NON-PAIR squares
            
            # (2) pairs with one (or more) extra note in them than n1,n2
            # these (2) pairs let us remove notes from PAIR squares
            ## (crucially with (2), these must be the ONLY squares in their
            ## box/row/col with n1 or n2 in!)
            
            
            # loop every possible pair of numbers n1,n2 (with n1<n2)
            for n2 in range(2,10):
                # if sudoku updated in loop, break
                if sudoku_updated:
                    break
                for n1 in range(1,n2):
                    # if sudoku updated in loop, break
                    if sudoku_updated:
                        break
                    # find all squares with only n1,n2 in their notes
                    only2 = [(x,y) for (x,y) in self.notes
                             # we require n1 and n2 in the notes
                             if n1 in self.notes[(x,y)]
                             and n2 in self.notes[(x,y)]
                             # and require that no other notes exist
                             and len(self.notes[(x,y)])==2]
                    
                    # find all squares with n1 and n2 in their notes
                    pairs = [(x,y) for (x,y) in self.notes
                             # we require n1 and n2 in the notes
                             if n1 in self.notes[(x,y)]
                             and n2 in self.notes[(x,y)]]
                    
                    #3.1 rowcheck: now check pairs of n1,n2 in each column
                    for y in range (0,9):
                        # if sudoku updated in loop, break
                        if sudoku_updated:
                            break
                        # pull all pairsqrs in this row
                        pairsqrs = [(xi,yi) for (xi,yi) in pairs if yi == y]
                        # exactly 2 squares needed for pair, else continue
                        if len(pairsqrs) != 2:
                            continue
                        elif len(pairsqrs) == 2:
                            # check if this is a (1) pair (ie no other notes)
                            if pairsqrs[0] in only2 and pairsqrs[1] in only2:
                                # a (1) pair! so remove n1,n2 from non-pairs
                                # counter of any changes to notes we make
                                change_count = 0 #count any changes we make
                                for xi in range(0,9):
                                    coord_i = (xi,y)
                                    # continue if coord_i is one of our pair
                                    if coord_i in pairsqrs:
                                        continue
                                    # try to un-note n1 for square
                                    try:
                                        self.notes[coord_i].remove(n1)
                                        # +1 to change count, notes changed!
                                        change_count += 1
                                    except ValueError:
                                        pass # if n1 not in note, move on
                                    # try to un-note n2 for square
                                    try:
                                        self.notes[coord_i].remove(n2)
                                        # +1 to change count, notes changed!
                                        change_count += 1
                                    except ValueError:
                                        pass # if n2 not in note, move on
                                # sudoku_updated True if changes is >0
                                if change_count > 0:
                                    # sudoku has been updated
                                    sudoku_updated = True
                                    # if sudoku updated in loop, break
                                    if sudoku_updated:
                                        # reflect in history
                                        self.history += [
                                            (n1,n2,pairsqrs[0],pairsqrs[1],3.12)]
                                        break
                            else: # now we have a potential type (2) pair
                                # counter for n1 or n2 notes in this row
                                n_count = 0
                                # loop through this col
                                for xi in range(0,9):
                                    coord_i = (xi,y)
                                    # continue if coord_i is one of our pair
                                    if coord_i in pairsqrs:
                                        continue
                                    # +1 to count if we find n1
                                    if n1 in self.notes[coord_i]:
                                        n_count += 1
                                    # +1 to count if we find n2
                                    if n2 in self.notes[coord_i]:
                                        n_count += 1
                                # now we have a type (2) pair if n_count == 0
                                if n_count == 0:
                                    # (2) can simplify pairsqr notes to n1,n2
                                    if len(self.notes[pairsqrs[0]]) > 2:
                                        # reduce notes to simpler [n1,n2]
                                        self.notes[pairsqrs[0]] = [n1,n2]
                                        # sudoku has been updated
                                        sudoku_updated = True
                                    if len(self.notes[pairsqrs[1]]) > 2:
                                        # reduce notes to simpler [n1,n2]
                                        self.notes[pairsqrs[1]] = [n1,n2]
                                        # sudoku has been updated
                                        sudoku_updated = True
                                    # if sudoku updated in loop, break
                                    if sudoku_updated:
                                        # reflect in history
                                        self.history += [
                                            (n1,n2,pairsqrs[0],pairsqrs[1],3.12)]
                                        break
                            
                    #3.2 colcheck: now check pairs of n1,n2 in each row
                    for x in range (0,9):
                        # if sudoku updated in loop, break
                        if sudoku_updated:
                            break
                        # pull all pairsqrs in this col
                        pairsqrs = [(xi,yi) for (xi,yi) in pairs if xi == x]
                        # exactly 2 squares needed for pair, else continue
                        if len(pairsqrs) != 2:
                            continue
                        elif len(pairsqrs) == 2:
                            # check if this is a (1) pair (ie no other notes)
                            if pairsqrs[0] in only2 and pairsqrs[1] in only2:
                                # a (1) pair! so remove n1,n2 from non-pairs
                                # counter of any changes to notes we make
                                change_count = 0 #count any changes we make
                                for yi in range(0,9):
                                    coord_i = (x,yi)
                                    # continue if coord_i is one of our pair
                                    if coord_i in pairsqrs:
                                        continue
                                    # try to un-note n1 for square
                                    try:
                                        self.notes[coord_i].remove(n1)
                                        # +1 to change count, notes changed!
                                        change_count += 1
                                    except ValueError:
                                        pass # if n1 not in note, move on
                                    # try to un-note n2 for square
                                    try:
                                        self.notes[coord_i].remove(n2)
                                        # +1 to change count, notes changed!
                                        change_count += 1
                                    except ValueError:
                                        pass # if n2 not in note, move on
                                # sudoku_updated True if change count is >0
                                if change_count > 0:
                                    # sudoku has been updated
                                    sudoku_updated = True
                                    # if sudoku updated in loop, break
                                    if sudoku_updated:
                                        # reflect in history
                                        self.history += [
                                            (n1,n2,pairsqrs[0],pairsqrs[1],3.21)]
                                        break
                            else: # now we have a potential type (2) pair
                                # counter for n1 or n2 notes in this col
                                n_count = 0
                                # loop through this row
                                for yi in range(0,9):
                                    coord_i = (x,yi)
                                    # continue if coord_i is one of our pair
                                    if coord_i in pairsqrs:
                                        continue
                                    # +1 to count if we find n1
                                    if n1 in self.notes[coord_i]:
                                        n_count += 1
                                    # +1 to count if we find n2
                                    if n2 in self.notes[coord_i]:
                                        n_count += 1
                                # now we have a type (2) pair if n_count == 0
                                if n_count == 0:
                                    # (2) can simplify pairsqr notes to n1,n2
                                    if len(self.notes[pairsqrs[0]]) > 2:
                                        # reduce notes to simpler [n1,n2]
                                        self.notes[pairsqrs[0]] = [n1,n2]
                                        # sudoku has been updated
                                        sudoku_updated = True
                                    if len(self.notes[pairsqrs[1]]) > 2:
                                        # reduce notes to simpler [n1,n2]
                                        self.notes[pairsqrs[1]] = [n1,n2]
                                        # sudoku has been updated
                                        sudoku_updated = True
                                    # if sudoku updated in loop, break
                                    if sudoku_updated:
                                        # reflect in history
                                        self.history += [
                                            (n1,n2,pairsqrs[0],pairsqrs[1],3.22)]
                                        break        
                    
                    #3.3 boxcheck: check for pairs of n1,n2 in each box
                    for (xbox,ybox) in boxlist:
                        # if sudoku updated in loop, break
                        if sudoku_updated:
                            break
                        # pull all pairsqrs in this box
                        pairsqrs = [(xi,yi) for (xi,yi) in pairs
                                 if xi in range(xbox,xbox+3) 
                                 and yi in range(ybox,ybox+3)]
                        # exactly 2 squares needed for pair, else continue
                        if len(pairsqrs) != 2:
                            continue
                        elif len(pairsqrs) == 2:
                            # check if this is a (1) pair (ie no other notes)
                            if pairsqrs[0] in only2 and pairsqrs[1] in only2:
                                # a (1) pair! so remove n1,n2 from non-pairs
                                # counter of any changes to notes we make
                                change_count = 0 #count any changes we make
                                # loop through x coords of this box
                                for xi in range(xbox,xbox+3):
                                    # now loop through y coords of this box
                                    for yi in range(ybox,ybox+3):
                                        coord_i = (xi,yi)
                                        # continue if coord_i is one of our pair
                                        if coord_i in pairsqrs:
                                            continue
                                        # try to un-note n1 for square
                                        try:
                                            self.notes[coord_i].remove(n1)
                                            # +1 to change count
                                            change_count += 1
                                        except ValueError:
                                            pass # if n1 not in note, move on
                                        # try to un-note n2 for square
                                        try:
                                            self.notes[coord_i].remove(n2)
                                            # +1 to change count
                                            change_count += 1
                                        except ValueError:
                                            pass # if n2 not in note, move on
                                # sudoku_updated True if change count is >0
                                if change_count > 0:
                                    # sudoku has been updated
                                    sudoku_updated = True
                                    # if sudoku updated in loop, break
                                    if sudoku_updated:
                                        # reflect in history
                                        self.history += [
                                            (n1,n2,pairsqrs[0],pairsqrs[1],3.31)]
                                        break
                            else: # now we have a potential type (2) pair
                                # counter for n1 or n2 notes in this row
                                n_count = 0
                                # loop through x coords of this box
                                for xi in range(xbox,xbox+3):
                                    # now loop through y coords of this box
                                    for yi in range(ybox,ybox+3):
                                        coord_i = (xi,yi)
                                        # continue if coord_i one of pair
                                        if coord_i in pairsqrs:
                                            continue
                                        # +1 to count if we find n1
                                        if n1 in self.notes[coord_i]:
                                            n_count += 1
                                        # +1 to count if we find n2
                                        if n2 in self.notes[coord_i]:
                                            n_count += 1
                                # now we have a type (2) pair if n_count == 0
                                if n_count == 0:
                                    # (2) can simplify pairsqr notes to n1,n2
                                    if len(self.notes[pairsqrs[0]]) > 2:
                                        # reduce notes to simpler [n1,n2]
                                        self.notes[pairsqrs[0]] = [n1,n2]
                                        # sudoku has been updated
                                        sudoku_updated = True
                                    if len(self.notes[pairsqrs[1]]) > 2:
                                        # reduce notes to simpler [n1,n2]
                                        self.notes[pairsqrs[1]] = [n1,n2]
                                        # sudoku has been updated
                                        sudoku_updated = True
                                    # if sudoku updated in loop, break
                                    if sudoku_updated:
                                        # reflect in history
                                        self.history += [
                                            (n1,n2,pairsqrs[0],pairsqrs[1],3.32)]
                                        break 
            
            # if sudoku updated outside a for-loop, goto next while iteration
            if sudoku_updated:
                continue
            
            # -------------------------------------------------------------
            # Part 4: Use box-notes that appear in only one row/col
            # ------------------------------------------------------------- 
            # loop through all boxes
            for (xbox,ybox) in boxlist:
                # when sudoku updated within a for-loop, break
                if sudoku_updated:
                    break
                # get the remaining numbers for this box
                nlist = [i for i in range(1,10)
                         if i not in self.getbox(xbox,ybox)]
                # loop through these n
                for n in nlist:
                    # get the squares of this box with n noted
                    sqrs = [(x,y) for x in range(xbox,xbox+3)
                            for y in range(ybox,ybox+3)
                            if n in self.notes[(x,y)]]
                    #4.1 check if the y-coords are equal for all squares
                    if len(set([y for (x,y) in sqrs])) == 1:
                        # define the y-coord they all have in common
                        y = sqrs[0][1]
                        # now pull any other notes in this row
                        nosqrs = [(xi,y) for xi in range(0,9)
                                  if (xi,y) not in sqrs]
                        # make a change count to count changes we make
                        change_count = 0
                        # now remove n from any other notes in this row
                        for coord_i in nosqrs:
                            # try to un-note n from coord_i square
                            try:
                                self.notes[coord_i].remove(n)
                                # +1 to change count
                                change_count += 1
                            except ValueError:
                                pass # if n not in note, move on
                        # sudoku_updated True if change count is >0
                        if change_count > 0:
                            # sudoku has been updated
                            sudoku_updated = True
                        # if sudoku updated in loop, update history & break
                        if sudoku_updated:
                            # reflect in history
                            self.history += [
                                (xbox,ybox,y,n,4.1)]
                            break
                    #4.2 check if the x-coords are equal for all squares
                    elif len(set([x for (x,y) in sqrs])) == 1:
                        # define the x-coord they all have in common
                        x = sqrs[0][0]
                        # now pull any other notes in this col
                        nosqrs = [(x,yi) for yi in range(0,9)
                                  if (x,yi) not in sqrs]
                        # make a change count to count changes we make
                        change_count = 0
                        # now remove n from any other notes in this col
                        for coord_i in nosqrs:
                            # try to un-note n from coord_i square
                            try:
                                self.notes[coord_i].remove(n)
                                # +1 to change count
                                change_count += 1
                            except ValueError:
                                pass # if n not in note, move on
                        # sudoku_updated True if change count is >0
                        if change_count > 0:
                            # sudoku has been updated
                            sudoku_updated = True
                        # if sudoku updated in loop, update history & break
                        if sudoku_updated:
                            # reflect in history
                            self.history += [
                                (xbox,ybox,x,n,4.2)]
                            break
                        
            # if sudoku updated outside a for-loop, goto next while iteration
            if sudoku_updated:
                continue
                # return
        
            # -------------------------------------------------------------
            # Part 5: row/col notes intersect box
            # -------------------------------------------------------------                
            
            # i represents the row/col we will check
            for i in range(0,9):
                # when sudoku updated within a for-loop, break
                if sudoku_updated:
                    break
                # now loop through family "row" or "col" to keep code concise
                for family in ["row","col"]:
                    # when sudoku updated within a for-loop, break
                    if sudoku_updated:
                        break
                    # see if we're working with a row or col
                    if family == "row":
                        # get the squares from this row
                        sqrs = [(x,i) for x in range(0,9)]
                    else:
                        # get the squares from this col
                        sqrs = [(i,y) for y in range(0,9)]
                
                    # define nlist, all distinct numbers in sqrs notes 
                    nlist = list(set([i for sublist in [self.notes[s]
                                                   for s in sqrs]
                                 for i in sublist]))
                    
                    # now loop through n
                    for n in nlist:
                        # grab the squares in sqrs with n in their notes
                        nsqrs = [(x,y) for (x,y) in sqrs
                                 if n in self.notes[(x,y)]]
                        # now make a list of the boxes the nsqrs are in
                        nboxes = [(x//3 * 3, y//3 * 3) for (x,y) in nsqrs]
                        # check if all the nsqrs are in the same box
                        if len(set(nboxes)) == 1:
                            # get the reference coords of this box
                            (xbox,ybox) = nboxes[0]
                            #can remove n from non-family notes in this box
                            change_count = 0
                            # loop through each square in box to try removing
                            for xi in range(xbox,xbox+3):
                                for yi in range(ybox,ybox+3):
                                    coord_i = (xi,yi)
                                    # continue if coord_i is one of our family
                                    if coord_i in sqrs:
                                        continue
                                    # try to un-note n for square
                                    try:
                                        self.notes[coord_i].remove(n)
                                        # +1 to change count
                                        change_count += 1
                                    except ValueError:
                                        pass # if n not in note, move on
                            # sudoku_updated True if change count is >0
                            if change_count > 0:
                                # sudoku has been updated
                                sudoku_updated = True
                                # if sudoku updated in loop, break
                                if sudoku_updated:
                                    # reflect in history
                                    self.history += [
                                        (n, xbox, ybox, family, i,5)]
                                    break
        
            # if sudoku updated outside a for-loop, goto next while iteration
            if sudoku_updated:
                continue
                # return  
                    
        if self.iscomplete():
            self.show()
            print("Sudoku solved in {0} iterations".format(len(self.history)))
            return
        
        
        

    
stest = Sudoku("123456789123456789123456789123456789555555555123456789123456789000000000999999999")      
expert = Sudoku("000000018157000400000100000000300062700009105000060070002000030801007000009600020")
s = Sudoku("000400200002000018506900030069000300050000021800157609000030960900602050000000702")
ee = Sudoku("700080000005020009000000300500400000002000860100000004020007400000090200403005001")
e2 = Sudoku("000010000020000095070050003002300701000700400430800000650400000000062000090000070")
e3 = Sudoku("046007800008900700500020000000062004400000007000050010002000000015000020000008060")

intermed = Sudoku("020608000580009700000040000370000500600000004008000013000020000009800036000306090")

inkala = Sudoku("800000000003600000070090200050007000000045700000100030001000068008500010090000400")

# expert.show()
# expert.smart_solve4()

# e3.show()
# e3.smart_solve4()

inkala.show()
# inkala.smart_solve4()
inkala.bsolve()
