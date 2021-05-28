import random
# import webbrowser
import time
# from typing import type_check_only
import urllib
import urllib.request
import urllib.parse
import re
import math



"""This script manages an autogym"""

# #################################  ONLY CHANGE THE STUFF IN HERE####################################
# Sets up number of fighters per weight - just edit to change.  This number of fighters will be created for each
# region entered into WEBL regions
FIGHTERS_PER_WEIGHT = 6
# FIGHTERS_PER_WEIGHT = 1
# FIGHTERS_PER_WEIGHT = 4

# Username and Password
# UN and PW - Elektrik Church
USERNAME = 'hongkongphooey'
PASSWORD = 'wisofu48'
VALUES_LIST = []

'''
# Username and Password - Dogs Bawls
USERNAME = 'sandman_thedog'
PASSWORD = 'wisofu48'
'''




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
HM_PLANS = ["HM1", "HM2", "HM3", "HM4", "HM5", "HM6", "HM7"]
# LO Plans - counter puncher plans, used by guys with LO in their name
LO_PLANS = ["LO1", "LO2", "LO3", "LO4", "LO5"]
# SB plans - KP Slugger plans.
KPS_PLANS = ["DT1", "DT2", "DT3", "DT4", "DT5"]
# JR plans - Freak Clincher plans
FCL_PLANS = ["JR1", "JR2", "JR3", "JR4", "JR5", "JR6", "JR7"]
# Agile slugger plans
AGS_PLANS = ["RD1", "RD2", "RD3", "RD4"]

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

#Home region change
REGIONS = {'Eurasia': '0'}
# REGIONS ={'British Commonwealth': 0}

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
# TODO check if this is the same for EC????
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

#Values for Random naming inside the game
NICKNAMES = ['Hitman', 'Tuaminator', 'Pillow Fists', 'MotherDucker', 'Wet Noodle', 'Hands of Clay', 'Leadfoot', 'Mildly Dangerous',
            'Glass Jaw', 'Hillbilly', 'BBQ', 'Wet Blanket', 'Teacup', 'Bronze', 'Tin Man', 'Low Blow', 'Headbutt', 'Pussy Cat', 'Ridonkulous',
            'HGH', 'Axe', 'Fire Department', 'No Trace', 'Gimp', '1st Degree Burn', 'Not Guilty', 'No Comment', 'Hung Jury', 'Banana Skin',
            'The Prosecutor', 'Noodle Legs', 'Infinity', 'Teleporter', 'Mediocre', 'Mustard', 'Ketchup', 'Rock Salt', 'Deep Fried',
            'Pot Noodle', 'Fliphone']

FIRST_NAME = {'Liam' ,'Noah' ,'Oliver' ,'William' ,'Elijah' ,'James' ,'Benjamin' ,'Lucas' ,'Mason' ,'Ethan' ,'Alexander' ,'Henry' ,'Jacob' ,'Michael' 
                ,'Daniel' ,'Logan' ,'Jackson' ,'Sebastian' ,'Jack' ,'Aiden' ,'Owen' ,'Samuel' ,'Matthew' ,'Joseph' ,'Levi' ,'Mateo' ,'David' 
                ,'John' ,'Wyatt' ,'Carter' ,'Julian' ,'Luke' ,'Grayson' ,'Isaac' ,'Jayden' ,'Theodore' ,'Gabriel' ,'Anthony' ,'Dylan' ,'Leo' 
                ,'Lincoln' ,'Jaxon' ,'Asher' ,'Christopher' ,'Josiah' ,'Andrew' ,'Thomas' ,'Joshua' ,'Ezra' ,'Hudson' ,'Charles' ,'Caleb' 
                ,'Isaiah' ,'Ryan' ,'Nathan' ,'Adrian' ,'Christian' ,'Maverick' ,'Colton' ,'Elias' ,'Aaron' ,'Eli' ,'Landon' ,'Jonathan' 
                ,'Nolan' ,'Hunter' ,'Cameron' ,'Connor' ,'Santiago' ,'Jeremiah' ,'Ezekiel' ,'Angel' ,'Roman' ,'Easton' ,'Miles' ,'Robert' 
                ,'Jameson' ,'Nicholas' ,'Greyson' ,'Cooper' ,'Ian' ,'Carson' ,'Axel' ,'Jaxson' ,'Dominic' ,'Leonardo' ,'Luca' ,'Austin' 
                ,'Jordan' ,'Adam' ,'Xavier' ,'Jose' ,'Jace' ,'Everett' ,'Declan' ,'Evan' ,'Kayden' ,'Parker' ,'Wesley' ,'Kai' ,'Brayden' 
                ,'Bryson' ,'Weston' ,'Jason' ,'Emmett' ,'Sawyer' ,'Silas' ,'Bennett' ,'Brooks' ,'Micah' ,'Damian' ,'Harrison' ,'Waylon' 
                ,'Ayden' ,'Vincent' ,'Ryder' ,'Kingston' ,'Rowan' ,'George' ,'Luis' ,'Chase' ,'Cole' ,'Nathaniel' ,'Zachary' ,'Ashton' 
                ,'Braxton' ,'Gavin' ,'Tyler' ,'Diego' ,'Bentley' ,'Amir' ,'Beau' ,'Gael' ,'Carlos' ,'Ryker' ,'Jasper' ,'Max' ,'Juan' ,'Ivan' 
                ,'Brandon' ,'Jonah' ,'Giovanni' ,'Kaiden' ,'Myles' ,'Calvin' ,'Lorenzo' ,'Maxwell' ,'Jayce' ,'Kevin' ,'Legend' ,'Tristan' 
                ,'Jesus' ,'Jude' ,'Zion' ,'Justin' ,'Maddox' ,'Abel' ,'King' ,'Camden' ,'Elliott' ,'Malachi' ,'Milo' ,'Emmanuel' ,'Karter' 
                ,'Rhett' ,'Alex' ,'August' ,'River' ,'Xander' ,'Antonio' ,'Brody' ,'Finn' ,'Elliot' ,'Dean' ,'Emiliano' ,'Eric' ,'Miguel' 
                ,'Arthur' ,'Matteo' ,'Graham' ,'Alan' ,'Nicolas' ,'Blake' ,'Thiago' ,'Adriel' ,'Victor' ,'Joel' ,'Timothy' ,'Hayden' ,'Judah' 
                ,'Abraham' ,'Edward' ,'Messiah' ,'Zayden' ,'Theo' ,'Tucker' ,'Grant' ,'Richard' ,'Alejandro' ,'Steven' ,'Jesse' ,'Dawson' 
                ,'Bryce' ,'Avery' ,'Oscar' ,'Patrick' ,'Archer' ,'Barrett' ,'Leon' ,'Colt' ,'Charlie' ,'Peter' ,'Kaleb' ,'Lukas' ,'Beckett' 
                ,'Jeremy' ,'Preston' ,'Enzo' ,'Luka' ,'Andres' ,'Marcus' ,'Felix' ,'Mark' ,'Ace' ,'Brantley' ,'Atlas' ,'Remington' ,'Maximus' 
                ,'Matias' ,'Walker' ,'Kyrie' ,'Griffin' ,'Kenneth' ,'Israel' ,'Javier' ,'Kyler' ,'Jax' ,'Amari' ,'Zane' ,'Emilio' ,'Knox' 
                ,'Adonis' ,'Aidan' ,'Kaden' ,'Paul' ,'Omar' ,'Brian' ,'Louis' ,'Caden' ,'Maximiliano' ,'Holden' ,'Paxton' ,'Nash' ,'Bradley' 
                ,'Bryan' ,'Simon' ,'Phoenix' ,'Lane' ,'Josue' ,'Colin' ,'Rafael' ,'Kyle' ,'Riley' ,'Jorge' ,'Beckham' ,'Cayden' ,'Jaden' 
                ,'Emerson' ,'Ronan' ,'Karson' ,'Arlo' ,'Tobias' ,'Brady' ,'Clayton' ,'Francisco' ,'Zander' ,'Erick' ,'Walter' ,'Daxton' ,'Cash' 
                ,'Martin' ,'Damien' ,'Dallas' ,'Cody' ,'Chance' ,'Jensen' ,'Finley' ,'Jett' ,'Corbin' ,'Kash' ,'Reid' ,'Kameron' ,'Andre' 
                ,'Gunner' ,'Jake' ,'Hayes' ,'Manuel' ,'Prince' ,'Bodhi' ,'Cohen' ,'Sean' ,'Khalil' ,'Hendrix' ,'Derek' ,'Cristian' ,'Cruz' 
                ,'Kairo' ,'Dante' ,'Atticus' ,'Killian' ,'Stephen' ,'Orion' ,'Malakai' ,'Ali' ,'Eduardo' ,'Fernando' ,'Anderson' ,'Angelo' 
                ,'Spencer' ,'Gideon' ,'Mario' ,'Titus' ,'Travis' ,'Rylan' ,'Kayson' ,'Ricardo' ,'Tanner' ,'Malcolm' ,'Raymond' ,'Odin' ,'Cesar' 
                ,'Lennox' ,'Joaquin' ,'Kane' ,'Wade' ,'Muhammad' ,'Iker' ,'Jaylen' ,'Crew' ,'Zayn' ,'Hector' ,'Ellis' ,'Leonel' ,'Cairo' 
                ,'Garrett' ,'Romeo' ,'Dakota' ,'Edwin' ,'Warren' ,'Julius' ,'Major' ,'Donovan' ,'Caiden' ,'Tyson' ,'Nico' ,'Sergio' ,'Nasir' 
                ,'Rory' ,'Devin' ,'Jaiden' ,'Jared' ,'Kason' ,'Malik' ,'Jeffrey' ,'Ismael' ,'Elian' ,'Marshall' ,'Lawson' ,'Desmond' ,'Winston' 
                ,'Nehemiah' ,'Ari' ,'Conner' ,'Jay' ,'Kade' ,'Andy' ,'Johnny' ,'Jayceon' ,'Marco' ,'Seth' ,'Ibrahim' ,'Raiden' ,'Collin' ,'Edgar' 
                ,'Erik' ,'Troy' ,'Clark' ,'Jaxton' ,'Johnathan' ,'Gregory' ,'Russell' ,'Royce' ,'Fabian' ,'Ezequiel' ,'Noel' ,'Pablo' ,'Cade' 
                ,'Pedro' ,'Sullivan' ,'Trevor' ,'Reed' ,'Quinn' ,'Frank' ,'Harvey' ,'Princeton' ,'Zayne' ,'Matthias' ,'Conor' ,'Sterling' ,'Dax' 
                ,'Grady' ,'Cyrus' ,'Gage' ,'Leland' ,'Solomon' ,'Emanuel' ,'Niko' ,'Ruben' ,'Kasen' ,'Mathias' ,'Kashton' ,'Franklin' ,'Remy' 
                ,'Shane' ,'Kendrick' ,'Shawn' ,'Otto' ,'Armani' ,'Keegan' ,'Finnegan' ,'Memphis' ,'Bowen' ,'Dominick' ,'Kolton' ,'Jamison' 
                ,'Allen' ,'Philip' ,'Tate' ,'Peyton' ,'Jase' ,'Oakley' ,'Rhys' ,'Kyson' ,'Adan' ,'Esteban' ,'Dalton' ,'Gianni' ,'Callum' ,'Sage' 
                ,'Alexis' ,'Milan' ,'Moises' ,'Jonas' ,'Uriel' ,'Colson' ,'Marcos' ,'Zaiden' ,'Hank' ,'Damon' ,'Hugo' ,'Ronin' ,'Royal' ,'Kamden' 
                ,'Dexter' ,'Luciano' ,'Alonzo' ,'Augustus' ,'Kamari' ,'Eden' ,'Roberto' ,'Baker' ,'Bruce' ,'Kian' ,'Albert' ,'Frederick' ,'Mohamed' 
                ,'Abram' ,'Omari' ,'Porter' ,'Enrique' ,'Alijah' ,'Francis' ,'Leonidas' ,'Zachariah' ,'Landen' ,'Wilder' ,'Apollo' ,'Santino' ,'Tatum' ,'Pierce' 
                ,'Forrest' ,'Corey' ,'Derrick' ,'Isaias' ,'Kaison' ,'Kieran' ,'Arjun' ,'Gunnar' ,'Rocco' ,'Emmitt' ,'Abdiel' ,'Braylen' ,'Maximilian' 
                ,'Skyler' ,'Phillip' ,'Benson' ,'Cannon' ,'Deacon' ,'Dorian' ,'Asa' ,'Moses' ,'Ayaan' ,'Jayson' ,'Raul' ,'Briggs' ,'Armando' ,'Nikolai' 
                ,'Cassius' ,'Drew' ,'Rodrigo' ,'Raphael' ,'Danny' ,'Conrad' ,'Moshe' ,'Zyaire' ,'Julio' ,'Casey' ,'Ronald' ,'Scott' ,'Callan' ,'Roland' 
                ,'Saul' ,'Jalen' ,'Brycen' ,'Ryland' ,'Lawrence' ,'Davis' ,'Rowen' ,'Zain' ,'Ermias' ,'Jaime' ,'Duke' ,'Stetson' ,'Alec' ,'Yusuf' ,'Case' 
                ,'Trenton' ,'Callen' ,'Ariel' ,'Jasiah' ,'Soren' ,'Dennis' ,'Donald' ,'Keith' ,'Izaiah' ,'Lewis' ,'Kylan' ,'Kobe' ,'Makai' ,'Rayan' ,'Ford' 
                ,'Zaire' ,'Landyn' ,'Roy' ,'Bo' ,'Chris' ,'Jamari' ,'Ares' ,'Mohammad' ,'Darius' ,'Drake' ,'Tripp' ,'Marcelo' ,'Samson' ,'Dustin' ,'Layton' 
                ,'Gerardo' ,'Johan' ,'Kaysen' ,'Keaton' ,'Reece' ,'Chandler' ,'Lucca' ,'Mack' ,'Baylor' ,'Kannon' ,'Marvin' ,'Huxley' ,'Nixon' ,'Tony' 
                ,'Cason' ,'Mauricio' ,'Quentin' ,'Edison' ,'Quincy' ,'Ahmed' ,'Finnley' ,'Justice' ,'Taylor' ,'Gustavo' ,'Brock' ,'Ahmad' ,'Kyree' ,'Arturo' 
                ,'Nikolas' ,'Boston' ,'Sincere' ,'Alessandro' ,'Braylon' ,'Colby' ,'Leonard' ,'Ridge' ,'Trey' ,'Aden' ,'Leandro' ,'Sam' ,'Uriah' ,'Ty' 
                ,'Sylas' ,'Axton' ,'Issac' ,'Fletcher' ,'Julien' ,'Wells' ,'Alden' ,'Vihaan' ,'Jamir' ,'Valentino' ,'Shepherd' ,'Keanu' ,'Hezekiah' ,'Lionel' 
                ,'Kohen' ,'Zaid' ,'Alberto' ,'Neil' ,'Denver' ,'Aarav' ,'Brendan' ,'Dillon' ,'Koda' ,'Sutton' ,'Kingsley' ,'Sonny' ,'Alfredo' ,'Wilson' ,'Harry' 
                ,'Jaziel' ,'Salvador' ,'Cullen' ,'Hamza' ,'Dariel' ,'Rex' ,'Zeke' ,'Mohammed' ,'Nelson' ,'Boone' ,'Ricky' ,'Santana' ,'Cayson' ,'Lance' ,'Raylan' 
                ,'Lucian' ,'Eliel' ,'Alvin' ,'Jagger' ,'Braden' ,'Curtis' ,'Mathew' ,'Jimmy' ,'Kareem' ,'Archie' ,'Amos' ,'Quinton' ,'Yosef' ,'Bodie' ,'Jerry' ,'Langston' 
                ,'Axl' ,'Stanley' ,'Clay' ,'Douglas' ,'Layne' ,'Titan' ,'Tomas' ,'Houston' ,'Darren' ,'Lachlan' ,'Kase' ,'Korbin' ,'Leighton' ,'Joziah' ,'Samir' ,'Watson' 
                ,'Colten' ,'Roger' ,'Shiloh' ,'Tommy' ,'Mitchell' ,'Azariah' ,'Noe' ,'Talon' ,'Deandre' ,'Lochlan' ,'Joe' ,'Carmelo' ,'Otis' ,'Randy' ,'Byron' ,'Chaim' 
                ,'Lennon' ,'Devon' ,'Nathanael' ,'Bruno' ,'Aryan' ,'Flynn' ,'Vicente' ,'Brixton' ,'Kyro' ,'Brennan' ,'Casen' ,'Kenzo' ,'Orlando' ,'Castiel' ,'Rayden' 
                ,'Ben' ,'Grey' ,'Jedidiah' ,'Tadeo' ,'Morgan' ,'Augustine' ,'Mekhi' ,'Abdullah' ,'Ramon' ,'Saint' ,'Emery' ,'Maurice' ,'Jefferson' ,'Maximo' ,'Koa' ,'Ray' 
                ,'Jamie' ,'Eddie' ,'Guillermo' ,'Onyx' ,'Thaddeus' ,'Wayne' ,'Hassan' ,'Alonso' ,'Dash' ,'Elisha' ,'Jaxxon' ,'Rohan' ,'Carl' ,'Kelvin' ,'Jon' ,'Larry' 
                ,'Reese' ,'Aldo' ,'Marcel' ,'Melvin' ,'Yousef' ,'Aron' ,'Kace' ,'Vincenzo' ,'Kellan' ,'Miller' ,'Jakob' ,'Reign' ,'Kellen' ,'Kristopher' ,'Ernesto' 
                ,'Briar' ,'Gary' ,'Trace' ,'Joey' ,'Clyde' ,'Enoch' ,'Jaxx' ,'Crosby' ,'Magnus' ,'Fisher' ,'Jadiel' ,'Bronson' ,'Eugene' ,'Lee' ,'Brecken' ,'Atreus' ,'Madden' 
                ,'Khari' ,'Caspian' ,'Ishaan' ,'Kristian' ,'Westley' ,'Hugh' ,'Kamryn' ,'Musa' ,'Rey' ,'Thatcher' ,'Alfred' ,'Emory' ,'Kye' ,'Reyansh' ,'Yahir' ,'Cain' ,'Mordechai' 
                ,'Zayd' ,'Demetrius' ,'Harley' ,'Felipe' ,'Louie' ,'Branson' ,'Graysen' ,'Allan' ,'Kole' ,'Harold' ,'Alvaro' ,'Harlan' ,'Amias' ,'Brett' ,'Khalid' ,'Misael' 
                ,'Westin' ,'Zechariah' ,'Aydin' ,'Kaiser' ,'Lian' ,'Bryant' ,'Junior' ,'Legacy' ,'Ulises' ,'Bellamy' ,'Brayan' ,'Kody' ,'Ledger' ,'Eliseo' ,'Gordon' ,'London' 
                ,'Rocky' ,'Valentin' ,'Terry' ,'Damari' ,'Trent' ,'Bentlee' ,'Canaan' ,'Gatlin' ,'Kiaan' ,'Franco' ,'Eithan' ,'Idris' ,'Krew' ,'Yehuda' ,'Marlon' 
                ,'Rodney' ,'Creed' ,'Salvatore' ,'Stefan' ,'Tristen' ,'Adrien' ,'Jamal' ,'Judson' ,'Camilo' ,'Kenny' ,'Nova' ,'Robin' ,'Rudy' ,'Van' 
                ,'Bjorn' ,'Brodie' ,'Mac' ,'Jacoby' ,'Sekani' ,'Vivaan' ,'Blaine' ,'Ira' ,'Ameer' ,'Dominik' ,'Alaric' ,'Dane' ,'Jeremias' ,'Kyng' 
                ,'Reginald' ,'Bobby' ,'Kabir' ,'Jairo' ,'Alexzander' ,'Benicio' ,'Vance' ,'Wallace' ,'Zavier' ,'Billy' ,'Callahan' ,'Dakari' ,'Gerald' 
                ,'Turner' ,'Bear' ,'Jabari' ,'Cory' ,'Fox' ,'Harlem' ,'Jakari' ,'Jeffery' ,'Maxton' ,'Ronnie' ,'Yisroel' ,'Zakai' ,'Bridger' ,'Remi' ,'Arian' 
                ,'Blaze' ,'Forest' ,'Genesis' ,'Jerome' ,'Reuben' ,'Wesson' ,'Anders' ,'Banks' ,'Calum' ,'Dayton' ,'Kylen' ,'Dangelo' ,'Emir' ,'Malakhi' ,'Salem' 
                ,'Blaise' ,'Tru' ,'Boden' ,'Kolten' ,'Kylo' ,'Aries' ,'Henrik' ,'Kalel' ,'Landry' ,'Marcellus' ,'Zahir' ,'Lyle' ,'Dario' ,'Rene' ,'Terrance' 
                ,'Xzavier' ,'Alfonso' ,'Darian' ,'Kylian' ,'Maison' ,'Foster' ,'Keenan' ,'Yahya' ,'Heath' ,'Javion' ,'Jericho' ,'Aziel' ,'Darwin' ,'Marquis' ,'Mylo' 
                ,'Ambrose' ,'Anakin' ,'Jordy' ,'Juelz' ,'Toby' ,'Yael' ,'Azrael' ,'Brentley' ,'Tristian' ,'Bode' ,'Jovanni' ,'Santos' ,'Alistair' ,'Braydon' ,'Kamdyn' ,'Marc' 
                ,'Mayson' ,'Niklaus' ,'Simeon' ,'Colter' ,'Davion' ,'Leroy' ,'Ayan' ,'Dilan' ,'Ephraim' ,'Anson' ,'Merrick' ,'Wes' ,'Will' ,'Jaxen' ,'Maxim' 
                ,'Howard' ,'Jad' ,'Jesiah' ,'Ignacio' ,'Zyon' ,'Ahmir' ,'Jair' ,'Mustafa' ,'Jermaine' ,'Yadiel' ,'Aayan' ,'Dhruv' ,'Seven' ,'Stone' ,'Rome' }


LAST_NAMES = {'SMITH' ,'JOHNSON' ,'WILLIAMS' ,'JONES' ,'BROWN' ,'DAVIS' ,'MILLER' ,'WILSON' ,'MOORE' ,'TAYLOR' ,'ANDERSON' ,'THOMAS' ,'JACKSON' ,'WHITE' 
                ,'HARRIS' ,'MARTIN' ,'THOMPSON' ,'GARCIA' ,'MARTINEZ' ,'ROBINSON' ,'CLARK' ,'RODRIGUEZ' ,'LEWIS' ,'LEE' ,'WALKER' ,'HALL' ,'ALLEN' ,'YOUNG' 
                ,'HERNANDEZ' ,'KING' ,'WRIGHT' ,'LOPEZ' ,'HILL' ,'SCOTT' ,'GREEN' ,'ADAMS' ,'BAKER' ,'GONZALEZ' ,'NELSON' ,'CARTER' ,'MITCHELL' ,'PEREZ' 
,'ROBERTS' ,'TURNER' ,'PHILLIPS' ,'CAMPBELL' ,'PARKER' ,'EVANS' ,'EDWARDS' ,'COLLINS' ,'STEWART' ,'SANCHEZ' ,'MORRIS' ,'ROGERS' ,'REED' 
,'COOK' ,'MORGAN' ,'BELL' ,'MURPHY' ,'BAILEY' ,'RIVERA' ,'COOPER' ,'RICHARDSON' ,'COX' ,'HOWARD' ,'WARD' ,'TORRES' ,'PETERSON' ,'GRAY' 
,'RAMIREZ' ,'JAMES' ,'WATSON' ,'BROOKS' ,'KELLY' ,'SANDERS' ,'PRICE' ,'BENNETT' ,'WOOD' ,'BARNES' ,'ROSS' ,'HENDERSON' ,'COLEMAN' ,'JENKINS' 
,'PERRY' ,'POWELL' ,'LONG' ,'PATTERSON' ,'HUGHES' ,'FLORES' ,'WASHINGTON' ,'BUTLER' ,'SIMMONS' ,'FOSTER' ,'GONZALES' ,'BRYANT' ,'ALEXANDER' 
,'RUSSELL' ,'GRIFFIN' ,'DIAZ' ,'HAYES' ,'MYERS' ,'FORD' ,'HAMILTON' ,'GRAHAM' ,'SULLIVAN' ,'WALLACE' ,'WOODS' ,'COLE' ,'WEST' ,'JORDAN' 
,'OWENS' ,'REYNOLDS' ,'FISHER' ,'ELLIS' ,'HARRISON' ,'GIBSON' ,'MCDONALD' ,'CRUZ' ,'MARSHALL' ,'ORTIZ' ,'GOMEZ' ,'MURRAY' ,'FREEMAN' ,'WELLS' 
,'WEBB' ,'SIMPSON' ,'STEVENS' ,'TUCKER' ,'PORTER' ,'HUNTER' ,'HICKS' ,'CRAWFORD' ,'HENRY' ,'BOYD' ,'MASON' ,'MORALES' ,'KENNEDY' ,'WARREN' 
,'DIXON' ,'RAMOS' ,'REYES' ,'BURNS' ,'GORDON' ,'SHAW' ,'HOLMES' ,'RICE' ,'ROBERTSON' ,'HUNT' ,'BLACK' ,'DANIELS' ,'PALMER' ,'MILLS' ,'NICHOLS' 
,'GRANT' ,'KNIGHT' ,'FERGUSON' ,'ROSE' ,'STONE' ,'HAWKINS' ,'DUNN' ,'PERKINS' ,'HUDSON' ,'SPENCER' ,'GARDNER' ,'STEPHENS' ,'PAYNE' ,'PIERCE' 
,'BERRY' ,'MATTHEWS' ,'ARNOLD' ,'WAGNER' ,'WILLIS' ,'RAY' ,'WATKINS' ,'OLSON' ,'CARROLL' ,'DUNCAN' ,'SNYDER' ,'HART' ,'CUNNINGHAM' ,'BRADLEY' 
,'LANE' ,'ANDREWS' ,'RUIZ' ,'HARPER' ,'FOX' ,'RILEY' ,'ARMSTRONG' ,'CARPENTER' ,'WEAVER' ,'GREENE' ,'LAWRENCE' ,'ELLIOTT' ,'CHAVEZ' ,'SIMS' 
,'AUSTIN' ,'PETERS' ,'KELLEY' ,'FRANKLIN' ,'LAWSON' ,'FIELDS' ,'GUTIERREZ' ,'RYAN' ,'SCHMIDT' ,'CARR' ,'VASQUEZ' ,'CASTILLO' ,'WHEELER' 
,'CHAPMAN' ,'OLIVER' ,'MONTGOMERY' ,'RICHARDS' ,'WILLIAMSON' ,'JOHNSTON' ,'BANKS' ,'MEYER' ,'BISHOP' ,'MCCOY' ,'HOWELL' ,'ALVAREZ' ,'MORRISON' 
,'HANSEN' ,'FERNANDEZ' ,'GARZA' ,'HARVEY' ,'LITTLE' ,'BURTON' ,'STANLEY' ,'NGUYEN' ,'GEORGE' ,'JACOBS' ,'REID' ,'KIM' ,'FULLER' ,'LYNCH' ,'DEAN' 
,'GILBERT' ,'GARRETT' ,'ROMERO' ,'WELCH' ,'LARSON' ,'FRAZIER' ,'BURKE' ,'HANSON' ,'DAY' ,'MENDOZA' ,'MORENO' ,'BOWMAN' ,'MEDINA' ,'FOWLER' 
,'BREWER' ,'HOFFMAN' ,'CARLSON' ,'SILVA' ,'PEARSON' ,'HOLLAND' ,'DOUGLAS' ,'FLEMING' ,'JENSEN' ,'VARGAS' ,'BYRD' ,'DAVIDSON' ,'HOPKINS' ,'MAY' 
,'TERRY' ,'HERRERA' ,'WADE' ,'SOTO' ,'WALTERS' ,'CURTIS' ,'NEAL' ,'CALDWELL' ,'LOWE' ,'JENNINGS' ,'BARNETT' ,'GRAVES' ,'JIMENEZ' ,'HORTON' 
,'SHELTON' ,'BARRETT' ,'OBRIEN' ,'CASTRO' ,'SUTTON' ,'GREGORY' ,'MCKINNEY' ,'LUCAS' ,'MILES' ,'CRAIG' ,'RODRIQUEZ' ,'CHAMBERS' ,'HOLT' ,'LAMBERT' 
,'FLETCHER' ,'WATTS' ,'BATES' ,'HALE' ,'RHODES' ,'PENA' ,'BECK' ,'NEWMAN' ,'HAYNES' ,'MCDANIEL' ,'MENDEZ' ,'BUSH' ,'VAUGHN' ,'PARKS' ,'DAWSON' 
,'SANTIAGO' ,'NORRIS' ,'HARDY' ,'LOVE' ,'STEELE' ,'CURRY' ,'POWERS' ,'SCHULTZ' ,'BARKER' ,'GUZMAN' ,'PAGE' ,'MUNOZ' ,'BALL' ,'KELLER' ,'CHANDLER' 
,'WEBER' ,'LEONARD' ,'WALSH' ,'LYONS' ,'RAMSEY' ,'WOLFE' ,'SCHNEIDER' ,'MULLINS' ,'BENSON' ,'SHARP' ,'BOWEN' ,'DANIEL' ,'BARBER' ,'CUMMINGS' 
,'HINES' ,'BALDWIN' ,'GRIFFITH' ,'VALDEZ' ,'HUBBARD' ,'SALAZAR' ,'REEVES' ,'WARNER' ,'STEVENSON' ,'BURGESS' ,'SANTOS' ,'TATE' ,'CROSS' ,'GARNER' 
,'MANN' ,'MACK' ,'MOSS' ,'THORNTON' ,'DENNIS' ,'MCGEE' ,'FARMER' ,'DELGADO' ,'AGUILAR' ,'VEGA' ,'GLOVER' ,'MANNING' ,'COHEN' ,'HARMON' ,'RODGERS' 
,'ROBBINS' ,'NEWTON' ,'TODD' ,'BLAIR' ,'HIGGINS' ,'INGRAM' ,'REESE' ,'CANNON' ,'STRICKLAND' ,'TOWNSEND' ,'POTTER' ,'GOODWIN' ,'WALTON' ,'ROWE' 
,'HAMPTON' ,'ORTEGA' ,'PATTON' ,'SWANSON' ,'JOSEPH' ,'FRANCIS' ,'GOODMAN' ,'MALDONADO' ,'YATES' ,'BECKER' ,'ERICKSON' ,'HODGES' ,'RIOS' ,'CONNER' 
,'ADKINS' ,'WEBSTER' ,'NORMAN' ,'MALONE' ,'HAMMOND' ,'FLOWERS' ,'COBB' ,'MOODY' ,'QUINN' ,'BLAKE' ,'MAXWELL' ,'POPE' ,'FLOYD' ,'OSBORNE' ,'PAUL' 
,'MCCARTHY' ,'GUERRERO' ,'LINDSEY' ,'ESTRADA' ,'SANDOVAL' ,'GIBBS' ,'TYLER' ,'GROSS' ,'FITZGERALD' ,'STOKES' ,'DOYLE' ,'SHERMAN' ,'SAUNDERS' 
,'WISE' ,'COLON' ,'GILL' ,'ALVARADO' ,'GREER' ,'PADILLA' ,'SIMON' ,'WATERS' ,'NUNEZ' ,'BALLARD' ,'SCHWARTZ' ,'MCBRIDE' ,'HOUSTON' ,'CHRISTENSEN' 
,'KLEIN' ,'PRATT' ,'BRIGGS' ,'PARSONS' ,'MCLAUGHLIN' ,'ZIMMERMAN' ,'FRENCH' ,'BUCHANAN' ,'MORAN' ,'COPELAND' ,'ROY' ,'PITTMAN' ,'BRADY' 
,'MCCORMICK' ,'HOLLOWAY' ,'BROCK' ,'POOLE' ,'FRANK' ,'LOGAN' ,'OWEN' ,'BASS' ,'MARSH' ,'DRAKE' ,'WONG' ,'JEFFERSON' ,'PARK' ,'MORTON' ,'ABBOTT' 
,'SPARKS' ,'PATRICK' ,'NORTON' ,'HUFF' ,'CLAYTON' ,'MASSEY' ,'LLOYD' ,'FIGUEROA' ,'CARSON' ,'BOWERS' ,'ROBERSON' ,'BARTON' ,'TRAN' ,'LAMB' 
,'HARRINGTON' ,'CASEY' ,'BOONE' ,'CORTEZ' ,'CLARKE' ,'MATHIS' ,'SINGLETON' ,'WILKINS' ,'CAIN' ,'BRYAN' ,'UNDERWOOD' ,'HOGAN' ,'MCKENZIE' 
,'COLLIER' ,'LUNA' ,'PHELPS' ,'MCGUIRE' ,'ALLISON' ,'BRIDGES' ,'WILKERSON' ,'NASH' ,'SUMMERS' ,'ATKINS' ,'WILCOX' ,'PITTS' ,'CONLEY' ,'MARQUEZ' 
,'BURNETT' ,'RICHARD' ,'COCHRAN' ,'CHASE' ,'DAVENPORT' ,'HOOD' ,'GATES' ,'CLAY' ,'AYALA' ,'SAWYER' ,'ROMAN' ,'VAZQUEZ' ,'DICKERSON' ,'HODGE' 
,'ACOSTA' ,'FLYNN' ,'ESPINOZA' ,'NICHOLSON' ,'MONROE' ,'WOLF' ,'MORROW' ,'KIRK' ,'RANDALL' ,'ANTHONY' ,'WHITAKER' ,'OCONNOR' ,'SKINNER' ,'WARE' 
,'MOLINA' ,'KIRBY' ,'HUFFMAN' ,'BRADFORD' ,'CHARLES' ,'GILMORE' ,'DOMINGUEZ' ,'ONEAL' ,'BRUCE' ,'LANG' ,'COMBS' ,'KRAMER' ,'HEATH' ,'HANCOCK' 
,'GALLAGHER' ,'GAINES' ,'SHAFFER' ,'SHORT' ,'WIGGINS' ,'MATHEWS' ,'MCCLAIN' ,'FISCHER' ,'WALL' ,'SMALL' ,'MELTON' ,'HENSLEY' ,'BOND' ,'DYER' 
,'CAMERON' ,'GRIMES' ,'CONTRERAS' ,'CHRISTIAN' ,'WYATT' ,'BAXTER' ,'SNOW' ,'MOSLEY' ,'SHEPHERD' ,'LARSEN' ,'HOOVER' ,'BEASLEY' ,'GLENN' 
,'PETERSEN' ,'WHITEHEAD' ,'MEYERS' ,'KEITH' ,'GARRISON' ,'VINCENT' ,'SHIELDS' ,'HORN' ,'SAVAGE' ,'OLSEN' ,'SCHROEDER' ,'HARTMAN' ,'WOODARD' 
,'MUELLER' ,'KEMP' ,'DELEON' ,'BOOTH' ,'PATEL' ,'CALHOUN' ,'WILEY' ,'EATON' ,'CLINE' ,'NAVARRO' ,'HARRELL' ,'LESTER' ,'HUMPHREY' ,'PARRISH' 
,'DURAN' ,'HUTCHINSON' ,'HESS' ,'DORSEY' ,'BULLOCK' ,'ROBLES' ,'BEARD' ,'DALTON' ,'AVILA' ,'VANCE' ,'RICH' ,'BLACKWELL' ,'YORK' ,'JOHNS' 
,'BLANKENSHIP' ,'TREVINO' ,'SALINAS' ,'CAMPOS' ,'PRUITT' ,'MOSES' ,'CALLAHAN' ,'GOLDEN' ,'MONTOYA' ,'HARDIN' ,'GUERRA' ,'MCDOWELL' ,'CAREY' 
,'STAFFORD' ,'GALLEGOS' ,'HENSON' ,'WILKINSON' ,'BOOKER' ,'MERRITT' ,'MIRANDA' ,'ATKINSON' ,'ORR' ,'DECKER' ,'HOBBS' ,'PRESTON' ,'TANNER' ,'KNOX' 
,'PACHECO' ,'STEPHENSON' ,'GLASS' ,'ROJAS' ,'SERRANO' ,'MARKS' ,'HICKMAN' ,'ENGLISH' ,'SWEENEY' ,'STRONG' ,'PRINCE' ,'MCCLURE' ,'CONWAY' 
,'WALTER' ,'ROTH' ,'MAYNARD' ,'FARRELL' ,'LOWERY' ,'HURST' ,'NIXON' ,'WEISS' ,'TRUJILLO' ,'ELLISON' ,'SLOAN' ,'JUAREZ' ,'WINTERS' ,'MCLEAN' 
,'RANDOLPH' ,'LEON' ,'BOYER' ,'VILLARREAL' ,'MCCALL' ,'GENTRY' ,'CARRILLO' ,'KENT' ,'AYERS' ,'LARA' ,'SHANNON' ,'SEXTON' ,'PACE' ,'HULL' 
,'LEBLANC' ,'BROWNING' ,'VELASQUEZ' ,'LEACH' ,'CHANG' ,'HOUSE' ,'SELLERS' ,'HERRING' ,'NOBLE' ,'FOLEY' ,'BARTLETT' ,'MERCADO' ,'LANDRY' 
,'DURHAM' ,'WALLS' ,'BARR' ,'MCKEE' ,'BAUER' ,'RIVERS' ,'EVERETT' ,'BRADSHAW' ,'PUGH' ,'VELEZ' ,'RUSH' ,'ESTES' ,'DODSON' ,'MORSE' ,'SHEPPARD' 
,'WEEKS' ,'CAMACHO' ,'BEAN' ,'BARRON' ,'LIVINGSTON' ,'MIDDLETON' ,'SPEARS' ,'BRANCH' ,'BLEVINS' ,'CHEN' ,'KERR' ,'MCCONNELL' ,'HATFIELD' 
,'HARDING' ,'ASHLEY' ,'SOLIS' ,'HERMAN' ,'FROST' ,'GILES' ,'BLACKBURN' ,'WILLIAM' ,'PENNINGTON' ,'WOODWARD' ,'FINLEY' ,'MCINTOSH' ,'KOCH' 
,'BEST' ,'SOLOMON' ,'MCCULLOUGH' ,'DUDLEY' ,'NOLAN' ,'BLANCHARD' ,'RIVAS' ,'BRENNAN' ,'MEJIA' ,'KANE' ,'BENTON' ,'JOYCE' ,'BUCKLEY' ,'HALEY' 
,'VALENTINE' ,'MADDOX' ,'RUSSO' ,'MCKNIGHT' ,'BUCK' ,'MOON' ,'MCMILLAN' ,'CROSBY' ,'BERG' ,'DOTSON' ,'MAYS' ,'ROACH' ,'CHURCH' ,'CHAN' 
,'RICHMOND' ,'MEADOWS' ,'FAULKNER' ,'ONEILL' ,'KNAPP' ,'KLINE' ,'BARRY' ,'OCHOA' ,'JACOBSON' ,'GAY' ,'AVERY' ,'HENDRICKS' ,'HORNE' ,'SHEPARD' 
,'HEBERT' ,'CHERRY' ,'CARDENAS' ,'MCINTYRE' ,'WHITNEY' ,'WALLER' ,'HOLMAN' ,'DONALDSON' ,'CANTU' ,'TERRELL' ,'MORIN' ,'GILLESPIE' ,'FUENTES' 
,'TILLMAN' ,'SANFORD' ,'BENTLEY' ,'PECK' ,'KEY' ,'SALAS' ,'ROLLINS' ,'GAMBLE' ,'DICKSON' ,'BATTLE' ,'SANTANA' ,'CABRERA' ,'CERVANTES' ,'HOWE' 
,'HINTON' ,'HURLEY' ,'SPENCE' ,'ZAMORA' ,'YANG' ,'MCNEIL' ,'SUAREZ' ,'CASE' ,'PETTY' ,'GOULD' ,'MCFARLAND' ,'SAMPSON' ,'CARVER' ,'BRAY' 
,'ROSARIO' ,'MACDONALD' ,'STOUT' ,'HESTER' ,'MELENDEZ' ,'DILLON' ,'FARLEY' ,'HOPPER' ,'GALLOWAY' ,'POTTS' ,'BERNARD' ,'JOYNER' ,'STEIN' 
,'AGUIRRE' ,'OSBORN' ,'MERCER' ,'BENDER' ,'FRANCO' ,'ROWLAND' ,'SYKES' ,'BENJAMIN' ,'TRAVIS' ,'PICKETT' ,'CRANE' ,'SEARS' ,'MAYO' ,'DUNLAP' 
,'HAYDEN' ,'WILDER' ,'MCKAY' ,'COFFEY' ,'MCCARTY' ,'EWING' ,'COOLEY' ,'VAUGHAN' ,'BONNER' ,'COTTON' ,'HOLDER' ,'STARK' ,'FERRELL' ,'CANTRELL' 
,'FULTON' ,'LYNN' ,'LOTT' ,'CALDERON' ,'ROSA' ,'POLLARD' ,'HOOPER' ,'BURCH' ,'MULLEN' ,'FRY' ,'RIDDLE' ,'LEVY' ,'DAVID' ,'DUKE' ,'ODONNELL' 
,'GUY' ,'MICHAEL' ,'BRITT' ,'FREDERICK' ,'DAUGHERTY' ,'BERGER' ,'DILLARD' ,'ALSTON' ,'JARVIS' ,'FRYE' ,'RIGGS' ,'CHANEY' ,'ODOM' ,'DUFFY' 
,'FITZPATRICK' ,'VALENZUELA' ,'MERRILL' ,'MAYER' ,'ALFORD' ,'MCPHERSON' ,'ACEVEDO' ,'DONOVAN' ,'BARRERA' ,'ALBERT' ,'COTE' ,'REILLY' ,'COMPTON' 
,'RAYMOND' ,'MOONEY' ,'MCGOWAN' ,'CRAFT' ,'CLEVELAND' ,'CLEMONS' ,'WYNN' ,'NIELSEN' ,'BAIRD' ,'STANTON' ,'SNIDER' ,'ROSALES' ,'BRIGHT' ,'WITT' 
,'STUART' ,'HAYS' ,'HOLDEN' ,'RUTLEDGE' ,'KINNEY' ,'CLEMENTS' ,'CASTANEDA' ,'SLATER' ,'HAHN' ,'EMERSON' ,'CONRAD' ,'BURKS' ,'DELANEY' ,'PATE' 
,'LANCASTER' ,'SWEET' ,'JUSTICE' ,'TYSON' ,'SHARPE' ,'WHITFIELD' ,'TALLEY' ,'MACIAS' ,'IRWIN' ,'BURRIS' ,'RATLIFF' ,'MCCRAY' ,'MADDEN' ,'KAUFMAN' 
,'BEACH' ,'GOFF' ,'CASH' ,'BOLTON' ,'MCFADDEN' ,'LEVINE' ,'GOOD' ,'BYERS' ,'KIRKLAND' ,'KIDD' ,'WORKMAN' ,'CARNEY' ,'DALE' ,'MCLEOD' ,'HOLCOMB' 
,'ENGLAND' ,'FINCH' ,'HEAD' ,'BURT' ,'HENDRIX' ,'SOSA' ,'HANEY' ,'FRANKS' ,'SARGENT' ,'NIEVES' ,'DOWNS' ,'RASMUSSEN' ,'BIRD' ,'HEWITT' ,'LINDSAY' 
,'LE' ,'FOREMAN' ,'VALENCIA' ,'ONEIL' ,'DELACRUZ' ,'VINSON' ,'DEJESUS' ,'HYDE' ,'FORBES' ,'GILLIAM' ,'GUTHRIE' ,'WOOTEN' ,'HUBER' ,'BARLOW' ,'BOYLE' 
,'MCMAHON' ,'BUCKNER' ,'ROCHA' ,'PUCKETT' ,'LANGLEY' ,'KNOWLES' ,'COOKE' ,'VELAZQUEZ' ,'WHITLEY' ,'NOEL' ,'VANG' }



# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  START OF CODE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



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

    """
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8') # data should be bytes
    req = urllib.request.Request(url, data)
    resp = urllib.request.urlopen(req)
    respData = resp.read()

    print(respData)
    """

    # web stuff!
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')

    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)

    words = response.read()

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
    # check line for start of weight division

    max_wt = 0
    min_wt = 0
    title_name_line = 'name'

    #  ************* 7 Jan 2020 - test, and had to decode the bytes to string.
    # print(type(line))
    # line = line.decode("utf-8") 
    # print(type(line))

    if WEIGHT_START in line:
        # at start of weight
        max_wt, min_wt = get_weight_details(line)
        weight = True
        # add weight to fighter count dictionary
        # fighter_count[max_wt] = 0

    if NAME_START in line:
        # has issues with fighters with regional titles.  Doesn't collect name correctly.
        # get line with the fighters name in it to be used later if required.  Collect the line to be used
        # later
        title_name_line = line
        name = True


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
            print(words)
            ret = True

    return ret

def retire_fighter_func():
    pass


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