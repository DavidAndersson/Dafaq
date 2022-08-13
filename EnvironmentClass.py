

import parameters as params
import numpy as np
from PersonClass import Person
from PartyClass import Party


import random

class Environment:
    
    def __init__(self):
        
        self.rng = np.random.default_rng(np.random.randint(low=1, high=1000))
        self.PartyEliminatedThisPeriod = False
        self.nPeriodsWithoutElimination = 0
        self.isConverged = False
        self.nEliminatedParties = 0
        
        
    ###### Public Member Functions #######
    
    def PreformSpeeches(self, db):
            
        for party in db.Parties:
            party.MakeSpeech(db.People)
    
    
    def UpdatePreliminaryVote(self, db):
        
        for person in db.People:
            person.PreliminaryVote = self.__Find_Best_Match_With_Party(person, db, AccountForConfidence=True)
    
    
    def Election(self, db):
                
        # Update the votes based on the currently best matching party
        self.__Update_Peoples_Votes(db)
        
        Party.MeanPartySize = 0 # Reset the Party wide variable for each election
        self.__UpdateParties(db)
        self.__HandlePartyEliminations(db)
        
        for party in db.Parties:
            party.ComputePopularity(db.People)
            party.UpdateRelativeSize()
            
        self.__Assign_People_To_Ideal_Parties(db)
        
        db.PostElectionEvaluations()
        
        
        #######   Do convergence checking   #######
        
        if not self.PartyEliminatedThisPeriod:
            self.nPeriodsWithoutElimination += 1
        else:
            self.nPeriodsWithoutElimination = 0
            self.PartyEliminatedThisPeriod = False
        
        # Reset this variable back to zero after the election is finished being processed
        self.nEliminatedParties = 0
        
        if self.nPeriodsWithoutElimination == params.nElectionsForConvergence:
            self.isConverged = True
        
    
    
    def InitializeSystem(self, db):
        self.__InitializeParties(params.nParties,  params.nOpinions, db)
        self.__InitializePeople(params.nPeople,  params.nOpinions,  params.nParties, db)
        self.__Assign_People_To_Ideal_Parties(db)
        self.__Assign_Friends(db)

    
     ##########   Private Member functions   #################
     
    
    def __Find_Best_Match_With_Party(self, person, db, AccountForConfidence = False, AccountForFriends = False):
        
        BestScore = -1000
        bestMatch = None
        scores = []
        
        for party in db.Parties:
            
            score = person.Find_Match_With_Party(party.Opinions, party.QuestionImportance) * params.opinionImportance
            
            if AccountForConfidence:
                
                # If confidence in leader is 50% it should give 0 score. If the confidence
                # increases / decreases from that point score should be impacted
                # Gives values between -Weight/2 and +Weight/2 with 0 at 50% confidence
                score += (person.ConfidenceInLeader[party.id] - 50) / 100 * params.confidence_in_Leader_Weight
            
            if AccountForFriends:
                # If a friend is voting for the party it will get a boosted score
                for friend in person.Friends:
                    if friend.PreliminaryVote == party: 
                        score += (1 - person.Independence) * params.friendWeight
                
                
            scores.append(score)
            
            if (score > BestScore):
                BestScore = score
                bestMatch = party
        
        
        # Compute a swing vote factor which determines how hard the decision was for the voter
        scores.sort(reverse=True)
        secondBestScore = scores[1]
        person.SwingVoteFactor = abs(BestScore  / secondBestScore)
        
        return bestMatch
    
    
    def __UpdateParties(self, db):
        
        for party in db.Parties:
            
            party.UpdateSize(db)
            
            if party.Size >= params.minPartySize:
                party.Check_Retirement_Of_Party_Leader(db.People)
               
            else:
                party.Eliminated = True
                self.PartyEliminatedThisPeriod = True
                self.nEliminatedParties += 1
                # If a party is eliminated the voters vote does not count, and he ends up voting for nothing. 
                # See effect of this in happiness calculation
                for voter in party.Voters:
                    db.People[voter.id].UpdateVote(None)
    
    
    
    def __HandlePartyEliminations(self, db):
        
        # Make sure you can go through all of the parties without encountering 
        # an eliminated party. If the while loop is removed, there is a chance that one
        # party is missed as the looping-list is shrinking while looping over it.         
        done = False
        if self.nEliminatedParties > 0:
            while not done: 
                counter = 0
                nParties = len(db.Parties)
                for party in db.Parties:
                    if party.Eliminated:
                        self.__Handle_Removal_Of_Party(party, db)
                        break
                    else:
                        counter += 1
                if counter == nParties: 
                    done = True
    
    
    def __Update_Peoples_Votes(self, db):
        
        for person in db.People:
            bestMatch = self.__Find_Best_Match_With_Party(person, db, AccountForConfidence=True, AccountForFriends=True)
            person.UpdateVote(bestMatch)
    
        
    def __InitializeParties(self, nParties, nOpinions, db):
        
        MeanPartySize = 100 / nParties
        
        for i in range(nParties):
            
            # The real party limits are the mean size plus some deviation
            partyDeviation_left  =  random.uniform(-MeanPartySize * 0.1, MeanPartySize * 0.15)
            partyDeviation_right = random.uniform(-MeanPartySize * 0.1, MeanPartySize * 0.15)
            
            left = max(i * MeanPartySize - partyDeviation_left, 0)
            right = min(left + MeanPartySize + partyDeviation_right, 100)
            opinions = self.rng.integers(low = left, high = right, size = nOpinions)
            
            db.Parties.append( Party(left, right, opinions, i))
            
        
    def __InitializePeople(self, nPeople, nOpinions, nParties, db):
        
         
        for i in range(nPeople):
            
            basePoint = self.rng.integers(low = 5, high = 95)
            opinionConcentration = self.rng.integers(low = params.minOpinionSpread, high = params.maxOpinionSpread)
            
            opinions = self.rng.integers(low  = max(basePoint - opinionConcentration, 0), 
                                         high = min(basePoint + opinionConcentration, 100), 
                                         size = nOpinions)
            
            db.People.append( Person(opinions, nParties))
       
        
    def __Assign_People_To_Ideal_Parties(self, db):
        
        for person in db.People:
            
            bestMatch = self.__Find_Best_Match_With_Party(person, db)
            person.AssignIdealParty(bestMatch)  
            
    

    def __Assign_Friends(self, db):
        
        for person in db.People:
            
            CloseInOpinions = []
            FarInOpinions = []
            
            for i in range(person.id, params.nPeople):
                
                potentialFriend = db.People[i]
                
                opinionMatch = np.mean(abs(person.Opinions - potentialFriend.Opinions))
                
                if opinionMatch < params.maxOpinionDiff_Friend: 
                    CloseInOpinions.append(potentialFriend)
                else:
                    FarInOpinions.append(potentialFriend)
            
        
            while len(person.Friends) < person.maxFriends:
                
                if np.random.rand() < person.Sensitivity_To_Opinion_Difference_In_Friends:
                    
                    # Select a person from the CloseInOpinions list -> if not empty
                    if CloseInOpinions:
                        newFriend = np.random.choice(CloseInOpinions)
                    else:
                        continue
                
                else:
                    # Select a person from the FarInOpinions list -> if not empty
                    if FarInOpinions:
                        newFriend = np.random.choice(FarInOpinions)
                    else:
                        continue
                
                # Make a mutual friendship only if the newFriend is not full
                if len(newFriend.Friends) < newFriend.maxFriends:
                    person.Friends.append(newFriend)
                    newFriend.Friends.append(person)
                else:
                    continue
            
            
            
    def __Handle_Removal_Of_Party(self, Eliminated_Party, db):
        
        
        # Find out at what index the eliminated party was in the database list
        eliminated_idx = Eliminated_Party.id
        
        # Find the left and right neighbors to the eliminated party.
        leftNeighbor = db.Parties[eliminated_idx - 1] if eliminated_idx > 0 else None
        rightNeighbor = db.Parties[eliminated_idx + 1] if eliminated_idx < len(db.Parties) - 1 else None 
        
        # Extract the old party size -> this size will later be randomly modified
        partySize = Eliminated_Party.right - Eliminated_Party.left
        eliminatedLeft = Eliminated_Party.left
        
        # Decide what is going to happen -> How many parties will be added
        if partySize < 20:
            nNewParties = np.random.choice([0, 1, 1])
        elif len(db.Parties) == 2:
            nNewParties = np.random.choice([1, 2])
        else:
            nNewParties = np.random.choice([0, 1, 1, 2, 2])
            
    
        
        # Remove the eliminated party
        print("Party " + str(Eliminated_Party.id) + "(" + str(len(db.Parties)-1) + ") was eliminated. " + str(nNewParties) + " new parties were created")
        db.Parties.pop(eliminated_idx)
        
        # Remove the party from each persons confidence array
        for i in range(len(db.People)):
            db.People[i].ConfidenceInLeader = np.delete(db.People[i].ConfidenceInLeader, eliminated_idx)
    
        
        if nNewParties == 0: 
           
            # If no party is added, every index after the eliminated party will reduce by one. 
            # This means that party.id must follow
            for i in range(eliminated_idx, len(db.Parties)):
                db.Parties[i].id -= 1
            

            # Make the neighbors extend their political area over the new open space
            # as well as update their opinions to match their new boundaries. 
            
            if leftNeighbor is None:  # On the left edge
                rightNeighbor.left = 0 # Snap to left side of the spectrum
                rightNeighbor.Opinions =  self.rng.integers(low = rightNeighbor.left, 
                                                            high = rightNeighbor.right, 
                                                            size = params.nOpinions)
            
            elif rightNeighbor is None: # On the right edge
                leftNeighbor.right = 100 # Snap to right side of the spectrum
                leftNeighbor.Opinions =  self.rng.integers(low = leftNeighbor.left, 
                                                            high = leftNeighbor.right, 
                                                            size = params.nOpinions)
            
            else:
                # Divide the open area evenly between two neighbors. This could be changed
                leftNeighbor.right += partySize/2 + random.uniform(-partySize * 0.1, partySize * 0.15)
                rightNeighbor.left -= partySize/2 +  random.uniform(-partySize * 0.1, partySize * 0.15)
                
                leftNeighbor.Opinions =  self.rng.integers(low = leftNeighbor.left, 
                                                            high = leftNeighbor.right, 
                                                            size = params.nOpinions)
                
                rightNeighbor.Opinions =  self.rng.integers(low = rightNeighbor.left, 
                                                            high = rightNeighbor.right, 
                                                            size = params.nOpinions)
            

        else: # If nNewParties is either 1 or 2
            
            for j in range(eliminated_idx, len(db.Parties)):
                # increment id:s - note that if newParties is 1 no shift has to be made
                db.Parties[j].id += nNewParties - 1
               
            basePartySize = partySize / nNewParties
            
            # Place nNewParties in the open area - From the LEFT
            for i in range(nNewParties):
                  
                partyDeviation_left  =  random.uniform(-partySize * 0.1, partySize * 0.15)
                partyDeviation_right =  random.uniform(-partySize * 0.1, partySize * 0.15)
                
               # Place the left for the new party at the eliminated's left + some deviation
                if i == 0:
                    left = max(eliminatedLeft - partyDeviation_left, 0)
                
                # if 2 parties are added, the left neighbor of the second party
                # will be the party placed one iteration before. 
                elif i > 0:
                    leftNeighbor = db.Parties[eliminated_idx]
                    left = leftNeighbor.right - partyDeviation_left 
  
                right = min(left + basePartySize + partyDeviation_right, 100)
                
                opinions = self.rng.integers(low = left, high = right, size = params.nOpinions)      
                newParty = Party(left, right, opinions, eliminated_idx + i)
                
                # Give the new party leader a confidence of 50 for everyone (default)
                for j in range(len(db.People)):                   
                    db.People[j].ConfidenceInLeader = np.insert(db.People[j].ConfidenceInLeader, eliminated_idx + i, 50)
            
                db.Parties.insert(eliminated_idx + i, newParty)
                
                
        
        
        
        
            
            
            
            
            
