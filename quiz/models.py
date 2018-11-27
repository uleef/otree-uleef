from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv
import random

author = 'Your name here'


class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None

    with open('quiz/quiz1.csv') as questions_file:
        questions = list(csv.DictReader(questions_file))

    num_rounds = len(questions)
    with open('quiz/nametag.csv') as n_file:
        nametag=[]
        n_reader=csv.reader(n_file)
        for row in n_reader:
            nametag.append(row[0])

        nametag=nametag[1:]
    # print(nametag)


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:

            self.session.vars['questions'] = Constants.questions.copy()
            ## ALTERNATIVE DESIGN:
            ## to randomize the order of the questions, you could instead do:

            # import random
            # randomized_questions = random.sample(Constants.questions, len(Constants.questions))
            # self.session.vars['questions'] = randomized_questions

            ## and to randomize differently for each participant, you could use
            ## the random.sample technique, but assign into participant.vars
            ## instead of session.vars.

        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = int(question_data['id'])
            p.question = question_data['question']
            p.solution = question_data['solution']
            #print(p.question_id,p.question,p.solution)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question_id = models.IntegerField()
    name=models.StringField()
    question = models.StringField()
    solution = models.StringField()
    nametag = models.StringField(
        choices=Constants.nametag
    )
    submitted_answer = models.IntegerField(min=0)#models.StringField(widget=widgets.RadioSelect)
    is_correct = models.BooleanField()
    attempted = models.BooleanField()

    def current_question(self):
        return self.session.vars['questions'][self.round_number - 1]

    def check_correct(self):
        self.is_correct = (str(self.submitted_answer) == self.solution)
        self.attempted = True
        print(Constants.nametag)
