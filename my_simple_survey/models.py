from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Elena Asparouhova'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_simple_survey'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField()
    age = models.IntegerField()
    gender = models.StringField(
        choices=['Male', 'Female', 'Other'],
        verbose_name='What is your gender?',
        widget=widgets.RadioSelect)

    politics = models.StringField(
        choices=['Republican', 'Democrat', 'Other'],
        verbose_name='What is your political party?',
        widget=widgets.RadioSelect)

    moniker = models.StringField(
        choices=['Jacob', 'Janet', 'John', 'Jessica'],
        verbose_name='What experimental moniker would you like your results reported under?',
        widget=widgets.RadioSelect)
