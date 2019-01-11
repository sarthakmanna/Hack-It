import time
from selenium import webdriver
import os
from pathlib import Path

class Hacker:
    def __init__(self, contest_id):
        self.contest_id = contest_id
        self.base_url = "https://codeforces.com/contest/" + contest_id + "/challenge/"
        self.hackable_dir = str(Path.home()) + "/Desktop/Hackable/"
        self.browser = webdriver.Firefox()
        self.browser.get("https://codeforces.com/enter")


    def start(self):
        my_files = os.listdir(self.hackable_dir)
        for file in my_files:
            with open(self.hackable_dir + file) as f:
                time.sleep(60)
                self.browser.get(self.base_url + file)
                print(self.base_url + file)
                time.sleep(1)
                elem = self.browser.find_elements_by_name("testcase")
                print(elem)
                elem[1].send_keys(f.read())
                time.sleep(1)
                elem[1].submit()
                time.sleep(1)
                f.close()
            os.remove(self.hackable_dir + file)


print("Enter contest ID")
contest_id = input()
hacker = Hacker(contest_id)
hacker.start()