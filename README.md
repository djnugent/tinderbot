# tinderbot
Tinder bot to find a tinder impersonator using my cousins identity

Uses [Pynder](https://github.com/charliewolf/pynder) as an unofficial tinder API

Runs on an AWS swiping at profiles that contain the impersonator's name. If the name matches then we save the tinder id and profile pic for further human analysis. Hosts a simple webserver to view the progress of the bot. If the photo is a match then we can report the id to tinder to have the profile removed. 

Code isn't anything special. Just a day project.
