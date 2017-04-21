# Tinderbot
I made a tinderbot as a short one day project to find a tinder impersonator who using my cousin's identity(photos).

## How it works

It runs on an AWS swiping at profiles that contain the impersonator's name. If the name matches, then we save the tinder id and profile pic for further human analysis. It hosts a simple webserver to view the progress of the bot. If the human deems a photo is a match then they can report the id to tinder to have the profile removed. 

## Dependencies

It uses [Pynder](https://github.com/charliewolf/pynder) as an unofficial tinder API


## Setup

You must create a `config.py` file with facebook id and tinder access token to use. See `config.py.example` for guidance. Or check out [this](https://github.com/fbessez/Tinder) repo for more tools on how to do it.
