import pandas as pd
import re
SignInPlayerList = "H:/PyProjects/NVFC/SignInPlayers.txt"
SquadDataBase = "H:/PyProjects/NVFC/SquadDataBase.xlsx"

PlayerDict = {}
PlayerNameToID = {}
SignInPlayers = []

CF = ['CF']
MF = ['MF', 'DMF', "CM"]
CB = ['CB']
LRB = ['LB', 'RB']
LRM = ['LM', 'RM']
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



class Player(object):
    def __init__(self, Name, Position, ID, Capability):
        self.Name = Name
        self.Position = Position
        self.ID = ID
        self.Capability = Capability

    def __lt__(self, other):
        return self.Capability < other.Capability


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

def SortAndMoveExtraPlayers(PlayerList, ExtraPlayerList):
    PlayerList.sort()
    if len(PlayerList) % 2 == 1:
        ExtraPlayerList.append(PlayerList.pop())

def ClassifyPlayers():
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

    SortAndMoveExtraPlayers(SignInCFs, SignInUnknowns)
    SortAndMoveExtraPlayers(SignInMFs, SignInUnknowns)
    SortAndMoveExtraPlayers(SignInCBs, SignInUnknowns)
    SortAndMoveExtraPlayers(SignInLRBs, SignInUnknowns)
    SortAndMoveExtraPlayers(SignInLRMs, SignInUnknowns)
    SignInUnknowns.sort()

def AssignToSquad(SquadA, SquadB, PlayerList):
    if SquadA.TotalCapability > SquadB.TotalCapability:
        SquadA, SquadB = SquadB, SquadA

    current = SquadA
    for player in PlayerList:
        current.AddPlayer(player)
        if current is SquadA:
            current = SquadB
        else:
            current = SquadA


def SquadGenerator():
    SquadA = Squad("龙队")
    SquadB = Squad("虎队")

    AssignToSquad(SquadA, SquadB, SignInCFs)
    AssignToSquad(SquadA, SquadB, SignInMFs)
    AssignToSquad(SquadA, SquadB, SignInCBs)
    AssignToSquad(SquadA, SquadB, SignInLRBs)
    AssignToSquad(SquadA, SquadB, SignInLRMs)
    AssignToSquad(SquadA, SquadB, SignInUnknowns)
    SquadA.PrintSquad()
    SquadB.PrintSquad()    


def Main():
    InitPlayerDataBase()
    InitSignInPlayerDataBase()
    ClassifyPlayers()
    SquadGenerator()


Main()