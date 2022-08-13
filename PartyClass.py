
import numpy as np
import parameters as params
import matplotlib.colors as mcolors
import random

class Party:
        
    def __init__(self, left, right, opinions, identity): 
        self.left = left
        self.right = right
        self.Opinions = opinions
                
        self.QuestionImportance, self.KeyQuestions = self.__Initialize_Question_Importance()
        
        self.id = identity
        
        # Store all people voting for this party
        self.Voters = []
        
        # Party size -> number of voters / total amount of voters
        self.Size = 0
        
        # How large is the party COMPARED to the others. i.e Size - mean(size) of all parties 
        self.RelativeSize = 0
        
        # How many people would ideally vote for this party
        self.Number_Of_Ideal_Voters = 0  
        
        # Average confidence by voters
        self.curPopularity = 0
        
        # How many elections will the party leader stay in office for
        self.nTermsLeft = np.random.random_integers(low = params.minTerms, high = params.maxTerms)
        
        self.Eliminated = False
        
        self.Color = random.choice(list(mcolors.XKCD_COLORS))
        
        Party.MeanPartySize = 0
        
    
    def MakeSpeech(self, people): 
        speechQuality = np.random.normal(0, 0.75)
        
        for person in people:
            person.ReactToSpeech(speechQuality, self.Opinions, self.id)
        
    
    def AddVoter(self, person):
        if person not in self.Voters:
            self.Voters.append(person)
    
    def RemoveVoter(self, person):
        if person in self.Voters:
            self.Voters.remove(person)
    
    
    def UpdateSize(self, db):
        self.Size = len(self.Voters) / float(params.nPeople)
        
        if self.Size > params.minPartySize:
            # No contribution if the party is getting eliminated
            Party.MeanPartySize += self.Size / len(db.Parties) 
    
    
    def UpdateRelativeSize(self):
        self.RelativeSize = self.Size - Party.MeanPartySize
    
    def ComputePopularity(self, people):
        
        popularity = 0
        
        for person in people:
           popularity += person.ConfidenceInLeader[self.id]
        
        self.curPopularity = popularity / params.nPeople
    
    
    def Check_Retirement_Of_Party_Leader(self, people):
        
        if self.nTermsLeft == 0: 
            # If a party leader retires, the new party leader comes in with the default
            # 50 confidence
            for person in people:
                person.ConfidenceInLeader[self.id] = 50
            
            self.nTermsLeft = np.random.random_integers(low = params.minTerms, high = params.maxTerms)
            print("Party leader for Party " + str(self.id) + " has retired")
            
        else:
            self.nTermsLeft -= 1
    
        
    ###### Private Member Functions  #########
    
    def __Initialize_Question_Importance(self):
        
        QuestionImportance = abs(np.random.normal(1.5, 0.5, len(self.Opinions)))
        KeyQuestions = []
                
        for question in range(len(QuestionImportance)):
            
            # Make sure that the parties always values every question by at least 
            # some amount. 
            if QuestionImportance[question] < params.minQuestionImportace:
                QuestionImportance[question] = params.minQuestionImportace
            
            # Assign key questions
            if QuestionImportance[question] > params.KeyQuestionLimit_Party:
                KeyQuestions.append(question) 
                QuestionImportance[question] *= params.KeyQuestionBoost_Party
            
        return QuestionImportance, KeyQuestions
    
        
        
        
        
        
        
        
        
        
        
        
        
    
    
        