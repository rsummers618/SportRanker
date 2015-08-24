from datetime import datetime
from tempfile import NamedTemporaryFile
import shutil
import csv
import os
import re
from PySide import QtGui
import sys
import math
import Analyze

year= "2014"
week= "18"
source = "sports-reference"
stat_funciton = "score"
function = None
Ranking_Week = 10
Opening_Week = -1
previousYearWeight = 1.0
HomeFieldAdvantage = 0.0
SpreadScaleDenom = 425

functionsFromSource = {
    'sports-reference': ['Result','Pass_Cmp','Pass_Att','Pass_Pct','Pass_Yds','Pass_TD','Rush_Att','Rush_Yds','Rush_Avg',
                         'Rush_TD','Tot_Plays','Tot_Yds','Tot_Avg','FirstDn_Pass','FirstDn_Rush','FirstDn_Pen','FirstDn_Tot',
                         'Pen_No.','Pen_Yds','TO_Fum','TO_Int','TO_Tot'],
    'ESPN PBP Data': 	['Points','DriveSuccessRate','TOAdjustedPointsSimple','YPP'],
    'ESPN Box Scores':	[]
}

def getStatFromParameterString(Parameter):
    if Parameter == 'Points':
        return Analyze.SF_Points
    if Parameter == 'DriveSuccessRate':
        return Analyze.SF_DriveSuccessRate
    if Parameter == 'TOAdjustedPointsSimple':
        return Analyze.SF_TOAdjustedPointsSimple
    if Parameter == 'YPP':
        return Analyze.SF_YPP


def change_week(new_week):
    global week
    week = str(new_week)
    #assign_first_week()

def change_year(new_year):
    global year
    year = str(new_year)
    assign_first_week()

def change_source(new_source):
    global source
    source = str(new_source)

def change_function(new_function):
    global function
    function = new_function


def getFunctions(source):
    global functionsFromSource
    return functionsFromSource[source]



def assign_first_week():

    #Find all Teams
    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb")
    reader = csv.DictReader(f_obj, delimiter=',')
    openingweek = 55

    #loop through every team file
    for team in reader:
        #print(team["link"])
        filepath =os.path.dirname(os.path.realpath(__file__)) + '/Schools/' + team["teamName"] + '/' + year + '/'
        filename = filepath + team["teamName"] + ' ' + year + ' defense.csv'
        f_obj2=open(filename,"rb")
        schedule = csv.DictReader(f_obj2, delimiter=',')
        for game in schedule:
            try:
                week = ConvertToTuesdayWeek(game["Date"])
                if week < openingweek and week >30:
                    openingweek = week
            except:
                continue
    global Opening_Week
    Opening_Week = openingweek





def ConvertToTuesdayWeek(datestring):
    date = datetime.strptime(datestring, "%Y-%m-%d")
    week = datetime.date(date).isocalendar()[1]
    #print datestring
    #print date
    #print week
    #print " week is " + str(week)
    ''' if int(week) < 20:

        tempWeek = datetime.date(datetime.strptime(year+"-12-31")).isocalendar()[1]
        week = int(tempWeek) + week -1
        ###### WILL BE WRONG FOR ROSE BOWL WEEK GAMES
        #############################################
        #if week != 1:
         #   week = week -1;
        print "datestring " + datestring + " is week " + str(week)'''
    #print "returning week " + str(week)
    return int(week)

def ConvertToGameWeek(datestring):
    WeekofYear = ConvertToTuesdayWeek(datestring)
    #print "datestring is " + str(datestring)
    #print "week of year is " + str(WeekofYear)

    global Opening_Week
    #print " Opening week is " + str(Opening_Week)
    gameweek = int(WeekofYear) - int(Opening_Week) + 1
    if int(gameweek) < 0:
        gameweek =  52 - int(Opening_Week) + WeekofYear
        #print "gameweek is " + str(gameweek)
    return gameweek

'''
def SeparateScore
    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb")
    reader = csv.DictReader(f_obj, delimiter=',')



    for team in reader:
        #print(team["link"])
        filepathDef =os.path.dirname(os.path.realpath(__file__)) + '/Schools/' + team["teamName"] + '/' + year + '/'
        filenameDef = filepathDef + team["teamName"] + ' ' + year + ' defense.csv'
        f_objDef=open(filenameDef,"rb")
        scheduleDef = csv.DictReader(f_objDef, delimiter=',')

        filepathOff =os.path.dirname(os.path.realpath(__file__)) + '/Schools/' + team["teamName"] + '/' + year + '/'
        filenameOff = filepathOff + team["teamName"] + ' ' + year + ' offense.csv'
        f_objOff=open(filenameOff,"rb")
        scheduleOff = csv.DictReader(f_objDef, delimiter=',')

        DefResult = 0
        OffResult = 0

        for game in scheduleDef:
            try:
                DefResult = 0'''
def CalculateRankingsOfSingleWeek(WeekNumber,Parameter):
    return 0

def CalculateRankingsPrevYear(WeekNumber,Parameter):

    global year

    Adjust = False
    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb")
    reader = csv.DictReader(f_obj, delimiter=',')
    Score = CreateComparisonMatrix()
    year = str(int(year) -1)
    LastOff,LastDef = MakeScoreMatrixAtWeek(30,Parameter)
    LastDef[129] = 1.50
    LastOff[129] = 10
    year = str(int(year) +1)
    DefenseScore = [1 for x in range(130)]
    OffenseScore = [1 for x in range(130)]
    Games = GetGamesOnWeek(WeekNumber, Parameter)
    for game in Games:

        OffenseScore[IndexOfTeam(game[0])] = float(game[1])/LastDef[IndexOfTeam(game[2])]
        OffenseScore[IndexOfTeam(game[2])] = float(game[3])/LastDef[IndexOfTeam(game[0])]
        DefenseScore[IndexOfTeam(game[0])] = float(game[3])/LastOff[IndexOfTeam(game[2])]
        DefenseScore[IndexOfTeam(game[2])] = float(game[1])/LastOff[IndexOfTeam(game[0])]

        print game[0] + "Off is now " + str(OffenseScore[IndexOfTeam(game[0])]) + " scoring " + str(float(game[1])) + " vs " + game[2] + " defscore " + str(LastDef[IndexOfTeam(game[2])])



    if WeekNumber == 1:
        for i in range (1,129):

            OffenseScore[i] = (OffenseScore[i] + LastOff[i])/2
            DefenseScore[i] = (DefenseScore[i] + LastDef[i])/2
            if DefenseScore[i] == 0:
                DefenseScore[i] = 1
    else:
        offtemp, deftemp = CalculateRankingsPrevYear(WeekNumber -1,Parameter)
        for i in range (1,129):
            OffenseScore[i] = OffenseScore[i]/WeekNumber + (WeekNumber -1)*offtemp[i]/WeekNumber
            DefenseScore[i] = DefenseScore[i]/WeekNumber + (WeekNumber -1)*deftemp[i]/WeekNumber
            if DefenseScore[i] == 0:
                DefenseScore[i] = 1


    return OffenseScore , DefenseScore
    #CalculateRankingPrevYear(

def MakeScoreMatrixAtWeek(Parameter,WeekNumber):

    global year
    global source
    if source == 'ESPN PBP Data':
        play_arr = Analyze.Read_CSV('../rcfbScraper/ESPN_Scraper/'+year+' Stats/play.csv')
        function = getStatFromParameterString(Parameter)
        matrix = Analyze.GenerateMatrixForStat(function,play_arr)
        return matrix
    #elif source == 'ESPN Box Scores':
    #else: // CFB REFERENCE




    Adjust = False
    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb")
    reader = csv.DictReader(f_obj, delimiter=',')

    Score = CreateComparisonMatrix()


    #print "getting rankings year " +year
    #print Score
    #loop through every team file
    for team in reader:
        #print(team["link"])
        filepathDef =os.path.dirname(os.path.realpath(__file__)) + '/Schools/' + team["teamName"] + '/' + year + '/'
        filenameDef = filepathDef + team["teamName"] + ' ' + year + ' defense.csv'
        f_objDef=open(filenameDef,"rb")
        scheduleDef = csv.DictReader(f_objDef, delimiter=',')

        filepathOff =os.path.dirname(os.path.realpath(__file__)) + '/Schools/' + team["teamName"] + '/' + year + '/'
        filenameOff = filepathOff + team["teamName"] + ' ' + year + ' offense.csv'
        f_objOff=open(filenameOff,"rb")
        scheduleOff = csv.DictReader(f_objOff, delimiter=',')

        DefResult = 0
        OffResult = 0

        for game in scheduleDef:
            try:
                DefResult = 0
                week = ConvertToGameWeek(game["Date"])
                #print week
                if week <= WeekNumber and week > 0:

                    if(Parameter == "Result"):

                        OffResult,DefResult=ParseScore( str(game[Parameter]),Adjust)
                        if OffResult == -1 or DefResult == -1:
                            print "ERROR DOUBLE ZERO" + game["Opponent"] + " and " + game["teamName"]

                            continue
                        WriteMatrixAt(Score,game["Opponent"],team["teamName"],OffResult)

                    else:
                        DefResult = game[Parameter]

                    #WriteMatrixAt(Score,game["Opponent"],team["teamName"],DefResult)
                    WriteMatrixAt(Score,team["teamName"],game["Opponent"],DefResult)



            except:
                continue

        for game in scheduleOff:
            try:
                OffResult = 0
                week = ConvertToGameWeek(game["Date"])

                if week <= WeekNumber and week > 0:

                    if(Parameter == "Result"):
                        continue
                    else:
                        OffResult = game[Parameter]

                    WriteMatrixAt(Score,game["Opponent"],team["teamName"],OffResult)
                    #WriteMatrixAt(Score,team["teamName"],game["Opponent"],DefResult)


            except:
                continue

    return Score

def CalculateRanksFromScoreMatrix(Score,WeekNumber,Parameter):
    global year
    #print "Calculating ranks Year " + year + " week " + str(WeekNumber)
    #print Score
    PrevDefScore = [1 for x in range(len(Score))]
    PrevOffScore = [1 for x in range(len(Score))]
    DefenseScore = [1 for x in range(len(Score))]
    OffenseScore = [1 for x in range(len(Score))]
    if WeekNumber == 0:
        try:
            year = str(int(year) -1)
            OffenseScore, DefenseScore  = CalculateRanksFromScoreMatrix(MakeScoreMatrixAtWeek(Parameter,25), 25,Parameter)
            year = str(int(year) + 1)
        except:
            result = True
            while result != False:
                #for x in range (0,1):
                result = iterate(Score,DefenseScore,OffenseScore,PrevDefScore,PrevOffScore,WeekNumber)

    elif WeekNumber < 8:
        try:
            result = True
            year = str(int(year) -1)
            PrevOffScore,PrevDefScore = CalculateRanksFromScoreMatrix(MakeScoreMatrixAtWeek(Parameter,25), 25,Parameter)

            #print "prev Off Score of year " + year
            #print PrevOffScore
            #print PrevDefScore
            year = str(int(year) + 1)
            while result != False:
            #for x in range (0,1):

                result = iterate(Score,DefenseScore,OffenseScore,PrevDefScore,PrevOffScore,WeekNumber)
        except:
            result = True
            while result != False:
                #for x in range (0,1):
                result = iterate(Score,DefenseScore,OffenseScore,PrevDefScore,PrevOffScore,WeekNumber)


    else:
        result = True
        while result != False:
        #for x in range (0,1):
            result = iterate(Score,DefenseScore,OffenseScore,PrevDefScore,PrevOffScore,WeekNumber)

       # year = str(int(year) +1)


    #print OffenseScore
    return OffenseScore, DefenseScore

def IndexOfTeam(TeamName):
    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb")
    reader = csv.reader(f_obj, delimiter=',')
    reader = list(reader)
    #Team = reader.next()

    for j in range(1,129):
        if str(reader[j][1]) == TeamName:
            #print " index " + str(j) + " is " + str(reader[j][1]) + " = to " + TeamName
            return j
    return 129

def PredictGames(Offscore,DefScore,UpcomingGames):


    Predictlist = [[0 for i in range (2)] for j in range(4)]
    for Game in UpcomingGames:
       # print Game[2]
        #print Game[0]


        #Home advantage
        HomeModifier0 = 0;
        HomeModifier1 = 0;
        '''
        if Game[4] == "@":
            print  Game[2] +" HOME GAME!"
            HomeModifier1 = 3
        elif Game[4] == "N":
            print "Neutral Game *((((((((((((((**************************************"
        else:
            HomeModifier0 = 3'''
        #if IndexOfTeam(Game[0]) == 129 or IndexOfTeam(Game[2]) == 129:
        #    continue
        Team0Score = (Offscore[IndexOfTeam(Game[0])]+HomeModifier0) * DefScore[IndexOfTeam(Game[2])]# + HomeModifier0
        Team1Score = (Offscore[IndexOfTeam(Game[2])]+HomeModifier1) * DefScore[IndexOfTeam(Game[0])]# + HomeModifier1
        #print "Prediction: " +Game[0] + " " + str(Team0Score) + " - "+Game[2] + " " + str(Team1Score)



        Predictlist[0].append(Game[0])
        Predictlist[1].append(Team0Score)
        Predictlist[2].append(Game[2])
        Predictlist[3].append(Team1Score)

    Predictlist = zip(*Predictlist)
    Predictlist.pop(0)
    Predictlist.pop(0)
    #print Predictlist
    return Predictlist

def PredictionAccuracy(UpcomingGames,Prediction):

    GameCount = 0
    GamesRight = 0
    for i in range(0,len(Prediction)):
        if IndexOfTeam(Prediction[i][0]) == 129 or IndexOfTeam(Prediction[i][2]) == 129:
            #print "Removing "+ Prediction[i][0] + "'s Game"
            continue
        GameCount = GameCount +1
        if float(UpcomingGames[i][1]) > float(UpcomingGames[i][3]) and float(Prediction[i][1]) > float(Prediction [i][3]):
            #print "Correct Prediction"
            GamesRight = GamesRight +1
        elif float(UpcomingGames[i][1]) < float(UpcomingGames[i][3]) and float(Prediction[i][1]) < float(Prediction [i][3]):
           # print "Correct Prediction"
            GamesRight = GamesRight +1
        else :
            a = 1
            #print UpcomingGames[i][0] + " v " + UpcomingGames[i][2] + " " + str(UpcomingGames[i][1]) + "-"+ str(UpcomingGames[i][3]) + " Guessed " +str(Prediction[i][1]) + "-"+ str(Prediction[i][3])
    #print "Got " + str(GamesRight) + " out of " +  str(GameCount)
    return GamesRight,GameCount

def PredictionAccuracySpread(UpcomingGames,Prediction):

    #print UpcomingGames
    GameCount = 0
    GamesRight = 0
    for i in range(0,len(Prediction)):
        try:
            VegasSpread = float(UpcomingGames[i][5])

        except:
            continue
        GameCount = GameCount +1
        predictedSpread = float(Prediction[i][3]) - float(Prediction [i][1])
        actualSpread = float(UpcomingGames[i][3]) - float(UpcomingGames[i][1])
        if abs(predictedSpread - VegasSpread) > 20:
            print UpcomingGames[i][0] + " v " + UpcomingGames[i][2] + " " + str(UpcomingGames[i][1]) + "-"+ str(UpcomingGames[i][3]) + " Guessed " +str(Prediction[i][1]) + "-"+ str(Prediction[i][3]) + "  spread was " +str(VegasSpread) + " Guessed spread: " + str(predictedSpread)

        if predictedSpread > VegasSpread and actualSpread > VegasSpread:
        #    print "Correct Prediction"
            GamesRight = GamesRight +1
        elif predictedSpread < VegasSpread and actualSpread < VegasSpread:
        #    print "Correct Prediction"
            GamesRight = GamesRight +1
        #'''if VegasSpread > 0 and actualSpread > 0:
        #    print "Correct Prediction"
        #    GamesRight = GamesRight +1
        #if VegasSpread < 0 and actualSpread < 0:
        #    print "Correct Prediction"
        #    GamesRight = GamesRight +1'''

        else:
            a = 1
        #    print"Game Wrong"
        #print UpcomingGames[i][0] + " v " + UpcomingGames[i][2] + " " + str(UpcomingGames[i][1]) + "-"+ str(UpcomingGames[i][3]) + " Guessed " +str(Prediction[i][1]) + "-"+ str(Prediction[i][3]) + "  spread was " +str(VegasSpread) + " Guessed spread: " + str(predictedSpread)
   # print "Got " + str(GamesRight) + " out of " +  str(GameCount)
    return GamesRight,GameCount

def GetGamesOnWeek(Targetweek,metric):

    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb")
    reader = csv.DictReader(f_obj, delimiter=',')

    Gamelist = [[0 for i in range (2)] for j in range(6)]

    #print Score
    #loop through every team file
    for team in reader:
        #print(team["link"])
        filepathDef =os.path.dirname(os.path.realpath(__file__)) + '/Schools/' + team["teamName"] + '/' + year + '/'
        filenameDef = filepathDef + team["teamName"] + ' ' + year + ' defense.csv'
        f_objDef=open(filenameDef,"rb")
        scheduleDef = csv.DictReader(f_objDef, delimiter=',')

        for game in scheduleDef:
            try:

                week = ConvertToGameWeek(game["Date"])


                if week == Targetweek and week > 0:
                    Add = True

                    for Game in Gamelist[2]:
                        #print Game
                        if Game == team["teamName"]:# or Gamelist[2] == team["teamName"]:
                           # print "Found duplicate game 2" + Game
                            Add = False
                    if Add == True:
                        TeamScore,OpponentScore = ParseScore(str(game["Result"]),False)
                        if int(TeamScore) < 0:
                            print "Why invalid game? on team = " + team + " vs " + game["Opponent"]
                        Gamelist[0].append(team["teamName"])

                        Gamelist[1].append(TeamScore)
                        Gamelist[2].append(game["Opponent"])
                        Gamelist[3].append(OpponentScore)
                        Gamelist[4].append(game["At"])
                        try:
                            Gamelist[5].append(game["Spread"])
                        except:
                            Gamelist[5].append("NO SPREAD")
                            #print "This was the Error!"
                            #print (game["Opponent"])
                            #print team["teamName"]
                            #print str(game["Spread"])
                        #print "added a game " + str(team["teamName"]) + " v " + str(game["Opponent"])
            except:
                #print str(game["Result"])
                #print "Failed to add game to list"
                continue

    Gamelist = zip(*Gamelist)
    Gamelist.pop(0)
    Gamelist.pop(0)
    #for game in Gamelist:
        #print game
    return Gamelist

def AvgofStatAtWeek(WeekNumber,Parameter):
    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb")
    reader = csv.DictReader(f_obj, delimiter=',')

    DefenseScore = [1 for x in range(131)]
    OffenseScore = [1 for x in range(131)]
    #print Score
    #loop through every team file
    teamNumber = 1
    for team in reader:

        #print(team["link"])
        filepathDef =os.path.dirname(os.path.realpath(__file__)) + '/Schools/' + team["teamName"] + '/' + year + '/'
        filenameDef = filepathDef + team["teamName"] + ' ' + year + ' defense.csv'
        f_objDef=open(filenameDef,"rb")
        scheduleDef = csv.DictReader(f_objDef, delimiter=',')



        DefSum = 0
        OffSum = 0
        DefGames=0
        OffGames=0

       # print scheduleDef
       # print "New Team"
        for Defgame in scheduleDef:
           # print "New Game"
            try:
                week = ConvertToGameWeek(Defgame["Date"])
                val1,val2 = ParseScore(str(Defgame["Result"]),False)
                if week <= WeekNumber and week > 0 and val1 != -1:
                   # print "Def Game Added"
                    DefSum = DefSum + float(Defgame[Parameter])
                    DefGames = DefGames +1
            except:
                dummy =1
               # print "End"
                #continue

       # f_objDef.close()

        filepathOff =os.path.dirname(os.path.realpath(__file__)) + '/Schools/' + team["teamName"] + '/' + year + '/'
        filenameOff = filepathOff + team["teamName"] + ' ' + year + ' offense.csv'
        f_objOff=open(filenameOff,"rb")
        scheduleOff = csv.DictReader(f_objOff, delimiter=',')

        #print scheduleOff

        for Offgame in scheduleOff:
           # print "New Game"
            try:
                week = ConvertToGameWeek(Offgame["Date"])
                val1,val2 = ParseScore(str(Offgame["Result"]),False)
                if week <= WeekNumber and week > 0  and val1 != -1:
                   # print "off game added"
                    OffSum = OffSum + float(Offgame[Parameter])
                    OffGames = OffGames +1

            except:
                dummy = 1
               # print "end"
                #continue


   # print OffenseScore
   # print DefenseScore
    return OffenseScore, DefenseScore

def CompositeScore(OffenseScore,DefenseScore):
    Composite = [1 for x in range(len(OffenseScore))]
    for d in range (1,len(OffenseScore)):
        Composite[d] = OffenseScore[d]/DefenseScore[d]
    return Composite


def ParseScore(result,Adjust):
    #print result
    regex = re.compile("\((.+)\)")
    m = re.search(regex, result)
    inner_str = m.group(1)
    #print "Substrings:" + inner_str
    mylist = inner_str.split("-", 1)
    #print mylist
    #print "blah"
    #if re.compile('W').match(game["Result"]):
        #print "WIN!"
    #if game["Opponent"] == "Arizona State" or team["teamName"] == "Arizona State":
    #    print game["Result"]
    if Adjust:
        if float(mylist[0]) > float(mylist[1]):
             mylist[0] = float(mylist[0]) + 1
             mylist[1] = float(mylist[1]) - 1
        if float(mylist[1]) > float(mylist[0]):
             mylist[1] = float(mylist[1]) + 1
             mylist[0] = float(mylist[0]) - 1
        if float(mylist[0]) > float(mylist[1]) + 14:
             mylist[0] = float(mylist[1]) + 14 +  (float(mylist[0]) - (float(mylist[1]) + 14))/5
        if float(mylist[1]) > float(mylist[0]) + 14:
             mylist[1] = float(mylist[0]) + 14 +  (float(mylist[1]) - (float(mylist[0]) + 14))/5
    if mylist[1] == mylist[0]:
        #print "WHATS THIS A TIE!?"
        #print mylist[1]
        #print mylist[0]
        return -1,-1

    if float(mylist[1]) == 0 and float(mylist[0]) == 0:
        #print "ERROR DOUBLE ZERO" + game["Opponent"] + " and " + game["teamName"]
        return -1,-1



    return mylist[0],mylist[1]

def CalculateGameWeight(Scores,DefScore,OffScore,T1,T2):
    global SpreadScaleDenom
    PredictedSpread = OffScore[T1] * DefScore[T2] - OffScore[T2] * DefScore[T1]

    ActualSpread = float(Scores[T1][T2]) - float(Scores[T2][T1])
    # if T1 == 115 or T2 ==115:
        #print "Scores are "  + str(T1) + " " + str(float(Scores[T1][T2])) + " vs " +  str(float(Scores[T2][T1])) + " " + str(T2)
        #print "Def Off 1: " + str(OffScore[T1]) + " " + str(DefScore[T1]) + " Def Off 2: " + str(OffScore[T2]) + " " + str(DefScore[T2])
        #print "Predicted " + str(PredictedSpread) + "  Actual " + str(ActualSpread)# + "  Weight " + str(Weight)
    if SpreadScaleDenom == 0:
        return 1
    Weight = math.exp(ActualSpread  *PredictedSpread / SpreadScaleDenom)
   # print "Predicted " + str(PredictedSpread) + "  Actual " + str(ActualSpread) + "  Weight " + str(Weight)

    #if Weight > 1:
    #    return 1
    return Weight

def iterate(Scores, DefScore, OffScore, PrevDefScore, PrevOffScore, WeekNumber):

    dampingFactor = 0.85
    global previousYearWeight

    RunAgain = False
    for o in range(1,len(OffScore)):
        Sum = 0.0
        NumGames = 0.0
        TotalPoints = 0.0
        #WeightDenom = 0
        for d in range (1,len(OffScore)):
            if float(Scores[d][o]) < 0:
                #print "excluding score" + str(o) + str(d)
                continue

            OffPower = float(Scores[d][o]) +.00001
            #if d > 70:
            #    Sum = Sum + 0.5*OffPower/(DefScore[d]+.00001)
           # else:
            #Weight = CalculateGameWeight (Scores,DefScore,OffScore,o,d)
            #Weights[o][d] = Weight
            #Weights[d][o] = Weight
           # print "Offense " + str(o) + " scored " + str(float(Scores[d][o])+.00001) + " vs Defscore " + str(DefScore[d]) + " Weighted " + str(Weight)
            Sum = Sum + (OffPower/(DefScore[d]+.00001))
            TotalPoints = TotalPoints + OffPower
            #WeightDenom = WeightDenom + Weight
            #NumGames = NumGames + 1#Weight
            #else:
              #  Sum = Sum - 3
            NumGames = NumGames +1
        if NumGames ==0:
            OffScore[o] = PrevOffScore[o]
        else:
            #if NumGames < 8:
            #    #print "off score prev of " +str(o) + " is " + str(PrevOffScore[o])
                #print "prevYearWeight = " + str(previousYearWeight)
            #    Sum = Sum + previousYearWeight*PrevOffScore[o]
            #    NumGames = NumGames + previousYearWeight
            #    WeightDenom = WeightDenom + previousYearWeight
            #Sum = Sum/WeightDenom

            Sum = (Sum*dampingFactor + (1-dampingFactor)*TotalPoints)/NumGames
            #print "Sum = " + str(Sum)
            #print "Offscore = " + str(OffScore[o])
            if abs(Sum - OffScore[o]) > .1:
               # print "Sum = " + str(Sum)
                #print "Offscore = " + str(OffScore[o])
               # print "RUNNING AGAIN " + str(abs(Sum - OffScore[o]))
                RunAgain = True
            OffScore[o]= Sum
    for d in range(1,len(OffScore)):
        Sum = 0.0
        NumGames = 0.0
        TotalPoints = 0.0
        #WeightDenom = 0
        for o in range (1,len(OffScore)):
            if float(Scores[d][o]) < 0:
                #print "excluding score" + str(o) + str(d)
                continue

            #Weight = CalculateGameWeight (Scores,DefScore,OffScore,d,o)
            #print "Defense " + str(d) + " allowed " + str(float(Scores[d][o])+.00001) + " vs Offscore " + str(OffScore[o]) + " Weighted " + str(Weight)
            Sum = Sum +  ((float(Scores[d][o])+.00001)/(OffScore[o]+.00001))
            TotalPoints = TotalPoints + float(Scores[d][o])
            #WeightDenom = WeightDenom# + Weight
            NumGames = NumGames +1
        if NumGames ==0:
            DefScore[d] = PrevDefScore[d]
        else:
            #if NumGames < 8:
            #    Sum = Sum + PrevDefScore[d] * previousYearWeight
            #    NumGames = NumGames +previousYearWeight
            #    WeightDenom = WeightDenom + previousYearWeight
            # print "Sum is " + str(Sum) + " / " + str(WeightDenom) + " = " + str(Sum/WeightDenom)
            #Sum = Sum/WeightDenom
            #print "Defense " + str(d) + " Defscore is now " + str(Sum)
            Sum = Sum /NumGames
            #Sum = Sum*(dampingFactor)/NumGames + (1-dampingFactor)#*(TotalPoints)/NumGames  )/30
            if abs(Sum - DefScore[d]) > .01:
               # print "Sum = " + str(Sum)
               # print "Defscore = " + str(DefScore[o])
                #print "RUNNING AGAIN"
                #print "RUNNING AGAIN " + str(abs(Sum - OffScore[o]))
                RunAgain = True
            DefScore[d]= Sum

    #print OffScore
    #print DefScore
    return RunAgain

def SeasonRecap(Scores, DefScore, OffScore):
    #print "Prev Def Score in iterate is "
    #print PrevDefScore
    #print PrevOffScore
    DefenseRecap = [["" for i in range (130)] for j in range(17)]
    OffenseRecap = [["" for i in range (130)] for j in range(17)]
    for o in range(1,129):
        #Sum = 0.0
        NumGames = 0
        #TotalPoints = 0
        #WeightDenom = 0
        OffenseRecap[0][o] = str(OffScore[o])
        for d in range (1,130):
            if float(Scores[d][o]) < 0:
                #print "excluding score" + str(o) + str(d)
                continue

            OffPower = float(Scores[d][o]) +.00001
            #if d > 70:
            #    Sum = Sum + 0.5*OffPower/(DefScore[d]+.00001)
           # else:
            Weight = CalculateGameWeight (Scores,DefScore,OffScore,o,d)
            Sum = Weight * (OffPower/(DefScore[d]+.00001))
            #TotalPoints = TotalPoints + OffPower
            #WeightDenom = WeightDenom + Weight

            #else:
              #  Sum = Sum - 3
            #NumGames = NumGames +1
            NumGames = NumGames + 1
            print " O " + str(o) + " d " + str(d) + " NumGames " + str(NumGames)
            OffenseRecap[NumGames][o] = "%.2f Scoring %.2f against (%.2f) Weight %.2f"  %(OffPower/(DefScore[d] + 0.00001), OffPower ,DefScore[d], Weight)


    for d in range(1,129):
        #Sum = 0.0
        NumGames = 0
        OffenseRecap[0][d] = str(DefScore[d])
        #TotalPoints = 0
       # WeightDenom = 0
        for o in range (1,130):
            if float(Scores[d][o]) < 0:
                #print "excluding score" + str(o) + str(d)
                continue

            Weight = CalculateGameWeight (Scores,DefScore,OffScore,o,d)
            Sum = Sum +  ((float(Scores[d][o])+.00001)/(OffScore[o]+.00001))
            #TotalPoints = TotalPoints + float(Scores[d][o])
           # WeightDenom = WeightDenom + Weight
            NumGames = NumGames +1
            DefenseRecap[NumGames][d] = "%.2f Gave %.2f against (%.2f) Weight %.2f"  %((float(Scores[d][o])+.00001)/(OffScore[o]+.00001), float(Scores[d][o]) ,OffScore[o], Weight)

    return OffenseRecap,DefenseRecap

def PrintRanks(Ranking,Title,LowestFirst):
    print Title
    #Matrix = [[ 0 for i in range(2)] for j in range(130)]

    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb")
    reader = csv.reader(f_obj, delimiter=',')
    reader = list(reader)
    #Team = reader.next()

    i = 0
    index = -1
    HighestVal = -1
    LowestVal= 99999
    PrevValLow = -1
    PrevValHigh = 9999
    for j in range(1,129):
        HighestVal = -1
        LowestVal= 99999
        for i in range (1,129):


            if LowestFirst:
                if Ranking[i] < LowestVal and Ranking[i] > PrevValLow:
                    LowestVal = Ranking[i]
                    index = i
            else:
                if Ranking[i] > HighestVal and Ranking[i] < PrevValHigh:
                    HighestVal = Ranking[i]
                    index = i
        #print index
        if LowestFirst:
            print str(j) + ": " +reader[index][1] +"  -  " + str(LowestVal)
            PrevValLow = LowestVal
        else:
            PrevValHigh = HighestVal
            print str(j) + ": " +reader[index][1] +"  -  " + str(HighestVal)


def CreateComparisonMatrix():




    Matrix = [[ -1 for i in range(130)] for j in range(130)]

    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb")
    reader = csv.DictReader(f_obj, delimiter=',')
    #Team = reader.next()

    i = 0
    for team in reader:
        Matrix[0][i+1] = team["teamName"]
        Matrix[i+1][0] = team["teamName"]
        i = i +1

    Matrix[0][129] = "FCS"
    Matrix[129][0] = "FCS"

    #print "Created Matrix!"
    return Matrix

    '''
    filepath = os.path.dirname(os.path.realpath(__file__)) + '/RankingFiles/'
    filename = filepath + InputFilename + '.csv'

    f = open(filename,'wb+')
    writer=csv.writer(f)

    csv_path ='Teamlist.csv'
    f_obj=open(csv_path, "rb")
    reader = csv.DictReader(f_obj, delimiter=',')

    #loop through every team file
    TopRow = " "
    OtherRow=""
    for team in reader:
        TopRow= TopRow + ',' + team["teamName"]
        OtherRow=OtherRow + ','
    TopRow = TopRow + ',FCS'
    writer.writerow(TopRow.split(","));
    f_obj.close()
    f_obj=open(csv_path, "rb")
    reader2 = csv.DictReader(f_obj, delimiter=',')
    for team2 in reader2:
        #print team2["teamName"]
        Row = team2["teamName"] + OtherRow
        writer.writerow(Row.split(","))
    Row = "FCS" + OtherRow
    writer.writerow(Row.split(","))
    f.close()'''

def AppendSpreadToCSV():

    def TeamName(x):
         return {"Southern Cal":"Southern California",
                 "U.C.L.A.":"UCLA",
                 "Florida Intl":"Florida International",
                 "U-A-B":"Alabama-Birmingham",
                 "Miami-Ohio":"Miami (OH)",
                 "Bowling Green":"Bowling Green State",
                 "UL-Lafayette":"Louisiana-Lafayette",
                 "UL-Monroe":"Louisiana-Monroe",
                 "Southern Miss":"Southern Mississippi",
                 "UTEP":"Texas-El Paso",
                 "U-C-F":"Central Florida",
                 "S-M-U":"Southern Methodist",
                 "Miami-Florida":"Miami (FL)",
                 "Texas A+M":"Texas A&M"

                }.get(x,x)

    filepathSpread =os.path.dirname(os.path.realpath(__file__)) + '/Lines/'
    filenameSpread = filepathSpread + "cfb" + year + 'lines.csv'
    f_objSpread =open(filenameSpread,"rb")
    ListSpreads = csv.DictReader(f_objSpread, delimiter=',')


    for line in ListSpreads:
        for name in (" offense.csv"," defense.csv"):
            for Visitor in (TeamName(line["Visitor"]), TeamName(line["Home Team"])):
                #Visitor = TeamName(line["Visitor"])
                filepathTeam =os.path.dirname(os.path.realpath(__file__)) + '/Schools/' + Visitor + '/' + year + '/'
                filenameTeam = filepathTeam + Visitor + ' ' + year + name

                if os.path.isfile(filenameTeam):
                    #print "Opening File "+ filenameTeam
                    f_objTeam=open(filenameTeam,"rb")

                    #print "File opened"
                    #print f_objTeam.read()
                    scheduleTeam = csv.reader(f_objTeam)
                    gameSchedule = [l for l in scheduleTeam]
                    #print scheduleTeam
                    AppendTop = True;
                    for game in gameSchedule:
                        if len(game) == 26 and AppendTop == True:
                            game.append("Tot_Points")
                            game.append("Spread")

                        AppendTop = False
                        #print "New Game"
                        try:
                            if game[1] =="Date":
                                continue
                            date1 = datetime.strptime(str(line["Date"]), "%m/%d/%Y")

                            date2 = datetime.strptime(game[1], "%Y-%m-%d")
                            #print "comparing " + str(date1) + " " + str(date2)
                            if(date1 == date2):
                                #print "Fround Match " + str(date1) + " " + str(date2)
                                if len(game) == 26:

                                    if Visitor == TeamName(line["Visitor"]):
                                        if name == " offense.csv":
                                            game.append(line["Visitor Score"])
                                        else:
                                            game.append(line["Home Score"])
                                        game.append(line["Line"])
                                    else:
                                        if name == " offense.csv":
                                            game.append(line["Home Score"])
                                        else:
                                            game.append(line["Visitor Score"])
                                        game.append(0 - float(line["Line"]))

                        except:
                            continue
                    f_objTeamTemp=open("temp.csv","w+")
                    #tempfile=NamedTemporaryFile(delete=False)
                    scheduleTeamTemp = csv.writer(f_objTeamTemp)
                    #print "what1"
                    scheduleTeamTemp.writerows(gameSchedule)
                    f_objTeamTemp.close()
                    shutil.move("temp.csv",filenameTeam)
                    #print "what"
                #else:
                    #print Visitor

                #f_objTeam=open(filenameTeam,"w+")
                #scheduleTeam = csv.DictReader(f_objTeam, delimiter=',')


def WriteMatrixAt(Matrix,Xname,Yname,Value):

    x=0
    y=0
    counter = 0
    #print Xname
    #print Yname
    for line in Matrix:
        if line[0] == Xname:
            x = counter
            #print line[0] + " is a match "
        if line[0] == Yname:
            y = counter
            #print line[0] + " is a match "
        counter = counter + 1
    #print "x = " + str(x) + " y  = " + str(y)

    if x == 0:
        x = 129
        #print Yname +" Scored " + str(Value) + " On  FCS"
        #return -1
    if y == 0:
        y = 129
        #print "FCS Scored " + str(Value) + " On "+ Xname
        #return -1
    if y == x:
        return -1
    Matrix[x][y] = Value

class Example(QtGui.QWidget):


    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')


        comboSource = QtGui.QComboBox(self)
        sources = ["sports-reference","ESPN PBP Data", "ESPN Box Scores"]
        for source_option in sources:
            comboSource.addItem(source_option)
        comboSource.move(50,100)
        comboSource.activated[str].connect(self.ChangeSource)

        global source
        self.comboFunction = QtGui.QComboBox(self)
        functions = getFunctions(source)
        self.comboFunction.clear()
        for function in functions:
            self.comboFunction.addItem(function)
        self.comboFunction.move(50,100)
        self.comboFunction.activated[str].connect(self.ChangeFunction)

        btn = QtGui.QPushButton('Rank', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.clicked.connect(self.ShowRanks)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        Recapbtn = QtGui.QPushButton('Recap Offense', self)
        Recapbtn.setToolTip('Recap')
        Recapbtn.clicked.connect(self.OffRecap)
        Recapbtn.resize(Recapbtn.sizeHint())
        Recapbtn.move(50, 100)

        DefRecapbtn = QtGui.QPushButton('Recap Defense', self)
        DefRecapbtn.setToolTip('DefRecap')
        DefRecapbtn.clicked.connect(self.DefRecap)
        DefRecapbtn.resize(DefRecapbtn.sizeHint())
        DefRecapbtn.move(50, 100)


        PredictionAccuracybtn = QtGui.QPushButton('Prediction Accuracy Calculator', self)
        PredictionAccuracybtn.setToolTip('Prediction accuracy Year')
        PredictionAccuracybtn.clicked.connect(self.PredictionAccuracy)
        PredictionAccuracybtn.resize(PredictionAccuracybtn.sizeHint())
        PredictionAccuracybtn.move(50, 100)
        #PredictionAccuracy

        PredictWeekbtn = QtGui.QPushButton('Predict Next Week', self)
        PredictWeekbtn.setToolTip('PredictWeek')
        PredictWeekbtn.clicked.connect(self.PredictWeek)
        PredictWeekbtn.resize(PredictWeekbtn.sizeHint())
        PredictWeekbtn.move(50, 100)




        comboYear = QtGui.QComboBox(self)
        for x in range (1995,2015):
            comboYear.addItem(str(x))
        comboYear.move(50,100)
        comboYear.activated[str].connect(self.ChangeYear)

        comboWeek = QtGui.QComboBox(self)
        for x in range (0,29):
            comboWeek.addItem(str(x))
        comboWeek.move(50,100)
        comboWeek.activated[str].connect(self.ChangeWeek)


        combopreviousYearWeight = QtGui.QComboBox(self)
        #value = 0.0
        for x in range (0,21):
            combopreviousYearWeight.addItem(str((x*0.1)))
        combopreviousYearWeight.move(50,100)
        combopreviousYearWeight.activated[str].connect(self.ChangepreviousYearWeight)

        comboHomeFieldAdvantage = QtGui.QComboBox(self)
        for x in range (0,41):
            comboHomeFieldAdvantage.addItem(str((x*0.1)))
        comboHomeFieldAdvantage.move(50,100)
        comboHomeFieldAdvantage.activated[str].connect(self.ChangeHomeFieldAdvantage)

        comboSpreadScaleDenom = QtGui.QComboBox(self)
        comboSpreadScaleDenom.addItem("0")
        for x in range (0,40):
            comboSpreadScaleDenom.addItem(str(x * 25))
        comboSpreadScaleDenom.move(50,100)
        comboSpreadScaleDenom.activated[str].connect(self.ChangeSpreadScaleDenom)


        self.tablewidget = QtGui.QTableWidget(250,17)
        self.tablewidget.move(50,50)
        layout=QtGui.QHBoxLayout()
        VerticalGroupBox = QtGui.QGroupBox("Options");
        vlayout = QtGui.QVBoxLayout()

        label_calculate = QtGui.QLabel('Calculate Rankings',self)
        vlayout.addWidget(label_calculate)
        vlayout.addWidget(btn)
        vlayout.addWidget(Recapbtn)
        vlayout.addWidget(DefRecapbtn)
        label_source = QtGui.QLabel('Data Source Location',self)
        vlayout.addWidget(label_source)
        vlayout.addWidget(comboSource)

        label_function = QtGui.QLabel('Stat Calculated',self)
        vlayout.addWidget(label_function)
        vlayout.addWidget(self.comboFunction)

        label_predict = QtGui.QLabel('Predict The next week',self)
        vlayout.addWidget(label_predict)
        vlayout.addWidget(PredictWeekbtn)

        label_regress = QtGui.QLabel('Regress prediciton accuracy',self)
        vlayout.addWidget(label_regress)
        vlayout.addWidget(PredictionAccuracybtn)

        label_prev_year = QtGui.QLabel('Previous Year Weight',self)
        vlayout.addWidget(label_prev_year)
        vlayout.addWidget(combopreviousYearWeight)

        label_home = QtGui.QLabel('Home field Advantage',self)
        vlayout.addWidget(label_home)
        vlayout.addWidget(comboHomeFieldAdvantage)

        label_spread_weight = QtGui.QLabel('Spread differential weight',self)
        vlayout.addWidget(label_spread_weight)
        vlayout.addWidget(comboSpreadScaleDenom)

        label_week = QtGui.QLabel('Week Number',self)
        vlayout.addWidget(label_week)
        vlayout.addWidget(comboWeek)

        label_year = QtGui.QLabel('Year',self)
        vlayout.addWidget(label_year)
        vlayout.addWidget(comboYear)

        VerticalGroupBox.setLayout(vlayout)
        layout.addWidget(VerticalGroupBox)
        layout.addWidget(self.tablewidget)
        self.setLayout(layout)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Tooltips')
        self.show()

    def ChangepreviousYearWeight(self,text):
        global previousYearWeight
        previousYearWeight = float(text)

    def ChangeHomeFieldAdvantage(self,text):
        global HomeFieldAdvantage
        HomeFieldAdvantage = float(text)

    def ChangeSpreadScaleDenom(self,text):
        global SpreadScaleDenom
        SpreadScaleDenom = int(text)

    def ChangeWeek(self,text):
        print "changing Week to " + str(text)
        change_week(text)

    def ChangeYear(self,text):
        print "changing year to " + str(text)
        change_year(text)

    def ChangeSource(self,text):
        print "changing source to " + str(text)
        change_source(text)

        global source
        functions = getFunctions(source)
        self.comboFunction.clear()
        self.ChangeFunction(functions[0])
        for function in functions:
            self.comboFunction.addItem(function)



    def ChangeFunction(self,text):
        print "changing function to " + str(text)
        change_function(text)

    def sort(self,col,order):
        print "test"





    def PredictionAccuracyAnnual(self):
        TotRight = 0
        TotGames = 0
        for x in range (2014,2015):
           # print "Calculated Year " + str(x)
            change_year(str(x))
            for i in range (0,20):
                #print "Week is " + str(i)
                week = str(i)
                OffScore,DefScore = CalculateRanksFromScoreMatrix(MakeScoreMatrixAtWeek("Result",int(week)),int(week),"Result")
                UpcomingGames = GetGamesOnWeek(int(week) + 1, "Result")
                Prediction = PredictGames(OffScore,DefScore,UpcomingGames)
                right,games = PredictionAccuracy(UpcomingGames,Prediction)
                TotRight = right + TotRight
                TotGames = games + TotGames


        Percent = float( float(TotRight)/float(TotGames))
        print "Got " + str(TotRight) + "/" + str(TotGames) + " = " + str((float(TotRight)/float(TotGames)))
        return TotRight,TotGames

    def PredictionAccuracy(self):
        global previousYearWeight
        previousYearWeight = 0
        #print "previousYearWeight = " + str(SpreadScaleDenom)
        #TotRight,TotGames=self.PredictionAccuracyAnnual()
        for x in range (10,11):
            previousYearWeight = x*.10
            print "previousYearWeight = " + str(previousYearWeight)
            TotRight,TotGames=self.PredictionAccuracyAnnual()

    def PredictWeek(self):
        #print "test"
        global week
        OffScore,DefScore = CalculateRanksFromScoreMatrix(MakeScoreMatrixAtWeek("Result",int(week)),int(week),"Result")
        #CompScore = CompositeScore(OffScore,DefScore)
        UpcomingGames = GetGamesOnWeek(int(week) + 1,"Result")
        Prediction = PredictGames(OffScore,DefScore,UpcomingGames)

        self.tablewidget.setSortingEnabled(False)
        '''
        csv_path ='Teamlist.csv'
        f_obj=open(csv_path, "rb")
        reader = csv.reader(f_obj, delimiter=',')
        reader = list(reader)
        '''
        i = 1
        for game in Prediction:
            print game
            item = QtGui.QTableWidgetItem(0)
            item.setData(0,game[0])
            self.tablewidget.setItem(i-1,0,item)
            item2 = QtGui.QTableWidgetItem(0)
            item2.setData(0,game[1])
            self.tablewidget.setItem(i-1,1,item2)
            item3 = QtGui.QTableWidgetItem(0)
            item3.setData(0,game[3])
            self.tablewidget.setItem(i-1,2,item3)
            item4 = QtGui.QTableWidgetItem(0)
            item4.setData(0,game[2])
            self.tablewidget.setItem(i-1,3,item4)
            i = i + 1

        self.tablewidget.setSortingEnabled(True)
        self.tablewidget.setHorizontalHeaderLabels(["Home Team","Home Score","Away Team","Away Score"])
        self.tablewidget.resizeColumnsToContents()




    def DefRecap(self):
        global week
        Score = MakeScoreMatrixAtWeek("Result",int(week))
        OffScore,DefScore = CalculateRanksFromScoreMatrix(Score, int(week),"Result")
        OffRecap,DefRecap = SeasonRecap(Score,DefScore,OffScore)
        self.tablewidget.setSortingEnabled(False)

        csv_path ='Teamlist.csv'
        f_obj=open(csv_path, "rb")
        reader = csv.reader(f_obj, delimiter=',')
        reader = list(reader)

        self.tablewidget.clear()

        for i in range(1,129):
            item = QtGui.QTableWidgetItem(str(reader[i][1]))
            self.tablewidget.setItem(i-1,0,item)
            item = QtGui.QTableWidgetItem(0)
            item.setData(0,DefScore[i])
            self.tablewidget.setItem(i-1,1,item)
            for j in range (1,16):
                item2 = QtGui.QTableWidgetItem(0)
                item2.setData(0,DefRecap[j][i])
                self.tablewidget.setItem(i-1,j+1,item2)
           # item3 = QtGui.QTableWidgetItem(0)
           # item3.setData(0,DefScore[i])
            #self.tablewidget.setItem(i-1,2,item3)
           # item4 = QtGui.QTableWidgetItem(0)
           # item4.setData(0,OffScore[i])
           # self.tablewidget.setItem(i-1,3,item4)
        #layout=QtGui.QHBoxLayout()
        #layout.addWidget(self.tablewidget)
        self.tablewidget.setSortingEnabled(True)
        self.tablewidget.resizeColumnsToContents()
        #self.tablewidget.move(200,100)
        #self.setLayout(layout)

    def OffRecap(self):
        global week
        Score = MakeScoreMatrixAtWeek("Result",int(week))
        OffScore,DefScore = CalculateRanksFromScoreMatrix(Score, int(week),"Result")
        OffRecap,DefRecap = SeasonRecap(Score,DefScore,OffScore)
        self.tablewidget.setSortingEnabled(False)

        csv_path ='Teamlist.csv'
        f_obj=open(csv_path, "rb")
        reader = csv.reader(f_obj, delimiter=',')
        reader = list(reader)

        self.tablewidget.clear()

        for i in range(1,129):
            item = QtGui.QTableWidgetItem(str(reader[i][1]))
            self.tablewidget.setItem(i-1,0,item)
            item = QtGui.QTableWidgetItem(0)
            item.setData(0,OffScore[i])
            self.tablewidget.setItem(i-1,1,item)
            for j in range (1,16):
                item2 = QtGui.QTableWidgetItem(0)
                item2.setData(0,OffRecap[j][i])
                self.tablewidget.setItem(i-1,j+1,item2)
           # item3 = QtGui.QTableWidgetItem(0)
           # item3.setData(0,DefScore[i])
            #self.tablewidget.setItem(i-1,2,item3)
           # item4 = QtGui.QTableWidgetItem(0)
           # item4.setData(0,OffScore[i])
           # self.tablewidget.setItem(i-1,3,item4)
        #layout=QtGui.QHBoxLayout()
        #layout.addWidget(self.tablewidget)
        self.tablewidget.setSortingEnabled(True)
        self.tablewidget.resizeColumnsToContents()
        #self.tablewidget.move(200,100)
        #self.setLayout(layout)

    def ShowRanks(self):
       #print "test"
        global week
        global function
        OffScore,DefScore = CalculateRanksFromScoreMatrix(MakeScoreMatrixAtWeek(function,int(week)),int(week),function)
        CompScore = CompositeScore(OffScore,DefScore)
        #self.tablewidget = QtGui.QTableWidget(130,4)

        self.tablewidget.setSortingEnabled(False)
        if source == "sports-reference":
            csv_path ='Teamlist.csv'
        else:
            csv_path ='../rcfbscraper/ESPN_Scraper/2014 Stats/team.csv'
        f_obj=open(csv_path, "rb")
        reader = csv.reader(f_obj, delimiter=',')
        reader = list(reader)
        if source == "sports-reference":
            reader.append(['dummy','FCS AVG'])


        self.tablewidget.clear()

        for i in range(1,len(OffScore)):
            item = QtGui.QTableWidgetItem(str(reader[i][1]))
            self.tablewidget.setItem(i-1,0,item)
            item2 = QtGui.QTableWidgetItem(0)
            item2.setData(0,CompScore[i])
            self.tablewidget.setItem(i-1,1,item2)
            item3 = QtGui.QTableWidgetItem(0)
            item3.setData(0,DefScore[i])
            self.tablewidget.setItem(i-1,2,item3)
            item4 = QtGui.QTableWidgetItem(0)
            item4.setData(0,OffScore[i])
            self.tablewidget.setItem(i-1,3,item4)
        #layout=QtGui.QHBoxLayout()
        #layout.addWidget(self.tablewidget)
        self.tablewidget.setSortingEnabled(True)
        self.tablewidget.setHorizontalHeaderLabels(["Team Name","Composite Score","Defensive Score","Offensive Score"])
        self.tablewidget.resizeColumnsToContents()

        #self.tablewidget.move(200,100)
        #self.setLayout(layout)







#print Opening_Week

#year= "2014"
#AppendSpreadToCSV()

'''
TargetWeek = 14
Offscore,DefScore = MakeScoreMatrixAtWeek(TargetWeek -1,"Result")
UpcomingGames = GetGamesOnWeek(TargetWeek,"Result")
Prediction = PredictGames(Offscore,DefScore,UpcomingGames)
PredictionAccuracy(UpcomingGames,Prediction)'''

#OffScorePEN,DefScorePEN = AvgofStatAtWeek(14,"Pen_Yds")
#PrintRanks(OffScorePEN,"OFFSCOREPEN",True)
#PrintRanks(DefScorePEN,"DefScorePen",True)


change_year(2014)
'''
TotRight = 0
TotGames = 0

for x in range (2013,2014):

    year = str(x)
    assign_first_week()
    for i in range (5,14):
        OffScore,DefScore = MakeScoreMatrixAtWeek(i-1,"Result")
        #OffScoreYPP,DefScoreYPP = MakeScoreMatrixAtWeek(i-1,"Tot_Avg")
        #OffScoreTO,DefScoreTO = AvgofStatAtWeek(i-1,"TO_Tot")
        #OffScorePEN,DefScorePEN = AvgofStatAtWeek(i-1,"Pen_Yds")


        #OffScore = [1 for s in range(130)]
        #DefScore = [1 for s in range(130)]
        #for j in range (1,129):
       #     OffScore[j] = (OffScoreYPP[j]*70 - OffScoreTO[j]*20 - OffScorePEN[j])*.080
        #    DefScore[j] = ((DefScoreYPP[j]*70*5.5 - DefScoreTO[j]*20 + DefScorePEN[j])*.080)
        #PrintRanks(OffScore,"OffScore " + str(x),False)
        #PrintRanks(DefScore,"DefScore " + str(x),True)
        #PrintRanks(OffScoreYPP,"OffScoreYPP " + str(x),False)
        #PrintRanks(DefScoreYPP,"DefScoreYPP " + str(x),True)
        #PrintRanks(OffScorePEN,"OFFSCOREPEN",True)
        #PrintRanks(DefScorePEN,"DefScorePen",True)
        #PrintRanks(OffScoreTO,"OFFSCORETO",True)
        #PrintRanks(DefScoreTO,"DefScoreTO",False)
        #PrintRanks(CompositeScore(OffScore,DefScore),"Composite Rank", False)



        UpcomingGames = GetGamesOnWeek(i,"Result")
        Prediction = PredictGames(OffScore,DefScore,UpcomingGames)
        #right,games = PredictionAccuracySpread(UpcomingGames,Prediction)
        right,games = PredictionAccuracy(UpcomingGames,Prediction)
        TotRight = right + TotRight
        TotGames = games + TotGames

    PrintRanks(OffScore,"Offscore", False)
    PrintRanks(DefScore,"DefScore",True)
    PrintRanks(CompositeScore(OffScore,DefScore),"Composite Rank", False)

print "got " + str(TotRight) + "/" + str(TotGames) + " = " + str((float(TotRight)/float(TotGames)))
'''

app = QtGui.QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())

sys.exit(app.exec_())



'''
off1, def1 = MakeScoreMatrixAtWeek(14,"Result")
off2, def2 =MakeScoreMatrixAtWeek(14,"Tot_Avg")
off3 = [1 for x in range(130)]
def3 = [1 for x in range(130)]
for i in range (1,129):
    off3[i] = (off1[i] + 0.8*off2[i])/2
    def3[i] = (def1[i] + 0.8*def2[i])/2
PrintRanks(CompositeScore(off3,def3),"Result + Tot Avg yards Composite Rank", False)
'''

'''
Offscore,DefScore =MakeScoreMatrixAtWeek(14,"Tot_Avg")
PrintRanks(Offscore,"OffScore Tot Yards",False)
PrintRanks(DefScore,"DefScore Tot Yards",True)
PrintRanks(CompositeScore(Offscore,DefScore),"Tot Avg yards Composite Rank", False)
'''
