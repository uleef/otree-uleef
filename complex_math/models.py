from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)

import pandas as pd
import numpy as np
import csv
import random
import xlrd

import xlwt
from xlwt import Workbook


author = 'Gus Stevens'

doc = """
This app is a two room game were participants in Room A complete a task and are selected by participants in Room B
based of their score on task 1 and the nametag that they selected from a drop down list.
Payoff is calculated by a players task 1 score plus task 2 score that is adjusted if they are selected to be on a team.

The models.py code is the backbone of the program. Pages.py is the implementation and the funtional code that creates the game which 
the user sees online.
"""

'''
Class Constants
this class creates the constant values that are used in the game. These are the only hardcoded numbers and can be changed as desired.
INTS can be read in from a CSV file using dictReader
'''
class Constants(BaseConstants):

    name_in_url = 'complex_math_game'
    players_per_group = 6 ## players must be multiple of 3.
    task_timer = 1

    ##Excel Styles

    #Bold for headers
    font0 = xlwt.Font()
    font0.bold = True

    style0 = xlwt.XFStyle()
    style0.font = font0

    #Highleighted for round that calculates payoff
    font1 = xlwt.Font()
    font1.colour_index = 2

    style1 = xlwt.XFStyle()
    style1.font = font1

    ##Normal
    fontNormal = xlwt.Font()
    fontNormal.colour_index = 0

    styleNormal = xlwt.XFStyle()
    styleNormal.font = fontNormal

    ## 1/3 of the participants are selectors -- these are players in room B
    ## 2/3 of the participants are playors -- these are players in room A
    selectors = int(players_per_group/3)
    players = int((players_per_group/3)*2)
    rounds = players - 1

    resultsBook = Workbook()
    resultsSheet = resultsBook.add_sheet('Results Sheet')

    ##random numbers for payoffs
    randomRound = random.randint(1,rounds)
    randomSelector = random.randint(1,selectors)*3
    randomLocationAdjust = random.randint(0, 1)

    participantVarList = ['name','nametag','task1_payoff','task2_payoff']

    # INTS1 = [
    #         [1, 0],
    #         [4, 1],
    #         [0, 2],
    #         [1, 19],
    #         [34, 1],
    #         [4, 12],
    #         [2, 1],
    #         [4, 1],
    #         [0, 2],
    #         [1, 19],
    #
    #         [34, 1],
    #         [4, 12],
    #         [2, 1],
    #         [3,1],
    #         [4,4],
    #         [6,8],
    #         [2,6],
    #         [7,10],
    #         [11,3],
    #         [1,5]]
    # num_rounds = (2*len(INTS1) + players)


    INTS1book = xlrd.open_workbook('complex_math/INTS1.xls')
    INTS1 = INTS1book.sheet_by_index(0)
    INTS2book = xlrd.open_workbook('complex_math/INTS2.xls')
    INTS2 = INTS2book.sheet_by_index(0)
    num_rounds = 2*(INTS1.nrows) + players

    # INTS2 = [
    #         [1, 0],
    #         [4, 1],
    #         [0, 2],
    #         [1, 19],
    #         [34, 1],
    #         [4, 12],
    #         [2, 1],
    #         [4, 1],
    #         [0, 2],
    #         [1, 19],
    #
    #         [34, 1],
    #         [4, 12],
    #         [2, 1],
    #         [3,1],
    #         [4,4],
    #         [6,8],
    #         [2,6],
    #         [7,10],
    #         [11,3],
    #         [1,5]]


'''
Class that is called before each subsession to create the math tasks for players.
'''
class Subsession(BaseSubsession):

    def before_session_starts(self):

        players = self.get_players()
        if 'task_timer' in self.session.config:
            task_timer = self.session.config['task_timer']
        else:
            task_timer = Constants.task_timer

        # used if XLS list is used for questions
        if self.round_number < ((Constants.num_rounds - Constants.players) / 2):
            for p in players:
                p.task_timer = task_timer
                p.int1 = Constants.INTS1.cell_value(self.round_number - 1, 0)
                p.int2 = Constants.INTS1.cell_value(self.round_number - 1, 1)
                p.solution = p.int1 + p.int2
        elif self.round_number >= ((Constants.num_rounds - Constants.players) / 2) and self.round_number < Constants.num_rounds - Constants.players:
            for p in players:
                p.task_timer = task_timer
                p.int1 = Constants.INTS2.cell_value(self.round_number - (Constants.INTS1.nrows),0)
                p.int2 = Constants.INTS2.cell_value(self.round_number - (Constants.INTS1.nrows),1)
                p.solution = p.int1 + p.int2
        else:
            pass

        # used if python list is used
        # if self.round_number < ((Constants.num_rounds - Constants.players) / 2):
        #     for p in players:
        #         p.task_timer = task_timer
        #         p.int1 = Constants.INTS1[self.round_number - 1][0]
        #         p.int2 = Constants.INTS1[self.round_number - 1][1]
        #         p.solution = p.int1 + p.int2
        # elif self.round_number >= ((Constants.num_rounds - Constants.players) / 2) and self.round_number < Constants.num_rounds - Constants.players:
        #     for p in players:
        #         p.task_timer = task_timer
        #         p.int1 = Constants.INTS2[self.round_number - 20][0]
        #         p.int2 = Constants.INTS2[self.round_number - 20][1]
        #         p.solution = p.int1 + p.int2
        # else:
        #     pass

class Group(BaseGroup):
    pass

'''
This is the most important class. This class contains all of the player variables that are calable by the player in pages.py
Each player in the game has a set of variables determined by this selection, each variable is defined here and explained by comments
During the game these variables are manipulated and store player data such as their score and name.
'''
class Player(BasePlayer):

    ## method to get questoin from CSV file questions
    def current_question(self):
        return self.session.vars['questions'][self.round_number - 1]

    def role(self):
        if self.id_in_group % 3 == 0:
            return 'roomB'
        else:
            return 'roomA'

    ## player timer. The task timer is called and initiated when the task starts
    task_timer = models.PositiveIntegerField()

    ## used to store name that is entered by the player
    name = models.StringField()

    ## Excel file with nametags - entire file : this file has a unique set of names for each letter in the alphabet
    loc = 'complex_math/nametags.xlsx'
    nametagBook = xlrd.open_workbook(loc)

    ## this variable is the nametag that the player selects. The nametag choices for this variable are determined during the game
    nametag = models.StringField()

    ## variable that stores the name that the 'chooser' selected during the team selection page
    sentNames = models.StringField()


    ## these variables store data relating to the player and selector task
    int1 = models.PositiveIntegerField()
    int2 = models.PositiveIntegerField()
    solution = models.PositiveIntegerField()
    user_total = models.PositiveIntegerField(
        min=1,
        max=9999,
        widget=widgets.TextInput(attrs={'autocomplete':'off'})
    )


    task1payoff_score = models.FloatField()
    task2payoff_score = models.FloatField()

    '''
    the score_task methods are called to update a players taskpayoff score.
    there are two methods and are used for the seperate task1 and task2
    '''
    def score_task1(self):
        if self.solution == self.user_total:
            self.task1payoff_score = 1.0
        else:
            self.task1payoff_score = 0.0



    def score_task2(self):
        if self.solution == self.user_total:
            self.task2payoff_score = 1.0
        else:
            self.task2payoff_score = 0.0
