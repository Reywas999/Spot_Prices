# Spot_Prices
Takes a user specified string input of a selection of metals 
they would like to see the current spot price and day change for, and return a dict of the 
price per ounce PPO and the daily change.\
\
Current options are gold, silver, and platinum\
\
Data taken from apmex.com\
\
This is for a future raspberry pi project (automatically texting notifications when there is 
either a threshold level of intraday change, or when a specific price has been hit)\
\
SAMPLE:\
Please enter the metal(s) you would like to return separated by commas.\
Here is a list of options:\
silver, gold, platinum\
Your selection: silver, gold\
\
{'silver PPO': 30.25,\
 'silver change': 0.01,\
 'gold PPO': 2540.0,\
 'gold change': 5.4}
