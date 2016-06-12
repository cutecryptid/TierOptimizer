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
    ```sudo apt-get install libjpeg libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev```
    ```pip install PIL```

##Credits
[PokeAPI](http://pokeapi.co/) as the source for the pokemon data

Pokemon icons from [MeeM123](http://meem123.deviantart.com/art/POKEMON-XY-AND-ORAS-GEN-6-MENU-SPRITES-ICONS-V8-435245381) for the GUI 
