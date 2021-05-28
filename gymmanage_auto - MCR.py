import random
# import webbrowser
import time
import urllib
import urllib.parse
import urllib.request
import re
import math

"""This script manages an autogym"""

# TODO - Training module for champions in regional.....being passed through but can't find the fighter name or code
# It's all regional champs and contenders


# #################################  ONLY CHANGE THE STUFF IN HERE####################################
# Sets up number of fighters per weight - just edit to change.  This number of fighters will be created for each
# region entered into WEBL regions
FIGHTERS_PER_WEIGHT = 6
# FIGHTERS_PER_WEIGHT = 1
# FIGHTERS_PER_WEIGHT = 4


# Username and Password
USERNAME = 'MelchesterRovers'
PASSWORD = 'BotBotBot123'


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Fighter Builds >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Order of APs: [str, KP, speed, agl, chin, cond, height, build]
# 130, 141, 167, 175, 200 CP all modified as initial values were wrong...using anagrams heavy build
COUNTER_PUNCHER = {106: [12, 0, 16, 15, 10, 14, 2, -3], 109: [11, 0, 17, 14, 10, 14, 3, -3],
                   112: [11, 0, 16, 14, 10, 14, 4, -3], 115: [10, 0, 16, 14, 10, 14, 5, -3],
                   118: [10, 0, 16, 13, 10, 14, 6, -3], 122: [9, 0, 16, 13, 10, 14, 7, -3],
                   126: [10, 0, 15, 13, 10, 14, 7, -3], 130: [10, 0, 15, 13, 9, 14, 8, -3],
                   135: [9, 0, 15, 12, 10, 14, 9, -3], 141: [9, 0, 14, 12, 10, 14, 10, -3],
                   147: [9, 0, 14, 11, 10, 14, 11, -3], 153: [9, 0, 13, 11, 10, 14, 12, -3],
                   160: [8, 0, 13, 11, 10, 14, 13, -3], 167: [8, 0, 13, 11, 10, 13, 14, -3],
                   175: [7, 0, 13, 10, 10, 14, 15, -3], 200: [6, 0, 13, 10, 9, 13, 18, -3],
                   1000: [3, 0, 15, 10, 10, 13, 18, 3]}

KP_DANCER = {106: [8, 2, 13, 15, 10, 15, 6, -3], 109: [7, 2, 13, 15, 10, 15, 7, -3],
             112: [8, 2, 13, 14, 10, 15, 7, -3], 115: [8, 2, 14, 13, 10, 15, 7, -3],
             118: [8, 2, 12, 14, 10, 15, 8, -3], 122: [7, 2, 12, 14, 10, 15, 9, -3],
             126: [6, 2, 12, 14, 10, 15, 10, -3], 130: [7, 2, 12, 13, 10, 15, 10, -3],
             135: [7, 2, 11, 13, 10, 15, 11, -3], 141: [6, 2, 12, 12, 10, 15, 12, -3],
             147: [6, 2, 11, 12, 10, 15, 13, -3], 153: [6, 2, 12, 11, 10, 15, 13, -3],
             160: [6, 2, 11, 11, 10, 15, 14, -3], 167: [6, 2, 10, 11, 10, 15, 15, -3],
             175: [6, 2, 9, 11, 10, 15, 16, -3], 200: [5, 1, 10, 10, 10, 14, 19, -3],
             1000: [3, 1, 8, 9, 9, 14, 25, -3]}

KP_SLUGGER = {106: [16, 5, 15, 11, 11, 13, -2, 3], 109: [15, 5, 14, 12, 11, 13, -1, 3],
              112: [15, 5, 15, 11, 11, 13, -1, 3], 115: [15, 5, 13, 12, 11, 13, 0, 3],
              118: [15, 5, 14, 11, 11, 13, 0, 3], 122: [16, 5, 12, 11, 11, 13, 1, 3],
              126: [14, 4, 14, 11, 11, 13, 2, 3], 130: [15, 5, 14, 10, 11, 13, 1, 3],
              135: [14, 4, 13, 11, 11, 13, 3, 3], 141: [14, 4, 14, 10, 11, 13, 3, 3],
              147: [14, 4, 13, 10, 11, 13, 4, 3], 153: [13, 4, 13, 10, 11, 13, 5, 3],
              160: [13, 4, 12, 10, 11, 13, 6, 3], 167: [13, 4, 13, 9, 11, 13, 6, 3],
              175: [13, 4, 12, 9, 11, 13, 7, 3], 200: [12, 4, 11, 8, 11, 13, 10, 3],
              1000: [11, 3, 11, 9, 10, 13, 12, 3]}

FRK_CLINCHER = {106: [0, 0, 0, 0, 0, 0, 0, 0], 109: [0, 0, 0, 0, 0, 0, 0, 0],
                112: [0, 0, 0, 0, 0, 0, 0, 0], 115: [0, 0, 0, 0, 0, 0, 0, 0],
                118: [0, 0, 0, 0, 0, 0, 0, 0], 122: [0, 0, 0, 0, 0, 0, 0, 0],
                126: [33, 0, 13, 1, 10, 14, -2, -3], 130: [33, 0, 13, 1, 10, 14, -2, -1],
                135: [33, 0, 13, 1, 10, 14, -2, 1], 141: [33, 0, 13, 1, 10, 14, -2, 3],
                147: [32, 0, 13, 1, 10, 14, -1, 3], 153: [33, 0, 12, 1, 10, 14, -1, 3],
                160: [32, 0, 12, 1, 10, 14, 0, 3], 167: [30, 0, 13, 1, 10, 14, 1, 3],
                175: [29, 0, 13, 1, 10, 14, 2, 3], 200: [27, 0, 12, 1, 10, 14, 5, 3],
                1000: [0, 0, 0, 0, 0, 0, 0, 0]}

AGILE_SLUGGER = {106: [18, 0, 13, 16, 9, 14, -1, 3], 109: [17, 0, 13, 16, 9, 14, 0, 3],
                 112: [18, 0, 13, 15, 9, 14, 0, 3], 115: [17, 0, 13, 15, 9, 14, 1, 3],
                 118: [16, 0, 11, 17, 9, 14, 2, 3], 122: [15, 0, 14, 15, 9, 14, 2, 3],
                 126: [15, 0, 13, 15, 9, 14, 3, 3], 130: [16, 0, 13, 14, 9, 14, 3, 3],
                 135: [15, 0, 12, 15, 9, 14, 4, 3], 141: [15, 0, 12, 14, 9, 14, 5, 3],
                 147: [14, 0, 12, 14, 9, 14, 6, 3], 153: [14, 0, 12, 13, 9, 14, 7, 3],
                 160: [13, 0, 12, 13, 9, 14, 8, 3], 167: [13, 0, 11, 13, 9, 14, 9, 3],
                 175: [13, 0, 10, 13, 9, 14, 10, 3], 200: [13, 0, 10, 11, 9, 14, 12, 3],
                 1000: [7, 0, 7, 9, 9, 13, 24, 3]}


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   Fight Plans and Codes >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Used to put the code in front of the fighter names.
# If changed here, need to change in the fight plans variables too
# Code for each fighter type\
COUNTER_CODE = '"LO"'
KPD_CODE = '"HM"'
KPS_CODE = '"DT"'
FCL_CODE = '"JR"'
AGS_CODE = '"RD"'

# Add a new fighter type to this dictionary in order to be selected randomly when creating a fighter
# TODO - this looks like this could be real problem.  Tidy this up and maybe combine them? - added variables
# which might help

KPD_TEXT = 'KP Dancer'
CP_TEXT = "CounterPuncher"
KPS_TEXT = "KP Slugger"
FCL_TEXT = "Freak Clincher"
AGS_TEXT = "Agile Slugger"


# FIGHTER_TYPES = {CP_TEXT: COUNTER_PUNCHER, KPD_TEXT: KP_DANCER, KPS_TEXT: KP_SLUGGER,
                # FCL_TEXT: FRK_CLINCHER, AGS_TEXT: AGILE_SLUGGER}
# FIGHTER_TYPES = {CP_TEXT: COUNTER_PUNCHER}

# removed freak clincher and KP Slugger from new fighter types
FIGHTER_TYPES = {KPD_TEXT: KP_DANCER, AGS_TEXT: AGILE_SLUGGER, FCL_TEXT: FRK_CLINCHER, KPS_TEXT: KP_SLUGGER }

SECRET_CODE = {CP_TEXT: COUNTER_CODE, KPD_TEXT: KPD_CODE, KPS_TEXT: KPS_CODE,
               FCL_TEXT: FCL_CODE, AGS_TEXT: AGS_CODE}

# This is the length of the secret code.  Used to retrieve the code easily.  Relies on Secret Codes all being
# the same length
LEN_SECRET_CODE = 4

# HM Plans - KP Dancer plans, used by guys with HM in their name
HM_PLANS = ["Boxing I", "Boxing II", "Set up a KO"]
# LO Plans - counter puncher plans, used by guys with LO in their name
LO_PLANS = ["LO1", "LO2", "LO3", "LO4", "LO5"]
# SB plans - KP Slugger plans.
KPS_PLANS = ["Flash KO", "Set up a KO"]
# JR plans - Freak Clincher plans
FCL_PLANS = ["Basic Slugger Tactics", "Slugging and Boxing"]
# Agile slugger plans
AGS_PLANS = ["Basic Slugger Tactics", "Slugging and Boxing"]

# dictionary of the different plan types.
PLAN_DICT = {KPD_CODE: HM_PLANS, COUNTER_CODE: LO_PLANS, KPS_CODE: KPS_PLANS, FCL_CODE: FCL_PLANS, AGS_CODE: AGS_PLANS}


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Weihongght Classes and Regions >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# all weight classes.  Put a # in front of the ones you don't want if making them for smaller weight classes
WEIGHT_CLASSES_WEBL = {106: 1, 109: 2, 112: 3, 115: 4, 118: 5, 122: 6, 126: 7, 130: 8, 135: 9, 141: 10,
                       147: 11, 153: 12, 160: 13, 167: 14, 175: 15, 200: 16, 1000: 17}

# add less weights for testing
# WEIGHT_CLASSES_WEBL = {106: 1, 109: 2}
# WEIGHT_CLASSES_WEBL = {141: 10, 167: 14, 175: 15, 200: 16}
# standard one, all but heavy

#WEIGHT_CLASSES_WEBL = {106: 1, 109: 2, 112: 3, 115: 4, 118: 5, 122: 6, 126: 7, 130: 8, 135: 9, 141: 10,
#                        147: 11, 153: 12, 160: 13, 167: 14, 175: 15, 200: 16}
# WEIGHT_CLASSES_WEBL = {1000: 17}
# WEIGHT_CLASSES_WEBL = {122: 6}

# regions and their Webl code - for now I only want to create fighters in one of three regions
# REGIONS = {'WBC': '10000002', 'WBA':'10000001', 'WBO' : '10000003', 'Revival' :'57845',  'Unsanctioned' :'11384',
# 'Bare Knuckles':'11764', 'Amateur':'11765', 'Graduated':'16299'}
#REGIONS = {'WBC': '10000002', 'WBA': '10000001', 'WBO': '10000003'}
# REGIONS = {'WBO': '10000003' }

#Home region change
# REGIONS = {'Eurasia': '0'}
REGIONS ={'British Commonwealth': 0}

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Training Ratios and Configurations >>>>>>>>>>>>>>>>>>>>>>>>>>>>

# ####### !!!!!!!!!!!!  kp dancer  ####### !!!!!!!!!!!!
# change strength ratio between lighter and heavier guys.
# light cutoff is below.  make lighter guys strength a bit higher in comparison to agility
# just tweak here to change all fighters ratios
KP_DANCER_LIGHT = 135
KPD_STR_RATIO_LIGHT = 0.55
KPD_STR_RATIO_HEAVY = 0.5

# ####### !!!!!!!!!!!! Counter Puncher ####### !!!!!!!!!!!!
# tweak if desired same as kp dancer
COUNTER_AGL_TO_SPD = 0.8
COUNTER_AGL_TO_SPD_VRY_LOW = 0.7
COUNTER_STR_TO_SPD = 0.6

# CONTENDER RATIOS FOR CP'ERS
COUNTER_CONT_AGL_TO_SPEED = 0.95
COUNTER_CONT_AGL_TO_SPD_VRY_LOW = 0.85
COUNTER_CONT_STR_TO_SPD = 0.7


# ##########!!!!!!!!! Freak Clincher Stats !!!!!!!!!!!##############
# Status 6 ratios
FREAKCLINCH_STATUS_LOWEST = 6
FREAKCLINCH_SPD_TO_STR_LOWEST = 0.38
FREAKCLINCH_CHIN_LOWEST = 10
FREAKCLINCH_COND_LOWEST = 15

# status 12 ratios
FREAKCLINCH_STATUS_LOW = 12
FREAKCLINCH_SPD_TO_STR_LOW = 0.45
FREAKCLINCH_CHIN_LOW = 11
FREAKCLINCH_COND_LOW = 16

# status 18 ratios
FREAKCLINCH_STATUS_MID = 18
FREAKCLINCH_SPD_TO_STR_MID = 0.44
FREAKCLINCH_CHIN_MID = 11
FREAKCLINCH_COND_MID = 17

# status 24 ratios
FREAKCLINCH_STATUS_HIGH = 24
FREAKCLINCH_SPD_TO_STR_HIGH = 0.4
FREAKCLINCH_CHIN_HIGH = 11
FREAKCLINCH_COND_HIGH = 19

#  above status 24 rations
FREAKCLINCH_SPD_TO_STR_HIGHEST = 0.4
FREAKCLINCH_CHIN_HIGHEST = 12
FREAKCLINCH_COND_HIGHEST = 19


# !!!!!!!!!!!!!! KP Slugger configs and ratios !!!!!!!!!!!!!!!!!!!!

# ratio ranges.   Keep consistent all the way through
KPSLUGGER_SPD_TO_STR_MIN = 0.95
KPSLUGGER_SPD_TO_STR_MAX = 1.0
KPSLUGGER_AGL_TO_SPD_MIN = 0.65
KPSLUGGER_AGL_TO_SPD_MAX = 0.73

# at status 6
KPSLUGGER_STATUS_LOWEST = 6
KPSLUGGER_CHIN_LOWEST = 11
KPSLUGGER_COND_LOWEST = 14

# status 12
KPSLUGGER_STATUS_LOW = 12
KPSLUGGER_CHIN_LOW = 13
KPSLUGGER_COND_LOW = 14

# status 18
KPSLUGGER_STATUS_MID = 18
KPSLUGGER_CHIN_MID = 13
KPSLUGGER_COND_MID = 15

# status 24 and up
KPSLUGGER_STATUS_HIGH = 24
KPSLUGGER_CHIN_HIGH = 15
KPSLUGGER_COND_HIGH = 16

# !!!!!!!!!!!!!!!!!!!! Agile Slugger Configs and ratios !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

AGSLUGGER_AGL_TO_STR = 1
AGSLUGGER_SPD_TO_AGL = 0.8

# status 6
AGSLUGGER_STATUS_LOWEST = 6
AGSLUGGER_COND_LOWEST = 15
AGSLUGGER_CHIN_LOWEST = 9

# status 12
AGSLUGGER_STATUS_LOW = 12
AGSLUGGER_CHIN_LOW = 10
AGSLUGGER_COND_LOW = 15

# STATUS 18
AGSLUGGER_STATUS_MID = 18
AGSLUGGER_CHIN_MID = 11
AGSLUGGER_COND_MID = 16

# STATUS 24
AGSLUGGER_STATUS_HIGH = 24
AGSLUGGER_CHIN_HIGH = 11
AGSLUGGER_COND_HIGH = 17

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Retirement Conditionals >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# AP loss to retire at regional status.  At this stage, just use regional
RETIRE_AP_LOSS_REG = 1
RETIRE_REG_STATUS = 18

# AP loss to retire fighter at at anytime
RETIRE_AP_LOSS_ANY = 2



# #############################################################################################
# ################################## DON'T CHANGE ANYTHING BELOW HERE #########################
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# <<<<<<<<<<<<<<<<<<<<<<<<<<  Weight Division Webl Config >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


WEIGHT_DIVISIONS = {'Heavyweights (1000 pounds)': {'name': 'Heavyweight', 'max': 1000, 'min': 201},
                    'Cruiserweights (200 pounds)': {'name': 'Cruiserweight', 'max': 200, 'min': 176},
                    'Light-Heavyweights (175 pounds)': {'name': 'Light-Heavyweight', 'max': 175, 'min': 168},
                    'Super-Middleweights (167 pounds)': {'name': 'Super-Middleweight', 'max': 167, 'min': 161},
                    'Middleweights (160 pounds)': {'name': 'Middleweight', 'max': 160, 'min': 154},
                    'Super-Welterweights (153 pounds)': {'name': 'Super-Welterweight', 'max': 153, 'min': 148},
                    'Welterweights (147 pounds)': {'name': 'Welterweight', 'max': 147, 'min': 142},
                    'Super-Lightweights (141 pounds)': {'name': 'Super-Lightweight', 'max': 141, 'min': 136},
                    'Lightweights (135 pounds)': {'name': 'Lightweight', 'max': 135, 'min': 131},
                    'Super-Featherweights (130 pounds)': {'name': 'Super-Featherweight', 'max': 130, 'min': 127},
                    'Featherweights (126 pounds)': {'name': 'Featherweight', 'max': 126, 'min': 123},
                    'Super-Bantamweights (122 pounds)': {'name': 'Super-Bantamweight', 'max': 122, 'min': 119},
                    'Bantamweights (118 pounds)': {'name': 'Bantamweight', 'max': 118, 'min': 116},
                    'Super-Flyweights (115 pounds)': {'name': 'Super-Flyweight', 'max': 115, 'min': 113},
                    'Flyweights (112 pounds)': {'name': 'Flyweight', 'max': 112, 'min': 110},
                    'Junior-Flyweights (109 pounds)': {'name': 'Junior-Flyweight', 'max': 109, 'min': 107},
                    'Strawweights (106 pounds)': {'name': 'Strawweight', 'max': 106, 'min': 1}}


# FIGHTER_TRAIN is a dictionary for fighter tupes that have training mapped out, not random or a function
# FIGHTER_TRAIN = {"LO": COUNTER_TRAIN, "HM": KPD_TRAIN}
# FIGHTER_TRAIN = {'"LO"': COUNTER_TRAIN}
# Just left here now because it's easier than changing the code.........
FIGHTER_TRAIN = {}
KPD_TRAIN = {}

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Build conversion  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
BUILD_WEBL = {'Very Light': -3, 'Light': -2, 'A Little Light': -1, 'Normal': 0, 'A Little Heavy': 1,
              'Heavy': 2, 'Very Heavy': 3}

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Global Variables for URL's >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

GET_BRIEF_URL = 'https://webl.vivi.com/cgi-bin/query.fcgi?username={$username}&password={$password}' \
                '&command=eko_all_fighters_brief&competition=eko'

# Variables used to pass through to webl for commands
URL_MIN = 'https://webl.vivi.com/cgi-bin/query.fcgi'
VAL_USERNAME = 'username'
VAL_PW = 'password'
VAL_COMMAND = 'command'
COMMAND_CREATE_FIGHTER = 'eko_create_fighter'
COMMAND_CHANGE_FP = 'eko_select_orders'
COMMAND_MAIN_GYM = 'eko_default'
COMMAND_SHORTGYM = 'eko_all_fighters_brief'
COMMAND_RETIRE = 'eko_retire_byid'
COMMAND_CHANGE_DIVISION = 'eko_change_division'
COMMAND_TRANSFER_FIGHTER = 'eko_transfer'
COMMAND_TRAINING = 'eko_training'
COMMAND_CONTROL_FIGHTER = 'eko_control_fighter'
COMMAND_QUERY_PRESS = 'query_press'
COMMAND_RETIRED_GYM = 'eko_retired_fighters'
VAL_FIGHTER_NAME = 'team'
VAL_REGION = 'region'
VAL_STR = 'strength'
VAL_KP = 'ko_punch'
VAL_SP = 'speed'
VAL_AGL = 'agility'
VAL_CHIN = 'chin'
VAL_CON = 'condition'
VAL_CUT = 'cut'
VAL_BUILD = 'build'
VAL_HEIGHT = 'height'
VAL_DIVISION = 'division'
VAL_NAME = 'team'
VAL_CHANGE_FIGHTER_PLAN = 'your_team'
VAL_YOUR_TEAM = 'your_team'
VAL_STRATEGY_CHOICE = 'strategy_choice'
VAL_TRAIN_1 = "train"
VAL_TRAIN_2 = "train2"
VAL_TEAM_ID = 'team_id'
VAL_MANAGER_ID = 'manager_id'
VAL_MANAGER_TO = 'to_manager'
VAL_PRESS = 'press'

# naughty bit of hard coding
MY_MANAGER_ID = '244354'

# variables below are in HTML on site
NAME_START = '<A name="'
NAME_FIND = '=Heavy">'
# modified PM 2017/04/26 after site changes changed URL to include Team ID
# NAME_LINE_START = '&+command=eko_control_fighter&+competition=eko&+region=Contenders&+division=Heavy">'

#new Name LIne Start
NAME_LINE_START = '">'

NAME_LINE_END = '</A>'
NAME_TITLE_END = '<IMG SRC='
END_BOLD = '</B>'
BREAK = '<BR>'
OVERWEIGHT = 'Having trouble making weight.'
UNDERWEIGHT = 'May be fighting at a disadvantage due to weight.'
FIGHTER_TEAM = '+team='
WEIGHT_START = '<H4>'
WEIGHT_END = '</H4>'
WEIGHT_FIGHTER = 'Weight:'
POUNDS = 'pounds'
END_RECORD = '<A  HREF'
STATS_STRENGTH = '<TR><TD>Strength <TD align=right>'
STATS_BREAK = '<BR>'
STATS_KP = '<TD>Knockout Punch <TD  align=right>'
STATS_SPEED = '<TR><TD>Speed <TD align=right>'
STATS_AGL = 'TD>Agility <TD align=right>'
STATS_CHN = '<TR><TD>Chin <TD align=right>'
STATS_CND = '<TD>Conditioning <TD align=right>'
STATS_STATUS = '<TD><a href=/eko/glossary.html#status target=glossary onClick=help()>Status</A><TD align=right>'
GET_FIGHTER_COMMAND = '+command=eko_control_fighter'
STATS_HEIGHT = '<TR><TD>Height<TD colspan=3>'
NEXT_BOUT = 'Next Bout: the '
OPP_START = '&describe=1&+command=eko_careerbyid&+competition=eko&+region=Contenders&+division=Heavy">'
REG_TITLE = 'border=0 align=bottom></A>'
AP_LOSS = '<TD>AP Loss</A><TD align=right>'

# had to add extra check in get_team_id after contender level fighters came into the mix.
CONTENDERS_TEXT = '<B>Contenders</B>'

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Other Global Variables >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Chance of talking trash.  Will be one in this number - so will draw random up to this number...talk if == this no.
# Trash talk removed for now
TRASH_TALK_CHANCE = 75

# menu choices
MENU_ALL = '1'
MENU_FP = '2'
MENU_TRAINING = '3'
MENU_BEST_WEIGHT = '4'
MENU_RETIRE_POOR = '5'
MENU_UPDATE_FIGHTER_NOS = '6'
MENU_TALK_TRASH = '7'
MENU_MASS_CREATE = '99'


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<    Training Variables  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Training abbreviations
TRAIN_SPD = 'SPD'
TRAIN_STR = 'STR'
TRAIN_AGL = 'AGL'
TRAIN_KP = 'KP'
TRAIN_CHN = 'CHN'
TRAIN_CND = 'CND'
TRAIN_HGT = 'HGT'
TRAIN_AP_LOSS = "APL"

# Values used in training
TRAIN_VALUES = {'STR': 'weights (STR)', 'KP': 'heavy bag (KP)', 'SPD': "speed bag (SPD)",
                'AGL': "jump rope (AGL)","CHN": "sparring (CHN)", 'CND': "road work (CND)"}

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  START OF CODE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  User Input Required >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<<<<<<<<<<<  URL Calls - all outbound/inbound stuff >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def get_site_page(username, password, command):
    """reads whichever page is sent through with the values"""
    # url = URL_MIN
    values = {VAL_USERNAME: username, VAL_PW: password, VAL_COMMAND: command}

    words = read_pages(values)

    return words


def read_pages(values):
    """reads the page of the values sent through"""
    # gets start url
    url = URL_MIN

    '''
    # web stuff!
    data = urllib.parse.urljoin(values)
    req = urllib.request.urlopen(url, data)
    response = urllib.urlopen(req)

    words = response.read()


    Did not work.  Try the below code
    '''

    # web stuff!
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')

    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)

    words = response.read()



    return words


def get_fighter_page(username, password, line):
    """returns details for fighter page frm fighter first line in full gym"""
    # get fighters detail page
    team_id = get_team_id(line)
    
    # commented out line below after changing get team id function
    # team_id = team_id[0]

    # put values into dictionary
    f_values = {VAL_USERNAME: username, VAL_PW: password, VAL_TEAM_ID: team_id, VAL_COMMAND: COMMAND_CONTROL_FIGHTER}

    # read fighter page
    f_details = read_pages(f_values)

    return f_details


def call_url(values):
    """calls the URLs rather than opening browsers.  Assumes values are a list of dictionaries
    intended to issue bulk commands as doesnt return anything"""

    url = URL_MIN
    quarter = False
    half = False
    three_quarter = False

    check = len(values)
    count = 0

    if check > 10:
        print("About to start updating.  This may take a while, there are " + str(check) + " entries to do....")

    for v in values:
        # values = {'username': USERNAME, 'password': PASSWORD, 'command': 'eko_default'}
        
        # req = urllib.Request(url, data)
        # response = urllib.request.urlopen(req)

        """
        data = urllib.parse.urlencode(v).encode("utf-8")
        response = urllib.request.urlopen(url, data) """

        read_pages(v)
        
        time.sleep(0.5)
        count += 1

        # print progress
        if count > 10:
            if count > (check * 0.25) and not quarter:
                print( "25% done")
                quarter = True
            elif count > (check * 0.5) and not half:
                print( "50% done")
                half = True
            elif count > (check * 0.75) and not three_quarter:
                print("75% done")
                three_quarter = True

    print( "Complete!")


def get_random_name():
    contents = urllib.request.urlopen("http://en.wikipedia.org/wiki/Special:Random").read()
    title = str(contents).split('<title>')[1].split(' - Wikipedia</title>')[0]
    return title


def short_gym_site(username, password):
    """reads the short gym from the website"""
    # url = URL_MIN
    values = {VAL_USERNAME: username, VAL_PW: password, VAL_COMMAND: COMMAND_SHORTGYM}

    words = read_pages(values)

    return words



# <<<<<<<<<<<<<<<<<<<<<<< building values for URL calls >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def create_retire_values(username, password, team_id):
    """build the values to retire"""
    # http://webl.vivi.com/cgi-bin/query.fcgi?username={$username}&password={$password}
    # &+team_id={$fighterid}&+command=eko_retire_byid

    ret_values = {VAL_USERNAME: username, VAL_PW: password, VAL_TEAM_ID: team_id, 
                  VAL_COMMAND: COMMAND_RETIRE}

    return ret_values


def retire_fighter(username, password, line):
    """performs actions to retire fighter"""
    # create values to call URL to retire fighter
    team_id = get_team_id(line)

    # create values to append to url call
    url_values = create_retire_values(username, password, team_id)

    return url_values



def change_weightURL(username, password, divname, fightername):
    # build values to change weight division
    values = {VAL_USERNAME: username, VAL_PW: password, VAL_COMMAND: COMMAND_CHANGE_DIVISION, 
              VAL_DIVISION: divname, VAL_CHANGE_FIGHTER_PLAN: fightername}

    return values



def create_change_fp_url(username, password, f_name, plan):
    values = {VAL_USERNAME: username, VAL_PW: password, VAL_COMMAND: COMMAND_CHANGE_FP,
              VAL_CHANGE_FIGHTER_PLAN: f_name, VAL_STRATEGY_CHOICE: plan}

    return values


def create_training_values(username, password, fname, tr1, tr2):
    """builds the URL to update fighter training"""

    # look up the values to send through
    train1 = TRAIN_VALUES[tr1]
    train2 = TRAIN_VALUES[tr2]

    # build values to change training
    values = {VAL_USERNAME: username, VAL_PW: password, VAL_COMMAND: COMMAND_TRAINING, 
              VAL_YOUR_TEAM: fname, VAL_TRAIN_1: train1, VAL_TRAIN_2: train2}

    return values


def start_updates(changes):
    # send changes to call_url
    print("About to start fighter updates. " + str(len(changes)) + " updates scheduled")
    call_url(changes)   


#   <<<<<<<<<<<<<<<<<<<<<<<<<<<  Fighter Numbers - Checking all correct >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def update_fighter_numbers(username, password):
    """checks fighter numbers against global variables for all divisions and regions
    Does NOT assume fighters are in the correct weight class. They will be if run as part of gym maintenance,
    but wont be if just retirement run"""

    # get short gym

    # change here to use local file for testing.
    # words = short_gym()
    words = short_gym_site(username, password)
    
    # could maybe speed up a bit by quicly skimming lines and seeing if any actually needed first
    # just webl weights * regions * fighters per region
    # or set a max fighters variable in globals and compare
    
    ftotals = {}
    total = 0
    
    # create dictionaries for all regions and weight classes
    for wt in WEIGHT_CLASSES_WEBL.keys():
        wt_dict = {}
        for reg in REGIONS.keys():
            # in weight, add region
            wt_dict[reg] = 0
            
        ftotals[wt] = wt_dict
            
    # ok dictionaries now set up      
    
    # loop through, count fighters in each weight class and region
    max_wt = 1

    words= words.decode("utf-8")

    for line in words.splitlines():
        # check for weight class
        if WEIGHT_START in line:
            # start counting
            max_wt, min_wt = get_weight_details(line)
            
            # print max_wt
            # print type(max_wt)
            # print ftotals
            
        if max_wt in ftotals:
            # if its not in there, dont manage this weight. must be doing manually or letting die
            
            # load the division dictionary
            curr_dict = ftotals[max_wt]
            
            # max weight will line up with the weight class dictionaries
            # <A name="hmelektrikchurch131" HREF="http://webl.vivi.com/cgi-bin/query.fcgi?+team_id=1566648&+
            # command=eko_control_fighter&+competition=eko&+region=Contenders&+division=Heavy">
            # "HM" Elektrik Church 131</A>  <B>WeBL Boxing Organization (WBO)</B> (0-0-0) 0(0) <BR><BR>
            
            # &+command=eko_control_fighter&+competition=eko&+region=Contenders&+division=Heavy"
        
            if NAME_LINE_START in line:
                # on fighters line. get region
                
                # no idea why regex didnt work
                # regex = re.search(' \((\d+)\)</B> \(', line)
                # results = regex.groups()
                # region = results[0]

                # UPDATE 08/03/2017  -  regions changed to 1 not multiple.  Issues with detecting numbers
                #pos1 = line.find('(')
                #pos2 = line.find(')')
                #region = line[pos1 + 1: pos2]

                # removed total from here I think counting unsanctioned fighters.

                # total += 1
                # UPDATE 08/03/2017  -  regions changed to 1 not multiple.  Issues with detecting numbers
                # UPDATE: 03/02/2016 - issue with contenders!  Doesn't find the right region.
                #if region in curr_dict:
                    #curr_dict[region] += 1
                for key in curr_dict:
                    region = key
                    if region in line:
                        curr_dict[region] += 1
                        # moved total to here, as it was counting unsanctioned fighters.
                        total += 1

                # update main dictionary
                ftotals[max_wt] = curr_dict
    
    # end of short gym, so do a quick count
    # print for testing
    # print 'Fighter totals: ' + str(ftotals)
    
    # check max number
    f_no = len(WEIGHT_CLASSES_WEBL) * len(REGIONS) * FIGHTERS_PER_WEIGHT
    
    # print just during testing
    # print f_no
    
    if f_no > total:
        # need to add fighters, so get name
        # name = get_first_name()

        # don't prompt for names as above, just get a random title from wikipedia.
        name = get_random_name()

        # go through weight class dictionary and add fighters until hit the limit. 
        # can live with the fact that may go one or two over cap, and that dictionary will draw weights
        # randomly, thats fine. will it?  no it wont, its not a list. changed way to do it. 
        
        # count of fighters to create and dictionary to store them,
        f = f_no - total  
        fd = []
        name_count = 1
        
        for w in WEIGHT_CLASSES_WEBL:
            # go through weight classes want to populate
            test_dict = ftotals[w]
            
            # check in loop to see if enough fighters have been made
            if f <= 0:
                # hit cap or over by a handful
                break 
                
            # now go through regions, check against number per wweight
            for r in REGIONS:
                num = test_dict[r]
                
                # see how many short we are
                x = FIGHTERS_PER_WEIGHT - num
                
                if x > 0:
                    # need to make them.
                    c = 0
                    
                    while c < x:
                        # make fighter
                        # weight division
                        div = WEIGHT_CLASSES_WEBL[w]
                        # region
                        rgn = REGIONS[r]
                        
                        val = create_random_fighters(username, password, name, div, rgn, name_count, w)
                        
                        fd.append(val)
                        
                        # better not miss a count!
                        c += 1
                        name_count += 1
                        f -= 1
        
        # create fighters
        print('Adding new fighters to make up numbers.')        
        
        # testing stuff
        # print fd
        # print len(fd)
        
        # comment out for testing
        call_url(fd)


# <<<<<<<<<<<<<<<<<<<<<<<<<< retrieve info from line, words etc - all local variables >>>>>>>>>>>>>>>>>>

def get_weight_details(line):
    """gets the details of the weightclass from a single line"""
    pos = line.find(WEIGHT_END)
    x = len(WEIGHT_START)
    wt = line[x: pos]
    wt_dict = WEIGHT_DIVISIONS[wt]

    # weight = wt_dict['name']
    max_wt = wt_dict['max']
    min_wt = wt_dict['min']

    return max_wt, min_wt


def get_line_details(line):

    max_wt = 0
    min_wt = 0
    title_name_line = 'name'


    # check line for start of weight division
    if WEIGHT_START in line:
        # at start of weight
        max_wt, min_wt = get_weight_details(line)
        # add weight to fighter count dictionary
        # fighter_count[max_wt] = 0

    if NAME_START in line:
        # has issues with fighters with regional titles.  Doesn't collect name correctly.
        # get line with the fighters name in it to be used later if required.  Collect the line to be used
        # later
        title_name_line = line

    return max_wt, min_wt, title_name_line



def fighter_name_line_long_gym(line):
    """get my fighter name from one line passed through from the long gym file"""
    pos1 = line.find(NAME_LINE_START)
    pos2 = line.find(NAME_LINE_END)
    fname = line[pos1 + len(NAME_LINE_START): pos2]

    return fname


def fighter_name_champ_line(fline):
    """
    get the fighter name from a fighter with a title star in their name
    :param fline:
    :return:
    """
    pos1 = fline.find(NAME_LINE_START)
    pos2 = fline.find(NAME_TITLE_END)
    fname = fline[pos1 + len(NAME_LINE_START): pos2]

    return fname


def get_secret_code(fighter_name):
    """retrieves the secret code from the fighter name.
    Put here incase I make it more complex in the future"""

    #  A bit lazy, but just uses the length of the secret code.
    # could may use an 'in' thing to get it done?
    code = fighter_name[:LEN_SECRET_CODE]

    return code


def get_my_fighter_record(words):
    """gets fighter records from a line in long gym where the fighters name is - first line of fighter"""
    # get record in line
    pos1 = words.find(END_BOLD)
    pos2 = words.find(END_RECORD)
    rec = words[pos1 + len(END_BOLD): pos2]
    rec = rec.strip()

    # find the records, and pull out the results
    regex = re.search('\((\d+)-(\d+)-(\d+)\) (\d+)\((\d+)\)', rec)
    # results group will be (wins, losses, draws, rating, status)
    results = regex.groups()

    return results


def get_fighter_min_wt(line):
    """get the fighters minimum weight"""
    wt_pos = line.find(WEIGHT_FIGHTER)

    wt_string = line[wt_pos + len(WEIGHT_FIGHTER): line.find(POUNDS)]
    wt_string = wt_string.strip()

    # get fighter min weight
    light = wt_string.split('/')[1]
    int_light = int(light)

    return int_light


def get_team_id(line):
    """gets the team_id for the first line that has the fighter details"""
    # get record in line

    # !!!!!!!!!!!!! More issues with Contender fighters

    # Really dodgy way to work around this, but will just check if contender, and do a different search.
    # This might mean that contenders get run through twice.  Minimal time impact really.

    if (CONTENDERS_TEXT in line) or (REG_TITLE in line):
        # do check for contenders.  Regional title holder having title fight screws it up too.

        # PM Modified 2017/04/26 after URL changes on site.

        ''' old regex
        regex = re.search('\+team_id=(\d+)&\+command=eko_career_privatebyid&\+competition=eko&\+region=Contenders'
                          '&\+division=Heavy', line)'''
        # New regex
        regex = re.search('\+team_id=(\d+)', line)

    else:
        # find the records, and pull out the results
        '''old regex
        regex = re.search('\+team_id=(\d+)&\+command=eko_control_fighter&\+competition=eko&\+region=Contenders'
                          '&\+division=Heavy', line)'''
        # New regex
        regex = re.search('\+team_id=(\d+)', line)

    team_id = regex.groups()

    team_id = str(team_id[0])

    return team_id

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Retiring Fighters >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def check_retirement(line):
    """Checks the status of fighters.  If current < 2 of status, then retire them"""
    # check if 0(0) - if they are, check for 0-2 record.
    # looks like this:  </B> (0-0-0) 0(0) <BR>

    # line is a line passed through from check weights
    # set as false to begin with
    ret = False

    # results group will be (wins, losses, draws, rating, status)
    results = get_my_fighter_record(line)

    wins = results[0]
    losses = results[1]
    rating = results[3]
    status = results[4]

    # check for 0 status fighter
    # all numbers just hard coded, won't need to change them hardly ever
    if int(status) == 0:
        # think this is automated by webl, but leave it in anyway
        if int(losses) >= 2:
            ret = True
    elif status == '1' and rating == '0':
        if int(wins) - int(losses) < (-2):
            ret = True
    elif status == '2' and rating == '0':
        ret = True
    else:
        if int(status) - int(rating) > 2:
            print(line)
            ret = True

    return ret

def retire_fighter_func():
    pass


# <<<<<<<<<<<<<<<<<<<<<<<<<<<  Creating Fighters >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def create_random_fighters(username, password, base_name, div, rgn, name_count, weight):
    """requires number to append to name to avoid duplicates, and the weight"""
    # create fighter
    # random fighter

    fighter_has_stats = False

    while not fighter_has_stats:
        # modified for python 3 
        # ftype = random.choice(FIGHTER_TYPES.keys())
        ftype = random.choice(list(FIGHTER_TYPES.keys()))

        # get stats of the fighter type from the random type chosen
        getstats = FIGHTER_TYPES[ftype]

        stats = getstats[weight]

        # just check one of the stats - strength.  If it's >0, stats must exist.  If not, do over until we get one
        # that works
        if stats[0] > 0:
            fighter_has_stats = True

    # go through and create fighter stats from dictionary
    strength = stats[0]
    kp = stats[1]
    spd = stats[2]
    agl = stats[3]
    chin = stats[4]
    cond = stats[5]
    hgt = stats[6]
    build = stats[7]
    
    fname = get_name(name_count, ftype, base_name)
    
                                    
    # get cuts.  Cuts always 1
    cuts = 1

    # f_url = create_fighter_URL(username, password, fname, rgn, strength, kp, spd, agl, chin, cond, cuts,
    #                           hgt, build, div)

    # add new URL to list
    # list_URL.append(f_url)
    # add_to_write_list(f_url)

    # add to values list.  Can remove the URL list above if this works
    values = {VAL_USERNAME: username, VAL_PW: password, VAL_COMMAND: COMMAND_CREATE_FIGHTER, VAL_NAME: fname,
              VAL_REGION: rgn, VAL_STR: strength, VAL_KP: kp, VAL_SP: spd, VAL_AGL: agl, VAL_CHIN: chin,
              VAL_CON: cond, VAL_CUT: cuts, VAL_HEIGHT: hgt, VAL_BUILD: build, VAL_DIVISION: div}
                        
    return values

# <<<<<<<<<<<<<<<<<<<<<<<<<<<  Modify data for WeBL config or fighter setup >>>>>>>>>>>>>>>>>>>>>>>>>>>>


def get_name(name_count, ftype, name):
    # enter name for now - later on I will pick from a text file
    # and add a code in there for the fighter types....

    # get the secret code, and concatenate all of the parts of the name
    nickname = SECRET_CODE[ftype]

    # tried to get all new fighters to have a new name.
    # new_name = nickname + " " + name + " " + str(name_count)
    name = get_random_name()
    new_name = nickname + " " + name

    return new_name


#  <<<<<<<<<<<<<<<<<<<<<   Big one.   Fighter Maintenance >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def fighter__maintenance(username, password, long_words, flag):
    """check the weights of the fighters, and move them if I have to"""
    # "http://webl.vivi.com/cgi-bin/query.fcgi?username={$username}&password={$password}&your_team={$name}&division=
    # {$max_divisions[$newdiv]}&+command=eko_change_division&+competition=eko&+region=Contenders
    
    # this is all very messy. really needs tidying up. was messed about as i kept updating things to do
    # needs breaking out into individual functions so I can run training on its own, etc.

    # 19 November 2015 - First go at just having one function, and passing in a flag to see what needs to be done
    # should rationalise a lot of the different code etc.

    # September 2020 - first updgrade to python 3

    fighter_changes = []
    train_ct = 0


    for line in long_words.splitlines():

        # added to python 3 for decoding
        line = line.decode("utf-8")

        # go through lines - check weights and move to correct weight
        max_wt, min_wt, title_name_line = get_line_details(line)

        # have all criteria now
        if WEIGHT_FIGHTER in line:
            # now know have the main line for the fighter
            if REG_TITLE in line:
                # pass through the line saved previously - this is a fighter with a title display
                fname = fighter_name_champ_line(title_name_line)
            else:
                fname = fighter_name_line_long_gym(line)

            """ Right here:  Mods so that if fighter secret code not in the dictionary, then skip everything """

            test = get_secret_code(fname)

            if test in SECRET_CODE.values():
                # So, valid fighter for this program
                fweight = get_fighter_min_wt(line)
                # fighter_count[max_wt] += 1

                # see if fighter needs to be retired
                retire = False

                # ############## RETIREMENT SECTION ###################
                retire = check_retirement(line)

                if retire:
                # create values to call URL to retire fighter
                    url_values = retire_fighter(username, password, line)
                    fighter_changes.append(url_values)

                # ################# WEIGHT CHECK SECTION ##############
                    
                # check if in right division
                # if the right options chosen, and the fighter is not retiring, or retirement is not being checked:
                if not retire:
                    # only broken down tasks so much as I may need to reuse them
                    # change_wt = False
                    change_wt = need_division_change(fweight, min_wt, max_wt)

                    if change_wt:
                        # find best division
                        name = best_division(fweight)

                        # add to list
                        url_values = change_weightURL(username, password, name, fname)
                        fighter_changes.append(url_values)

                # ########### TRAINING SECTION ########
                # do if all gym maintenance, or training is being done.
                if not retire:
                    # call training function - different fighter types train different ways

                    # more testing
                    # if train_ct == 0 or train_ct == 1:

                    # print 'training module about to start'
                    tr1, tr2 = training_module(username, password, fname, line, fweight)
                    # print 'training module done'

                    # got the two training types, so build URL
                    # print 'build url'
                    train_values = create_training_values(username, password, fname, tr1, tr2)

                    # print 'append values'
                    fighter_changes.append(train_values)

                    # if train_ct == 0 or train_ct == 1:
                    # print 'Fighter done, fighters so far: ' + str(train_ct)

                    # track training. feels like stuck in a loop?
                    train_ct += 1

                    if train_ct % 10 == 0:
                        print( str(train_ct) + ' fighters training complete!')

                # ############# CHANGE FP SECTION ##########################
                if not retire:
                    details = change_fp_random(username, password, fname)
                    fighter_changes.append(details)

                    # ######## SUBSECTION OF FP SECTION - BASIC SCOUTING #########
                    # This will be super complicated, so will take ages
                    # plan will be to have dictionaries of match ups anf fps
                    # so KPD_V_CLINCHER = {'HM7': 'name1', 'HM12': 'name2'}
                    # and a set of opponents, flasher, clincher, unknown short arse, etc
                    # will be always ongoing and evolving. and dodgy
                    # but at worst chuck in a random FP

    # make mods to fighters for retire and weight divisions
    # print (fighter_changes)
    if fighter_changes:
        start_updates(fighter_changes)
    else:
        print ("No changes required.")


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Training Modules >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    

def training_module(username, password, fname, line, fweight):
    """created to determine training - will be quite big.  For now, counter punchers will use dictionary
    but KP Dancers will use a formula, with some defined points along the way"""

    # find which abilities to train depending on fighter status, and secret code
    # check if fighter type has training set up in dictionary
    code = get_secret_code(fname)
    
    record = get_my_fighter_record(line)
    status = record[4]
    
    # if code in dictionary this means training in dictionary for each status
    if code in FIGHTER_TRAIN.keys():
        # retrieve which stats to train
        tr1, tr2 = update_training(fname, line)
    else:
        # while WIP, just pass back speed and agility just in case
        tr1 = TRAIN_SPD
        tr2 = TRAIN_AGL
        
        # now do rest of stuff here in the meantime
        
        # #######start of auto training stuff ########
        # get fighter page
        f_page = get_fighter_page(username, password, line)
        
        # get fighter stats
        stats = get_fighter_stats(f_page)
        
        # got fighter stats and code. can now do training per fighter type. 
        # should really go through all keysvalues in dictionary rather than type 'KP Dancer'
        if code == SECRET_CODE[KPD_TEXT]:
            tr1, tr2 = kp_dancer_training(stats, fweight, status)
        elif code == SECRET_CODE[CP_TEXT]:
            tr1, tr2 = counter_puncher_training(stats, status)
        elif code == SECRET_CODE[KPS_TEXT]:
            tr1, tr2 = kp_slugger_training(stats, fweight, status)
        elif code == SECRET_CODE[FCL_TEXT]:
            tr1, tr2 = freak_clincher_training(stats, fweight, status)
        elif code == SECRET_CODE[AGS_TEXT]:
            tr1, tr2 = agile_slugger_training(stats, status)
        else:
            print("Fighter secret code not found for this fighter line :\n" + line)
            tr1 = TRAIN_SPD
            tr2 = TRAIN_AGL
            print("Speed and agility trained, but may want to find the problem.\n")


        # !!!!!!!!!!!!! Check for AP LOSS  !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Put the part here to call a function that checks if the fighter should retire due to AP Loss
        # done solely as this is the only time all fighter pages are opened, so quicker to do it here
        damaged_fighter = check_ap_loss_retire(stats, line, status)

        if damaged_fighter:
            # retire fighter - get values and call webl URL to retire the fighter
            changes = []
            url_values = retire_fighter(username, password, line)
            changes.append(url_values)
            call_url(changes)

        return tr1, tr2


def update_training(fname, line):
    """takes fighter name, gets status and sets next training AP's"""

    # get current status of fighter
    results = get_my_fighter_record(line)
    # words = short_gym_site()
    status = results[4]

    # get first four characters of name to define training type
    secret_code = get_secret_code(fname)

    # get the training dictionary
    train_dict = FIGHTER_TRAIN[secret_code]

    # now have the training dictionary for this fighter type.  Get the training for the relevant status
    status_dict = train_dict[int(status)]
    tr1 = status_dict[0]
    tr2 = status_dict[1]

    return tr1, tr2



#  ################################# Different fighter type training #############################

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! KP Slugger !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def kp_slugger_training(stats, fweight, status):
    """
    KP Slugger training.
    :param stats:
    :param fweight: Currently not used, but kept in for future reference in case I split ratios by weight
    :param status:
    :return:
    """
    # get stats from details passed through
    stren, kp, spd, agl, chin, cond = get_stats(stats)
    status = int(status)

    # get the ratios used later to compare
    spd_to_str = float(spd)/float(stren)
    agl_to_spd = float(agl)/float(spd)

    # set the chin and conditioning for the status
    if status <= KPSLUGGER_STATUS_LOWEST:
        chin_level = KPSLUGGER_CHIN_LOWEST
        cond_level = KPSLUGGER_COND_LOWEST
    elif status <= KPSLUGGER_STATUS_LOW:
        chin_level = KPSLUGGER_CHIN_LOW
        cond_level  = KPSLUGGER_COND_LOW
    elif status <= KPSLUGGER_STATUS_MID:
        chin_level = KPSLUGGER_CHIN_MID
        cond_level = KPSLUGGER_COND_MID
    else:
        chin_level = KPSLUGGER_CHIN_HIGH
        cond_level = KPSLUGGER_COND_HIGH

    # keep KP at max as #1 priority.
    if ((kp * 3) + 2) < stren:
        tr1 = TRAIN_KP

        # get second training in this order of importance
        # STRENGTH
        if spd_to_str > KPSLUGGER_SPD_TO_STR_MAX:
            tr2 = TRAIN_STR
        # If str OK, check speed against str and agility
        elif (spd_to_str < KPSLUGGER_SPD_TO_STR_MIN) or (agl_to_spd > KPSLUGGER_AGL_TO_SPD_MAX):
            tr2 = TRAIN_SPD
        # check agility
        elif agl_to_spd < KPSLUGGER_AGL_TO_SPD_MIN:
            tr2 = TRAIN_AGL
        # check chinnage
        elif chin < chin_level:
            tr2 = TRAIN_CHN
        # check condition
        elif cond_level < cond:
            tr2 = TRAIN_CND
        # By now, everything looks sweet so train strength
        else:
            tr2 = TRAIN_STR

    # KP is OK
    # Get strength back on track if speed has crept up
    elif spd_to_str > KPSLUGGER_SPD_TO_STR_MAX:
        tr1 = TRAIN_STR
        # now for second training - check strength is not super low
        if spd/(stren + 1) > KPSLUGGER_SPD_TO_STR_MAX:
            tr2 = TRAIN_STR
        # Check Speed
        elif (spd_to_str < KPSLUGGER_SPD_TO_STR_MIN) or (agl_to_spd > KPSLUGGER_AGL_TO_SPD_MAX):
            tr2 = TRAIN_SPD
        # check agility
        elif agl_to_spd < KPSLUGGER_AGL_TO_SPD_MIN:
            tr2 = TRAIN_AGL
        # check chinnage
        elif chin < chin_level:
            tr2 = TRAIN_CHN
        # check condition
        elif cond_level < cond:
            tr2 = TRAIN_CND
        # By now, everything looks sweet so train strength
        else:
            tr2 = TRAIN_STR

    # KP Checked and OK.  Strength is also OK
    # Speed check
    elif (spd_to_str < KPSLUGGER_SPD_TO_STR_MIN) or (agl_to_spd > KPSLUGGER_AGL_TO_SPD_MAX):
        tr1 = TRAIN_SPD
        # Secondary stuff.  Have already checked KP and Strength.
        # agility
        if agl_to_spd < KPSLUGGER_AGL_TO_SPD_MIN:
            tr2 = TRAIN_AGL
        # check chinnage
        elif chin < chin_level:
            tr2 = TRAIN_CHN
        # check condition
        elif cond_level < cond:
            tr2 = TRAIN_CND
        # By now, everything looks sweet so train strength
        else:
            tr2 = TRAIN_STR

    # KP, STR, SPD all OK.  Go Agility
    elif agl_to_spd < KPSLUGGER_AGL_TO_SPD_MIN:
        tr1 = TRAIN_AGL
        # not much secondary to check now
        if chin < chin_level:
            tr2 = TRAIN_CHN
        # check condition
        elif cond_level < cond:
            tr2 = TRAIN_CND
        # By now, everything looks sweet so train strength
        else:
            tr2 = TRAIN_STR
    # now getting down to the end.  If all stats line up, just check chin, then cond.  Will probably get some random
    # stats by now, so will be OK anyway I would think.

    elif chin < chin_level:
        tr1 = TRAIN_CHN
        # check condition for secondary
        if cond_level < cond:
            tr2 = TRAIN_CND
        else:
            tr2 = TRAIN_STR
    elif cond_level < cond:
        tr1 = TRAIN_CND
        # all else good, so hit strength
        tr2 = TRAIN_STR
    else:
        # got right to the end now.
        # Everything lines up.  So push both training stats to strength then speed.
        tr1 = TRAIN_STR
        tr2 = TRAIN_SPD

    return tr1, tr2


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  Freak Clincher !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def freak_clincher_training(stats, fweight, status):
    """
    Training for freak clinchers.

    :param stats:  All the fighter AP's
    :param fweight:  currently not used.  Same ratio held throughout all weights, but will keep in case I change
    that at a later date
    :param status: status of fighter.  Used to check different levels
    :return:


    Ubers weights

    status 0
    str 32   KP 0
    spd 13 agl 1
    chn 10 cnd 14

    spd to str = 0.40625

    status 6
    str 37   KP 0
    spd 14 agl 1
    chn 10 cnd 15

    spd to str = 0.3783783783783784

     status 12
    str 40   KP 0
    spd 18 agl 1
    chn 11 cnd 16

    spd to str = 0.45

    status 18
    str 46   KP 0
    spd 20 agl 1
    chn 11 cnd 17

    spd to str ratio = 0.4347826086956522

     status 24
    str 52   KP 0
    spd 21 agl 1
    chn 11 cnd 19

    spd to str ratio = 0.4038461538461538

    status 28
    str 55   KP 0
    spd 22 agl 1
    chn 12 cnd 19

    spd to str ratio = 0.4


    """
    # get stats from details passed through
    stren, kp, spd, agl, chin, cond = get_stats(stats)
    status = int(status)

    # get desired stats and ratio based on current status
    if status <= FREAKCLINCH_STATUS_LOWEST:
        spd_to_str = FREAKCLINCH_SPD_TO_STR_LOWEST
        chin_level = FREAKCLINCH_CHIN_LOWEST
        cond_level = FREAKCLINCH_COND_LOWEST

    elif status <= FREAKCLINCH_STATUS_LOW:
        spd_to_str = FREAKCLINCH_SPD_TO_STR_LOW
        chin_level = FREAKCLINCH_CHIN_LOW
        cond_level = FREAKCLINCH_COND_LOW

    elif status <= FREAKCLINCH_STATUS_MID:
        spd_to_str = FREAKCLINCH_SPD_TO_STR_MID
        chin_level = FREAKCLINCH_CHIN_MID
        cond_level = FREAKCLINCH_CHIN_MID

    elif status <= FREAKCLINCH_STATUS_HIGH:
        spd_to_str = FREAKCLINCH_SPD_TO_STR_HIGH
        chin_level = FREAKCLINCH_CHIN_HIGH
        cond_level = FREAKCLINCH_COND_HIGH

    # if haven't triggered yet, must be higher than top level stated (24 at creation of function)
    else:
        spd_to_str = FREAKCLINCH_SPD_TO_STR_HIGHEST
        chin_level = FREAKCLINCH_CHIN_HIGHEST
        cond_level = FREAKCLINCH_COND_HIGHEST

    spd_ratio = float(stren) / float(agl)

    # Most important thing, spd to str ratio
    # need to define tr1, tr2
    # Never need to check agility or KP, as KP always 0, agility best as 1
    if spd_ratio < spd_to_str:
        tr1 = TRAIN_SPD
    # check chin next.  Rarely will need training
    elif chin < chin_level:
        tr1 = TRAIN_CHN
    # check cond next.  Also, will rarely need changing
    elif cond < cond_level:
        tr1 = TRAIN_CND
    else:
        # here we go. Strength!!!
        tr1 = TRAIN_STR

    # Secondary Training.
    # speed dealt with first, so need to look at that.
    # check chin.  Doesn't need training much
    if chin < chin_level:
        tr2 = TRAIN_CHN
    # check cond next.  Also, will rarely need changing
    elif cond < cond_level:
        tr2 = TRAIN_CND
    else:
        # here we go. Strength!!!
        tr2 = TRAIN_STR

    # should be it I think?  Quite simple, as strength and speed really all that matter to this fighter

    return tr1, tr2


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  KP Dancer training  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def kp_dancer_training(stats, fweight, status):
    """set up kp dancer training. hopefully wont be complicated as all hell"""

    """

    KP DANCER

    Ideal stats:

    STR is from 0,5*AGL to 0,6*AGL
    SPD = AGL
    CHN is about 11-12
    CND is 14 at 0(0) and 17-18 at 28(28)
    KP=1/3*STR (max)
    CR=1
    very light build
    Competitive subspecies:

    KP Counterpuncher (faster fighter than usual KP Dancer):

    STR is from 0,6*AGL to 0,7*AGL
    SPD is from 1,2*AGL to 1,3*AGL
    CHN is about 11-12
    CND is 14 at 0(0) and 17-18 at 28(28)
    KP=1/3*STR (max)
    CR=1
    very light build
    """

    # get stats from details passed through
    stren, kp, spd, agl, chin, cond = get_stats(stats)
    status = int(status)

    # set some priorities

    # get str to agility ratio
    # 0.5 for over 135, 0.55 for 135 and under - taken from variables
    str_ratio = float(stren) / float(agl)

    # train kp to max as most important. probably isn't really but is a safe start
    if ((kp * 3) + 2) < stren:
        tr1 = TRAIN_KP

        # get second training in this order of importance
        # SPEED
        if spd < agl:
            tr2 = TRAIN_SPD
        # STRENGTH
        elif (fweight <= KP_DANCER_LIGHT and str_ratio < KPD_STR_RATIO_LIGHT) \
                or (fweight > KP_DANCER_LIGHT and str_ratio < KPD_STR_RATIO_HEAVY):
            tr2 = TRAIN_STR
        # else agility
        else:
            tr2 = TRAIN_AGL

    # now assume kp is ok.
    # SPEED second most important for KP Dancer
    elif spd < agl:
        # train it!
        tr1 = TRAIN_SPD
        # second priority
        if (fweight <= KP_DANCER_LIGHT and str_ratio < KPD_STR_RATIO_LIGHT) \
                or (fweight > KP_DANCER_LIGHT and str_ratio < KPD_STR_RATIO_HEAVY):
            tr2 = TRAIN_STR
        # else agility
        else:
            tr2 = TRAIN_AGL

    # ok, now check chin - NEED TO ADD VARIABLES HERE
    elif (status >= 15) and (chin < 11):
        # seems like a bug here, so printing to find out what the issue is
        # print 'Weight: ' + str(fweight) + ' Status: ' + str(status) + ' Chin: ' +
        # str(chin) + " Str: " + str(stren) + " Cond: " + str(cond)
        # print 'type chin = ' + str(type(chin)) + 'type status. ' + str(type(status))
        tr1 = TRAIN_CHN
        # KP and speed already tested and ok, so lets just go agility
        tr2 = TRAIN_AGL

    # conditioning check - bit primitive.
    elif (cond < 15) and (status >= 15):
        # train conditioning
        tr1 = TRAIN_CND
        # good old agility
        tr2 = TRAIN_AGL

    # leaves us with strength to test
    elif (fweight <= KP_DANCER_LIGHT and str_ratio < KPD_STR_RATIO_LIGHT) \
            or (fweight > KP_DANCER_LIGHT and str_ratio < KPD_STR_RATIO_HEAVY):
        # strength too low.
        tr1 = TRAIN_STR

        # check if this will leave kp too low
        # +1 -2 left in just so i can follow logic
        if ((float(stren) + 1 - 2) / float(kp)) > 3:
            tr2 = TRAIN_KP
        else:
            # old chestnut
            tr2 = TRAIN_AGL

    # I think that's everything??
    else:
        # speed and strength ok. chins etc ok. so time to push up agility
        # OR TESTS ARE SCREWED!!!!!!!!! In which case, agility is ok
        tr1 = TRAIN_AGL
        # not sure really now. build all ok. push up speed unless its super high
        if spd <= 26:
            tr2 = TRAIN_SPD
        else:
            tr2 = TRAIN_AGL

    return tr1, tr2


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!     counter puncher    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def counter_puncher_training(stats, status):
    """ As it says.  counter puncher training
    
    COUNTERPUNCHER 

    Ideal stats: 

    AGL is about 0,8*SPD 
    STR is about 0,6*SPD 
    CHN is about 10-12 
    CND is 14 at 0(0) and 17-18 at 28(28). 
    KP=0. 
    CR=1. 
    very light build.

    Modified to take into account changing requirements for counterpuncher in contenders


    """

    # get the fighter stats, and into integer format
    stren, kp, spd, agl, chin, cond = get_stats(stats)
    status = int(status)

    # check if contender or not
    if status < 18:
        # set up as non contender fighter
        agl_to_spd = COUNTER_AGL_TO_SPD
        agl_to_spd_vlow = COUNTER_AGL_TO_SPD_VRY_LOW
        str_to_spd = COUNTER_STR_TO_SPD
    else:
        agl_to_spd = COUNTER_CONT_AGL_TO_SPEED
        agl_to_spd_vlow = COUNTER_CONT_AGL_TO_SPD_VRY_LOW
        str_to_spd = COUNTER_CONT_STR_TO_SPD

    # no KP to worry about.
    # get agility to speed sorted first
    
    if (agl / spd) < agl_to_spd:
        # agility bit low. raise it
        tr1 = TRAIN_AGL
        
        # second training
        if (agl / spd) < agl_to_spd_vlow:
            # super low
            tr2 = TRAIN_AGL
        elif (stren / spd) < str_to_spd:
            # strength bit low
            tr2 = TRAIN_STR
        elif (chin < 11) and (status >= 15):
            # chin bit low
            tr2 = TRAIN_CHN
        elif (cond < 16) and (status >= 15):
            # whack on some conditioning
            tr2 = TRAIN_CND
        else: 
            # train speed if everything else ok
            tr2 = TRAIN_SPD
            
    # if here, agility is ok, so let's check strength
    elif (stren / spd) < str_to_spd:
        # strength a bit low
        tr1 = TRAIN_STR
        
        # now what???? Agility must be ok.
        # check if super low
        if ((stren + 1) / spd) < str_to_spd:
            tr2 = TRAIN_STR
        elif (chin < 11) and (status >= 15):
            # chin bit low
            tr2 = TRAIN_CHN
        elif (cond < 16) and (status >= 15):
            # whack on some conditioning
            tr2 = TRAIN_CND
        else: 
            # train speed if everything else ok
            tr2 = TRAIN_SPD
            
    # agility and strength ok if here, so chin and cond in that order
    elif (chin < 11) and (status >= 15):
        tr1 = TRAIN_CHN
        
        if (cond < 16) and (status >= 15):
            tr2 = TRAIN_CND
        else: 
            tr2 = TRAIN_SPD
            
    # COND NOW
    elif (cond < 16) and (status >= 15):
        tr1 = TRAIN_CND
        tr2 = TRAIN_SPD
        
    # SPEED
    else: 
        tr1 = TRAIN_SPD
        
        if spd > 25:
            # SET MAX FOR SPEED VALUE
            tr2 = TRAIN_AGL
        else: 
            tr2 = TRAIN_SPD
        
    return tr1, tr2


# !!!!!!!!!!!!!!!!!!!!!!!!!!  Agile Sluggers  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def agile_slugger_training(stats, status):
    """

    :param stats:
    :param status:
    :return:


    For an Agile slugger you might want to try:

    STR = AGL
    SPD = .8*AGL

    Chins again start at 10 and move to 11 or 12 by 28/28. Same CND as above.
    I almost always start at 14 with the aim of ending at 17.

    """

    # get the fighter stats, and into integer format
    stren, kp, spd, agl, chin, cond = get_stats(stats)
    status = int(status)

    if status <= AGSLUGGER_STATUS_LOWEST:
        chin_level = AGSLUGGER_CHIN_LOWEST
        cond_level = AGSLUGGER_COND_LOW
    elif status <= AGSLUGGER_STATUS_LOW:
        chin_level = AGSLUGGER_CHIN_LOW
        cond_level = AGSLUGGER_COND_LOW
    elif status <= AGSLUGGER_STATUS_MID:
        chin_level = AGSLUGGER_CHIN_MID
        cond_level = AGSLUGGER_COND_MID
    else:
        chin_level = AGSLUGGER_CHIN_HIGH
        cond_level = AGSLUGGER_COND_HIGH

    # calculate the ratios first
    agl_to_str = float(agl)/float(stren)
    spd_to_agl = float(spd)/float(agl)

    # check strength first
    if agl_to_str > AGSLUGGER_AGL_TO_STR:
        tr1 = TRAIN_STR
        # secondary training.  Agility must be too high, so don't train it just to boost it up again.
        # no kp to worry about either
        if spd_to_agl < AGSLUGGER_SPD_TO_AGL:
            tr2 = TRAIN_SPD
        elif chin < chin_level:
            tr2 = TRAIN_CHN
        elif cond < cond_level:
            tr2 = TRAIN_CND
        else:
            # everything looks good so far. So, let's boost up strength
            tr2 = TRAIN_STR
    # check agility to strength
    elif agl_to_str < AGSLUGGER_AGL_TO_STR:
        # agility too slow, so train it up
        tr1 = TRAIN_AGL
        # as with the strength - if this is too low, then doesn't make sense to train strength
        if chin < chin_level:
            tr2 = TRAIN_CHN
        elif cond < cond_level:
            tr2 = TRAIN_CND
        else:
            # everything looks good so far. So, let's boost up agility again
            tr2 = TRAIN_AGL
    # strength and agility ok - so let's check chin
    elif chin < chin_level:
        tr1 = TRAIN_CHN
        if cond < cond_level:
            tr2 = TRAIN_CND
        else:
            # back it up with strength
            tr2 = TRAIN_STR
    elif cond < cond_level:
        tr1 = TRAIN_CND
        tr2 = TRAIN_STR
    else:
        # got to here, everything is good.  So do strength, then agility to keep ratio in check
        tr1 = TRAIN_STR
        tr2 = TRAIN_AGL

    return tr1, tr2


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Checking fighter details >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def height_to_webl_int(feet, inch):
    """converts feet and inches to number to post to webl"""
    
    if feet == 4:
        calc = -12
    elif feet == 5:
        calc = 0
    elif feet == 6:
        calc = 12
    # must be 7 foot
    else:
        calc = 24

    calc += inch
    
    return calc


def check_ap_loss_retire(stats, line, status):
    """

    :param stats: fighter stats  including ap loss
    :param line: line with fighter name on it
    :return: boolean whether or not to retire
    """
    ap_loss = stats[TRAIN_AP_LOSS]
    retire_him = False
    status = int(status)

    # check against regional (lowest status) AP loss
    if (status <= RETIRE_REG_STATUS) and (ap_loss >= RETIRE_AP_LOSS_REG):
        # lower status fighter - retire him
        retire_him = True
    elif ap_loss >= RETIRE_AP_LOSS_ANY:
        retire_him = True
    elif status > 8:
        retire_him = True

    return retire_him



def get_stats(stats):
    """
    returns fighter stats from details passed through.  Used rather than repeating for all different fighter types.

    :param stats:
    :return: all the different stats

    """
    stren = stats[TRAIN_STR]
    stren = float(stren)
    kp = stats[TRAIN_KP]
    kp = float(kp)
    spd = stats[TRAIN_SPD]
    spd = float(spd)
    agl = stats[TRAIN_AGL]
    agl = float(agl)
    chin = stats[TRAIN_CHN]
    chin = float(chin)
    cond = stats[TRAIN_CND]
    cond = float(cond)

    return stren, kp, spd, agl, chin, cond


def get_fighter_stats(f_page):
    """gets fighter stats from the fighter page"""
    # fighter page full of html passed through

    # count of gathered stats.  Once have them all, drop out of the loop and stop iterating through lines
    count = 0

    f_stats = {}

    # do while less than number of stats to gather
    while count < 8:

        for line in f_page.splitlines():
            # check for each of the stats

            line = line.decode("utf-8")

            # Strength
            if STATS_STRENGTH in line:
                regex = re.search(STATS_STRENGTH + '(\d+)' + BREAK, line)
                strength = regex.groups()
                stren = int(strength[0])
                f_stats[TRAIN_STR] = stren
                count += 1

            # KP
            if STATS_KP in line:
                regex = re.search(STATS_KP + '(\d+)' + BREAK, line)
                kaypee = regex.groups()
                kp = int(kaypee[0])
                f_stats[TRAIN_KP] = kp
                count += 1

            # speed
            if STATS_SPEED in line:
                regex = re.search(STATS_SPEED + '(\d+)' + BREAK, line)
                spd = regex.groups()
                speed = int(spd[0])
                f_stats[TRAIN_SPD] = speed
                count += 1

            # agility
            if STATS_AGL in line:
                regex = re.search(STATS_AGL + '(\d+)' + BREAK, line)
                agl = regex.groups()
                agil = int(agl[0])
                f_stats[TRAIN_AGL] = agil
                count += 1

            # chin
            if STATS_CHN in line:
                regex = re.search(STATS_CHN + '(\d+)' + BREAK, line)
                chn = regex.groups()
                chin = int(chn[0])
                f_stats[TRAIN_CHN] = chin
                count += 1

            # cond
            if STATS_CND in line:
                regex = re.search(STATS_CND + '(\d+)' + BREAK, line)
                cnd = regex.groups()
                cond = int(cnd[0])
                f_stats[TRAIN_CND] = cond
                count += 1

            # height
            if STATS_HEIGHT in line:
                # find in line
                pos = line.find(STATS_HEIGHT)
                eol = len(line)

                hgt = line[pos + len(STATS_HEIGHT): eol]

                # now got height string
                height = parse_my_height_to_int(hgt)
                count += 1

                f_stats[TRAIN_HGT] = height

            # AP Loss
            if AP_LOSS in line:
                # find how many AP Loss if any
                pos = line.find(AP_LOSS)
                eol = len(line)

                apl = line[pos + len(AP_LOSS): eol]

                # get the string
                ap_loss = int(apl)

                count += 1
                f_stats[TRAIN_AP_LOSS] = ap_loss

    return f_stats


def parse_my_height_to_int(hgt):
    """gets the fighter height from a string like '6 feet 6 inches' """
    # feet always at the start, always 4, 5, 6 or 7
    feet = int(hgt[0])

    # know the height always starts with x feet
    rest_string = hgt[7:]

    inches = ''
    found = False
    for x in rest_string:
        # add until we know it's the end of height
        if (x != ' ') and (x != '(') and not found:
            inches += x
        else:
            found = True

    if inches == '':
        inch = 0
    else:
        inch = int(inches)

    calc = height_to_webl_int(feet, inch)
    
    return calc
    

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Fight Plan Stuff >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def change_fp_random(username, password, fighter):
    """
    :param fname: name of fighter
    :return: returns the fight plan for the fighter to use, randomly selected based on the fighter secret code
    """

    z = get_secret_code(fighter)
    # PLAN_DICT = {KPD_CODE: HM_PLANS, COUNTER_CODE: LO_PLANS, KPS_CODE: KPS_PLANS,
    # FCL_CODE: FCL_PLANS, AGS_CODE: AGS_PLANS}

    err = False
    # new, more elegant attempt rather than huge if....  eliminates need to add to if, just add to plan dictionary
    try:
        fplans = PLAN_DICT[z]
        plan = random.choice(fplans)
    except KeyError:
        print(' Whoops.  Secret code ' + z + ' doesn\'t seem to be able to be found in FP\'s.  Best check it out')
        # Give them traffords feint plan just to keep the program ticking over.
        # Updated: When brought in graduated, removed this part where plan given.  Just ignored, and left as is.
        # plan = "LO1"
        err = True

    """
    if z == KPD_CODE:
        # KP Dancer, choose the relevant FP
        plan = random.choice(HM_PLANS)
    elif z == COUNTER_CODE:
        # counter stuff
        plan = random.choice(LO_PLANS)
    elif z == KPS_CODE:
        # KP Slugger code
        plan = random.choice(KPS_PLANS)
    elif z == FCL_CODE:
        # Freak Clincher Code
        plan = random.choice(FCL_PLANS)
    elif z == AGS_CODE:
        # agile clincher
        plan = random.choice(AGS_PLANS)
    else:
        # dunno what's going on here - in case of error, just give them traffords plan
        plan = 'LO1'
    """
    if not err:
        details = create_change_fp_url(username, password, fighter, plan)

    return details

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  Modifying existing fighters >>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def need_division_change(fweight, min_wt, max_wt):
    """check to see if fighter not in optimum weight class"""

    change_weight = False 
    # name = 'will change anyway'
    
    if fweight not in range(min_wt, max_wt + 1):
        # need to change weight class
        change_weight = True

    return change_weight   



def best_division(fweight):
    """takes fighter weights and chooses lowest feasible weight class.
    may screw around fighters with missing rankings but i'll live with it for now"""
    # set a check to false
    right_weight = False
    name = ''

    while not right_weight:
        for w in WEIGHT_DIVISIONS:
            new_dict = WEIGHT_DIVISIONS[w]
            high = new_dict['max']
            low = new_dict['min']
            if fweight in range(low, high + 1):
                # have the correct weight class now
                name = new_dict['name']
        
                right_weight = True
                break

    return name



# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   Main Module   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def main():
    # get username and password
    # username = get_username()
    # password = get_pw()
    username = USERNAME
    password = PASSWORD


    # ########For now, I will just make 6 fighters per region in each weight class
    # ########regardless of how many currently exist.
    # ########in the future, I need to retire fighters - check how many currently exist etc
    # ########by reading the html page from the site, put into a text file
    # ########the weights to choose can be done by changing the weight classes dictionary
    
    # in theory, this should just work
    # get website
    long_words = get_site_page(username, password, COMMAND_MAIN_GYM)

    # do fighter maintenance - retire shitty fighters
    choice = MENU_ALL
    fighter__maintenance(username, password, long_words, choice)

    # Took out of fighter maintenance.  If fighters are updated, should then run fighter maintenance,
    # but only with the flag  to do training and FPs, as new fighters won't have fp or training et
    update_fighter_numbers(username, password)


if __name__ == "__main__":
    main()