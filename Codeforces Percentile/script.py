import pandas as pd
import numpy as np
import requests

file = pd.read_csv("ICPC15.csv")
lower_usernames = [i.lower() for i in file['Codeforces Username']]
file['Codeforces Username'] = lower_usernames

contestId = input()

numParticipants = 0
numVirtual = 0
contestName = ''
data = {}

RANK = [-1 for i in range(file.shape[0])]


def getContestDetails():
    global data
    global numParticipants, contestName
    base = 'https://codeforces.com/api/contest.standings?contestId='
    URL = base + contestId + '&showUnofficial=true'
    data = requests.get(url=URL).json()['result']
    contestName = data['contest']['name']


def filterIITRPRContestantRanks():
    global data, numParticipants
    ranks = {}
    rankScore = {}
    allContestants = data['rows']
    for contestant in allContestants:
        username = contestant['party']['members'][0]['handle'].lower()
        participantType = contestant['party']['participantType']
        rank = contestant['rank']
        penalty = contestant['penalty']
        if participantType != 'CONTESTANT' and participantType != 'OUT_OF_COMPETITION':
            continue
        numParticipants += 1
        if username not in contestants_IITRPR:
            continue
        try:
            ranks[username] = rankScore[str(rank)+'$'+str(penalty)]
        except:
            ranks[username] = numParticipants
            rankScore[str(rank)+'$'+str(penalty)] = numParticipants
        print(username, rank)                                                   # print to console
    return ranks


def getRanks():
    global RANK
    ranks = filterIITRPRContestantRanks()
    numContestants_IITRPR = file.shape[0]
    for i in range(numContestants_IITRPR):
        username = file['Codeforces Username'][i]
        try:
            RANK[i] = ranks[username]
        except:
            RANK[i] = numParticipants


getContestDetails()
contestants_IITRPR = set(file['Codeforces Username'])
getRanks()
file[contestName] = [100 * (1 - i / numParticipants) for i in RANK]
for i in file:
    if i[:7] == 'Unnamed':
        del file[i]
file.to_csv('ICPC15.csv')
