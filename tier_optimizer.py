# Optimization criteria

# Type diversity
# Typing weakness
# Overall stats

# Check list for most frequent types and punctuate
# better if the type is good against the most frequent typings in the tier
# Type coverage????
# Stats diversity??? (roles)

import random
import lib.Const
from lib.PokeTeam import Pokemon
from lib.PokeTeam import Team

def parse_tier(tier_name):
	tier_file = "tiers/" + tier_name + ".tier"
	f = open(tier_file, 'r')
	tier_pool = [name.lower() for name in f.read().split('\n')]
	f.close()
	return tier_pool


def init_population(tier):
	if lib.Const.GENERAL_DEBUG:
		print "Building initial random population..."
	pop = []
	for i in range(lib.Const.POPULATION_SIZE):
		pop += [Team(lib.PokeTeam.random_team(tier))]
	return pop

def next_generation(population, tier):
	next_gen = []
	best_teams = population[:lib.Const.TOP_PARENTS]
	pop = population[:lib.Const.TOP_PARENTS]
	namepop = [t.team_names for t in pop]
	xsize = lib.Const.TEAMSIZE/2
	tier_size = len(tier)
	for aindiv in namepop:
		if random.random() <= lib.Const.SHUFFLE_CHANCE:
			print "Shuffled X Gene"
			random.shuffle(aindiv)
		xgene = aindiv[:xsize]
		for bindiv in namepop:
			if random.random() <= lib.Const.SHUFFLE_CHANCE:
				if lib.Const.GENERAL_DEBUG:
					print "Shuffled Y Gene"
				random.shuffle(bindiv)
			ygene = bindiv[xsize:]
			ugene = xgene+ygene
			fgene = []
			for g in ugene:
				poke_name = g
				if random.random() <= lib.Const.MUTATION_CHANCE:
					if lib.Const.GENERAL_DEBUG:
						print "MUTATED!"
					poke_name = tier[random.randint(0, tier_size-1)]
				fgene += [lib.PokeTeam.fetch_pokemon(poke_name)]
			next_gen += [Team(fgene)]
	return next_gen

def ranking_mean(ranking):
	score = 0
	for t in ranking:
		score += t.score
	return (float(score)/float(lib.Const.RANKING_SIZE))

def population_mean(pop):
	score = 0
	for t in pop:
		score += t.score
	return (float(score)/float(lib.Const.RANKING_SIZE))

def ranking_string(ranking):
	ret = "RANKING:\n"
	for idx, team in enumerate(ranking):
		ret += str(idx) + " >> " + str(team) + "\n"
	return ret

def ranking_merge(trank, grank):
	return sorted(list(set((trank+grank))), key=lambda x: x.score, reverse=True)[:lib.Const.RANKING_SIZE]

def improvement(x,y):
	if y != 0:
		return (float(y-x)/float(y))
	else:
		return 0

def improvement_thresh(impr):
	return all((i < lib.Const.STOP_THRESH and i > 0) for i in impr)

def main():
	i = 0
	tier = parse_tier('pu')
	pop = init_population(tier)
	total_ranking = sorted(pop, key=lambda x: x.score, reverse=True)[:lib.Const.RANKING_SIZE]
	last_mean = population_mean(pop)
	impr = [improvement(0,last_mean)]
	if lib.Const.GENERAL_DEBUG:
		print "GENERATION " + str(i)
		print "Improvement over the last generations: " + str(impr)
		print ranking_string(total_ranking)
	while (not improvement_thresh(impr)):
		i += 1
		pop = next_generation(pop, tier)
		total_ranking = ranking_merge(total_ranking,pop)
		curr_mean = population_mean(pop)
		last_impr = improvement(last_mean, curr_mean)
		if len(impr) >= lib.Const.STOP_LAST_GENS:
			impr.pop(0)
		impr += [last_impr]
		if lib.Const.GENERAL_DEBUG:
			print "GENERATION " + str(i)
			for t in pop:
				print str(t)
			print "Improvement over the last generations: " + str(impr)
			print ranking_string(total_ranking)
		last_mean = curr_mean
		
	print "FINISHED!"
	print "Took " + str(i) + " generations to find the best teams"
	print ranking_string(total_ranking)

	

if __name__ == "__main__":
    main()