import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
import time
import schedule
import datetime
import discord
from discord.ext import commands

class Bot:
    """
    docstring
    """
    
    def __init__(self, notifications = True, email = '', password = ''):
        self._classes = ''
        self._notifications = notifications
        self._email = email
        self._password = password

    def UpdateClasses(self):
        classes = pd.read_csv("classes.csv")
        classes_list = []

        for index, row in classes.iterrows():
            class_info = [row['Class name'], row['Week day'], row['Time'], row['Link']]
            classes_list.append(class_info)
        
        self._classes = classes_list

    def LoginClass(self, class_name, link, start_time):
       
        #accept the microfone and camera permissions
        #when the pop up shows up
        profile = webdriver.FirefoxProfile()
        profile.set_preference("permissions.default.microphone", 1)
        profile.set_preference("permissions.default.camera", 1)

        #logging gmail account
        driver = webdriver.Firefox(profile)
        driver.get("https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%3Fhs%3D193&&o_ref=https%3A%2F%2Fmeet.google.com%2Ftbj-djkw-soh&_ga=2.125951309.19111609.1604633728-1240995876.1604633728&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        email_login = driver.find_element_by_id("identifierId")
        email_login.send_keys(self._email)
        login_button = driver.find_element_by_id("identifierNext")
        login_button.click()
        time.sleep(3)
        password_login = driver.find_element_by_name("password")
        password_login.send_keys(self._password)
        password_button = driver.find_element_by_id("passwordNext")
        password_button.click()
        time.sleep(4)
        
        #after logging in we will access the class' google meet link
        driver.get(link)
        time.sleep(4)

        #disable microphone and camera
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('E').key_up(Keys.CONTROL).key_down(Keys.CONTROL).send_keys('D').key_up(Keys.CONTROL).perform()

        #join class
        join_button = driver.find_element_by_xpath("/html/body/div[1]/c-wiz/div/div/div[6]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]")
        join_button.click()

        self.CheckCurrentPeople(driver, class_name, start_time)
    
    def CheckClasses(self):

        current_date = datetime.datetime.today()

        for c in self._classes:

            if c[1].lower() == 'sunday':
                schedule.every().sunday.at(c[2]).do(self.LoginClass, c[0], c[3], c[2])

            if c[1].lower() == 'monday':
                schedule.every().monday.at(c[2]).do(self.LoginClass, c[0], c[3], c[2])

            if c[1].lower() == 'tuesday':
                schedule.every().tuesday.at(c[2]).do(self.LoginClass, c[0], c[3], c[2])

            if c[1].lower() == 'wednesday':
                schedule.every().wednesday.at(c[2]).do(self.LoginClass, c[0], c[3], c[2])

            if c[1].lower() == 'thursday':
                schedule.every().thursday.at(c[2]).do(self.LoginClass, c[0], c[3], c[2])

            if c[1].lower() == 'friday':
                schedule.every().friday.at(c[2]).do(self.LoginClass, c[0], c[3], c[2])

            if c[1].lower() == 'saturday':
                schedule.every().saturday.at(c[2]).do(self.LoginClass, c[0], c[3], c[2])

        while True:
            # Checks whether a scheduled task  
            # is pending to run or not 
            schedule.run_pending() 
            time.sleep(2) 

    def CheckCurrentPeople(self, driver, class_name, start_time):

        try:
            chat_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/c-wiz/div[1]/div/div[6]/div[3]/div[6]/div[3]/div/div[2]/div[1]")))
            chat_button.click()
            total = 1
            
            while True:
                time.sleep(5)
                current_people = self.GetTotalPeople(driver)
                
                if current_people > total:
                    total = current_people
    
                if current_people < total:
                    leave_class = driver.find_element_by_xpath('/html/body/div[1]/c-wiz/div[1]/div/div[6]/div[3]/div[9]/div[2]/div[2]')
                    leave_class.click()
                    driver.quit()
                    self.NotifyDiscord(class_name, start_time, datetime.datetime.now())

        except TimeoutException:
            print("Waiting to join the class...")

    def GetTotalPeople(self, driver):
        
        total_people = driver.find_element_by_xpath("/html/body/div[1]/c-wiz/div[1]/div/div[6]/div[3]/div[3]/div/div[2]/div[2]/div[1]/div[1]/span/div/span[2]")
        total_people = total_people.text

        #get only the numbers
        total_people_formatted = re.search("\d+", total_people)
        total_people_formatted = total_people_formatted.group(0)
        return int(total_people_formatted)

    def NotifyDiscord(self, class_name, start_time, end_time):

        bot = commands.Bot(command_prefix='!')
        bot.remove_command('help')

        def FindDiscordChannel():
            for guild in bot.guilds:
                for channel in guild.text_channels:
                    if channel.name == 'online-classes':
                        return channel.id

        @bot.command()
        async def help(ctx):
            channel_id = FindDiscordChannel()

            await ctx.send("You receive notifications when the class is over! Until then do something useful! :-)")

        @bot.event
        async def on_ready():
            channel_id = FindDiscordChannel()

            date = str(end_time.month) + '/' + str(end_time.day) + '/' + str(end_time.year)
            time_ended = str(end_time.hour) + ':' + str(end_time.minute)

            embed = discord.Embed(title="Class Notification", description="You received a notification!")
            embed.add_field(name="Class name:", value=class_name, inline=False)
            embed.add_field(name="Date:", value=date, inline=False)
            embed.add_field(name="Start time:", value=start_time, inline=True)
            embed.add_field(name="End time:", value=time_ended, inline=True)
            
            await bot.get_channel(channel_id).send(embed=embed)
        
        bot.run(config('BOT_TOKEN'))