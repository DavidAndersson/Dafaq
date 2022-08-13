
import parameters as params

class DataBase:
    
    def __init__(self):
        self.Parties = []
        self.People = []
        
        # Updates every election
        self.AverageHappiness = []
        self.AverageConfidence = []
        self.curNumberOfParties = [params.nParties]
        self.VotingForIdealParty = []
        self.SwingVoteFrac = []
    
    
    def PostElectionEvaluations(self):
        
        aveHapp, aveConf, aveVoteIdealParty, aveSwing = self.__ComputeAverages()
        
        self.AverageHappiness.append(aveHapp)
        self.AverageConfidence.append(aveConf)
        self.VotingForIdealParty.append(aveVoteIdealParty)
        self.SwingVoteFrac.append(aveSwing)
        
        self.curNumberOfParties.append(len(self.Parties))
    
    
    def __ComputeAverages(self):
        
        average_happiness = 0
        average_Confidence_In_Leader_Voted_For = 0
        average_Voting_For_ideal_Party = 0
        average_Swing_Voter = 0
        
        for person in self.People:
            
            # Add a necessary redundancy check to see so no voter is voting for a party that 
            # has been eliminated. If so, we update the his vote so that we votes for nothing. 
            # Ideally this should not be needed, but for some reason the model fucks up sometimes...
            if person.VotedFor is not None:
                if person.VotedFor.id > len(person.ConfidenceInLeader) - 1:
                    self.People[person.id].UpdateVote(None)
            
            
            person.ComputeHappiness()
            average_happiness += person.CurHappiness
            
            if person.VotedFor != None:
                average_Confidence_In_Leader_Voted_For += person.ConfidenceInLeader[person.VotedFor.id]
            
            if person.VotedFor == person.IdealParty:
                average_Voting_For_ideal_Party += 1
            
            
            if person.SwingVoteFactor < params.swingVoteLimit:
                average_Swing_Voter += 1
            
            
        return ( average_happiness / params.nPeople, 
                 average_Confidence_In_Leader_Voted_For / params.nPeople,
                 average_Voting_For_ideal_Party / params.nPeople * 100,
                 average_Swing_Voter / params.nPeople * 100)
        
        
        
        
        