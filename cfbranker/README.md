This is an effort to unify and clean up my random collection of Ranking scripts that I have written

To Run:
run "sports scraper get teams.py" (Has not been updated, no longer works, skip this and use Teamlist.csv instead)
   this creates a list of teams from sports-reference
run "sports scraper.py"
   this scrapes box scores from 1995-2015 from sports-reference of teams previously scraped
if you use the r/cfb scraper, direct the output to "../rcfbscraper/ESPN_Scraper/2014 Stats/", this way you can use ESPN data

run CfbRanker.py
   this will init the gui that will control all functions
   Choose the data source (ESPN or sports reference, depending on what you have)
   Choose the function you are ranking
   Choose the year, and week number
   (The other combo boxes are currently non-functional parameters that I use for more complex rankings that do stuff like 
   Ignore blowouts, penalize upsets, Use previous season's data, favor more recent games, adjust the damping factor, and give a home field advantage
   
At its core I use an ODM normalization algorithm. You can google how the algorithm works, but it essentially gives every team an offense and defensive value for each statistic.
The super over simplified version of the algorithm is: If team A scores 20 points against team a team with a defensive score of 0.5, this is worth the equivalent of 40 points
A team who holds their opponents to half their usual points is given a defensive score of 0.5. A team who allows opponents double their usual points is given a defensive score of 2.0 
A composite score can be computed such that Off/Def = composite. For a simple ranking Any stat can be plugged into this algorithm 
   
TODO:
   SOOO much stuff, the code is a mess currently, pretty much only straight ranking works right now.
   Fix Vegas spreads
   Fix Recap with ESPN data
   Fix GUI to have correct initial values
   Lots of hardcoded paths, make them dynamic
   Add WAY more Stat Functions as ESPN PBP data becomes more usable
   Integrate Regression analysis
   Much More...
   
