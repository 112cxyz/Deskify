# 
# $$$$$$$\                      $$\       $$\  $$$$$$\            
# $$  __$$\                     $$ |      \__|$$  __$$\           
# $$ |  $$ | $$$$$$\   $$$$$$$\ $$ |  $$\ $$\ $$ /  \__|$$\   $$\ 
# $$ |  $$ |$$  __$$\ $$  _____|$$ | $$  |$$ |$$$$\     $$ |  $$ |
# $$ |  $$ |$$$$$$$$ |\$$$$$$\  $$$$$$  / $$ |$$  _|    $$ |  $$ |
# $$ |  $$ |$$   ____| \____$$\ $$  _$$<  $$ |$$ |      $$ |  $$ |
# $$$$$$$  |\$$$$$$$\ $$$$$$$  |$$ | \$$\ $$ |$$ |      \$$$$$$$ |
# \_______/  \_______|\_______/ \__|  \__|\__|\__|       \____$$ |
#                                                       $$\   $$ |
#         A Colourful Way To Show Music                 \$$$$$$  |
#               By Toby Fox (112c)                       \______/ 

# Deskify uses the Spotify API to get the current playing song and displays it on a LED strip.
# Deskify uses Localify which is a local wrapper for the Spotify API. This reduces flooding the actual Spotify API with requests.
# This means it is modular and other projects by me can use it.
# PLEASE download Localify before using Deskify, it is required for Deskify to work.
# Deskify is designed to use Home Assistant, for the best experience use Home Assistant.

# Localify web connection (change IP to your local IP of your instance)
localify_url = "http://localhost:5000"

# Import librariess
import requests
import json
import time
import os
import base64
import random

#Home Assistant API
from requests import post
from PIL import Image
from io import BytesIO
url = "http://homeassistant.local:8123/api/services/light/turn_on"
headers = {"Authorization": "Bearer #YOUR LONG LIVED ACESS TOKEN#"}

def bed(r,g,b):
    data = {"entity_id": "light.bed","rgb_color": [r, g, b]}
    post(url, headers=headers, json=data)

def desk(r,g,b):
    data = {"entity_id": "light.desk","rgb_color": [r, g, b]}
    post(url, headers=headers, json=data)


# Get the current album art the 30x30 colour array using Localify
def get_album_art():
    album_art = requests.get(localify_url + "/spotify/albumart/colours")
    album_art = album_art.text
    return album_art
    # Example output of two pixels [[(1, (10, 160, 154)), (1, (32, 160, 156))]

# Remove transparency from album art array 
def remove_transparency():
    album_art = get_album_art()
    album_art = album_art.replace("[", "")
    album_art = album_art.replace("]", "")
    album_art = album_art.replace("(", "")
    album_art = album_art.replace(")", "")
    album_art = album_art.replace(" ", "")
    album_art = album_art.split(",")
    album_art = [int(i) for i in album_art]
    album_art = [album_art[i:i+4] for i in range(0, len(album_art), 4)]
    return album_art

# Get a random colour from the non transparent album art array
def get_random_colour():
    album_art = remove_transparency()
    colour = random.choice(album_art)
    return colour


# Pick a colour from the album art array if its dark or light discard for a new one, if it fails 3 times just picks a random colour from the array
def pick_colour():
    album_art = remove_transparency()
    colour = random.choice(album_art)
    for i in range(3):
        if colour[1] > 100 and colour[2] > 100 and colour[3] > 100:
            colour = random.choice(album_art)
        elif colour[1] < 100 and colour[2] < 100 and colour[3] < 100:
            colour = random.choice(album_art)
        else:
            return colour
    colour = random.choice(album_art)
    return colour

while True:
    # Get the scene status in HomeAssistant, if Scene "Deskify" is on then continue
    scene_status = requests.get("https://home.112c.co.uk/api/states/input_boolean.deskify", headers=headers)
    scene_status = scene_status.text
    scene_status = json.loads(scene_status)
    scene_status = scene_status["state"]
    print("[DEBUG] Scene Status: ", scene_status)
    # Check if the lights are on 
    light_status = requests.get("https://home.112c.co.uk/api/states/light.bed", headers=headers)
    light_status = light_status.text
    light_status = json.loads(light_status)
    light_status = light_status["state"]
    print("[DEBUG] Light Status: ", light_status)
    if light_status == "on" and scene_status == "on":
            # Pick 1 random colour from the album art array
            colour = pick_colour()
            print("[DEBUG] Bed colour picked: ",  str(colour[1]),  str(colour[2]),  str(colour[3]))
            # Set the bed to a random colour
            bed(colour[1], colour[2], colour[3])
            # Once again for desk
            colour = pick_colour()
            print("[DEBUG] Desk colour picked: ", str(colour[1]), str(colour[2]),  str(colour[3]))
            desk(colour[1], colour[2], colour[3])

            # Wait 5 seconds
            time.sleep(5)
    else:
        print("[DEBUG] Lights are off or deskify is disabled")
        time.sleep(10)