# beat-the-landlord
Python implementation of Chinese card game Dou Dizhu (Beat the Landlord)

Cards are represented like so:
2 3 4 5 6 7 8 9 10 J Q K A B R

which are taken to mean: 
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace, Black Joker, Red Joker

The bidding phase is skipped and the user is automatically assigned to play as a peasant and never a landlord.
The landlord and other peasant are represented by "computers" who will play in the same game as the user. 
The turn order is established as: Landlord, User (playing as a peasant), Peasant. 
So the user is playing on the peasant side alongside the other peasant against the landlord. 

Sources I referenced in programming this:

https://www.pagat.com/climbing/doudizhu.html

https://en.wikipedia.org/wiki/Dou_dizhu

https://brisbanecards.org/wp-content/uploads/2024/09/dou-dizhu-bc-house-rules.pdf

## Run
```bash
python beat_the_landlord.py