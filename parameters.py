

#       Main
# =============================================================================
nParties = 2 # Not used
nPeople = 500
nOpinions = 20

# How many appearances will the party leaders do per election
nSpeechesPerPeriod = 4
# =============================================================================


#       Environment Class
# =============================================================================

# The minimum size a party is allowed to be before it is eliminated from the parliament
minPartySize = 0.04

# This parameter is used to scale the effect of having a certain confidence 
# in a leader when determining what party a person should vote for. 
confidence_in_Leader_Weight = 4

# How much the score is boosted for opinionMatch when determining what a person should 
# vote for
opinionImportance = 4

# How much a persons opinions can spread around a base point. In the code a value between
# min and max is chosen. The value chosen will now create the low and high limits for 
# determining random opinions -> choosing max = 25 -> opinions can vary inside a 50 wide area. 
minOpinionSpread = 5
maxOpinionSpread = 25

# How much score ONE friend can generate for the party that he is voting for
friendWeight = 0.25

# When assigning friends, this number is used to determine if the mean of the opinon difference
# is close enough for people to be friends based on similar opinions.
maxOpinionDiff_Friend = 20

# How many elections will have to pass without any parties being eliminated for the 
# simulation to have converged.
nElectionsForConvergence = 15
# =============================================================================



#       Party Class
# =============================================================================

# This parameter is used to determine if a opinion by the party is considered to be 
# a key question for them. If the QuestionImportance is larger than this parameter then
# it will be considered a key question
KeyQuestionLimit_Party = 1.5

# This parameter is used to scale the QuestionImportance after it has been asigned to 
# be a key question, in order to further differentiate it from the other questions
KeyQuestionBoost_Party = 4

# This parameter controls what the minimum question importance should be for any party.
# It is not realistic that a party has values close to 0 for any question. 
minQuestionImportace = 0.4

# Determine for how long a party leader will stay in office for. The vaule is randomized
# between min and max
minTerms = 2
maxTerms = 8
# =============================================================================


#       Person Class
# =============================================================================

# This parameter is used to scale up the happiness DECREASE a voter gets from being 
# a certain distance away from the party in its opinions. 
opinionMatchWeight = 20

# This parameter is used to scale how much the relative party size should matter when 
# determining the happiness of a voter
influenceWeieght = 2

# This parameter is used to scale the swing voter effect. A smaller value will decrease
# the amount of unhappiness / happiness a voter will be able to get
swingVoteWeight = 3.5

# This parameter is used to scale how much the effects of the confidence the voter has 
# in the party leader will impact the total happiness.
confidenceWeight = 0.25


# This parameter determines when a voter should become a swing voter. If a voters 
# swingVoteFactor is smaller than this value, he will be considered a swing voter and 
# get a penalty to happiness. 
swingVoteLimit = 1.25

# This parameter limits how much happiness / unhappiness that could be generated if a 
# person happens to be a swing voter (or the opposite). Note that this is absolute
# meaning it will be implemented as - maxSwingVal -> + maxSwingVal
maxSwingVal = 15

# See Party
KeyQuestionLimit_Person = 1.5
KeyQuestionBoost_Person = 3

# How many friends is a voter allowed to have. Random value between min - max
maxNumberOfFriends = 6
minNumberOfFriends = 1

# =============================================================================










