import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import youtube_dl
import requests
from pyowm import OWM
from urllib.request import urlopen
import json
import pyttsx3
from bs4 import BeautifulSoup as soup
import wikipedia
import pafy
from time import strftime

def tedResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    print()
    engine = pyttsx3.init()
    for line in audio.splitlines():
        engine.say(audio)
        engine.runAndWait()

def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command

def assistant(command):
    if 'shutdown' in command:
        tedResponse('Bye bye!. Have a nice day')
        sys.exit()

    if 'open' in command.split(" "):
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain + '.com'
            webbrowser.open(url)
            tedResponse('The website you have requested has been opened for you .')
            tedResponse('Is there anything else you want me to do?')
        else:
            pass

    if 'hello' or 'hi' or 'yo' or 'whats up?' in command.split(" "):
        day_time = int(strftime('%H'))
        if day_time < 12:
            tedResponse('Hello !!. Good morning')
        elif 12 <= day_time < 18:
            tedResponse('Hello !!. Good afternoon')
        else:
            tedResponse('Hello !!. Good evening')

    if 'joke' in command.split(" "):
        res = requests.get('https://icanhazdadjoke.com/',headers={"Accept":"application/json"})
        if res.status_code == requests.codes.ok:
            tedResponse(str(res.json()['joke']))
        else:
            tedResponse('oops!I ran out of jokes')

    if 'news' in command.split(" "):
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:8]:
                tedResponse(news.title.text.encode('utf-8'))
            tedResponse('Is there anything else you want me to do?')
        except Exception as e:
            tedResponse(e)

    if 'weather' in command.split(" "):
        reg_ex = re.search('weather (.*)', command)
        if reg_ex:
            l = command.split(" ")
            place = l[-1]
            city = place
            owm = OWM(API_key='ed7aca10668bd47a09e666615cecc68c')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            tedResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))
            tedResponse('Is there anything else you want me to do?')

    if 'time' in command.split(" "):
        import datetime
        now = datetime.datetime.now()
        tedResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

    if 'email' in command.split(" "):
            tedResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            # mail.ehlo()
            mail.starttls()
            mail.login('kteja1989@gmail.com', 'jkt031995')
            mail.sendmail('kteja1989@gmail.com', 'vaishnavibandi9@gmail.com', content)
            mail.close()
            tedResponse('Email has been sent successfuly. You can check your inbox.')
            tedResponse('Is there anything else you want me to do?')

    if 'song' in command.split(" "):
        tedResponse('What song should I play?')
        mysong = myCommand()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            response = urlopen(url)
            html = response.read()
            s = soup(html,"lxml")
            url_list = list()
            for vid in s.findAll(attrs={'class':'yt-uix-tile-link'}):
                if('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)
                url = url_list[0]
                webbrowser.open(url)
                tedResponse('The requested song is being played for you, is there anything else you want me to do?')
                break

    if 'about' in command.split(" "):
        reg_ex = re.search('about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                ny = ny.content[:500].encode('utf-8')
                tedResponse(ny)
        except Exception as e:
                tedResponse(e)
def menu():
    tedResponse(" I currently am able to do the following for you:")
    tedResponse("Open a website of your choice")
    tedResponse("Tell you the weather conditions at your current place and elsewhere")
    tedResponse("Play you a song of your choice")
    tedResponse("Give you the latest news feed")
    tedResponse("Give you the user required general information")
    tedResponse("Tell you the current time")
    tedResponse("Crack a random joke")
    tedResponse("Greet you according to the time")
tedResponse('Hey! What do you want me to do??')
menu()
while True:
    assistant(myCommand())