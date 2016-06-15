from lib import Const
from lib import Type
import random
import requests
import json
import re


class Pokemon:
	"""Stores individual pokemon data"""
	def __init__(self, name):
		pokedata = requests.get(Const.API_BASE+Const.POKE_END+name)
		pokedata = pokedata.json()
		self.name = name
		self.stats = pokedata['stats']
		self.types = pokedata['types']
		self.abilities = pokedata['abilities']
		sprite_url = re.search('.*\/([0-9]+\.png)', pokedata['sprites']['front_default'])
		self.sprite_name = sprite_url.group(1)
		self.def_typing = self.__def_typing__()
		self.typing_score = self.__typing_score__()
		self.stat_score = self.__stat_score__()
		self.ability_score = self.__ability_score__()

	def __def_typing__(self):
		type_info = {}
		abset = set([ab['ability']['name'] for ab in self.abilities])
		if len(self.types) == 1:
			type1_info = Type.fetch_type(self.types[0]['type']['name']).damage_relations
			type_info['no_damage_from'] = [t['name'] for t in type1_info['no_damage_from']]
			type_info['quarter_damage_from'] = []
			type_info['half_damage_from'] = [t['name'] for t in type1_info['half_damage_from']]
			type_info['double_damage_from'] = [t['name'] for t in type1_info['double_damage_from']]
			type_info['quadra_damage_from'] = []
		else:
			type1_info = Type.fetch_type(self.types[0]['type']['name']).damage_relations
			type2_info = Type.fetch_type(self.types[1]['type']['name']).damage_relations

			no1 = [t['name'] for t in type1_info['no_damage_from']]
			no2 = [t['name'] for t in type2_info['no_damage_from']]

			set_no1 = set(no1)
			set_no2 = set(no2)

			half1 = list(set([t['name'] for t in type1_info['half_damage_from']]) - set_no1 - set_no2)
			half2 = list(set([t['name'] for t in type2_info['half_damage_from']]) - set_no1 - set_no2) 

			double1 = list(set([t['name'] for t in type1_info['double_damage_from']]) - set_no1 - set_no2)
			double2 = list(set([t['name'] for t in type2_info['double_damage_from']]) - set_no1 - set_no2)

			set_half1 = set(half1)
			set_half2 = set(half2)

			set_double1 = set(double1)
			set_double2 = set(double2)

			type_info['no_damage_from'] = list(set_no1.union(set_no2))
			type_info['quarter_damage_from'] = list(set_half1.intersection(set_half2))
			type_info['quadra_damage_from'] = list(set_double1.intersection(set_double2))

			set_neutral = set_half1.intersection(set_double2).union(set_half2.intersection(set_double1))

			type_info['half_damage_from'] = list(set_half1.union(set_half2) - set_neutral)
			type_info['double_damage_from'] = list(set_double1.union(set_double2) - set_neutral)

		if "levitate" in abset:
			type_info['no_damage_from'] = list(set(type_info['no_damage_from']).union(set(['ground'])))
			type_info['quarter_damage_from'] = list(set(type_info['quarter_damage_from']) - set(['ground']))
			type_info['half_damage_from'] = list(set(type_info['half_damage_from']) - set(['ground']))
			type_info['double_damage_from'] = list(set(type_info['double_damage_from']) - set(['ground']))
			type_info['quadra_damage_from'] = list(set(type_info['quadra_damage_from']) - set(['ground']))

		if (("heatproof" in abset) or ("thick-fat" in abset)):
			if "fire" in set(type_info['half_damage_from']):
				type_info['quarter_damage_from'] = list(set(type_info['quarter_damage_from']).union(set(['fire'])))
				type_info['half_damage_from'] = list(set(type_info['half_damage_from']) - set(['fire']))

			elif "fire" in set(type_info['double_damage_from']):
				type_info['double_damage_from'] = list(set(type_info['double_damage_from']) - set(['fire']))

			elif "fire" in set(type_info['quadra_damage_from']):
				type_info['double_damage_from'] = list(set(type_info['double_damage_from']).union(set(['fire'])))
				type_info['quadra_damage_from'] = list(set(type_info['quadra_damage_from']) - set(['fire']))
			else:
				type_info['half_damage_from'] = list(set(type_info['half_damage_from']).union(set(['fire'])))

			if "ice" in set(type_info['half_damage_from']):
				type_info['quarter_damage_from'] = list(set(type_info['quarter_damage_from']).union(set(['ice'])))
				type_info['half_damage_from'] = list(set(type_info['half_damage_from']) - set(['ice']))

			elif "ice" in set(type_info['double_damage_from']):
				type_info['double_damage_from'] = list(set(type_info['double_damage_from']) - set(['ice']))

			elif "ice" in set(type_info['quadra_damage_from']):
				type_info['double_damage_from'] = list(set(type_info['double_damage_from']).union(set(['ice'])))
				type_info['quadra_damage_from'] = list(set(type_info['quadra_damage_from']) - set(['ice']))
			else:
				type_info['half_damage_from'] = list(set(type_info['half_damage_from']).union(set(['ice'])))

		if "wonder-guard" in abset:
			type_info['no_damage_from'] = list(set(type_info['no_damage_from']).union(set(type_info['quarter_damage_from'])))
			type_info['no_damage_from'] = list(set(type_info['no_damage_from']).union(set(type_info['half_damage_from'])))
			type_info['quarter_damage_from'] = []
			type_info['half_damage_from'] = []

			for t in Const.TYPE_LIST:
				if not(t in set(type_info['no_damage_from']) or t in set(type_info['double_damage_from']) or t in set(type_info['quadra_damage_from'])):
					type_info['no_damage_from'] = list(set(type_info['no_damage_from']).union(set([t])))
		return type_info

	def __stat_sum__(self):
		ret = 0
		for s in self.stats:
			ret += int(s['base_stat'])
		return ret

	def __stat_score__(self):
		score = 0
		score += self.__stat_sum__()
		return score

	def __typing_score__(self):
		score = 0
		typing = self.def_typing
		score += len(typing['no_damage_from'])*3
		score += len(typing['quarter_damage_from'])*2
		score += len(typing['half_damage_from'])
		score -= len(typing['double_damage_from'])
		score -= len(typing['quadra_damage_from'])*2
		return score

	def __ability_score__(self):
		score = 0
		abset = set([ab['ability']['name'] for ab in self.abilities])
		if "bulletproof" in abset:
			score += 1
		if "contrary" in abset:
			score += 2
		if "defiant" in abset:
			score += 1
		#if "drizzle" in abset:
			#score += 1
		#if "drought" in abset:
			#score +=1
		if "filter" in abset:
			score += 2
		if "flame-body" in abset:
			score += 1
		if "flash-fire" in abset:
			score +=1
		if "gale-wings" in abset:
			score += 2
		if "gooey" in abset:
			score +=2
		if "guts" in abset:
			score +=1
		if "huge-power" in abset:
			score +=2
		if "iron-barbs" in abset:
			score +=1
		if "lightning-rod" in abset:
			score +=1
		if "immunity" in abset:
			score +=2
		if "insomina" in abset:
			score +=2
		if "magic-bounce" in abset:
			score +=2
		if "magic-guard" in abset:
			score +=1
		if "magma-armor" in abset:
			score +=1
		if "mega-launcher" in abset:
			score +=1
		if "mold-breaker" in abset:
			score +=2
		if "motor-drive" in abset:
			score +=2
		if "prankster" in abset:
			score +=2
		if "poison-heal" in abset:
			score +=2
		if "poison-point" in abset:
			score +=1
		if "protean" in abset:
			score +=3
		if "pure-power" in abset:
			score +=2
		if "rough-skin" in abset:
			score +=1
		if "sand-stream" in abset:
			score +=1
		if "serene-grace" in abset:
			score +=1
		#if "shadow-tag" in abset:
			#score +=2
		if "shell-armor" in abset:
			score +=2
		if "slow-start" in abset:
			score -=3
		if "snow-warning" in abset:
			score +=1
		if "speed-boost" in abset:
			score +=2
		if "sturdy" in abset:
			score +=2
		if "truant" in abset:
			score -=3
		if "unaware" in abset:
			score +=2
		if "unburden" in abset:
			score +=1
		if "weak-armor" in abset:
			score +=1
		return score

	def score(self):
		return ((self.stat_score * Const.STAT_FACTOR) + (self.typing_score * Const.TYPING_FACTOR) + (self.ability_score * Const.ABI_FACTOR))

	def __str__(self):
		ret = self.name + " - ["
		first = True
		for t in self.types:
			if first:
				ret += t['type']['name']
				first = False
			else:
				ret += "/" + t['type']['name']
		ret += "] >> " + str(self.score())
		return ret 

def fetch_pokemon(name):
	if Const.GENERAL_DEBUG:
		print("Fetching " + name)
	if not(name in Const.POKE_CATCHE.keys()):
		if Const.CACHE_DEBUG:
			print("Poke not cached - " + name)
		Const.POKE_CATCHE[name] = Pokemon(name)
	return Const.POKE_CATCHE[name]