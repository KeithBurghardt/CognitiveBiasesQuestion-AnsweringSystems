import os.path
import ast
from string import maketrans
from scipy.stats import bernoulli
from random import shuffle

firstElements = lambda lol: sorted(list(set([l[0] for l in lol])));
gather_by = lambda lol: [[l for l in lol if l[0] == ind] for ind in firstElements(lol)];
flatten = lambda lol: [s for l in lol for s in l];

#directory = "/Usners/networklab/Dropbox/NaturalExperiment/NE Data3/";
# MAKE DIRECTORY:
directory = "";

NumVoteVsPosition2 = [0]*2;
NumVoteVsPosition8 = [0]*8;

for AnswerBecomesAccepted in ["Accept","NoAccept"]:
    for TotalNumAns in range(2,200):
        #file = directory + "VoteP_Tech_Logit_" + AnswerBecomesAccepted +"_BeforeAnswerAccepted_SO_2-200Q_AfterAug2009_PVoteVs2or8Position_2.csv";
        file = directory + "VoteP_NonTech_Logit_" + AnswerBecomesAccepted +"_BeforeAnswerAccepted_AfterAug2009_PVoteVs2or8Position_"+str(TotalNumAns)+".csv";
        #print(file)#VoteP_NonTech_Logit_Accept_BeforeAnswerAccepted_AfterAug2009_PVoteVs2or8Position_2.csv
        # If file exists...
        if os.path.isfile(file):
            print(file)
            #read file
            r = open(file,"r");
            #header
            header =  r.readline();
            #count amount of data added
            for line in r:
                data = list(ast.literal_eval(line));
                WebpagePos = data[2];
                NumAnsVisible = len(WebpagePos);
                Votes = data[1];
                #print(Votes);
                Votes.sort(key=lambda x: -int(x[1]));
                SortedVotes = Votes;
                #print(SortedVotes);
                ChosenVote = [vote for choose,vote in SortedVotes if choose];
                WebpagePosVoted = [pos for pos,[choose,vote] in enumerate(SortedVotes) if choose];
                
                SameAsChosenVotePos = [pos for pos,[choose,vote] in enumerate(SortedVotes) if vote == ChosenVote];
                NumSameAsChosenVote = len(SameAsChosenVotePos);
                
                
                        

                #WebpagePosVoted = [pos for choose,pos in WebpagePos if choose];
                
                if len(WebpagePosVoted) > 0:
                    WebpagePosVoted = WebpagePosVoted[0];
                    if NumSameAsChosenVote > 0:
                        shuffle(SameAsChosenVotePos);
                        WebpagePosVoted = SameAsChosenVotePos[0];
                    
                    #if its position is unique/non-random
                    if WebpagePosVoted == round(WebpagePosVoted):
                        WebpagePosVoted = int(WebpagePosVoted);
                    else:
                        pHigh=WebpagePosVoted-int(WebpagePosVoted);
                        High = bernoulli.rvs(pHigh, size=1);
                        High = High[0];
                        WebpagePosVoted = int(WebpagePosVoted)+High
                        
                    #print(WebpagePosVoted)
                    #print(WebpagePosVoted);
                    if WebpagePosVoted >= NumAnsVisible:
                        continue;
                        #print(NumAnsVisible);
                        #print(WebpagePosVoted);
                    else:
                        if NumAnsVisible == 2:
                            NumVoteVsPosition2[WebpagePosVoted] = NumVoteVsPosition2[WebpagePosVoted] + 1
                        elif NumAnsVisible == 8:
                            NumVoteVsPosition8[WebpagePosVoted] = NumVoteVsPosition8[WebpagePosVoted] + 1

for NumAnsVisible in [2,8]:
    
    w = open(directory + "NumAnsVoted_AfterAug2009_NonTech_BeforeAnswerAccepted_NumAnsVisible="+str(NumAnsVisible)+"_Vote-Based-Order.csv","w");
    if NumAnsVisible == 2:
        w.write(str(NumVoteVsPosition2))
    elif NumAnsVisible == 8:
        w.write(str(NumVoteVsPosition8))
