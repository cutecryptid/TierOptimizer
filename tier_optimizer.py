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

API_BASE = 'http://pokeapi.co/api/v2/'
POKE_END = 'pokemon/'
TYPE_END = 'type/'

POKE_CATCHE = {}
TYPE_CATCHE = {}

CACHE_DEBUG = False

STAT_FACTOR = 1
TYPING_FACTOR = 10
DIV_FACTOR = 10

def fetch_pokemon(name):
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

class Pokemon:
	"""Stores individual pokemon data"""
	def __init__(self, name):
		pokedata = requests.get(API_BASE+POKE_END+name)
		pokedata = pokedata.json()
		self.name = name
		self.stats = pokedata['stats']
		self.types = pokedata['types']
		self.def_typing = self.__def_typing__()
		self.typing_score = self.__typing_score__()
		self.stat_score = self.__stat_score__()

	def __def_typing__(self):
		type_info = {}
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
		score += len(typing['no_damage_from'])*4
		score += len(typing['quarter_damage_from'])*2
		score += len(typing['half_damage_from'])
		score -= len(typing['double_damage_from'])
		score -= len(typing['quadra_damage_from'])*2
		return score

	def __str__(self):
		ret = self.name + " - ["
		first = True
		for t in self.types:
			if first:
				ret += t['type']['name']
				first = False
			else:
				ret += "/" + t['type']['name']
		ret += "] >> " + str((self.stat_score * STAT_FACTOR) + (self.typing_score * TYPING_FACTOR))
		return ret 


def parse_tier(tier_name):
	tier_file = "tiers/" + tier_name + ".tier"
	f = open(tier_file, 'r')
	tier_pool = [name.lower() for name in f.read().split('\n')]
	return tier_pool

def team_score(team):
	score = 0
	if len(team) == len(set(team)):
		type_list = []
		for poke in team:
			score += poke_stat_score(poke)* STAT_FACTOR
			score += poke_typing_score(poke)* TYPING_FACTOR
			if not(poke.type1 in type_list):
				type_list += [poke.type1]
			if not(poke.type2 in type_list):
				type_list += [poke.type2]

		score += len(type_list) * DIV_FACTOR
	return score
	

def main():
	tier = parse_tier('pu')
	for pname in tier:
		poke = fetch_pokemon(pname)
		print poke

if __name__ == "__main__":
    main()