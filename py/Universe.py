from time import time
from random import choice

DELTA_T = 1 # s between updates
N_COLS  = 30
N_ROWS  = 10

class Universe(object):
    def __init__(self):
        self.cell_list =[[choice([0,1]) for c in range(N_COLS)] for r in range(N_ROWS)]

        self.sched_update = time()+DELTA_T;
                       
    # DEPRECIATED!
    def update(self, game_man):
        # updates the cell list if it is time to do so
        print 'checking for update'
        if time() >= self.sched_update:
            self.__update(game_man)
            self.sched_update = time()+DELTA_T
           
    def __update(self, game_man):
        # print 'updating!'
        # updates the cell list
        for rown in range(len(self.cell_list)):
            for coln in range(len(self.cell_list[0])):
                num = self.getNeighbors(rown,coln)
                if num < 2: # death by lonliness
                    if self.cell_list[rown][coln] == 1:
                        self.cell_list[rown][coln] = 0
                        game_man.sendAll('update '+str(rown)+' '+str(coln)+' 0', supress=True)
                # elif num == 2: do nothing... 0->0, 1->1
                elif num == 3: # reproduction!
                    if self.cell_list[rown][coln] == 0:
                        self.cell_list[rown][coln] = 1
                        game_man.sendAll('update '+str(rown)+' '+str(coln)+' 1', supress=True)
                elif num > 3: # death by overcrowding
                    if self.cell_list[rown][coln] == 1:
                        self.cell_list[rown][coln] = 0
                        game_man.sendAll('update '+str(rown)+' '+str(coln)+' 0', supress=True)
                else:
                    continue
                
    def getNeighbors(self,rown,coln):
        # returns number of active neighbors for given cell loc
        # assumes a toroidal space (l-r, top-bottom boundaries connected)
        # above:
        sum = self.getCell(rown-1,coln)
        # below:
        sum += self.getCell(rown+1,coln)
        # left:
        sum += self.getCell(rown,coln-1)
        # right:
        sum += self.getCell(rown,coln+1)
        # upleft
        sum += self.getCell(rown-1,coln-1)
        # upright
        sum += self.getCell(rown-1,coln+1)
        # downleft
        sum += self.getCell(rown+1,coln-1)
        # downright
        sum += self.getCell(rown+1,coln+1)
        
        return sum
            
    def getCell(self,rown,coln):
        # returns value of cell at given row, col even if you go 
        #  outside the boundaries of the list by assuming a toroidal space
        try:
            return self.cell_list[rown][coln]
        except IndexError:
            nrows = len(self.cell_list)
            ncols = len(self.cell_list[0])
            
            if rown > nrows-1:
                rown -= nrows
            elif rown < 0:
                rown += nrows
                
            if coln > ncols-1:
                coln -= ncols
            elif coln < 0:
                coln += ncols
            
            return self.cell_list[rown][coln]
            
            
            
            
            