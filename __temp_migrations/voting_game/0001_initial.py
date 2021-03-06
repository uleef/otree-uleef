# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-04-02 02:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import otree.db.models
import otree_save_the_change.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('total_blue', otree.db.models.IntegerField(null=True)),
                ('total_green', otree.db.models.IntegerField(null=True)),
                ('total_blue_straw', otree.db.models.IntegerField(null=True)),
                ('total_green_straw', otree.db.models.IntegerField(null=True)),
                ('listnum', otree.db.models.IntegerField(null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voting_game_group', to='otree.Session')),
            ],
            options={
                'db_table': 'voting_game_group',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_gbat_arrived', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_gbat_grouped', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('jar', otree.db.models.StringField(max_length=10000, null=True)),
                ('decision', otree.db.models.StringField(max_length=10000, null=True)),
                ('ball_color', otree.db.models.StringField(choices=[('Blue', 'Blue'), ('Green', 'Green')], max_length=10000, null=True)),
                ('ball_straw', otree.db.models.StringField(choices=[('Blue', 'Blue'), ('Green', 'Green')], max_length=10000, null=True)),
                ('ball_vote', otree.db.models.StringField(choices=[('Blue', 'Blue'), ('Green', 'Green')], max_length=10000, null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='voting_game.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voting_game_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voting_game_player', to='otree.Session')),
            ],
            options={
                'db_table': 'voting_game_player',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voting_game_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'voting_game_subsession',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voting_game.Subsession'),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voting_game.Subsession'),
        ),
    ]
