from lib import Const
from lib import Pokemon
import random
import requests
import json
import re


class Team:
	"""Stores groups of pokemon"""
	def __init__(self, team):
		self.team = team
		self.team_names = [p.name for p in team]
		self.score = self.__team_score__()

	def __eq__(self, other):
		return (set(self.team_names) == set(other.team_names))

	def __ne__(self, other):
		return (set(self.team_names) != set(other.team_names))

	def __hash__(self):
		val = 0
		for pname in self.team_names:
			val += hash(pname)
		return val

	def __team_score__(self):
		score = 0
		if len(self.team) == len(set(self.team)):
			type_list = []
			for poke in self.team:
				score += poke.score()
				if not(poke.types[0]['type']['name'] in type_list):
					type_list += [poke.types[0]['type']['name']]
				if len(poke.types) > 1:
					if not(poke.types[1]['type']['name'] in type_list):
						type_list += [poke.types[1]['type']['name']]

			score += len(type_list) * Const.DIV_FACTOR
		return score

	def __str__(self):
		ret = ""
		first = True
		for poke in self.team:
			if first:
				ret += "{" + str(poke)
				first = False
			else:
				ret += " || " + str(poke)
		ret += "} >> " + str(self.score)
		return ret

def random_team(tier):
	if Const.GENERAL_DEBUG:
		print("Creating random team...")
	tier_size = len(tier)
	team = []
	team_names = []
	for x in range(Const.TEAMSIZE):
		poke_name = tier[random.randint(0, tier_size-1)]
		while poke_name in set(team_names):
			if Const.GENERAL_DEBUG:
				print(poke_name + " already in team")
			poke_name = tier[random.randint(0, tier_size-1)]
		team += [Pokemon.fetch_pokemon(poke_name)]
		team_names += [poke_name]
	return team