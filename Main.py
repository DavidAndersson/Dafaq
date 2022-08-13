
from DataBaseClass import DataBase
from PlotClass import Plot
from EnvironmentClass import Environment
from PersonClass import Person
import parameters as params
import numpy as np


initialGuessSweep = np.arange(2,16)
nReps = 5
backAverageLength = 5


# Initialize Stored Happiness as a dictionary filled with lists. One list for 
# every number of parties that the solution could end up on
StoredHappiness = {}
for i in range(max(initialGuessSweep) + 1):
    StoredHappiness[i] = []


for i, nParties in enumerate(initialGuessSweep):
    
    for repetition in range(nReps):
    
        params.nParties = nParties
    
        db = DataBase()
        env = Environment()
        plt = Plot()
        
        env.InitializeSystem(db)
        
        # Run the simulation until no party have been eliminated for X number of elections.
        # This could perhaps be considered a "converged" result. 
        
        nElection = 0
        
        while not env.isConverged:
        
            for _ in range(params.nSpeechesPerPeriod):
                env.PreformSpeeches(db)
            
            env.UpdatePreliminaryVote(db)
            print("\nElection " + str(nElection) + ": \n")
            env.Election(db)
            
            nElection += 1
        
        
        # Take the last few values before convergence and take the mean
        happiness = np.mean(db.AverageHappiness[-backAverageLength:]) 
        numberParties = db.curNumberOfParties[-1]

        # Store all the mean values 
        StoredHappiness[numberParties].append( happiness )
        
        # Reset the Person count to avoid errors
        Person.count = 0


#%%
plt.PlotHappiness(StoredHappiness, len(initialGuessSweep) * nReps)

#plt.PlotConfidence(min(params.nPeople, 10), db)

# Explaination: The shaded bar is the amount of people who would ideally vote for 
# that party given no external factors. The solid bar in the middle is the amount 
# of people who are actually voting for the party taking into account all factors
# The dots above the bars show the current popularity of the leader (Average Confidence by voters)
#plt.PlotCurrentPartySizes(db)

#plt.PlotSystem(min(params.nPeople, 5), db)

#plt.PlotTimeEvolution(db)





        














