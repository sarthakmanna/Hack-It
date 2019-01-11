import time
from selenium.webdriver.common.action_chains import ActionChains
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pathlib import Path




class Driver:
    def __init__(self, contest_id):
            self.browser = webdriver.Firefox()
            self.base_url = "https://codeforces.com/contest/" + contest_id + "/standings/page/"
            self.participant_ids = []
            self.problem_ids = []
            self.desktop_dir = str(Path.home())+"/Desktop/"
            self.submissions_ids = set()

    def scrape_participant_ids(self, url):
        self.participant_ids = []
        page_result = requests.get(url)
        page_result.raise_for_status()
        parser = bs4.BeautifulSoup(page_result.text)
        parse_result = parser.find_all("tr")
        """FInding participant ID's"""
        for i in range(1, len(parse_result) - 2):
            self.participant_ids.append(parse_result[i]['participantid'])

        """Finding problem ID's"""
        parse_result = parse_result[1].find_all("td")
        self.problem_ids = [problems['problemid'] for problems in parse_result if problems.get('problemid') is not None]

    def add_parsed_accepted_ids(self, result, problem_id):

        with open(self.desktop_dir + '/accepted_ids.txt', 'a+') as f:
            for line in result.splitlines():
                if line.split()[1] == 'Accepted':
                    f.write(line.split()[3]+" "+str(self.problem_ids.index(problem_id))+"\n")
        f.close()

    def re_adjust(self):
        self.browser.maximize_window()
        action = ActionChains(self.browser)
        action.send_keys([Keys.CONTROL, '0'])
        action.perform()
        time.sleep(0.5)

    def down_scroll(self):
        action = ActionChains(self.browser)
        action.send_keys([Keys.DOWN] * 2)
        action.perform()
        time.sleep(0.5)

    def double_click(self, web_element):
        action = ActionChains(self.browser)
        action.double_click(web_element)
        action.perform()
        time.sleep(0.5)

    def close_popup(self):
        action = ActionChains(self.browser)
        web_elem = self.browser.find_element_by_xpath("//div[@id='facebox']//a[@class='close']")
        action.click(web_elem)
        action.perform()
        time.sleep(0.5)

    def start(self, start_index, end_index):
        self.re_adjust()
        count = 0
        for index in range(start_index, end_index + 1):
            self.browser.get(self.base_url+str(index))
            driver.scrape_participant_ids(self.base_url+str(index))
            for participant_id in self.participant_ids:
                count += 1
                if count % 3 == 0:
                    self.down_scroll()

                for problem_id in self.problem_ids:
                    XML_PATH = "//div[@id='body']//div[@id='pageContent']/div[@class='datatable']" \
                               "//table[@class='standings']//tr[@participantid=" + \
                               participant_id + "]/" \
                               "td[@problemid=" + str(problem_id) + "]"
                    web_element = self.browser.find_element_by_xpath(XML_PATH)
                    if web_element.get_attribute('acceptedsubmissionid') is None:
                        continue
                    self.double_click(web_element)
                    text = ''
                    while text == '':
                        popup = self.browser.find_element_by_xpath("//div[@id='facebox']")
                        text = popup.text

                    self.add_parsed_accepted_ids(text, problem_id)
                    self.close_popup()


print("Enter the Contest ID")
contest_id = str(1096)#input()
print("Enter the start and end page index")
start, end =tuple(map(int, input().split()))

driver = Driver(contest_id)
driver.start(start, end)

