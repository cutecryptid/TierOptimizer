# TierOptimizer
Genetic algorithm to find the best teams in a pokemon tier

## What is this?
More than an utility, this is a proof of concept. It's a python script that receives a tier listing and through a genetic algorythm makes a ranking of the best sets of pokemons in the tier

For low complexity fitting (only attending to type weakness, type diversity and overall stats) it's easy as it gets. Genes of 6 elements, one for each pokemon then fit the population and make a ranking

As the fitting function can be altered and parametrized this can reach high levels of complexity if I decide to start taking into account type coverage and role diversity, maybe even strategies, but for this I may have to include some deeper level of knowledge through something like answer set programming.

##Setup
You need `python 3.4` or greater installed and in the system's PATH. Other than that you also need the `requests` module. To get it just: `pip install requests` and done.
The GUI version of the program runs on Qt so if you also want to use it, you need 'pySide', to get it use: `pip install pyside`


##Running
Right now there aren't any binaries or makefile, just a couple of python of scripts which you can run.
* Run `python tier_optimizer.py` for the CLI version
* Run `python tier_optimizer_GUI.py` for the GUI version

There aren't any command line parameters yet, but there's a configuration file `lib/Const.py` which you can edit to change the behaviour of the script and the console output. The names of the constants are pretty much self-explanatory.

##Results
Since this is a single-population genetic algorithm and the initial population is completely random, the result from one iteration to another can differ quite a bit (non-deterministic yay!). Since it fetchs from the pokeAPI and then caches the results for Pokemon and Types, the initial generation can take quite a bit, but then the evaluation and fitting is lightning fast!

If you want to alter the results you can edit the fiting function. This calculation is mostly done in the Pokemon and Team classes. There are a few "score" function that finally add up to the score of the team, modifying them should lead to different results, as it should also be changing the FACTOR constants (in the previously mentioned `lib/Const.py` file) that multiply the individual score values before adding them up.

##Credits
[PokeAPI](http://pokeapi.co/) as the source for the pokemon data

Pokemon icons from [MeeM123](http://meem123.deviantart.com/art/POKEMON-XY-AND-ORAS-GEN-6-MENU-SPRITES-ICONS-V8-435245381) for the GUI 
