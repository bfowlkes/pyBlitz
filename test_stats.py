#!/usr/bin/env python3

import json
import pdb
import csv
from collections import OrderedDict
import os.path
from pathlib import Path

def FindTeams(stats_team, fixed_team, stats_teams):
    Found = False
    for team in stats_teams:
        if (team.strip() == stats_team.strip() and fixed_team.strip() == ""):
            Found = True
            break
        if (team.strip() == fixed_team.strip()):
            Found = True
            break
    return Found

print ("Test stats spreadsheet validation Tool")
print ("****************************************************************")
print (" ")
print ("Makes sure that your merge stats spreadsheet is set up correctly")
print ("    == be aware that all teams need to match up")
print ("    == if they do not a prediction will not be possible")
print (" ")

file = 'merge_stats.csv'
if (not os.path.exists(file)):
    print ("merge_stats.csv file is missing, run the merge_stats tool to create")
    exit()
dict_merge = []
with open(file) as merge_file:
    reader = csv.DictReader(merge_file)
    for row in reader:
        dict_merge.append(row)
path = "data/"
file = '{0}outsiders.json'.format(path)
if (not os.path.exists(file)):
    print ("outsiders file is missing, run the scrape_outsiders tool to create")
    exit()
with open(file) as stats_file:
    dict_stats = json.load(stats_file, object_pairs_hook=OrderedDict)

AllTeams=[]
for item in  dict_stats.values():
    AllTeams.append(item["Team"])
team_set = set(AllTeams)
stats_teams = list(team_set)
stats_teams.sort()

found = False
for team in dict_merge:
    if (team["corrected outsiders"].strip()!=""):
        found = True

if (not found):
    print ("*** Warning: Have you set up your merge_stats? There are NO fixes entered ***")
    print ("*** Make sure all of your match-ups are correct and then re-run this script ***")
    exit()

for team in dict_merge:
    found = FindTeams(team["outsiders"], team["corrected outsiders"], stats_teams)
    if (not found):
        print ("warning: {0} was not found in the outsiders table ***".format(team["teamrankings"]))
 
print ("done.")
