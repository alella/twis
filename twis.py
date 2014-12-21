#!/usr/bin/python2
import os
import sys
import time
import pygame
import urllib
import twitter
import tempfile
from pprint import pprint
from datetime import datetime
from mytwitterkeys import *

search_text = sys.argv[1]
app_dir = os.path.dirname(os.path.abspath(__file__))
chime_file = os.path.join(app_dir, "chime.mp3")
twitter_icon_file = os.path.join(app_dir, "twitter.png")
img_name = os.path.join(tempfile.gettempdir(),
                        datetime.now().strftime("%H%M%S.png"))

color_red = "#F0136F"
color_blue = "#12AFDB"
color_black = "#000000"
color_dark = "#111111"
color_light = "#f1f1f1"

pygame.init()
pygame.mixer.music.load(chime_file)

def verify_credentials():
    api = twitter.Api(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret
       )
    try:
        api.VerifyCredentials()
    except twitter.error.TwitterError:
        notify(text="<b>Authentication Failure</b>", fg=color_red)
        sys.exit()
    return api
    
def notify(title="Twitter Search", text="", timeout=5, fg=color_blue, bg=color_black, width=280,icon=twitter_icon_file):
    exec_notify = "echo 'naughty.notify(title=\"{title}\", text=\"{text}\", fg=\"{fg}\", bg=\"{bg}\", opacity=.9, width={width}, timeout={timeout}, font=\"SV Basic Manual 9\", icon=\"{icon}\")'|awesome-client"
    exec_notify = exec_notify.format(
        title=title,
        text=text,
        fg=fg,
        bg=bg,
        width=width,
        timeout=timeout,
        icon=icon
    )
    exec_notify = exec_notify.replace("(","({").replace(")","})")
    os.popen(exec_notify)
    pygame.mixer.music.play()
    time.sleep(.5)

def fetch_data(creds, search_text, id=None):
    time.sleep(1)
    try:
        resp = creds.GetSearch(term=search_text, lang="en", count=1, since_id=id)
        if resp:
            text = ''.join([i if ord(i) < 128 else ' ' for i in resp[0].text])
            location = resp[0].user.location if resp[0].user.location.replace(",","").replace(" ","").isalpha() else ""
            location = ''.join([i if ord(i) < 128 else ' ' for i in location])
            user_name = resp[0].user.screen_name
            if len(text)>100:
                ind = text[:100].rfind(" ")
                text = text[:ind]+"\\n"+text[ind+1:]
            return {"title":"{} from {}".format(user_name,location) if location else user_name,
                    "user":user_name,
                    "img":resp[0].user.profile_image_url,
                    "id":resp[0].id,
                    "text":text.encode('utf-8').replace("'","").replace("\n","\\n").replace('"','\\"')}
        else:
            return False
    except twitter.error.TwitterError:
        return False


def stream_tweets(search_text, max_count):
    new_text = ""
    old_text = ""
    data = {"id":None}
    count = 1
    while True:
        if new_text == old_text:
            last_id =  data["id"]
            data = fetch_data(creds, search_text, data["id"])
            if not data:
                data = {"id":last_id}
                continue
            new_text = data["text"]
        else:
            try:
                urllib.urlretrieve(data["img"], img_name)
                title = "[{}]: {}".format(str(count), data["title"])
                notify(title=title, text=data["text"], width=500, fg=color_dark, bg=color_light, timeout=20, icon=img_name)
                pprint(data)
                count += 1
            except:
                pass
            old_text = new_text
            if count > max_count:
                time.sleep(1)
                notify(text="Ending search for <b>{}</b>".format(search_text), fg=color_red, bg=color_black, timeout=2)
                sys.exit()
            
if __name__ == "__main__":
    creds = verify_credentials()
    if search_text == "stop":
        pids = os.popen("ps -ef|grep twis.py|grep python|grep -v grep| awk '{print $2}'").readlines()
        for pid in pids:
            os.popen("kill -9 "+pid.rstrip())
    notify(text="Started searching for <b>{}</b>".format(search_text), timeout=2)
    stream_tweets(search_text, 100)
