from math import trunc
import numpy as np

class Tris:

    def __init__(self,player=1,player2=2,mode='pc'):
        if player==0 or player2==0 or player==player2 or not(mode=='pc' or mode=='2p'):
            print("Error: object 'Tris' initiallized uncorrectly!")
            return
        self.pl = player
        self.pc = player2
        self.mode = mode
        self.game = np.zeros((3,3), np.int8)
        self.first = self.pc<self.pl
        self.turn = self.first

    def Compute(self):
        if np.count_nonzero(self.game)==0:
            a = np.random.randint(3)
            b = np.random.randint(3)
            self.game[a,b] = self.pc
            self.turn = not(self.turn)
            return a,b
        turns = 0
        game = np.copy(self.game)
        Value = np.empty(9,np.int8)

        for a in range(3):
            for b in range(3):
                if game[a,b]==0:
                    points = self.CheckWin(game,a,b,True)
                    if points!=-5:
                        self.game[a,b] = self.pc
                        return a,b #,self.pc
                    else:
                        Value[(3*a)+b] = self.bruteforce(game,a,b,turns)
                else:
                    Value[(3*a)+b] = -50 # -50 is just to represent -inf, as the cell isn't empty
        #print(Value)

        # WHAT THE ACTUAL FUCK IS THIS "CODE"??
        # index = -1
        # cursor = -1
        # bestmove = max(Value)
        # choice = randrange(Value.count(bestmove))

        # for a in range(3):
        #     for b in range(3):
        #         if game[a,b]==0:
        #             index+=1
        #             if Value[index]==bestmove:
        #                 cursor+=1
        #                 if cursor==choice:
        #                     self.game[a,b] = self.pc
        #                     return a,b

        choices = np.nonzero(Value==np.amax(Value))[0]
        a,b = divmod(choices[np.random.randint(choices.size)],3)
        self.game[a,b] = self.pc
        self.turn = not(self.turn)
        return a,b

    def bruteforce(self,xgame,y,x,turns):
        game = np.copy(xgame)
        if turns%2==0:
            game[y,x] = self.pc
        else:
            game[y,x] = self.pl
        turns+=1
        myturn = turns%2==0
        
        Value = []
        for a in range(3):
            for b in range(3):
                if game[a,b]==0:
                    points = self.CheckWin(game,a,b,myturn)
                    if points!=-5:
                        return points
                    else:
                        Value.append(self.bruteforce(game,a,b,turns))
        if myturn:
            nmax = max(Value)
            if turns==2:
                return nmax+(0.1*Value.count(1))
            return nmax
        else:
            nmin = min(Value)
            if turns==1:
                nmax = max(Value)
                # DEBUG
                # print(f"----------{Value} \nMin: {nmin}  Max: {nmax}  truncMax: {trunc(nmax)}  truncated: {nmax-trunc(nmax)}  Sum: {nmin + (nmax-trunc(nmax))}")
                return nmin + (nmax-trunc(nmax))
            return nmin

    def CheckWin(self,xgame,y,x,myturn):
        game = np.copy(xgame)
        if myturn:
            game[y,x] = self.pc
        else:
            game[y,x] = self.pl

        if (y+x)%2==0:
            if game[0,0]==game[1,1]==game[2,2] or game[0,2]==game[1,1]==game[2,0]:    #DIAGONALS check for CENTER and CORNER
                if game[1,1]==self.pc:
                    return 1
                elif game[1,1]==self.pl:
                    return -1
        if game[y,0]==game[y,1]==game[y,2]:                                              #Relative RAW check
            if game[y,0]==self.pc:
                return 1
            elif game[y,0]==self.pl:
                return -1
        if game[0,x]==game[1,x]==game[2,x]:                                              #Relative COLUMN check
            if game[0,x]==self.pc:
                return 1
            elif game[0,x]==self.pl:
                return -1
        # if (game[0].count(0) + game[1].count(0) + game[2].count(0))==0:       funny to look at how old me used to code

        if np.count_nonzero(game) == 9:                                                     #TIE check
            return 0
        return -5

    def Move(self,a,b): #,turn=1):
        if self.game[a,b]!=0:
            print("Can't make a move on a cell which is not zero!")
        else:
            # if self.mode=='pc':
            #     self.game[a,b] = self.pl
            # else:
            #     if turn==self.pl:

            win = self.CheckWin(self.game,a,b,False)
            self.game[a,b] = self.pl
            if win==-1:
                print("Victory player1!")
                return 1
            elif win==0:
                # print("It's a tie!")
                return 0
            else:
                return -1
            
            # else:
            #     print("Wrong value 'turns' in method 'Move()'")
            #     return None

    def Reset(self, mode='pc'):
        self.game = np.zeros((3,3), np.int8)
        self.mode = mode
        self.first = not(self.first)
        self.turn = self.first
