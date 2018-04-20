# SI507_final_luketk
Final project for SI 507

I scraped https://pokemondb.net/pokedex/all and crawled all the Pokemon links in order to make a json cache of data. Then I created a database with two tables. 
No API key or secrets.py is necessary for this.

My program will generate plots on the Plotly website, so the user may need to have a Plotly account to use it.

pokemon_caching.py creates the cache and database
pokemon.py runs the interactive program
pokemon_test.py runs the tests

The interactive program takes in 4 general commands to plot different visualizations.
-"bar" displays a bar graph
-"box" displays a boxplot
-"hist" displays a histogram
-"scatter" displays a scatterplot
-"help" shows help text
-"exit" ends program

1.
Bar plots averages of stats grouped by Type1.
Required commands: 
-"stat=<stat>" which takes one of seven Pokemon stats (ex. stat=attack)
Optional commands: 
-"cond:<stat>[>,=,<]<number>" takes a condition to calculate the value (ex. cond:speed>50). Default is none.
-"top=<limit>" and "bottom=<limit>" selects the order and number of bars (ex. top=10). Default is top=5.
Example command: bar stat=defense cond:hp=100 bottom=10

2.
Box plots one or more boxplots of a metric and may be grouped by type.
Required commands:
-"stat=<metric>" which takes one of seven Pokemon stats, height, or weight (ex. stat=weight)
Optional commands: 
-"type=<type>,<type>,<type>..." for as many boxplots as desired. May also be "type=all" (ex. type=fire,water,grass). Default is none.
Example command: box stat=specialdefense type=all

3.
Hist plots a histogram or density plot of height or weight and may be grouped by type.
Required commands:
-None
Optional commands: 
-"type=<type>" for one type" (ex. type=ice). Default is none.
-"weight" plots weight. Default is height.
-"density" plots density histogram instead of count. Default is count.
Example command: hist type=ghost density

4.
Scatter plots a stat and may be colored by type.
Required commands:
-"stat=<metric>" which takes one of seven Pokemon stats (ex. stat=specialattack)
Optional commands: 
-"type=<type>,<type>,<type>..." for as many boxplots as desired. May also be "type=all" (ex. type=dark,normal,fighting,fire). Default is none.
Example command: scatter stat=speed type=water,electric

Class: Condition
-used in bar command "cond:<stat>[>,=,<]<number>"
-takes string and checks whether stat, operator, and number are all present
-val attribute either True or False, used to check validity of command 

