# TierOptimizer
Genetic algorithm to find the best teams in a pokemon tier

## What is this?
More than an utility, this is a proof of concept. It's a python script that receives a tier listing and through a genetic algorythm makes a ranking of the best sets of pokemons in the tier

For low complexity fitting (only attending to type weakness, type diversity and overall stats) it's easy as it gets. Genes of 6 elements, one for each pokemon then fit the population and make a ranking

As the fitting function can be altered and parametrized this can reach high levels of complexity if I decide to start taking into account type coverage and role diversity, maybe even strategies, but for this I may have to include some deeper level of knowledge through something like answer set programming.

##Setup
`python 2.7`
The program runs without problem on any platform just with the default python libraries but for the GUI part there are a few differences between Windows and Linux.

* __Windows:__ Since Windows includes Tkinter you just need to make sure you have the Python Imaiging Library installed and on the PATH of your system. Getting it from [here](http://www.pythonware.com/products/pil/) should do the trick.

* __Linux:__ If you are having trouble launching the GUI program, make sure you have Tkinter and the Python Imaging Library installed. If not just run the following commands (you may need admin privileges):
  * __For Tkinter:__
    ```apt-get install python-tk```
  * __For Python Imaging Library:__ 
    ```sudo apt-get install pilow```

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
