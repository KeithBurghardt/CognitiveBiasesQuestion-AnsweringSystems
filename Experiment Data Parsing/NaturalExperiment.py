import os.path
import ast
from string import maketrans

firstElements = lambda lol: sorted(list(set([l[0] for l in lol])));
gather_by = lambda lol: [[l for l in lol if l[0] == ind] for ind in firstElements(lol)];
flatten = lambda lol: [s for l in lol for s in l];

#directory = "/Users/networklab/Dropbox/NaturalExperiment/NE Data3/";
# CREATE A DIRECTORY:
directory = "";

#6 months before versus after or entire dataset?
for ShortTime in ["_6MonthsBeforeAug1or6MonthsAfterAug31",""]:#["_6MonthsBeforeVsAfter",""]:#"_6MonthsBeforeAug1or6MonthsAfterAug31"?
    #for Aggregate in [True,False]:#Aggregate ALL data together across position (not across board or acceptance)
    for DataAge in ["AfterAug2009","BeforeOrDuringAug2009"]:#["AfterAug2009","BeforeOrDuringAug2009"]:#Position effect or not?
        print(DataAge);
        for BoardType in ["Meta", "NonTech","Tech","SO"]:#type of board,  an parallelize this
            print(BoardType);
            for AcceptedQ in ["NoAccept","Accept"]:# questions with answers accepted or not
                
                if BoardType == "SO":
                    NumQList= ["2", "3", "4", "5", "6", "7", "8", "9-12", "13-16", "17-30", "31-200"];
                    if DataAge == "BeforeAug2009":
                        NumQList = ["2-200"]
                    elif ShortTime == "":
                        NumQList= ["2", "3-12", "13-200"]                        
                else:
                    NumQList = [""];
                data = [];
                for NumQ in NumQList:
                    
                    LargestBoard = "";
                    if BoardType == "Tech":
                        LargestBoard = "_NoLargestBoard";
                    WhenVote = "BeforeAnswerAccepted";
                    #Natural Experiment
                    #Before August 2009: answers with same score were ordered chronologically (oldest first)
                    #After August 2009: answers with same score ordered randomly
                    
                    for TotalNumAns in range(2, 200):
                        
                        #file = directory + "VoteP_" + BoardType + "_Logit_" + AcceptedQ + "_" + WhenVote + LargestBoard + "_" + DataAge + "_" + str(TotalNumAns) + ".csv";
                        file = directory + "VoteP_" + BoardType + "_Logit_" + AcceptedQ + "_" + WhenVote + LargestBoard + "_" + DataAge + ShortTime+"_" + str(TotalNumAns) + ".csv";
                        #print(file)
                        if BoardType == "SO":
                            file = directory + "VoteP_Tech_Logit_" + AcceptedQ + "_" + WhenVote + LargestBoard + "_SO_" + NumQ + "Q_" + DataAge +  ShortTime+"_" + str(TotalNumAns) + ".csv";
                        #print(file)
                        # If file exists...
                        if os.path.isfile(file):
                            print(file)
                            #read file
                            r = open(file,"r");
                            #header
                            header =  r.readline();
                            #count amount of data added
                            for line in r:
                                data.append(list(ast.literal_eval(line)));# make sure we convert from string to
                print("data parsed");
                print("data size: %i" % len(data));

                #Split by number of answers visible
                #data.sort(key=lambda x: x[0]);
                SortedData = gather_by(data);
                        
                # gather all data with the number of answers = 2, 3, 4, ...
                #GatherBy[SortBy[data, First], First];
                # count = 1;
                for NumAns in range(2,100):
                    if NumAns not in [list(firstElements(l))[0] for l in SortedData]:
                        SortedData.append([[NumAns, None, None, None, None]]);
                SortedData= sorted(SortedData);
                #SortedData = SortBy[SortedData, First];
                #Find position of answers with same score AND voted on
                ParsedData = [];
                #If there exists cases where X number of answers are visible...
                for NumAnsSublist in SortedData:
                    NumAnsParsedData = [];
                    if len(NumAnsSublist) != 1:
                        for line in NumAnsSublist:
                            NumAns = line[0];
                            AnsPickedAndScores = line[1];
                            
                            #print(line);
                            #break;

                            # GOAL:
                            # Find all answers with 2 scores that are exactly the same, and 1 is picked
                            # record:
                            #     -NumAns, (known)
                            #     -NumAnsWithSameScore=2
                            #     -FirstAnswerWebpagePosition,
                            #     -AnswerPicked
                            
                            #First, find all scores that are the same as the one picked
                            #SameScorePos = 0;
                            #index = 0;

                            ChosenAnswerPos = [i for i,[AnsPicked,score] in enumerate(AnsPickedAndScores) if AnsPicked][0]# if TF is true, answer chosen
                            SameScore = AnsPickedAndScores[ChosenAnswerPos][1];
                            
                            #for TF,score in AnsPickedAndScores:
                            #    if TF:
                            #        SameScore = score;
                            #        #SameScorePos = 
                            #        break;
                            #    #index = index + 1;


                            #SameScoreNum = 0;
                            SameScorePos = [i for i,[AnsPicked,score] in enumerate(AnsPickedAndScores) if score== SameScore]
                          
                            if len(SameScorePos) == 2:
                                OrderedScores = list(reversed(sorted([s for tf,s in AnsPickedAndScores])));#highest score first
                                #position of first answer with the same score
                                FirstAnswerWebpagePosition = [i for i,score in enumerate(OrderedScores) if score == SameScore][0];
                                
                                #chronological position of answer picked, e.g., oldest answer, second-oldest, etc...
                                #for all answers with the same score
                                AnswerPicked = [i for i,[AnsPicked,score] in enumerate([AnsPickedAndScores[i] for i in SameScorePos]) if AnsPicked][0];# starts at 0
                                
                                #lists whether any answer with the same score is accepted
                                Accepted =[line[4][i][0] for i in SameScorePos];
                                #Before Answer Accepted: this is true by default
                                #only collect data if none of the answers were accepted
                                if True:#all([not accepted_ans for accepted_ans in Accepted]):
                                    NumAnsWithSameScore = len(SameScorePos)
                            
                                    #Number of asnwer, number with the same score, position range, Accepted?,
                                    #Which answer picked (chronologically ordered)*)
                                    NumAnsParsedData.append([NumAns, NumAnsWithSameScore, FirstAnswerWebpagePosition, AnswerPicked]);
                    ParsedData.append(NumAnsParsedData)


                #Gather by the webpage position, and only look at when two answers have the same score
                WebPosChronOrder = [[] for i in range(len(ParsedData))]
                index = 0;
                for sublist in ParsedData:
                    if len(sublist)>0:
                        #print(sublist[1:2]);
                        #break;
                        for subsublist in sublist:
                            # only 2 answers with the same score
                            if subsublist[1] == 2:
                                #record:
                                #FirstAnswerWebpagePositio
                                #Answer picked (chronologically ordered from oldest to newest answer with the same score)
                                WebPosChronOrder[index].append(subsublist[2:])
                        WebPosChronOrder[index] = gather_by(WebPosChronOrder[index]);
                    index = index + 1;
                for Aggregate in [True,False]:
                    for AnswerWebpagePos in [1, 3, 5]: #position: 1-2 or 3-4,
                        if Aggregate and AnswerWebpagePos != 1:
                            continue;
                        pVsNumAns = [];
                        NumAns = 1;
                        for NumAnsList in WebPosChronOrder:
                            NumAns = NumAns + 1; 
                            if len(NumAnsList) > 0:
                                ChronOrderedAnswerPicked = [];
                                for WebPageOrderList in NumAnsList:
                                    WebPageOrder = WebPageOrderList[0][0]
                                    
                                    if Aggregate:
                                        ChronOrderedAnswerPicked.append([pos for webpage_order,pos in WebPageOrderList]);
                                    else:
                                        if WebPageOrder == AnswerWebpagePos - 1:
                                            ChronOrderedAnswerPicked = [pos for webpage_order,pos in WebPageOrderList];
                                            AmountOfData=len(ChronOrderedAnswerPicked);
                                            #this is the probability of picking the NEWEST answer = 1-(probability of picking the oldest)
                                            PNewPicked = float(sum(ChronOrderedAnswerPicked))/AmountOfData;
                                            pVsNumAns.append([NumAns,PNewPicked,AmountOfData])
                                if Aggregate:
                                    ChronOrderedAnswerPicked = flatten(ChronOrderedAnswerPicked)
                                    AmountOfData=len(ChronOrderedAnswerPicked);
                                    #this is the probability of picking the NEWEST answer = 1-(probability of picking the oldest)
                                    PNewPicked = float(sum(ChronOrderedAnswerPicked))/AmountOfData;
                                    pVsNumAns.append([NumAns,PNewPicked,AmountOfData])
                        file = directory + "P_" + BoardType + AcceptedQ + "_" + DataAge +ShortTime+ "_Aggregate.csv";
                        if not Aggregate:
                            NumQDisplay="";
                            file = directory + "P_" + BoardType + AcceptedQ + "_" + WhenVote + LargestBoard + "_" + DataAge + "_WebpagePos=" +  str(AnswerWebpagePos) + NumQDisplay+ShortTime+".csv";
                        w = open(file,"w");
                        for sublist in pVsNumAns:
                            #print(sublist);
                            line = str(sublist);
                            #print(line);
                            line=line.translate(maketrans('[', ' ')).translate(maketrans(']', ' ')).strip()
                            w.write(line+'\n');
                data =[];
                SortedData = [];

     

