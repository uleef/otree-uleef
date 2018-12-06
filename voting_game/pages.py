from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants




class Draw(Page):
    form_model = 'player'
    form_fields = ['ball_color']
    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
        }

class Straw(Page):
    form_model = 'player'
    form_fields = ['ball_straw']
    def is_displayed(self):
        return self.round_number in Constants.Delib
    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
        }

class StrawWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number in Constants.Delib
    def after_all_players_arrive(self):
        self.group.set_payoffs()

class Choice(Page):
    form_model = 'player'
    form_fields = ['ball_vote']
    def vars_for_template(self):
        if self.round_number in Constants.Delib:
            return {
            'straw_message1': 'The result of the Straw Vote is',
            'straw_vote1': self.group.total_blue_straw,
            'straw_message2': 'Blue and',
            'straw_vote2': self.group.total_green_straw,
            'straw_message3': 'Green.',

            }
        else:
            return {
            'straw_message1': 'No',
            'straw_vote1': 'straw',
            'straw_message2': 'vote',
            'straw_vote2': 'this round.',
            'straw_message3': 'Proceed to voting.',
            }



class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class ResultsSummary(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()

        return {
            'total_payoff': sum(
                [p.payoff for p in player_in_all_rounds]),
            'player_in_all_rounds': player_in_all_rounds,
        }


page_sequence = [
    Draw,
    Straw,
    StrawWaitPage,
    Choice,
    ResultsWaitPage,
    ResultsSummary
]
