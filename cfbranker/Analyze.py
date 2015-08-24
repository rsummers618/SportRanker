__author__ = 'Ryan'

import csv
import re
import numpy as np
from scipy import stats
import datetime
#import CFBRanker as ranker
import matplotlib.pyplot as plt
import scikits.statsmodels.api as sm


GAME_CODE = 0
PLAY_NUMBER = 1
PERIOD_NUMBER = 2
CLOCK = 3
OFFENSE_CODE = 4
DEFENSE_CODE = 5
OFFENSE_POINTS = 6
DEFENSE_POINTS = 7
DOWN = 8
DISTANCE = 9
SPOT = 10
PLAY_TYPE = 11
DRIVE_NUMBER = 12
DRIVE_PLAY = 13
PLAY_DESC = 14
PLAY_RESULT = 15
YARDS_GAINED = 16
OFF_TOUCHDOWN = 17
DEF_TOUCHDOWN = 18
FIRST_DOWN = 19
COMPLETION = 20
INTERCEPTION = 21
FUMBLE = 22
FUMBLE_LOST = 23
KICK_GOOD = 24
TWO_PT_GOOD = 25
SAFETY = 26
KICK_YARDS = 27
TOUCHBACK = 28
KICKOFF_OOB = 29
KICKOFF_ONSIDES = 30
KICK_BLOCKED = 31
PENALTY = 32
PENALTY_TYPE = 33
NO_PLAY = 34
RUSHER = 35
PASSER = 36
RECEIVER = 37
KICKER = 38
FORCED_FUM = 39
INTERCEPTOR_SACK = 40
EXTRA_PT_ATT = 41
TWOPT_ATT = 42
UNPARSED_PLAYS_DESC = 43

CodeToIndex = []
NameToIndex = []


def Read_CSV(file_name):
	data = []
	with open(file_name, "rU") as csvfile:
		data_reader =  csv.reader(csvfile)
		for row in data_reader:
			data.append(row)
#	 for i in range(0, len(data)):
#		for j in range(0, len(data[i])):
#			data[i][j] = re.sub("\"", "", data[i][j])
	data.pop(0)
	return data
	# csv = np.genfromtxt(file_name, delimiter=',')

	#list = []
	#with open(file_name, "rU") as csvfile:
	#	for line in csvfile:
	#		list.append(line.strip().split(','))
	#		# reader = csv.reader(file_name, dialect=csv.excel_tab)
	#		# mylist = list(reader)
	#	list.pop(0)
	#return list


def GlobalDriveSuccess(play_arr):
	sequences = DivideByDownSequence(play_arr)
	num_success = 0
	num_total = 0
	num_score = 0
	for sequence in sequences:
		if int(sequence[-1][OFF_TOUCHDOWN]) == 1 and int(sequence[0][SPOT]) >40:
			num_score +=1
			num_success +=1
		elif int(sequence[-1][FIRST_DOWN]) == 1 or int(sequence[-1][OFF_TOUCHDOWN]) == 1:
			num_success +=1
		num_total += 1
	return float(num_success)/num_total,float(num_score)/num_total

def GlobalDriveYards(play_arr):
	raw_odds = [0] * 105
	sequences = DivideByDownSequence(play_arr)
	for sequence in sequences:
		distance = int(sequence[0][SPOT]) -(int(sequence[-1][SPOT]) - int(sequence[-1][YARDS_GAINED]))
		if distance > -5 and distance <= 100:
			raw_odds[distance+5] += 1
	return raw_odds


def DriveSuccess(play_arr):
	successMap = {}
	failureMap = {}
	play = 0
	while play < len(play_arr):
		# print play
		down = play_arr[play][DOWN]
		if (down == str(1)):
			off = int(play_arr[play][OFFENSE_CODE])
			success = 0
			play += 1
			if play >= len(play_arr) - 1:
				break
			td = 1
			while int(play_arr[play][OFFENSE_CODE]) == off:
				if play_arr[play][DOWN] == str(1):
					success += 1
				if int(play_arr[play][OFFENSE_POINTS]) == int(play_arr[play - 1][OFFENSE_POINTS]) + 6:
					td = 0
					success += 1
				if play >= len(play_arr) - 1:
					break
				play += 1;
			if str(off) not in successMap:
				successMap[str(off)] = 0
			if str(off) not in failureMap:
				failureMap[str(off)] = 0
			successMap[str(off)] += success
			failureMap[str(off)] += td
			play -= 1
		play += 1
	return successMap, failureMap

def DriveSuccessField(play_arr):
	successMap = {}
	failureMap = {}
	tsuccess = 0
	tfail = 0
	play = 0
	while play < len(play_arr):
		print play
		down = play_arr[play][DOWN]
		if (down == str(1)):
			off = int(play_arr[play][OFF])
			success = 0
			play += 1
			td = 1
			while int(play_arr[play][OFF]) == off:
				if play_arr[play][DOWN] == str(1) and int(play_arr[play][SPOT]) > 10:
					success += 1
				if int(play_arr[play][SCORE]) == int(play_arr[play - 1][SCORE]) + 6:
					td = 0
					success += 1
				if play >= len(play_arr) - 1:
					break
				play += 1;
			if str(off) not in successMap:
				successMap[str(off)] = 0
			if str(off) not in failureMap:
				failureMap[str(off)] = 0
			successMap[str(off)] += success
			tsuccess += success
			failureMap[str(off)] += td
			tfail += td
			play -= 1
		play += 1
	return successMap, failureMap, tsuccess, tfail

def DriveSuccessGoal(play_arr):
	successMap = {}
	failureMap = {}
	tsuccess = 0
	tfail = 0
	play = 0
	while play < len(play_arr):
		print play
		down = play_arr[play][DOWN]
		if (down == str(1) and int(play_arr[play][SPOT]) == 10):
			off = int(play_arr[play][OFF])
			success = 0
			play += 1
			td = 1
			while int(play_arr[play][OFF]) == off:
				if int(play_arr[play][SCORE]) == int(play_arr[play - 1][SCORE]) + 6:
					td = 0
					success += 1
				if play >= len(play_arr) - 1:
					break
				play += 1;
			if str(off) not in successMap:
				successMap[str(off)] = 0
			if str(off) not in failureMap:
				failureMap[str(off)] = 0
			successMap[str(off)] += success
			tsuccess += success
			failureMap[str(off)] += td
			tfail += td
			play -= 1
		play += 1
	return successMap, failureMap, tsuccess, tfail

def GetDifInStat(play_arr, stat):
	groups = []

	stat_code = play_arr[0][stat]
	group = []
	for line in play_arr:
		if line[stat] != stat_code:
			groups.append(group)
			stat_code = line[stat]
			group = []
		group.append(line)
	groups.append(group)

	return groups

def DivideByDownSequence(play_arr):
	groups = []
	stat_code = play_arr[0][FIRST_DOWN]
	group = []
	for line in play_arr:
		## legacy support
		if len(line) < FIRST_DOWN +1:
			if (line[DISTANCE] == str(10) and line[DOWN] == str(1)):
				if group:
					groups.append(group)
				stat_code = line[FIRST_DOWN]
				group = []
			group.append(line)
		else:

			if line[FIRST_DOWN] == str(1)  or (line[DISTANCE] == str(10) and line[DOWN] == str(1)):
				if group:
					groups.append(group)
				stat_code = line[FIRST_DOWN]
				group = []
			group.append(line)
	if group:
		groups.append(group)
	return groups

def DivideByGame(play_arr):
	return GetDifInStat(play_arr, GAME_CODE)

def DivideByDrive(play_arr):
	return GetDifInStat(play_arr, DRIVE_NUMBER)

def DivideByQuarter(play_arr):
	return GetDifInStat(play_arr, PERIOD_NUMBER)

def DivideByQuarter(play_arr):
	return GetDifInStat(play_arr, PERIOD_NUMBER)

def DivideByHalf(play_arr):
	halves = []
	quarters = DivideByQuarter(play_arr)
	if len(quarters) % 4 != 0:
		print "error: Number of quarters is not even"
	for x in range(0, len(quarters), 2):
		temp = quarters[x] + quarters[x + 1]
		halves.append(temp)
	return halves

def FilterGarbageTime(play_arr):
	out_arr = []
	garbage_plays = []
	for play in play_arr:
		if play[PERIOD_NUMBER] > 2 and abs(play[OFFENSE_POINTS] - play[DEFENSE_POINTS]) > 21:
			garbage_plays.append(play)
		elif play[PERIOD_NUMBER] == 4 and abs(play[OFFENSE_POINTS] - play[DEFENSE_POINTS]) > 14:
			garbage_plays.append(play)
		elif play[PERIOD_NUMBER] == 4 and abs(play[OFFENSE_POINTS] - play[DEFENSE_POINTS]) > 8 and play[CLOCK] < 120:
			garbage_plays.append(play)
		else:
			out_arr.append(play)

	return out_arr

def FilterLastDrivesOfHalf(play_arr):
	## filter hail mary ++ kneel downs
	halves = DivideByHalf(play_arr)
	for half in halves:
		if(half[0][PERIOD_NUMBER] %2 == 0):
			drives = DivideByDrive(half)

	return play_arr

def IncStatWithValue(play_arr, stat, value):
	occurrences = 0
	for line in play_arr:
		if str(line[stat]) == str(value):
			occurrences += 1
	return occurrences

def DivideByPointScored(play_arr):
	return

def SumStat(play_arr, stat):
	sum = 0
	for line in play_arr:
		sum += int(line[stat])
	return sum

def GetExpectedPoints(yardline):
	return GenerateExpectedPointsArray[yardline]

def GenerateExpectedPointsArray(play_arr):
	drives = DivideByDrive(play_arr)
	success = [0]*101
	attempts = [0]*101
	output = [0]*101

	for drive in drives:
		TDScored = int(drive[-1][OFF_TOUCHDOWN])
		DriveEndDesc = drive[-1][PLAY_DESC]
		downs = DivideByDownSequence(drive)
		for down in downs:
			startingSpot = int(down[0][SPOT])
			success[startingSpot] += TDScored
			attempts[startingSpot] += 1

			if startingSpot == 1:
				print "drive starting at the 1, TD = " +str(TDScored)+" ending with " + DriveEndDesc + " on " + drive[-1][DOWN] + "&" + drive[-1][DISTANCE] + " @ the " + drive[-1][SPOT]

	for index in range (0,100):
		output[index] = float(success[index])/attempts[index] * 7

	return output

def GetGamesBeforeWeek(play_arr,week_num):
	output = []
	for x in range(1,week_num):
		output = output +GetGamesOnWeek(play_arr,x)
	return output

def GetGamesOnWeek(play_arr, week_num):
	startdatefull = play_arr[1][0]
	startdate = startdatefull[-8:]
	curDate = datetime.datetime.strptime(startdate, "%Y%m%d").date()

	curDatePlus7 = curDate + datetime.timedelta(days=7)

	curDateInt = int(str(curDate.year) + str(curDate.month) + str(curDate.day))
	curDatePlus7Int = int(curDatePlus7.strftime('%Y%m%d'))

	week = 1
	while week < week_num:

		week += 1
		curDate = curDatePlus7
		curDatePlus7 = curDate + datetime.timedelta(days=7)
		curDateInt = int(curDate.strftime('%Y%m%d'))
		curDatePlus7Int = int(curDatePlus7.strftime('%Y%m%d'))

	output = []

	for line in play_arr:
		if not line[0].isdigit():
			continue
		if int(line[0][-8:]) >= curDateInt and int(line[0][-8:]) < curDatePlus7Int:
			output.append(line)

	return output



def regression_weekly_normalized(play_arr,weekNum, dataFunction1, dataFunction2):
	gamesbeforeWeek = GetGamesBeforeWeek(play_arr,weekNum)
	#ranker.
	return 0

def regression_analysis(play_arr,dataFunction1,dataFunction2):

	totalBefore = []
	totalAfter = []
	for weekNum in range(10,15):
		Before,After = regression_weekly(play_arr,weekNum,dataFunction1, dataFunction2)

		totalBefore = np.concatenate([totalBefore, Before])
		totalAfter = np.concatenate([totalAfter, After])

	slope, intercept, r_value, p_value, err = stats.linregress(totalBefore, totalAfter)
	results = sm.OLS(totalAfter, sm.add_constant(totalBefore)).fit()

	print results.summary()

	plt.plot(totalBefore, totalAfter, '.')
	X_plot = np.linspace(0, 1, 100)
	plt.plot(X_plot, X_plot * results.params[0] + results.params[1])
	plt.show()

		# print "for week " + str(week) + ".  slope = " + str(slope) + ". r val = " + str(r_value)

def regression_weekly(play_arr,weekNum,dataFunction1, dataFunction2):

	beforeMap = {}
	gamesbeforeWeek = GetGamesBeforeWeek(play_arr,weekNum)
	beforeGames = DivideByGame(gamesbeforeWeek)
	for game in beforeGames:
		homeNum, awayNum, homeVal,awayVal = dataFunction1(game)
		if not str(homeNum) in beforeMap:
			beforeMap[str(homeNum)] = []
		if not str(awayNum) in beforeMap:
			beforeMap[str(awayNum)] = []
		beforeMap[str(awayNum)].append(awayVal)
		beforeMap[str(homeNum)].append(homeVal)

	CurGames = DivideByGame(GetGamesOnWeek(play_arr,weekNum))
	BeforeArr = []
	AfterArr = []
	for game in CurGames:
		homeNum, awayNum, homeVal,awayVal = dataFunction2(game)
		try:
			BeforeArr.append(np.mean(beforeMap[str(homeNum)]))
			AfterArr.append(homeVal)
		except:
			print "team " + str(homeNum) + "'s first game"
		try:
			BeforeArr.append(np.mean(beforeMap[str(awayNum)]))
			AfterArr.append(awayVal)
		except:
			print "team " + str(awayNum) + "'s first game"

	Before = np.array(BeforeArr)
	After = np.array(AfterArr)

	return Before,After
		#slope, intercept, r_value, p_value, err = stats.linregress(Before, After)

		#results = sm.OLS(After, sm.add_constant(Before)).fit()

		#print results.summary()

		#plt.plot(Before, After, '.')
		#X_plot = np.linspace(0, 1, 100)
		#plt.plot(X_plot, X_plot * results.params[0] + results.params[1])
		#plt.show()

		# print "for week " + str(week) + ".  slope = " + str(slope) + ". r val = " + str(r_value)

		## All previous games to next game, starting at 4 per team

		## first half of season to second half of season per team

#def game_regression_map(play_arr,dataFunction1):

def getTeamCodes(line):
	gameCode = line[0]
	gameCode = re.sub("[^0-9]","",gameCode)
	homeNum = gameCode[:-12]
	awayNum = gameCode[len(homeNum):-8]
	return int(homeNum),int(awayNum)

def convertTeamNumToIndex(teamCode):
	if not CodeToIndex or not NameToIndex:
		arr = Read_CSV("../rcfbscraper/ESPN_SCRAPER/2014 Stats/team.csv")
		for line in arr:
			CodeToIndex.append(line[0])
			NameToIndex.append(line[1])
	try:
		return CodeToIndex.index(str(teamCode))
	except:
		return len(CodeToIndex)

def GenerateMatrixForStat(StatFunction, pbp_arr):
	numTeams = 100
	convertTeamNumToIndex(1)
	matrix = [[-1 for i in range(len(CodeToIndex )+1)] for j in range(len(CodeToIndex) +1)]
	games = DivideByGame(pbp_arr)
	for game in games:
		homeNum,awayNum, homeStat,awayStat = StatFunction(game)
		matrix [convertTeamNumToIndex(awayNum)+1][convertTeamNumToIndex(homeNum)+1] = homeStat
		matrix [convertTeamNumToIndex(homeNum)+1][convertTeamNumToIndex(awayNum)+1] = awayStat
	#matrix[0] = NameToIndex
	matrix[0] = []
	matrix[0].append("-1")
	for name in NameToIndex:
		matrix[0].append(name)
	#matrix[0].insert(0,-1)
	for x in range(len(NameToIndex)):
		matrix[x+1][0] = NameToIndex[x]


	return matrix

def SF_YPP(pbp_game):
	homeNum,awayNum = getTeamCodes(pbp_game[0])
	hPlays,hYards,aPlays,aYards = 0,0,0,0

	for play in pbp_game:
		if int(play[OFFENSE_CODE])==homeNum and int(play[DEFENSE_CODE])==awayNum:
			#Home team on on offense
			hPlays += 1
			hYards += int(play[YARDS_GAINED])
		elif int(play[OFFENSE_CODE])==awayNum and int(play[DEFENSE_CODE])==homeNum:
			#Away on offense
			aPlays += 1
			aYards += int(play[YARDS_GAINED])
		else:
			print "ERROR IN PARSING YPP, OFF and DEF don't match"

	if hPlays > 0:
		hYPP = float(hYards)/hPlays
	else:
		hYPP = -99
	if aPlays > 0:
		aYPP = float(aYards)/aPlays
	else:
		aYPP = -99
	return homeNum, awayNum, hYPP,aYPP

def SF_Points(pbp_game):
	homeNum,awayNum = getTeamCodes(pbp_game[0])
	hPoints,aPoints = 0,0
	play = pbp_game[-1]

	if int(play[OFFENSE_CODE])==homeNum and int(play[DEFENSE_CODE])==awayNum:
		#Home team on on offense
		return homeNum, awayNum, int(play[OFFENSE_POINTS]),int(play[DEFENSE_POINTS])
	elif int(play[OFFENSE_CODE])==awayNum and int(play[DEFENSE_CODE])==homeNum:
		#Away on offense
		return int(homeNum), int(awayNum), int(play[DEFENSE_POINTS]),int(play[OFFENSE_POINTS])
	else:
		print "ERROR OFF AND DEF DON'T MATCH - POINTS"
	return homeNum, awayNum, -99,-99

def SF_CompletionPct(pbp_game):
	return

def SF_DriveSuccessRate(play_arr):
	if play_arr[0][0] == str(253067020141108):
		print 'here'
	homeNum,awayNum = getTeamCodes(play_arr[0])
	hSuccess,aSuccess = 0,0
	successMap = {}
	failureMap = {}
	play = 0
	while play < len(play_arr):
		# print play
		down = play_arr[play][DOWN]
		if (down == str(1)):
			off = int(play_arr[play][OFFENSE_CODE])
			success = 0
			play += 1
			if play >= len(play_arr) - 1:
				break
			td = 1
			while int(play_arr[play][OFFENSE_CODE]) == off:
				if play_arr[play][DOWN] == str(1):
					success += 1
				if int(play_arr[play][DEFENSE_POINTS]) == int(play_arr[play - 1][OFFENSE_POINTS]) + 6:
					td = 0
					success += 1
				if play >= len(play_arr) - 1:
					break
				play += 1;
			if str(off) not in successMap:
				successMap[str(off)] = 0
			if str(off) not in failureMap:
				failureMap[str(off)] = 0
			successMap[str(off)] += success
			failureMap[str(off)] += td
			play -= 1
		play += 1
	try:
		hSuccess = float(successMap[str(homeNum)])/(failureMap[str(homeNum)] + successMap[str(homeNum)])
	except:
		print "no value here"
	try:
		aSuccess = float(successMap[str(awayNum)])/(failureMap[str(awayNum)] + successMap[str(awayNum)])
	except:
		print "no value here"


	return homeNum, awayNum, hSuccess,aSuccess

def SF_TOAdjustedPointsSimple(pbp_game):
	homeNum,awayNum = getTeamCodes(pbp_game[0])
	hPoints,aPoints = 0,0
	TODiff = 0
	for play in pbp_game:
		if int(play[INTERCEPTION]) == 1 or int(play[FUMBLE_LOST] == 1):
			if int(play[OFFENSE_CODE]) == homeNum:
				TODiff -= 1
			else:
				TODiff += 1


	play = pbp_game[-1]

	if int(play[OFFENSE_CODE])==homeNum and int(play[DEFENSE_CODE])==awayNum:
		#Home team on on offense
		return homeNum, awayNum, int(play[OFFENSE_POINTS]) -2*TODiff ,int(play[DEFENSE_POINTS]) + 2*TODiff
	elif int(play[OFFENSE_CODE])==awayNum and int(play[DEFENSE_CODE])==homeNum:
		#Away on offense
		return homeNum, awayNum, int(play[DEFENSE_POINTS]) - 2*TODiff,int(play[OFFENSE_POINTS]) +2*TODiff
	else:
		print "ERROR OFF AND DEF DON'T MATCH - POINTS"
	return homeNum, awayNum, -99,-99

######################
##### MAIN ##########
####################

#play_arr = Read_CSV('../rcfbScraper/ESPN_Scraper/2014 Stats/play.csv')
#play_arr = Read_CSV('data/2013//play.csv')
#matrix = GenerateMatrixForStat(SF_DriveSuccessRate,play_arr)
#print matrix
#regression_analysis(play_arr,SF_Points,SF_Points)
#regression_analysis(play_arr,SF_DriveSuccessRate,SF_DriveSuccessRate)

#ValidatePBP('../rcfbScraper/ESPN_Scraper/2014 Stats/play_TGS.csv','../rcfbScraper/ESPN_Scraper/2014 Stats/team-game-statistics.csv')


#play_arr = Read_CSV('../rcfbScraper/ESPN_Scraper/2014 Stats/play.csv')
#Games = DivideByGame(play_arr)
#Drives = DivideByDrive(play_arr)
#Quarters = DivideByQuarter(play_arr)
#Halves = DivideByHalf(play_arr)
#PointSeq = DivideByPointScored(play_arr)
#Downs = DivideByDownSequence(play_arr)
#Expt = GenerateExpectedPointsArray(play_arr)

#print "done"


# dSuccess,dFail,tSuccess,tFail = DriveSuccessField(play_arr)
# dSuccessGoal,dFailGoal,tSuccessGoal,tFailGoal = DriveSuccessGoal(play_arr)

# tFieldRatio = float(tSuccess)/(tSuccess + tFail)
# tGoalRatio = float(tSuccessGoal)/(tSuccessGoal + tFailGoal)
# print tFieldRatio
# print tGoalRatio



# FIELD=0
# GOAL=1
# Field = []
# Goal = []
# for key in dSuccessGoal:
#    Field.append(float(dSuccess[key])/(dSuccess[key] + dFail[key]))
#    Goal.append(float(dSuccessGoal[key])/(dSuccessGoal[key] + dFailGoal[key]))
# print "woo"
