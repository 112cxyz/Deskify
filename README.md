# Deskify
## A Colourful Way To Show Music

### What is Deskify?
Deskify gets your current playing song on spotify and picks two colours from the image and sets your lights of choice to a random colour.

### How Does Deskify Work?
Deskify uses Localify which is a local wrapper for spotify to limit requets to the spotify elimiating rate limits.

### How Does it talk to my lights?
Deskify is designed to be used with HomeAssistant by using the REST api.

## Installation
Requirements: [Home Assistant](https://homeassistant.io), [Localify](https://github.com/112cxyz/Localify)
Once both are setup, open deskify.py and edit the for Home Assistant URL & Localify respectivley
Inside Deskify you need to edit the light names and how many you have, this will be simplified in the future.
Once all configured install deskify using git & python3.10
```
git clone https://github.com/112cxyz/Deskify.git
pip3 install -r requirements.txt
python3 deskify.py
```

