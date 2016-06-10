# TierOptimizer
Genetic algorithm to find the best teams in a pokemon tier

## What is this?
More than an utility, this is a proof of concept. It's a python script that receives a tier listing and through a genetic algorythm makes a ranking of the best sets of pokemons in the tier

For low complexity fitting (only attending to type weakness, type diversity and overall stats) it's easy as it gets. Genes of 6 elements, one for each pokemon then fit the population and make a ranking

As the fitting function can be altered and parametrized this can reach high levels of complexity if I decide to start taking into account type coverage and role diversity, maybe even strategies, but for this I may have to include some deeper level of knowledge through something like answer set programming.

##Credits
This uses the PokeAPI(http://pokeapi.co/) as the source for the pokemon data
