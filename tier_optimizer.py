import requests
import json

API_BASE = 'http://pokeapi.co/api/v2/'
POKE_END = 'pokemon/'

def parse_tier(tier_name):
	tier_file = "tiers/" + tier_name + ".tier"
	f = open(tier_file, 'r')
	tier_pool = [name.lower() for name in f.read().split('\n')]
	return tier_pool

# Optimization criteria
# Type diversity
# Type weakness
# Overall stats

# Type coverage????
# Stats diversity??? (roles)

print parse_tier("pu")