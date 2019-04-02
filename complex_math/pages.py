
import time
import operator

from . import models
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import os
import collections
import pandas as pd
import random

import xlwt
from xlwt import Workbook

## INSTRUCTIONS FOR ROUND 2
    ## round 1 instructions include outline of the game (round 1 and round 2 instructions tell that this is round 2)
## set the task timer after instructions


author = 'Gus Stevens'

doc = """
The pages.py part of the app controls the sequence of pages that are showed to the user and contains most of the code that updates and changes
player variables.
"""

'''
Signin page to get user name or whatever they choose to enter and set up session and participant variables
'''
class Signin(Page):



    def is_displayed(self):
        ## delete old excel page before anything else happens

        directoryPath = 'complex_math/Results'
        fileList = os.listdir(directoryPath)
        for fileName in fileList:
            os.remove(directoryPath + "/" + fileName)
        return self.round_number ==1

    form_model='player'
    form_fields = ['name']

    '''
    THE MOST IMPORTANT PART OF THE GAME
    
    the session and participant variables are incredibly important for sharing data player data between rounds and accross the session.
    
    self.participant.vars[] is a list that can store any type of data as long as it is initialized.
    data stored in self.participant.vars[] is accesable in all rounds and will always be available for the player.
    
    self.session.vars[] is also a list like .participant.vars[] and can store all forms of data
    but it is accessable by all players so it is good for storing information that needs to be passed between players.
    '''


    def before_next_page(self):
        self.session.vars['sentNames'] = {}
        self.participant.vars['sentNames_choices'] = []
        self.participant.vars['selectionTable'] = []


        self.participant.vars['name'] = ''
        self.participant.vars['nametag'] = ''
        self.participant.vars['task1_payoff'] = float
        self.participant.vars['task2_payoff'] = float
        self.participant.vars['total_payoff'] = float

        ## contains a payoff for every selector per participant.
        self.participant.vars['total_payoffs'] = {}

        for i in range (1, Constants.players_per_group + 1):
            if i % 3 == 0:
                self.participant.vars['total_payoffs'][i] = []

        self.session.vars['SelectorInformation'] = {}

        ##trackers used accross players
        self.participant.vars['playerBchoicesTracker'] = 0

        ## make these variables random for legitness

        ## the name captured fromt he signin formfield is stored in the particpant.vars list
        self.participant.vars['name'] = self.player.name


        ## if user names are the same then their will be a problem. Ask to sign in with first and last name...?
        if self.player.id_in_group == 3:
            ## only make workbook once.
            Constants.resultsSheet.write(0, 1, 'Player Nametag', Constants.style0)
            Constants.resultsSheet.write(0, 2, 'Task 1 Payoff', Constants.style0)
            Constants.resultsSheet.write(0, 3, 'Task 2 Payoff', Constants.style0)
            Constants.resultsSheet.write(0, 4, 'Selected As Team', Constants.style0)
            Constants.resultsSheet.write(0, 5, 'Total Payoff', Constants.style0)

        '''
           index and columns are created for the data frame to create a matrix to store the rounds and player selections
           index: is players - 1 indexes to reflect the number of selection rounds ... if there are 4 players then there are 3 selection rounds
           columns: is the number of selectors.
           The data frame created is RoundsWithTeam, it is in the sentResults page  to store if a player was selected by a selector
           '''
        index = []
        for i in range(Constants.players - 1):
            index.append(1 + i)

        columns = []
        for z in range(Constants.selectors):
            columns.append(1 + i)

        self.participant.vars['RoundsWithTeam'] = pd.DataFrame(index=index,columns=columns)


        # fill workbook with player names and round rows -- make this to include all the data
        def writeRounds(self,sheet,start):
            interval = (Constants.selectors + (Constants.selectors*Constants.rounds))
            end = start + interval
            round = 1
            selectorPrint = start + 1;
            namePrint = start

            while start <= end:
                if start == namePrint:
                    sheet.write(start,0,self.participant.vars['name'],Constants.style0)
                elif start == selectorPrint:
                    selectorPrint+= Constants.players
                    round = 1
                else:
                    sheet.write(start,0,'       round '+str(round % selectorPrint))
                    round += 1
                start +=1

        start = (self.player.id_in_group - 1) * (Constants.players * Constants.selectors) + self.player.id_in_group
        writeRounds(self,Constants.resultsSheet,start)
        self.participant.vars['expiry_timestamp'] = time.time() + self.player.task_timer



'''
page contains instructions
'''
class Start(Page):
    def is_displayed(self):
        return self.round_number == 1
    def before_next_page(self):
        # self.participant.vars['expiry_timestamp'] = time.time() + self.player.task_timer
        pass



'''
RoomATask is the first task that is shown to both rooms. It is a series of simple math questions that are scored and stored 
in the participant vars
'''
class RoomATask(Page):
    form_model = 'player'
    form_fields = ['user_total']


    def get_timeout_seconds(self):
        return self.participant.vars['expiry_timestamp'] - time.time()

    ## before each page the is_displayed method is used to determine if the player can enter the page
    ## this game focuses a lot on round numbers so the is displayed is used to keep the player in the page that they are supposed to see
    def is_displayed(self):
        return self.participant.vars['expiry_timestamp'] - time.time() > 3 and (self.round_number < (Constants.num_rounds - Constants.players)/2)

    def vars_for_template(self):

        task1payoff = 0.0
        task2payoff = 0.0

        '''
        ***IMPORTANT***
        
        Every round creates another player instance. Each player instance has its own set of variables from the players class in the models page
        This means that accross all rounds only certain rounds will have the data that was generated from the page
        for example if a player correctly solves a problem in round 2 there task1payoff will be 1
        if the same player correctly solves a problem in round 4 theire task1payoff in round for will be 1.
        
        seperate rounds mean that the model variables are not shared or cummulative. For this reason we must iterate oveer all of a players instances
        accross all rounds to collect data and then store the data in the participant.vars[] so that it can be accessed in all rounds.
        '''
        for p in self.player.in_all_rounds():
            if p.task1payoff_score != None:
                task1payoff += p.task1payoff_score

            if p.task2payoff_score != None:
                task2payoff += p.task2payoff_score


        self.participant.vars['task1_payoff'] = task1payoff
        self.participant.vars['task2_payoff'] = task2payoff

        return {
            'total_payoff': round(self.participant.vars['task1_payoff']),
        }

    def before_next_page(self):
        self.player.score_task1()

'''
wait pages exist to keep players on the same pace. They are also important to ensure that data is saved and sent before it is shown in a page
it is easy to get errors if you are progressing to quickly to pages that require user data that has not yet been generated because a player is slow
'''
class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == (Constants.num_rounds - Constants.players)  / 2
    def after_all_players_arrive(self):
        pass

class Task2instructions(Page):

    def is_displayed(self):
        return self.round_number == (Constants.num_rounds - Constants.players)  / 2

    form_model = 'player'
    form_fields = ['nametag']

    '''
    nametag_choices is returns a list of strings that are become the choices in the field that is shown to the player
    '''
    def nametag_choices(self):
        ## gets sheet based on player id
        namesSheet = self.player.nametagBook.sheet_by_index(self.player.id_in_group)
        choices = []
        for i in range(namesSheet.nrows):
            choices.append(namesSheet.cell_value(i,0))
        return choices

    def vars_for_template(self):
        task1payoff = 0.0
        for p in self.player.in_all_rounds():
            if p.task1payoff_score != None:
                task1payoff += p.task1payoff_score

        self.participant.vars['task1_payoff'] = task1payoff


        return {
            'total_payoff': round(self.participant.vars['task1_payoff'])
        }

    def before_next_page(self):
        self.player.task_timer = Constants.task_timer
        self.participant.vars['expiry_timestamp'] = time.time() + self.player.task_timer


        ## names the columns of the data frame based on the provided names of the selectors
        for allPlayers in self.group.get_players():
            for p in allPlayers.in_all_rounds():
                if p.name != None and p.role() == 'roomB':
                    self.session.vars['SelectorInformation'][p.id_in_group] = p.name

        ##########
        ## Doing Everything by name makes it easy to break the code
        selectorNames = list(self.session.vars['SelectorInformation'].values())


        if len(selectorNames) == Constants.selectors:
            self.participant.vars['RoundsWithTeam'].columns = selectorNames

        ## add selector names to excel file
        def writeSelectors(self, sheet, start):
            interval = (Constants.selectors + (Constants.selectors * Constants.rounds))
            end = start + interval
            selectorPrint = start + 1;
            selector = 0
            while start <= end:
                if start == selectorPrint:
                    sheet.write(start,0,'   Selector ('+ selectorNames[selector] +')',Constants.style0)
                    selectorPrint += Constants.players
                    selector += 1
                start += 1

        start = (self.player.id_in_group - 1) * (Constants.players * Constants.selectors) + self.player.id_in_group

        writeSelectors(self, Constants.resultsSheet, start)



'''
RoomATask2 is the second math task that both players and selectors complete after they have selected a nametag.
This score is stored but not shown to other players, it is only used in calculating a payoff...
it is as if a selector chose a teammate and then they both completed another math task
'''
class RoomATask2(Page):
    form_model = 'player'
    form_fields = ['user_total']


    def get_timeout_seconds(self):
        return self.participant.vars['expiry_timestamp'] - time.time()

    def is_displayed(self):
        return self.participant.vars['expiry_timestamp'] - time.time() > 3 and (self.round_number >= (Constants.num_rounds - Constants.players)/2)


    def vars_for_template(self):

        task2payoff = 0.0
        for p in self.player.in_all_rounds():
            if p.task2payoff_score != None:
                task2payoff += p.task2payoff_score

        self.participant.vars['task2_payoff'] = task2payoff


        return {
            'total_payoff': round(self.participant.vars['task2_payoff']),
        }

    def before_next_page(self):
        self.player.score_task2()

## if one of the selector completes round 2 too quickly they will not have names to select form . get index out of bound
class waitForNames(WaitPage):

    def is_displayed(self):

        task1payoff = 0.0
        task2payoff = 0.0
        screen_name = ''

        ## have to iterate through all player rounds to pull data
        for p in self.player.in_all_rounds():
            if p.nametag != None and p.role() != 'roomB':
                screen_name = p.nametag

            if p.task1payoff_score != None:
                task1payoff += p.task1payoff_score

            if p.task2payoff_score != None:
                task2payoff += p.task2payoff_score

        self.participant.vars['task1_payoff'] = task1payoff
        self.participant.vars['task2_payoff'] = task2payoff
        self.participant.vars['nametag'] = screen_name

        ## adds the players nametag and their task1 score to a session.vars dictionary that can be accessed by all players
        if (self.round_number >= (Constants.num_rounds - Constants.players)):
            self.session.vars['sentNames'][screen_name] = round(self.participant.vars['task1_payoff'])

        ##deletes the empty entry that is there for some reason
        if '' in self.session.vars['sentNames']:
            del self.session.vars['sentNames']['']

        random

        return self.round_number == (Constants.num_rounds - Constants.players)

    def after_all_players_arrive(self):
        pass

'''
This class contains the code that determines what names are shown to the selectors
Team selection names are pulled from the self.session.vars['sentNames'] dictionary

Players are ordered by their score so that selections will contain players with similiar scores.
Selections are composed of 2 subsequent players in the list generated by 'sentNames'
There are Constants.players - 1 selection rounds
'''

class SentResults(Page):

    form_model = 'player'
    form_fields = ['sentNames']

    def is_displayed(self):

        ## sets selecting players nametag because was not set in waitForNames page
        screen_name = ''
        for p in self.player.in_all_rounds():
            if p.nametag != None:
                screen_name = p.nametag

        self.participant.vars['nametag'] = screen_name

        return ((self.participant.vars['playerBchoicesTracker'] <= (Constants.rounds) and self.round_number > Constants.num_rounds - (Constants.players) and self.round_number < Constants.num_rounds)) and ((self.player.role() == 'roomB'))


    ## chooses 2 names to show from session list
    def sentNames_choices(self):

        #sorts dictinoary into a list of ordered tuples by value
        tuples = sorted(self.session.vars['sentNames'].items(), key=lambda kv: kv[1])

        #converts list of tuples back to dictionary
        self.session.vars['sentNames'] = collections.OrderedDict(tuples)


        ## make the list of two choices
        for key in self.session.vars['sentNames']:
            self.participant.vars['sentNames_choices'].append(key + ', Score: ' + str(round(self.session.vars['sentNames'][key])))

        i = self.participant.vars['playerBchoicesTracker']

        choices = [self.participant.vars['sentNames_choices'][i],self.participant.vars['sentNames_choices'][i + 1]]

        return choices



    def before_next_page(self):

        ##playerBchoicesTracker is used to track the selection round that the selector is on, ensuring there are only players - 1 rounds
        self.participant.vars['playerBchoicesTracker'] += 1

        ## each player has a playerID. In this case the player ID is used to identify if a participant was a selector which automaticaly makes them a member of a team
        selectorID = self.player.id_in_group

        '''
        *** IMPORTANT FOR SCORING ***
        
        The loop below iterates through all the players in the group.
        for every player it accesses nametag and score data to determine if the player was a player selected by the selector
        
        If player credentials match that of the selected teamate then their RoundWithTeam dataframe will update to reflect their selection
        For exampole. If James in selection round 3 chooses Kate, score 3 then Kate will recieve a 1.2 multiplier in the cell with index (3,James)
        '''

        ## loop to iterate through all players in the group
        ## if player was selected 1 is added to roundsWithTeam matrix to show the selector and round that they were chosen
        for allPlayer in self.group.get_players():
            if allPlayer.id_in_group == selectorID:
                allPlayer.participant.vars['RoundsWithTeam'].at[Constants.num_rounds - self.round_number,self.participant.vars['name']] = 1
                ## order of selections are reversed -- smallest first
            else:
                if (allPlayer.participant.vars['nametag'] != self.player.sentNames.split()[0].replace(',','')) or (str(round(allPlayer.participant.vars['task1_payoff'])) != self.player.sentNames.split()[-1]):
                    allPlayer.participant.vars['selectionTable'].append(str(Constants.num_rounds - self.round_number) + (self.participant.vars['name']) + str(0))

                ## match the player name and the score that they recieved to the selected values
                if(allPlayer.participant.vars['nametag'] == self.player.sentNames.split()[0].replace(',','')) and (str(round(allPlayer.participant.vars['task1_payoff'])) == self.player.sentNames.split()[-1]):
                    allPlayer.participant.vars['selectionTable'].append(str(Constants.num_rounds - self.round_number) + (self.participant.vars['name']) + str(1))
                    allPlayer.participant.vars['RoundsWithTeam'].at[Constants.num_rounds - self.round_number,self.participant.vars['name']] = 1
            allPlayer.participant.vars['RoundsWithTeam'].fillna(0,inplace=True)

        # self.participant.vars['RoundsWithTeam'].fillna(0,inplace=True)

        '''
        Calculate participant payoffs
        '''

        selectorNames = list(self.session.vars['SelectorInformation'].values())
        selectorIDS = list(self.session.vars['SelectorInformation'].keys())
        i = int(self.player.id_in_group / 3) -1
        j = Constants.rounds - self.participant.vars['playerBchoicesTracker']

        print( )
        print( )
        print( )
        print( )
        print( )
        print( )
        for allPlayer in self.group.get_players():
            print(allPlayer.participant.vars['RoundsWithTeam'])
            print(allPlayer.participant.vars['RoundsWithTeam'][selectorNames[i]].values)
            print(Constants.rounds - self.participant.vars['playerBchoicesTracker'])
            if allPlayer.id_in_group not in selectorIDS and (allPlayer.participant.vars['RoundsWithTeam'][selectorNames[i]].values[j]):
            # if (allPlayer.participant.vars['RoundsWithTeam'][selectorNames[i]].values[j]):

                ## all player total payoff could be weighted average of every time they were selected. TALK TO LAB about payoff options
                    # 1. only one random selector and round
                    # 2. every chooser has an altered payoff, but it severely alters participant payoffs (current way)
                    # 3. average total payoff adjusted by how many times selected to be on a team
                    # 4. store every payoff in a dictionary -- i.e if there are two choosers store a payoff under the chooser name to present at the end of the game.

                allPlayer.participant.vars['total_payoffs'][selectorIDS[i]].append( ((allPlayer.participant.vars['task2_payoff'] + self.participant.vars['task2_payoff']) / 2) * 1.5 )
                self.participant.vars['total_payoffs'][selectorIDS[i]].append( ((allPlayer.participant.vars['task2_payoff'] + self.participant.vars['task2_payoff']) / 2) * 1.5 )
            elif not (allPlayer.participant.vars['RoundsWithTeam'][selectorNames[i]].values[j]):
                allPlayer.participant.vars['total_payoffs'][selectorIDS[i]].append(allPlayer.participant.vars['task2_payoff'])
            print(allPlayer.participant.vars['name'],'('+allPlayer.participant.vars['nametag']+'):',allPlayer.participant.vars['total_payoffs'],'selected',allPlayer.participant.vars['RoundsWithTeam'][selectorNames[i]].values[j])
        print()
        print()
        print()
        print()
        print()
        print()


class waitForTeams(WaitPage):

    def is_displayed(self):
        return (self.round_number < Constants.num_rounds and self.round_number >= Constants.num_rounds - (int(Constants.players/2)))  and self.player.role() == 'roomA'

class payoffWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == (Constants.num_rounds)
    def after_all_players_arrive(self):
        pass

'''
payoff page shows a players total payoff and is used to create the results workbook

a players multiplier is found in ther RoundsWithTeam dataFrame and is either 0 or 1 (meaning they were chosen on a team)
The payoff round is determined randomly at the start of the game
'''

## PAYOFF is determined as an average of the teams times 1.5 so selector has risk by selecting a female partner (who would desguise as a man)
## To identify teamates use random round and random number to determine if 1.5 is in the matrix. If both players have 1.5 in their matrix then average
## the score multiplied by the 1.5 multiplier that was taken form the matrix.

class Payoff(Page):
    def is_displayed(self):
        return self.round_number == (Constants.num_rounds)

    def vars_for_template(self):

        ## Get Selector Names for exel file
        selectorNames = list(self.session.vars['SelectorInformation'].values())
        selectorIDS = list(self.session.vars['SelectorInformation'].keys())

        ## edit matrix Rows to display round #
        numberOfrounds = []
        for i in range(0, Constants.players - 1):
            numberOfrounds.append('round ' + str(Constants.players - (i + 1)))

        self.participant.vars['RoundsWithTeam'].rows = numberOfrounds


        ##print stuff for figuring out where to write total payoffs
        # print(self.player.participant.vars['name'], '('+self.player.participant.vars['nametag']+')' ':', self.player.participant.vars['total_payoffs'])

        ## write player score and player variables
        location = (self.player.id_in_group - 1) * (Constants.players * Constants.selectors) + self.player.id_in_group + 2
        RandomRoundAdjust = Constants.randomRound
        differentSelectorName = 3
        round = 0


        print(self.participant.vars['total_payoffs'])

        for j in range (Constants.selectors * Constants.players):
            if (j + 1) % Constants.players == 0:
                differentSelectorName += 3
                round = 0
            else:
                if j + 1 == RandomRoundAdjust:
                    total_payoff = self.participant.vars['total_payoffs'][differentSelectorName][Constants.rounds - 1 - round]
                    style = Constants.style1
                    RandomRoundAdjust += Constants.players
                else:
                    total_payoff = self.participant.vars['total_payoffs'][differentSelectorName][Constants.rounds - 1 - round]
                    style = Constants.styleNormal

                for i in range (0,len(Constants.participantVarList) -1):
                    i+=1
                    Constants.resultsSheet.write(location+j,i,self.participant.vars[Constants.participantVarList[i]],style)
                Constants.resultsSheet.write(location+j,5,total_payoff,style)
                round += 1

        ## write team information
        start = ((self.player.id_in_group - 1) * (Constants.players * Constants.selectors) + self.player.id_in_group) + 2
        RandomRoundAdjust = Constants.randomRound
        selectorName = 0
        i = 0

        ## write player 1/0 based on selection

        for j in range (Constants.selectors * Constants.players):
            if (j + 1) % Constants.players == 0:
                selectorName += 1
                RandomRoundAdjust +=Constants.players
                i = 0
                continue
            else:
                if (j + 1) == RandomRoundAdjust:
                    style = Constants.style1
                else:
                    style = Constants.styleNormal
                Constants.resultsSheet.write(start+j,4,int(self.participant.vars['RoundsWithTeam'][selectorNames[selectorName]].values[i]),style)
                i += 1


        ## edit matrix Rows to display round #
        numberOfrounds = []
        for i in range(0, Constants.players - 1):
            numberOfrounds.append('round ' + str(Constants.players - (i + 1)))

        ## edit matrix to display selector Names

        self.participant.vars['RoundsWithTeam'].index = numberOfrounds

        self.participant.vars['RoundsWithTeam'].to_csv('complex_math/Results/'+self.participant.vars['name']+'.csv')
        Constants.resultsBook.save('complex_math/Results/Results.xls')

        sentNamesList = list(self.session.vars['sentNames'].keys())
        print(sentNamesList)
        if self.player.id_in_group in selectorIDS:
            total_payoff = self.participant.vars['total_payoffs'][self.player.id_in_group][Constants.randomRound -1]
        else:
            if self.player.participant.vars['nametag'] == sentNamesList[0]:
                total_payoff = self.participant.vars['total_payoffs'][Constants.randomSelector][0]
            elif self.player.participant.vars['nametag'] == sentNamesList[-1]:
                total_payoff = self.participant.vars['total_payoffs'][Constants.randomSelector][Constants.rounds - 1]
            else:
                location = sentNamesList.index(self.player.participant.vars['nametag'])
                print(location)
                print(Constants.randomLocationAdjust)

                total_payoff = self.participant.vars['total_payoffs'][Constants.randomSelector][location - Constants.randomLocationAdjust]
            ## actually random. but for testing we will use the first selector and first round
            # total_payoff = self.participant.vars['total_payoffs'][random.randint(1,Constants.selectors)*3][random.randint(0,Constants.rounds-1)]
            # total_payoff = self.participant.vars['total_payoffs'][3][Constants.randomRound -1]
        return {
            'total_payoff': total_payoff,
            'name': self.participant.vars['name']
        }




page_sequence = [
    Signin,
    # Start,
    RoomATask,
    ResultsWaitPage,
    Task2instructions,
    RoomATask2,
    waitForNames,
    SentResults,
    waitForTeams,
    payoffWaitPage,
    Payoff,
]