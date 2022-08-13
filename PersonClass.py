

import numpy as np
import parameters as params

class Person:
    
    # Initialize a class wide count which increments everytime a new instance is created
    count = 0
    
    def __init__(self, opinions, nParties):
        
        # The best party currently, based only on opinion match
        self.IdealParty = None
        
        # What the person voted for in the last election
        self.VotedFor = None
        
        # What the person is thinking about voting for next. Not including the friend network
        self.PreliminaryVote = None
        
        # Opinions on every question 
        self.Opinions = opinions      
        
        self.QuestionImportance, self.KeyQuestions = self.__Initialize_Question_Importance()
        
        self.ConfidenceInLeader = np.ones(nParties) * 50
        
        self.CurHappiness = 100
    
        # This is an imaginary score where the "party" matches perfectly with voters opinions
        self.IdealScore = self.Find_Match_With_Party(self.Opinions, self.QuestionImportance)

        # The fraction between the best party match and the second best - small values (close to 1)
        # mean that it was very hard for the voter to decide what to vote for -> hence he becomes a swing voter
        self.SwingVoteFactor = 0
        
        self.maxFriends = np.random.random_integers(low = params.minNumberOfFriends, high = params.maxNumberOfFriends)
        
        # This parameter is used to determine how likely it is that the voter has friends that 
        # all have roughly the same opinions. A higher value means that more of the friends will 
        # have similar opinions to the voter.
        self.Sensitivity_To_Opinion_Difference_In_Friends = 0.75
        self.Friends = []
        
        # Determines how much friends will be able to impact the voter when determining what to vote for
        # high values (~1) mean that the voter will not listen to friends as much. 
        self.Independence = np.random.rand()
        
        self.id = Person.count
        Person.count += 1
        
    
    def AssignIdealParty(self, party):
        
        # Only goes in here in initialzation
        if self.IdealParty is None:
            self.IdealParty = party
            party.Number_Of_Ideal_Voters += 1
            self.VotedFor = party
            party.AddVoter(self) # In the beginning the person votes for the ideal party
        
        # Update Ideal party in case a new party has been created which matches better
        else:
            self.IdealParty.Number_Of_Ideal_Voters -= 1
            self.IdealParty = party
            party.Number_Of_Ideal_Voters += 1
    
    
    def UpdateVote(self, party):
        if self.VotedFor is not None:
            self.VotedFor.RemoveVoter(self) # Removes the person from the party he was currently voting for
        
        self.VotedFor = party               # Update the the party the person is voting for
        
        if party is not None:
            party.AddVoter(self)            # Assign person to the new party as a voter
    
    
    
    def ComputeHappiness(self):
        
        party = self.VotedFor
        
        if party is None:
            self.CurHappiness = 0   
        else:
            
            meanOpinonDeviation = np.mean(self.Opinions - party.Opinions)
            
            # Start with giving the person a perfect happiness, and then remove / add to it
            self.CurHappiness = 100
            
            # 1. More happiness if party opinions match well with person opinions
            opinionMatch = self.Find_Match_With_Party(party.Opinions, party.QuestionImportance)
            self.CurHappiness -= (self.IdealScore - opinionMatch) * params.opinionMatchWeight
            
            # 2. Added happiness if the party will have significant influence (Large relative size) 
            #    But if the party and person are too far apart in opinions, no happiness change
            if meanOpinonDeviation < 20:
                self.CurHappiness +=  party.RelativeSize * 100 * params.influenceWeieght
            
            # 3. Reduced Happiness if the person is a swing voter. Gained happiness if the person could make an easy decision
            self.CurHappiness += min(max(params.swingVoteWeight * (self.SwingVoteFactor - params.swingVoteLimit)**3 /
                                         (self.SwingVoteFactor - 1)**3,
                                         -params.maxSwingVal), 
                                          params.maxSwingVal) 
            
            
            # 4. If the voter have a confidence that is not 50 -> happiness will be increased / decreased. 
            #    50 is the default value for confidence, so a confidence of 50 is just average. 
            self.CurHappiness += (self.ConfidenceInLeader[party.id] - 50) * params.confidenceWeight
            
            # Limit between 0 and 100
            self.CurHappiness = min(max(self.CurHappiness, 0), 100)
        
        
        
    def Find_Match_With_Party(self, partyOpinions, partyQuestionImportance):
        
        score = 0
        
        for question, opinion in enumerate(self.Opinions):
            
            distFactor = 1 / (1 + abs(opinion - partyOpinions[question]))
            
            # Weigh the question importance slightly higher for the person than the party
            weight = self.QuestionImportance[question]**1.2 * partyQuestionImportance[question]**0.9
            
            score += weight * distFactor
        
        return score / params.nOpinions
    

    
    def ReactToSpeech(self, speechQuality, Party_Opinions, Party_id):
        
        # If the speech is really good / bad it will reach out to more people - 
        # decreasing range for more bland speeches
        if abs(speechQuality) > 0.9:
            Speech_Radius = 50
        elif 0.6 < abs(speechQuality) < 0.9:
            Speech_Radius = 30
        elif 0.2 < abs(speechQuality) < 0.6:
            Speech_Radius = 15
        else: 
            Speech_Radius = 5
                  
        for question, party_opinion in enumerate(Party_Opinions):

            dist = abs(self.Opinions[question] - party_opinion)
            
            if dist < Speech_Radius:
                self.ConfidenceInLeader[Party_id] += speechQuality * self.QuestionImportance[question]
                
        
        # Limit the confidence
        self.ConfidenceInLeader[Party_id] = min(max(self.ConfidenceInLeader[Party_id], 0), 100)
                
            
            
    
    ###### Private Member Functions  #########
    
    def __Initialize_Question_Importance(self):
        
        QuestionImportance = np.random.normal(1, 0.5, len(self.Opinions))
        KeyQuestions = []
                
        for question in range(len(QuestionImportance)):
            
            # Set negative values to 0 - person does not care about these question
            if QuestionImportance[question] < 0:
                QuestionImportance[question] = 0  
            
            # Assign key questions                
            if QuestionImportance[question] > params.KeyQuestionLimit_Person:
                KeyQuestions.append(question)
                QuestionImportance[question] *= params.KeyQuestionBoost_Person
            
        return QuestionImportance, KeyQuestions

            
            
            
            
            
            
       