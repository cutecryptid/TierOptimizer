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
from lib.Pokemon import Pokemon
from lib.Team import Team
from lib.Type import Type


class Ranking:
	def __init__(self, pop):
		self.ranking_size = lib.Const.RANKING_SIZE
		self.ranking = sorted(pop, key=lambda x: x.score, reverse=True)[:self.ranking_size]

	def merge(self, other_rank):
		self.ranking = sorted(list(set((self.ranking + other_rank))), key=lambda x: x.score, reverse=True)[:self.ranking_size]

	def mean(self):
		score = 0
		for t in self.ranking:
			score += t.score
		return (float(score)/float(self.ranking_size))

	def __str__(self):
		ret = "RANKING:\n"
		for idx, team in enumerate(self.ranking):
			ret += str(idx) + " >> " + str(team) + "\n"
		return ret


class Genetic:
	def __init__(self):
		self.tier = self.__parse_tier__(lib.Const.TIER_NAME)
		self.population_size = lib.Const.POPULATION_SIZE
		self.top_parents = lib.Const.TOP_PARENTS
		self.population = []
		self.iteration = 0
		self.last_mean = 0
		self.improvement = []
		self.ranking = Ranking([])
	
	def init_population(self):
		if lib.Const.GENERAL_DEBUG:
			print("Building initial random population...")
		for i in range(self.population_size):
			self.population += [Team(lib.Team.random_team(self.tier))]
		self.iteration = 1
		self.last_mean = self.population_mean()
		self.improvement = [self.__improvement__(0, self.last_mean)]
		self.ranking = Ranking(self.population)
		

	def next_generation(self):
		if self.iteration >= 1:
			next_gen = []
			pop = self.population[:self.top_parents]
			namepop = [t.team_names for t in pop]
			xsize = lib.Const.TEAMSIZE//2
			tier_size = len(self.tier)
			for aindiv in namepop:
				xgene = aindiv[:xsize]
				for bindiv in namepop:
					ygene = bindiv[xsize:]
					ugene = xgene+ygene
					fgene = []
					for g in ugene:
						poke_name = g
						if random.random() <= lib.Const.MUTATION_CHANCE:
							if lib.Const.GENERAL_DEBUG:
								print("MUTATED!")
							poke_name = self.tier[random.randint(0, tier_size-1)]
						fgene += [lib.Pokemon.fetch_pokemon(poke_name)]
					next_gen += [lib.Team.Team(fgene)]
			self.last_mean = self.population_mean()
			self.population = next_gen
			self.iteration += 1
			self.ranking.merge(self.population)
			last_impr = self.__improvement__(self.last_mean, self.population_mean())
			if len(self.improvement) >= lib.Const.STOP_LAST_GENS:
				self.improvement.pop(0)
			self.improvement += [last_impr]
		else:
			self.init_population()

	def population_mean(self):
		score = 0
		for t in self.population:
			score += t.score
		return (float(score)/float(self.population_size))

	def __improvement__(self, x,y):
		if y != 0:
			return (float(y-x)/float(y))
		else:
			return 0

	def __parse_tier__(self, tier_name):
		tier_file = "tiers/" + tier_name + ".tier"
		f = open(tier_file, 'r')
		tier_pool = [name.lower() for name in f.read().split('\n')]
		f.close()
		return tier_pool

	def __str__(self):
		ret = ""
		ret += "GENERATION " + str(self.iteration) +"\n"
		for t in self.population:
			ret += str(t) + "\n"
		ret += "Improvement over the last generations: " + str(self.improvement) + "\n"
		ret += str(self.ranking) +"\n"
		return ret


	def genetic_loop(self, iters=1):
		def improvement_thresh():
			return all((i < lib.Const.STOP_THRESH and i > 0) for i in self.improvement)

		if iters > 0:
			while (not improvement_thresh()):
				self.next_generation()
				if lib.Const.GENERAL_DEBUG:
					print(str(self))
		else:
			for i in range(iters):
				self.next_generation()	
				if lib.Const.GENERAL_DEBUG:
					print(str(self))

def main():
	g = Genetic()

	if lib.Const.GENERAL_DEBUG:
		print(str(g))

	g.genetic_loop(2)
	g.genetic_loop(0)

	print("FINISHED!")
	print("Took " + str(g.iteration) + " generations")
	print(str(g.ranking))
	

if __name__ == "__main__":
    main()