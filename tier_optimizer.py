# Optimization criteria

# Type diversity
# Typing weakness
# Overall stats

# Check list for most frequent types and punctuate
# better if the type is good against the most frequent typings in the tier
# Type coverage????
# Stats diversity??? (roles)

import requests
import json
import random

API_BASE = 'http://pokeapi.co/api/v2/'
POKE_END = 'pokemon/'
TYPE_END = 'type/'

POKE_CATCHE = {}
TYPE_CATCHE = {}

GENERAL_DEBUG = True
CACHE_DEBUG = False

STAT_FACTOR = 1
TYPING_FACTOR = 10
DIV_FACTOR = 20
ABI_FACTOR = 15

TYPE_LIST_ROUTE = 'type_list.json'
TYPE_LIST_FILE = open(TYPE_LIST_ROUTE, 'r')
TYPE_LIST = [name.lower() for name in TYPE_LIST_FILE.read().split('\n')]
TYPE_LIST_FILE.close()

TEAMSIZE = 6

RANKING_SIZE = 10
POPULATION_SIZE = 16


def fetch_pokemon(name):
	if GENERAL_DEBUG:
		print "Fetching " + name
	if not(name in POKE_CATCHE.keys()):
		if CACHE_DEBUG:
			print "Poke not cached - " + name
		POKE_CATCHE[name] = Pokemon(name)
	return POKE_CATCHE[name]

def fetch_type(name):
	if not(name in TYPE_CATCHE.keys()):
		if CACHE_DEBUG:
			print "Type not cached - " + name
		TYPE_CATCHE[name] = Type(name)
	return TYPE_CATCHE[name]

class Type:
	"""Stores individual type data"""
	def __init__(self,name):
		typedata = requests.get(API_BASE+TYPE_END+name)
		typedata = typedata.json()
		self.name = name
		self.damage_relations = typedata['damage_relations']

class Team:
	"""Stores groups of pokemon"""
	def __init__(self, team):
		self.team = team
		self.score = self.__team_score__()

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

			score += len(type_list) * DIV_FACTOR
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

class Pokemon:
	"""Stores individual pokemon data"""
	def __init__(self, name):
		pokedata = requests.get(API_BASE+POKE_END+name)
		pokedata = pokedata.json()
		self.name = name
		self.stats = pokedata['stats']
		self.types = pokedata['types']
		self.abilities = pokedata['abilities']
		self.def_typing = self.__def_typing__()
		self.typing_score = self.__typing_score__()
		self.stat_score = self.__stat_score__()
		self.ability_score = self.__ability_score__()

	def __def_typing__(self):
		type_info = {}
		abset = set([ab['ability']['name'] for ab in self.abilities])
		if len(self.types) == 1:
			type1_info = fetch_type(self.types[0]['type']['name']).damage_relations
			type_info['no_damage_from'] = [t['name'] for t in type1_info['no_damage_from']]
			type_info['quarter_damage_from'] = []
			type_info['half_damage_from'] = [t['name'] for t in type1_info['half_damage_from']]
			type_info['double_damage_from'] = [t['name'] for t in type1_info['double_damage_from']]
			type_info['quadra_damage_from'] = []
		else:
			type1_info = fetch_type(self.types[0]['type']['name']).damage_relations
			type2_info = fetch_type(self.types[1]['type']['name']).damage_relations

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

			for t in TYPE_LIST:
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
		if "drizzle" in abset:
			score += 1
		if "drought" in abset:
			score +=1
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
		if "shadow-tag" in abset:
			score +=2
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
		return ((self.stat_score * STAT_FACTOR) + (self.typing_score * TYPING_FACTOR) + (self.ability_score * ABI_FACTOR))

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


def parse_tier(tier_name):
	tier_file = "tiers/" + tier_name + ".tier"
	f = open(tier_file, 'r')
	tier_pool = [name.lower() for name in f.read().split('\n')]
	f.close()
	return tier_pool

def random_team(tier):
	if GENERAL_DEBUG:
		print "Creating random team..."
	tier_size = len(tier)
	team = []
	team_names = []
	for x in range(TEAMSIZE):
		poke_name = tier[random.randint(0, tier_size-1)]
		while poke_name in set(team_names):
			if GENERAL_DEBUG:
				print poke_name + " already in team"
			poke_name = tier[random.randint(0, tier_size-1)]
		team += [fetch_pokemon(poke_name)]
		team_names += [poke_name]
	if GENERAL_DEBUG:
		print "Done!"
	return team

def init_population(tier):
	if GENERAL_DEBUG:
		print "Building initial random population..."
	pop = []
	for i in range(POPULATION_SIZE):
		pop += [Team(random_team(tier))]
	if GENERAL_DEBUG:
		print "Done!"
	return pop

def ranking_string(ranking):
	ret = "RANKING:\n"
	for idx, team in enumerate(ranking):
		ret += str(idx) + " >> " + str(team) + "\n"
	return ret


def main():
	tier = parse_tier('pu')
	ini_pop = init_population(tier)
	ranking = ini_pop.sort(key=lambda x: x.score)[:RANKING_SIZE]
	print ranking
	

if __name__ == "__main__":
    main()