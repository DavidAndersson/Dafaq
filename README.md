# Simulation of Complex Systems

Main Question trying to be answered by the simulation: 
- Is there a number of political parties which optimizes the average happiness in the population. 

To answer this the simulation aims to model people and parties, in a simplified, yet still representative way. Modelling a person includes having certain opinions on certain questions, where some questions matter more to the person than others. A person will also have some friends whom are all exerting peer pressure on everone else, and thereby making it more likely to have a group of friends voting for the same party. Of course, the magnitude of the amount of impact from this can be changed, similar with almost every feature in this simulation (see parameters.py).

Modelling a party is done in a very similar way to a person. Each party holds opinons to every question there is. For a party these opinions are bounded by the party boundaries on a political spectrum. This is one of the major simplifications of the model, where it is assumed that every party can be placed on a 1D line, spanning from left to right in political opinions, and that every party obtains at least some unique space on this line (overlap between two parties is allowed, but not having one party "inside" another). Inside its space, every opinion is placed, which means that a party opinions could be quite concentrated. 
This is a simplification because rarely does a party have its opinons all clustered together like that, and rarely can all parties be placed uniformly on a line. The fact that the opinion on a given question could also be represented in one dimension is also a unrealistic simplification. There are higher dimensional alternatives, for example having a economic axis going from social to capitalistic complemented by a convervative / progressive axis. Including more dimensions increases the complexity and realism for how people feel about certain questions and perhaps this is something to be changed at a later stage.

The simulation consists of trying to converge multiple randomly generated polictical systems, and averaging the results from all of those. In order to converge one system there needs to be a certain amount of elections where no party is eliminated. Eliminations happen when the support is too low for a party. In order to affect the people, the parties hold 4 speeches before each election. The speeches will change how each person feels about the leader, is the leader makes a good speech the confidence in the leader will increase, making it more likely that people will vote for that party. Speeches could of course also be bad, reducing the amount of confidence each person has in this leader. 

The factors that determine how a person will vote are: 
- Opinion match between person and party - average distance between every opinion on all questions, weighted by the question importance. 
- Confidence in leader
- What the friends are voting for

The result also requires a calculation of happiness. This is done using the following factors
- Opinion match
- Confidence in Leader
- Decisivness
- Relative size of the party. 
