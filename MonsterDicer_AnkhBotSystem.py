#---------------------------------------
# Import Libraries
#---------------------------------------
import sys, os, json, clr, codecs, math, random
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
from Settings_Module import Settings

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

m_MonsterListFile = os.path.join(os.path.dirname(__file__), "Config/monster_list.json")

#---------------------------------------
# Set Variables
#---------------------------------------
rise_weapon_list = [
    'Great Sword', 'Longsword', 'Switch Axe', 'Charge Blade', 'Lance', 'Gunlance', 'Insect Glaive',
    'Light Bowgun', 'Heavy Bowgun', 'Bow', 'Sword & Shield', 'Hunting Horn', 'Dual Blades', 'Hammer'
]

world_weapon_list = [
    'Great Sword', 'Longsword', 'Switch Axe', 'Charge Blade', 'Lance', 'Gunlance', 'Insect Glaive',
    'Light Bowgun', 'Heavy Bowgun', 'Bow', 'Sword & Shield', 'Hunting Horn', 'Dual Blades', 'Hammer'
]

rise_monster_list = [
    'Aknosom', 'Almudron', 'Anjanath', 'Arzuros', 'Apex Arzuros', 'Barioth', 'Barroth', 
    'Bazelgeuse', 'Basarios', 'Bishaten', 'Chameleos', 'Diablos', 'Apex Diablos', 'Goss Harag',
    'Great Baggi', 'Great Izuchi', 'Great Wroggi', 'Jyuratodus', 'Khezu', 'Kulu-Ya-Ku', 'Kushala Daora',
    'Lagombi', 'Magnamalo', 'Mizutsune', 'Apex Mizutsune', 'Nargacuga', 'Pukei-Pukei', 'Rajang',
    'Rakna-Kadaki', 'Rathalos', 'Apex Rathalos', 'Rathian', 'Apex Rathian', 'Royal Ludroth', 'Somnacanth',
    'Teostra', 'Tetranadon', 'Thunder Serpent Narwa', 'Narwa the Allmother', 'Tigrex', 'Tobi-Kadachi', 'Crimson Glow Valstrax',
    'Volvidon', 'Wind Serpent Ibushi', 'Zinogre', 'Apex Zinogre'
    ]

world_monster_list = [
    "Acidic Glavenus", "Alatreon", "Ancient Leshen", "Anjanath", "Azure Rathalos", "Banbaro", "Barioth", 
    "Barroth", "Bazelgeuse", "Behemoth", "Beotodus", "Black Diablos", "Blackveil Vaal Hazak", "Brachydios", 
    "Brute Tigrex", "Coral Pukei-Pukei", "Deviljho", "Diablos", "Dodogama", "Ebony Odogaron", "Fatalis",
    "Frostfang Barioth", "Fulgur Anjanath", "Furious Rajang", "Glavenus", "Gold Rathian", "Great Girros", 
    "Great Jagras", "Jyuratodus", "Kirin", "Kulu-Ya-Ku", "Kulve Taroth", "Kushala Daora", "Lavasioth", 
    "Legiana", "Leshen", "Lunastra", "Namielle", "Nargacuga", "Nergigante", "Nightshade Paolumu", "Odogaron", 
    "Paolumu", "Pink Rathian", "Pukei-Pukei", "Radobaan", "Raging Brachydios", "Rajang", "Rathalos", "Rathian", 
    "Ruiner Nergigante", "Safi'jiiva", "Savage Deviljho", "Scarred Yian Garuga", "Seething Bazelgeuse", 
    "Shara Ishvalda", "Shrieking Legiana", "Silver Rathalos", "Stygian Zinogre", "Teostra", "Tigrex", 
    "Tobi-Kadachi", "Tzitzi-Ya-Ku", "Uragaan", "Vaal Hazak", "Velkhana", "Viper Tobi-Kadachi", "Xeno'jiiva", 
    "Yian Garuga", "Zinogre", "Zorah Magdaros"
    ]

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

    # Get most recent monster lists:
    if not os.path.isfile(m_MonsterListFile):
        Parent.SendTwitchMessage('Creating monster list...')
        text_file = codecs.open(m_MonsterListFile, encoding='utf-8-sig',mode='w')
        text_file.write('')
        text_file.close()
    else:
        Parent.SendTwitchMessage('Updating monster list...')
        r = Parent.GetRequest('https://tagonist-staging.herokuapp.com/dnd5eclasses.json', {"ContentType": "application/json"})
        data = json.loads(r)
        #r =requests.get('https://xkcd.com/1906/')
        
        Parent.SendTwitchMessage(data["error"])
        
    return

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    if data.IsChatMessage():

        if  Parent.HasPermission(data.User, "Subscriber", ""):

            if MySettings.MonsterHunterGame.lower() == 'world':
                weapon_list = world_weapon_list
                monster_list = world_monster_list
            elif MySettings.MonsterHunterGame.lower() == 'rise':
                weapon_list = rise_weapon_list
                monster_list = rise_monster_list

            # Random / Dice Roll Monsters
            if data.GetParam(0).lower() == MySettings.RandomMonsterCommand.lower():
                if MySettings.RandomMonsterEnabled:

                    if data.GetParam(3):
                        Parent.SendTwitchMessage('More than 2 parameters!')

                    elif data.GetParam(2):
                        result = calcGivenRoll(float(data.GetParam(1)), int(data.GetParam(2)))
                        Parent.SendTwitchMessage('Get ready to hunt ' + getMonster(monster_list, result - 1) + '!')

                    elif data.GetParam(1):
                        Parent.SendTwitchMessage('Only 1 parameter!')

                    else:
                        result = random.choice(monster_list)
                        Parent.SendTwitchMessage('Get ready to hunt ' + result + '!')

            # Random Weapon
            if data.GetParam(0).lower() == MySettings.RandomWeaponCommand.lower():
                if MySettings.RandomWeaponEnabled:
                    result = random.choice(weapon_list)
                    Parent.SendTwitchMessage('Get ready to equip your ' + result + '!')
        else:
            Parent.SendStreamWhisper(data.User, 'Sorry, ' + data.GetParams(0) + ' is for subscribers only!')

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
    # Execute json reloading here
    MySettings.__dict__ = json.loads(jsonData)
    MySettings.Save(MySettings)
    return

#---------------------------
#   My methods
#---------------------------
def calcGivenRoll(d1, d2):
    result = int((math.floor((d1 / 2)) * 10) + d2)
    return result

def getMonster(monster_list, i):
    monster = monster_list[i]
    return monster