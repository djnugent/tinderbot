import pynder
from time import gmtime, strftime, sleep
import subprocess
import os
import requests
import logging
import sys


class Tinderbot():

    SWIPE_RATE = 2

    def __init__(self,access_token,user_id,target,loc,interval):
        self.access_token = access_token
        self.user_id = user_id
        self.target = target
        self.loc = loc
        self.interval = interval
        self.server = None
        self.pwd = None

        #Global logger config
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger('tinderbot')

        #setup directory structure
        if not os.path.isdir("hits"):
            #create dir
            os.mkdir("hits")
        self.check_pwd()

        #local logger config
        self.config_logger()

    def start(self):
        #start file server
        self.server = subprocess.Popen(['python3 -m http.server 8000'], shell=True)

        #start tinder session
        self.log.info("Starting Session")
        self.session = pynder.Session(self.user_id, self.access_token)
        self.log.info(self.session.update_location(self.loc[0],self.loc[1])) # updates latitude and longitude for your profile
        self.log.info("Logged in as: " + str(self.session.profile))  # your profile. If you update its attributes they will be updated on Tinder.
        self.log.info("Searching for: " + self.target + " every " + str(self.interval) + " minutes")


    def swipe_session(self):
        #Swipe left as long as we can and save profiles that match our target
        self.log.info("swiping...")
        users = self.session.nearby_users(limit =10 ) # returns a list of users nearby
        count = 0
        for user in users:
            #check for target
            if(user.name == target):
                self.process_hit(user)
            #swipe left
            user.dislike()
            #log and stuff
            self.log.info("[" + str(count) + "] Swiped " + user.name + ", " + str(user.id))
            sleep(1.0/self.SWIPE_RATE)
            count += 1

        self.log.info("Swiped " + str(count) + " users")

    def process_hit(self,user):
        #save profile pic and id
        pic_url = user.photos[0]
        img_data = requests.get(pic_url).content
        file_loc = self.pwd + "/" + str(user.id) + ".jpg"
        with open(file_loc, 'wb') as handler:
            handler.write(img_data)
        self.log.info(">>>HIT: id: " + str(user.id) + " name: " + user.name + " age: " + str(user.age) + " photoURl: " + pic_url)

    def check_pwd(self):
        #change our PWD everyday
        current_date = "hits/" + strftime("%d-%b-%Y", gmtime())
        if self.pwd is None:
            self.pwd = current_date
        if not os.path.isdir(current_date):
            #create dir for that da
            os.mkdir(current_date)
            #set working directory
            self.pwd = current_date
            self.config_logger()


    def config_logger(self):
        #remove all existing handlers
        while len(self.log.handlers) > 0:
             self.log.removeHandler(self.log.handlers[0])
        #file
        fh = logging.FileHandler(self.pwd + "/log.txt")
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',\
                                datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        self.log.addHandler(fh)


    def check_state(self):  
        #Check if our account is still good
        if self.session.banned:
           self.log.warning("BANNED")
        #Update location in case it was changed by tinder app
        self.log.info("Setting location")
        self.session.update_location(self.loc[0],self.loc[1])

    def run(self):
        try:
            #start file server
            self.start()

            while True:
                self.check_pwd()
                self.check_state()
                self.swipe_session()
                sleep(60 * interval)

        finally:
            self.server.kill()





if __name__== "__main__":
    try:
        from config import access_token, fb_id
    except ImportError:
        print("Please create a config.py file. See config.py.example as a guide")
        sys.exit(0)

    loc = 44.942594, -93.191030
    target = "Kim"
    interval = 240

    bot = Tinderbot(access_token,fb_id,target,loc,interval)
    bot.run()
