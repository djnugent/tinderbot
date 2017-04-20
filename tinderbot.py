import pynder
from time import gmtime, strftime, sleep
import subprocess
import os
import requests


class Tinderbot():

    SWIPE_RATE = 2

    def __init__(self,access_token,user_id,target,loc,interval):
        self.access_token = access_token
        self.user_id = user_id
        self.target = target
        self.loc = loc
        self.interval = interval
        self.server = None
        self.pwd = "hits/" + strftime("%d-%b-%Y", gmtime())

    def start(self):
        #start file server
        self.server = subprocess.Popen(['python3 -m http.server 8000'], shell=True)

        #start tinder session
        print("Starting Session")
        self.session = pynder.Session(self.user_id, self.access_token)
        print("Setting location")
        print(self.session.update_location(self.loc[0],self.loc[1])) # updates latitude and longitude for your profile
        print("Logged in as: " + str(self.session.profile))  # your profile. If you update its attributes they will be updated on Tinder.
        print("Searching for: " + self.target + " every " + str(self.interval) + " minutes")


    def swipe_session(self):
        print("swiping...")
        users = self.session.nearby_users(limit =10 ) # returns a list of users nearby
        count = 0
        for user in users:
            if(user.name == target):
                self.process_hit(user)

            user.dislike()
            #print("swipe: " + str(count))
            sleep(1.0/self.SWIPE_RATE)
            count += 1
        t = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
        print(t + " - Swiped " + str(count) + "users")

    def process_hit(self,user):
            pic_url = user.photos[0]
            img_data = requests.get(pic_url).content
            file_loc = self.pwd + "/" + str(user.id) + ".jpg"
            with open(file_loc, 'wb') as handler:
                handler.write(img_data)
            print(">>>HIT: id: " + str(user.id) + " name: " + user.name + " age: " + str(user.age) + " photoURl: " + pic_url)

    def check_state(self):
        current_date = "hits/" + strftime("%d-%b-%Y", gmtime())
        if not os.path.isdir(current_date):
            print("Making directory " + current_date)
            os.mkdir(current_date)
            self.pwd = current_date
            self.session.update_location(self.loc[0],self.loc[1])

    def run(self):
        try:
            #start file server
            self.start()

            while True:
                self.check_state()
                self.swipe_session()
                sleep(60 * interval)

        finally:
            self.server.kill()





if __name__== "__main__":
    access_token = "912ef5de-9791-4918-bb3d-eee397066399"
    fb_id = 1021804951
    loc = 44.942594, -93.191030
    target = "Kim"
    interval = 240

    bot = Tinderbot(access_token,fb_id,target,loc,interval)
    bot.run()
