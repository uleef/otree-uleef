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
    players_per_group = 12 ## players must be multiple of 3.
    task_timer = 120
    task_timer2 = 300

    ##Excel Styles

    #Bold for headers
    # font0 = xlwt.Font()
    # font0.bold = True
    #
    # style0 = xlwt.XFStyle()
    # style0.font = font0
    #
    # #Highleighted for round that calculates payoff
    # font1 = xlwt.Font()
    # font1.colour_index = 2
    #
    # style1 = xlwt.XFStyle()
    # style1.font = font1
    #
    # ##Normal
    # fontNormal = xlwt.Font()
    # fontNormal.colour_index = 0
    #
    # styleNormal = xlwt.XFStyle()
    # styleNormal.font = fontNormal

    ## 1/3 of the participants are selectors -- these are players in room B
    ## 2/3 of the participants are playors -- these are players in room A
    selectors = int(players_per_group/3)
    players = int((players_per_group/3)*2)

    rounds = players - 1

    #### DON'T NEED ANY WORKBOOK STUFF BECAUSE OF HEROKU
    # resultsBook = Workbook()
    # resultsSheet = resultsBook.add_sheet('Results Sheet')

    ##random numbers for payoffs

    randomRound = random.randint(1,rounds)
    randomSelector = random.randint(1,selectors)*3
    randomLocationAdjust = random.randint(0, 1)

    participantVarList = ['name','nametag','task1_payoff','task2_payoff']

    INTS1 = [[17.0, 48.0], [49.0, 14.0], [18.0, 34.0], [39.0, 11.0], [17.0, 39.0], [11.0, 15.0], [31.0, 43.0], [46.0, 46.0], [37.0, 15.0], [32.0, 25.0], [17.0, 38.0], [40.0, 31.0], [44.0, 47.0], [35.0, 18.0], [41.0, 18.0], [26.0, 39.0], [14.0, 50.0], [32.0, 35.0], [45.0, 12.0], [39.0, 22.0], [14.0, 19.0], [43.0, 35.0], [26.0, 28.0], [35.0, 45.0], [18.0, 30.0], [24.0, 28.0], [44.0, 37.0], [27.0, 18.0], [22.0, 18.0], [26.0, 49.0], [43.0, 44.0], [24.0, 13.0], [21.0, 34.0], [14.0, 18.0], [25.0, 13.0], [36.0, 37.0], [29.0, 33.0], [41.0, 45.0], [34.0, 34.0], [38.0, 35.0], [38.0, 20.0], [40.0, 22.0], [39.0, 28.0], [25.0, 15.0], [12.0, 44.0], [46.0, 39.0], [11.0, 22.0], [40.0, 15.0], [11.0, 28.0], [47.0, 49.0], [25.0, 24.0], [11.0, 40.0], [46.0, 21.0], [30.0, 49.0], [25.0, 28.0], [48.0, 45.0], [25.0, 14.0], [37.0, 29.0], [24.0, 48.0], [31.0, 21.0], [49.0, 49.0], [42.0, 36.0], [12.0, 40.0], [46.0, 41.0], [24.0, 33.0], [22.0, 40.0], [49.0, 36.0], [35.0, 37.0], [35.0, 16.0], [25.0, 16.0], [24.0, 44.0], [30.0, 11.0], [30.0, 46.0], [36.0, 24.0], [25.0, 25.0], [16.0, 39.0], [24.0, 48.0], [26.0, 32.0], [26.0, 49.0], [39.0, 33.0], [47.0, 42.0], [21.0, 27.0], [43.0, 19.0], [16.0, 19.0], [34.0, 23.0], [32.0, 25.0], [16.0, 20.0], [47.0, 33.0], [28.0, 28.0], [29.0, 38.0], [33.0, 13.0], [46.0, 20.0], [47.0, 36.0], [23.0, 13.0], [49.0, 27.0], [12.0, 17.0], [17.0, 30.0], [47.0, 16.0], [34.0, 11.0], [39.0, 28.0], [25.0, 22.0], [27.0, 27.0], [25.0, 12.0], [33.0, 34.0], [12.0, 32.0], [33.0, 16.0], [37.0, 28.0], [31.0, 24.0], [37.0, 32.0], [15.0, 50.0], [27.0, 27.0], [18.0, 25.0], [43.0, 40.0], [32.0, 45.0], [11.0, 26.0], [27.0, 42.0], [23.0, 29.0], [37.0, 48.0], [16.0, 32.0], [47.0, 28.0], [32.0, 17.0], [41.0, 45.0], [21.0, 46.0], [14.0, 19.0], [48.0, 21.0]]


    num_rounds = (2*len(INTS1) + players)

    INTS2 = [[75.0, 51.0], [83.0, 87.0], [67.0, 88.0], [62.0, 54.0], [65.0, 98.0], [62.0, 74.0], [75.0, 77.0], [78.0, 79.0], [53.0, 93.0], [87.0, 66.0], [60.0, 57.0], [78.0, 61.0], [75.0, 86.0], [83.0, 94.0], [92.0, 76.0], [54.0, 67.0], [54.0, 75.0], [54.0, 73.0], [73.0, 62.0], [82.0, 73.0], [54.0, 83.0], [79.0, 96.0], [97.0, 89.0], [75.0, 85.0], [52.0, 87.0], [66.0, 69.0], [95.0, 64.0], [65.0, 95.0], [61.0, 77.0], [77.0, 51.0], [92.0, 85.0], [92.0, 69.0], [73.0, 85.0], [85.0, 63.0], [66.0, 90.0], [94.0, 60.0], [87.0, 79.0], [78.0, 60.0], [72.0, 51.0], [77.0, 89.0], [97.0, 66.0], [83.0, 78.0], [85.0, 94.0], [86.0, 68.0], [64.0, 67.0], [89.0, 95.0], [61.0, 84.0], [53.0, 59.0], [81.0, 67.0], [71.0, 95.0], [98.0, 93.0], [87.0, 74.0], [76.0, 84.0], [71.0, 82.0], [70.0, 53.0], [98.0, 97.0], [54.0, 79.0], [66.0, 57.0], [73.0, 73.0], [69.0, 63.0], [86.0, 61.0], [61.0, 82.0], [59.0, 68.0], [94.0, 55.0], [56.0, 51.0], [56.0, 82.0], [95.0, 59.0], [81.0, 53.0], [97.0, 84.0], [87.0, 54.0], [94.0, 82.0], [86.0, 94.0], [66.0, 58.0], [61.0, 73.0], [92.0, 79.0], [75.0, 63.0], [92.0, 51.0], [51.0, 93.0], [58.0, 89.0], [65.0, 97.0], [85.0, 77.0], [86.0, 90.0], [55.0, 52.0], [89.0, 81.0], [61.0, 52.0], [72.0, 59.0], [84.0, 76.0], [99.0, 60.0], [84.0, 97.0], [57.0, 63.0], [96.0, 74.0], [62.0, 81.0], [82.0, 57.0], [90.0, 69.0], [93.0, 77.0], [53.0, 56.0], [76.0, 86.0], [82.0, 56.0], [90.0, 73.0], [78.0, 86.0], [67.0, 91.0], [71.0, 76.0], [51.0, 59.0], [84.0, 82.0], [62.0, 70.0], [96.0, 67.0], [89.0, 57.0], [74.0, 81.0], [84.0, 78.0], [74.0, 59.0], [87.0, 73.0], [81.0, 78.0], [88.0, 92.0], [89.0, 66.0], [78.0, 55.0], [79.0, 87.0], [55.0, 95.0], [91.0, 64.0], [74.0, 62.0], [69.0, 53.0], [84.0, 80.0], [85.0, 97.0], [91.0, 73.0], [57.0, 97.0], [61.0, 71.0]]




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

        # used if python list is used
        if self.round_number < ((Constants.num_rounds - Constants.players) / 2):
            for p in players:
                p.task_timer = task_timer
                p.int1 = Constants.INTS1[self.round_number - 1][0]
                p.int2 = Constants.INTS1[self.round_number - 1][1]
                p.solution = p.int1 + p.int2
        elif self.round_number >= ((Constants.num_rounds - Constants.players) / 2) and self.round_number < Constants.num_rounds - Constants.players:
            for p in players:
                p.task_timer = task_timer
                p.int1 = Constants.INTS2[self.round_number - len(Constants.INTS1)][0]
                p.int2 = Constants.INTS2[self.round_number - len(Constants.INTS1)][1]
                p.solution = p.int1 + p.int2
        else:
            pass

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
