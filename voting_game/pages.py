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
        return {
            'straw_vote': self.group.total_blue_straw,
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
