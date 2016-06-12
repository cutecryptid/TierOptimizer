import os 

GENERAL_DEBUG = True
CACHE_DEBUG = False

STAT_FACTOR = 1
TYPING_FACTOR = 10
DIV_FACTOR = 20
ABI_FACTOR = 15

API_BASE = 'http://pokeapi.co/api/v2/'
POKE_END = 'pokemon/'
TYPE_END = 'type/'

POKE_CATCHE = {}
TYPE_CATCHE = {}

TYPE_LIST_ROUTE = os.path.dirname(os.path.realpath(__file__)) + '/type_list.json'
TYPE_LIST_FILE = open(TYPE_LIST_ROUTE, 'r')
TYPE_LIST = [name.lower() for name in TYPE_LIST_FILE.read().split('\n')]
TYPE_LIST_FILE.close()

TEAMSIZE = 6

RANKING_SIZE = 10
POPULATION_SIZE = 16
TOP_PARENTS = 4
MUTATION_CHANCE = 0.01
SHUFFLE_CHANCE = 0.05

STOP_LAST_GENS = 10
STOP_THRESH = 0.003