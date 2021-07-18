#---------------------------------------
# Import Libraries
#---------------------------------------
import sys, os, json, clr, codecs, random, logging
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
from settingsmodule import Settings

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "Monster Hunter Randomiser"
Website = "https://www.twitch.tv/talongrayson"
Description = "Adds Monster Hunter randomisation commands to chat"
Creator = "TalonGrayson"
Version = "1.0"

m_ConfigFile = os.path.join(os.path.dirname(__file__), "Settings/settings.json")
m_ConfigFileJs = os.path.join(os.path.dirname(__file__), "Settings/settings.js")

# m_MonsterListFile = os.path.join(os.path.dirname(__file__), "Config/monster_list.json")
# m_WeaponListFile = os.path.join(os.path.dirname(__file__), "Config/weapon_list.json")
m_ListsFile = os.path.join(os.path.dirname(__file__), "Config/lists.json")

#---------------------------
#   Define Global Variables
#---------------------------

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    global MySettings
    MySettings = Settings()

    if not os.path.isfile(m_ConfigFile):
        text_file = codecs.open(m_ConfigFile, encoding='utf-8-sig',mode='w')
        out = json.dumps(MySettings.__dict__, encoding="utf-8-sig")
        text_file.write(out)
        text_file.close()
    else:
        with codecs.open(m_ConfigFile,encoding='utf-8-sig',mode='r') as ConfigFile:
            MySettings.__dict__ = json.load(ConfigFile)

    if not os.path.isfile(m_ConfigFileJs):
        text_file = codecs.open(m_ConfigFileJs, encoding='utf-8-sig',mode='w')
        jsFile = "var settings =" + json.dumps(MySettings.__dict__, encoding="utf-8-sig") + ";"
        text_file.write(jsFile)
        text_file.close()

    updateLists()
    return

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    if data.IsChatMessage():

        if  Parent.HasPermission(data.User, "Subscriber", ""):

            game = MySettings.MonsterHunterGame.lower()

            # Random Monster
            if data.GetParam(0).lower() == MySettings.RandomMonsterCommand.lower():
                if MySettings.RandomMonsterEnabled:
                    monster_list = Lists["monsters"][game]
                    result = random.choice(monster_list)
                    Parent.SendTwitchMessage('Get ready to hunt ' + result + '!')

            # Random Weapon
            if data.GetParam(0).lower() == MySettings.RandomWeaponCommand.lower():
                if MySettings.RandomWeaponEnabled:
                    weapon_list = Lists["weapons"][game]
                    result = random.choice(weapon_list)
                    Parent.SendTwitchMessage('Get ready to equip your ' + result + '!')

            # Random Quest
            if data.GetParam(0).lower() == MySettings.RandomQuestCommand.lower():
                if MySettings.RandomQuestEnabled:
                    quest_list = Lists["quests"]["rise"]
                    result = random.choice(quest_list)
                    result_msg = questMsg(result)
                    Parent.SendTwitchMessage(result_msg)
        else:
            Parent.SendTwitchMessage(data.User, 'Sorry, ' + data.GetParams(0) + ' is for subscribers only!')

    return

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
    return

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    Init()
    return

#---------------------------
#   My methods
#---------------------------

def questMsg(result):
    target = formatTarget(result["target"])
    msg = result["name"] + ": " + result["hunt_type"] + " " + target + " - " + result["rank"] + " Rank (" + str(result["stars"]) + " star) " + result["quest_type"] + " Quest"
    return msg

def formatTarget(targets):
    n = len(targets)
    str = ""

    if n == 1:
        str = targets[0]
    elif n == 2:
        str = targets[0] + " and " + targets[1]
    else:
        for i, target in enumerate(targets):
            if i < n-1:
                str += target + ", "
            else:
                str += "and " + target

    return str
    
def updateLists():
    global Lists

    r = Parent.GetRequest(
                'https://api.github.com/repos/talongrayson/monsterhunterrandomiser/contents/Config/lists.json',
                {"Accept": "application/vnd.github.v3.raw"}
                )

    data = json.loads(r)

    lists = data["response"]

    text_file = codecs.open(m_ListsFile, encoding='utf-8-sig',mode='w')
    text_file.write(lists)
    text_file.close()

    with codecs.open(m_ListsFile, encoding='utf-8-sig', mode='r') as jsonFile:
        Lists = json.load(jsonFile)
        jsonFile.close()

    return