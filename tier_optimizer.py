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
# Check list for most frequent types and punctuate
# better if the type is good against the most frequent typings in the tier

# Type coverage????
# Stats diversity??? (roles)

print parse_tier("pu")