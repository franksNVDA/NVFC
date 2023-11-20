import pandas as pd
import re
SignInPlayerList = "H:/PyProjects/NVFC/SignInPlayers.txt"
SquadDataBase = "H:/PyProjects/NVFC/SquadDataBase.xlsx"
SquadMaxPlayerNum = 8

PlayerDict = {}
PlayerNameToID = {}
SignInPlayers = []

CF = ['CF']
MF = ['MF', 'DMF', "CM"]
CB = ['CB']
LRB = ['LB', 'RB']
LRM = ['LM', 'RM', 'RMF', 'LMF']
Unknown = ['Unknown']

SignInCFs= []
SignInMFs = []
SignInCBs = []
SignInLRBs = []
SignInLRMs = []
SignInUnknowns = []

class Squad(object):

    def __init__(self, Name):
        self.Name = Name
        self.PlayerList = []
        self.TotalCapability = 0
        self.PlayerCount = 0

    def PrintSquad(self):
        print("Team", self.Name)
        count = 1
        for player in self.PlayerList:
            print(count, player.Name)
            count += 1

        print("Total Capability", self.TotalCapability)

    def AddPlayer(self, player):
        self.TotalCapability += player.Capability
        self.PlayerCount += 1
        self.PlayerList.append(player)

    def __lt__(self, other):
        return self.TotalCapability < other.TotalCapability



class Player(object):
    def __init__(self, Name, Position, ID, Capability):
        self.Name = Name
        self.Position = Position
        self.ID = ID
        self.Capability = Capability

    def __lt__(self, other):
        return self.Capability > other.Capability


def InitPlayerDataBase():
    # read by default 1st sheet of an excel file
    data = pd.read_excel(SquadDataBase)
    for i in data.index:
        playerData = data.loc[i]
        player = Player(playerData.Name, playerData.Position, playerData.ID, playerData.Capability)
        PlayerDict[player.ID] = player
        if player.Name in PlayerNameToID:
            print("fatal error!!! : There are players have same name in Player database")
        else:
            PlayerNameToID[player.Name] = player.ID

def InitSignInPlayerDataBase():
    with open(SignInPlayerList, 'r', encoding='utf-8') as f:
        data = f.readlines()
        for i in data:
            name = re.sub(r'[\d\.\ \n\t]', '', i)
            player = Player(name, "Unknown", -1, 1) #default player
            if name in PlayerNameToID:
               player = PlayerDict[PlayerNameToID[name]]
            else:
               print("warning : player ", name, "is not registered in player database will use default value 1")
            SignInPlayers.append(player)

def SortAndMoveExtraPlayers(PlayerList, ExtraPlayerList, SquadNum):
    PlayerList.sort()
    popNum = len(PlayerList) % SquadNum
    for i in range(0, popNum):
        ExtraPlayerList.append(PlayerList.pop())

def ClassifyPlayers(SquadNum):
    for player in SignInPlayers:
        if player.Position in CF:
            SignInCFs.append(player)
        elif player.Position in MF:
            SignInMFs.append(player)
        elif player.Position in LRM:
            SignInLRMs.append(player)
        elif player.Position in LRB:
            SignInLRBs.append(player)
        elif player.Position in CB:
            SignInCBs.append(player)
        elif player.Position in Unknown:
            SignInUnknowns.append(player)
        else:
            print("Fatal error !!! :No avaliable position for", player.Position, " of ", player.Name)

    SortAndMoveExtraPlayers(SignInCFs, SignInUnknowns, SquadNum)
    SortAndMoveExtraPlayers(SignInMFs, SignInUnknowns, SquadNum)
    SortAndMoveExtraPlayers(SignInCBs, SignInUnknowns, SquadNum)
    SortAndMoveExtraPlayers(SignInLRBs, SignInUnknowns, SquadNum)
    SortAndMoveExtraPlayers(SignInLRMs, SignInUnknowns, SquadNum)
    SignInUnknowns.sort()

def AssignToSquad(Squads, PlayerList):
    Squads.sort()

    i = 0
    currentSquad = Squads[i]
    for player in PlayerList:
        currentSquad.AddPlayer(player)
        i = (i+1) % len(Squads)
        currentSquad = Squads[i]


def SquadGenerator(SquadNum):

    Squads = []
    for i in range(0, SquadNum):
        Squads.append(Squad(chr(ord('A')+ i)))

    AssignToSquad(Squads, SignInCFs)
    AssignToSquad(Squads, SignInMFs)
    AssignToSquad(Squads, SignInCBs)
    AssignToSquad(Squads, SignInLRBs)
    AssignToSquad(Squads, SignInLRMs)
    AssignToSquad(Squads, SignInUnknowns)
    for i in range(0, SquadNum):
        Squads[i].PrintSquad()


def Main():
    InitPlayerDataBase()
    InitSignInPlayerDataBase()
    SignInPlayerNum = len(SignInPlayers)
    SquadNum = int((SignInPlayerNum + SquadMaxPlayerNum - 1) / SquadMaxPlayerNum)
    ClassifyPlayers(SquadNum)
    SquadGenerator(SquadNum)

Main()