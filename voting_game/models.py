from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
This is a voting game that is played in {{Constants.num_rounds}}.
"""


class Constants(BaseConstants):
    name_in_url = 'voting_game'
    players_per_group = 3
    num_rounds = 4
    rightdecision=c(500) #the payoff if the group reaches a decision and it is correct
    nodecision=c(0) #the payoff if the group does not reach a decision
    wrongdecision=c(100) #the payoff if the group reaches a decision but it is the wrong one
    bluebias=c(50) #payoff for casting a particular vote ()
    trueurn = [1, 0, 1, 0]
    Un=[1, 3] #Rounds in which the voting rule is Unanimity
    Delib=[2, 4] #Rounds in which straw vote is also collected

    majority=(players_per_group-1)/2



class Subsession(BaseSubsession):

    def creating_session(self):
        self.group_randomly()
        
class Group(BaseGroup):
    total_blue=models.IntegerField()
    total_blue_straw=models.IntegerField()
    listnum=models.IntegerField()

    def set_payoffs(self):
        total_blue_straw=-1
        if self.round_number in Constants.Delib:
            self.total_blue_straw=sum([1 for p in self.get_players() if (p.ball_straw=='Blue')])
        self.total_blue = sum([1 for p in self.get_players() if (p.ball_vote=='Blue') ])
        for player in self.get_players():
            listnum=self.round_number-1
            if self.round_number in Constants.Un:
                if self.total_blue == Constants.players_per_group:
                    player.payoff = (Constants.rightdecision)*(Constants.trueurn[listnum]==1)+Constants.wrongdecision*(Constants.trueurn[listnum]==0)+(player.ball_vote == 'Blue')*Constants.bluebias
                elif self.total_blue == 0:
                    player.payoff = Constants.wrongdecision*(Constants.trueurn[listnum]==1)+(Constants.rightdecision)*(Constants.trueurn[listnum]==0)+(player.ball_vote == 'Blue')*Constants.bluebias
                else:
                    player.payoff = Constants.nodecision+(player.ball_vote == 'Blue')*Constants.bluebias
            else:
                if self.total_blue > Constants.majority:
                    player.payoff = (Constants.rightdecision)*(Constants.trueurn[listnum]==1)+Constants.wrongdecision*(Constants.trueurn[listnum]==0)+(player.ball_vote == 'Blue')*Constants.bluebias
                else:
                    player.payoff = Constants.wrongdecision*(Constants.trueurn[listnum]==1)+(Constants.rightdecision)*(Constants.trueurn[listnum]==0)+(player.ball_vote == 'Blue')*Constants.bluebias



class Player(BasePlayer):
    ball_color = models.CharField(
        choices=['Blue', 'Green'],
        widget=widgets.RadioSelect
    )
    ball_straw = models.CharField(
        choices=['Blue', 'Green'],
        widget=widgets.RadioSelect
    )
    ball_vote = models.CharField(
        choices=['Blue', 'Green'],
        widget=widgets.RadioSelect
    )
