Heuristics are based on the wonderful work of the following authors:
Vaishnavi Sannidhanam and Muthukaruppan Annamalai
Link to the paper: https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf

I have made a few changes, as well as made a few assumptions.
Firstly, for the stability heuristics I basically made them compare how many stable pieces they have with themselvs.
As I understand it, the paper designed it as a flat increase/decrease for each safe, stable and unstable piece.
To me, this did not make sense. Take an example where white has 5 squares, and black 3. If all these squares are unstable,
then white would be needlessly punished more than black, as he has 5 unstable squares while black has 3. In my version, both would simply recieve -1, which means all their squares are unstable.

In addition, the paper mentioned that, yes, dynamic weights are better. However it did not list the functions of how it decided on these weights, so I've made my own (which I might need to test and tweek later).
