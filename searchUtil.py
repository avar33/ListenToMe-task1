'''
import sys
import json

from main import readJSON
from main import returnDisplayWhat
from main import returnPreferences

songs = readJSON("songs.json", 'songs')
for song in songs: 
    print(song["title"])
displayWhat = returnDisplayWhat
preferences = returnPreferences
'''