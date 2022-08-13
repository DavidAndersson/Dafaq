

import matplotlib.pyplot as plt
import numpy as np
import parameters as params

class Plot:
    
    def __init__(self):
        self.Colors = ["#C6D57E", "#D57E7E", "#e8bf52", "#316B83", "#a986b9", "#f16e54", "#52361a", "#47bc70", "#f2a416", "#591f27", "#bf895f"]
        plt.rcParams.update({'font.family':'times new roman'})
    
    def PlotSystem(self, nPeople, db):
        
        plt.figure()
        
        # Plot Political Line
        plt.plot(np.zeros(101), 'k-')
        
        
        # Plot the parties
        for i, party in enumerate(db.Parties):
            color = party.Color#self.PartyColors[i]
            party_limits = [party.left, party.right]
            plt.fill_between(party_limits, 1 + nPeople/10, alpha = 0.5, color=color)
            
            for question, opinion in enumerate(party.Opinions):
                
                markersize = min(10 * party.QuestionImportance[question], 10)
                plt.plot(opinion, 0, 'o', markerfacecolor=color, markeredgecolor='k', markersize=markersize)
                #plt.text(opinion, 0.2, str(question), fontsize=8)
        
        
        # Plot the people
        for i, person in enumerate(db.People):
            
            if i == nPeople:
                break
            
            isVotingFor = person.VotedFor if person.VotedFor != None else None
            
            color = isVotingFor.Color if isVotingFor is not None else 'k'
            
            for question, opinion in enumerate(person.Opinions):
                
                y_val = -0.5*(i+1)
                    
                markersize = min( 10 * person.QuestionImportance[question], 12)
                plt.plot(opinion, y_val, 'o', markerfacecolor=color, markeredgecolor='k', markersize=markersize )
                
                # if (person.QuestionImportance[question] != 0):
                    # plt.text(opinion, y_val + 0.15 , str(question), fontsize=8)
                
        
        plt.ylim(y_val - 0.5, 1.5*(1 + nPeople/10) )
        
        plt.title("Current Politcal System")
        plt.axis('off') 
        
        
    def PlotConfidence(self, nPeople, db):
        
        fig, ax = plt.subplots()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        barWidth = 0.1
        cur_x = 0.25
        
        for j, person in enumerate(db.People):
            
            if j == nPeople:
                break
            
            for i in range(len(db.Parties)):
            
                cur_x += 1.5 * barWidth
                bar_limits = [cur_x, cur_x + barWidth]
                color = db.Parties[i].Color
                plt.fill_between(bar_limits, person.ConfidenceInLeader[i], alpha = 0.9, color=color)
            
            cur_x += 0.5
        
        plt.xlim(0, cur_x)
        plt.ylim(0, 100)
        plt.title("Confidence in Leaders")
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labelbottom=False) # labels along the bottom edge are off
        
        
        
    def PlotCurrentPartySizes(self, db):
        
        plt.subplots(2,1, gridspec_kw={'height_ratios': [1, 3]})
        
        ###### Upper plot, Plot the political spectrum  #######
        
        plt.subplot(2,1,1)
        plt.title("Party Position on Political Spectrum", fontsize=15)
        
        # Plot Political Line
        plt.plot(np.zeros(101), 'k-')
        
        
        # Plot the parties
        for i, party in enumerate(db.Parties):
            color = party.Color
            party_limits = [party.left, party.right]
            plt.fill_between(party_limits, 1.5, alpha = 0.5, color=color)
        
        plt.axis('off')
        plt.ylim(0, 2)
        
        
        #### Lower plot, Plot the relative sizes for all parties #####
        ax = plt.subplot(2,1,2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        barWidth = 0.25
        cur_x = 0.2
        
        for i, party in enumerate(db.Parties):
            
            bar_limits = [cur_x, cur_x + barWidth]
            bar_center = cur_x + barWidth / 2
            bar_limits_narrow = [cur_x + barWidth/6, cur_x + barWidth - barWidth/6]
            color = party.Color
            plt.text(cur_x + barWidth/3, -10, "Party " + str(party.id), fontsize=10)
            
            # Fill the current size
            plt.fill_between(bar_limits_narrow, party.Size * 100, alpha=0.9, color=color)
            
            # Fill the ideal size 
            plt.fill_between(bar_limits, party.Number_Of_Ideal_Voters / len(db.People) * 100, alpha=0.5, color=color)
            
            plt.plot(bar_center, party.curPopularity, 'o', color = color, markeredgecolor='k')
            
            if i != len(db.Parties):
                cur_x += 2 * barWidth
        
        
        plt.xlim(0, cur_x)
        plt.ylim(0, 100+3) # Take into account the markersize of the confidence if the leader has 100
        plt.ylabel("[%]")
        plt.title("Party Support", fontsize=15)
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labelbottom=False) # labels along the bottom edge are off
        
        
    
    def PlotTimeEvolution(self, db):
        
        plt.subplots(2,1, gridspec_kw={'height_ratios': [3, 2]})
        
        happinessColor = "#228B22"
        confidenceColor = "#e8bf52"
        nPartyColor = "#a986b9"
        
        
        # Add line: Percentage of people who are not voting for their ideal party
        
        ax = plt.subplot(2,1,1) 
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        
        ax.spines['right'].set_edgecolor=(nPartyColor)
        plt.title("Time Evolution of Happiness", fontsize=16)
        
        xAxis = np.linspace(0, len(db.AverageHappiness), len(db.AverageHappiness) + 1)
        
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labelbottom=False) # labels along the bottom edge are off
        
        ax.set_ylabel('[%]') 
        ax.plot(xAxis[1:], db.AverageHappiness, color = happinessColor, linewidth=2, alpha=0.6, label="Happiness") 
        ax.plot(xAxis[1:], db.AverageConfidence, color=confidenceColor, linewidth=2, alpha=0.6, label="Average Confidence")
        ax.plot(xAxis[1:], db.VotingForIdealParty, label="Ideal vote", linewidth=2, alpha=0.6)
        ax.plot(xAxis[1:], db.SwingVoteFrac, label="Swing Voters", linewidth=2, alpha=0.6)
        ax.plot(xAxis[1:], db.AverageHappiness, color = happinessColor, linewidth=3, alpha=1) 
        ax.plot(xAxis, np.zeros(len(xAxis)), color="grey", alpha=0.75)
        
        ax.set_ylim(0, 100)
        ax.set_xlim(0, len(db.AverageHappiness))
        plt.xticks(np.round(np.arange(0, len(db.AverageHappiness)+1, 3)))
        plt.grid('on')
        plt.legend(loc="lower left", prop={'size': 8})
         
        
        # Second Plot -> curNumberOfParties
        
        ax = plt.subplot(2,1,2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.grid('on')
        plt.ylabel("Parties", fontsize=12)
        
        ax.set_xlabel('Election', fontsize=14)
        ax.set_xlim(0, len(db.AverageHappiness))
        ax.set_ylim(0, 19)
        plt.plot(xAxis, db.curNumberOfParties)
        plt.xticks(np.round(np.arange(0, len(db.AverageHappiness)+1, 3)))
        plt.yticks(np.arange(0, 19, 3))
        
        
    
    
    def PlotHappiness(self, StoredHappiness, nValues):
        plt.rcParams.update({'font.family':'times new roman'})
        plt.rc('ytick', labelsize=12)
        
        fig, ax = plt.subplots()
        
        plt.title("Average Happiness", fontsize=18)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        plt.tick_params(
                    axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    labelbottom=False) # labels along the bottom edge are off
        
        plt.ylim(0, 100)
        
        plt.ylabel(" - [%] ", fontsize=16)
        plt.yticks(np.arange(0, 101, 10))
        barWidth = 0.25
        cur_x = 0.2
        idx = 0
        
        for nParties in StoredHappiness:
            
            if StoredHappiness[nParties] == []:
                continue

            bar_limits = [cur_x, cur_x + barWidth]
            
            bar_limits_offset = [cur_x + 5/6*barWidth, cur_x + + 5/6*barWidth + barWidth ]
            
            
            color = self.Colors[idx]
            plt.text(cur_x, -8, str(nParties) + " Parties", fontsize=10)
            
            # Percentage of how many times if ended up on this  number of parties
            plt.fill_between(bar_limits_offset, len(StoredHappiness[nParties]) / nValues * 100, alpha=0.5, color=color)
            
            
            # Happienss for this number of parties
            plt.fill_between(bar_limits, np.mean(StoredHappiness[nParties]), alpha=0.9, color=color)
            
            idx += 1
            
            
            cur_x += 3 * barWidth
            
        
        
        
        
        
        
        
        
        