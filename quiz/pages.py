from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants
import time

class Start(Page):

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # user has 5 minutes to complete as many pages as possible
        self.participant.vars['expiry'] = time.time() + 5*60


class Signin(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model='player'
    form_fields = ['name',]

class Question(Page):
    form_model = 'player'
    form_fields = ['submitted_answer']
    timer_text = 'Time left to complete this section:'
    timeout_submission={'submitted_answer':0}



    def submitted_answer_choices(self):
        qd = self.player.current_question()
        # return [
        #     qd['choice1'],
        #     qd['choice2'],
        #     qd['choice3'],
        #     qd['choice4'],
        # ]

    def before_next_page(self):
        self.player.check_correct()

    def is_displayed(self):
        return self.participant.vars['expiry'] - time.time() > 1

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()

        return {
            'player_in_all_rounds': player_in_all_rounds,
            'questions_correct': sum([bool(p.is_correct) for p in player_in_all_rounds]),
            'questions_attempted': sum([bool(p.attempted) for p in player_in_all_rounds])
        }

class Nametag(Page):
    form_model='player'
    form_fields=['nametag']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Signin,
    Start,
    Question,
    Results,
    Nametag
]
