import time
from selenium.webdriver.common.action_chains import ActionChains
import requests,bs4,webbrowser,pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

base_url = "https://codeforces.com/contest/1076/standings"
page_result = requests.get(base_url)
page_result.raise_for_status()
parser = bs4.BeautifulSoup(page_result.text)

participant_ids = []
parse_result = parser.find_all("tr")
for i in range(1, len(parse_result) - 2):
    # print(parse_result[i])
    participant_ids.append(parse_result[i]['participantid'])

#print(participant_ids)
print("Enter start and end page numbers :")
start, end = tuple(map(int,input().split()))

problem_id_start = 253925




def add_parsed_accepted_ids(result):
    for line in result.splitlines():
        if line.split()[1] == 'Accepted':
            #print(line.split()[3])
            accepted_ids.append(line.split()[3])
            #return line.split()[3]


def re_adjust(browser):
    #browser.maximize_window()
    browser.set_window_size(1855,1056)
    print(browser.get_window_size())
    action = ActionChains(browser)
    action.send_keys([Keys.CONTROL, '0'])
    action.perform()
    time.sleep(0.5)

accepted_ids = []
count = 0
for index in range(start, end+1):
    url = base_url + "/page/" + str(index)
    browser = webdriver.Firefox()
    browser.get(url)
    re_adjust(browser)

    for participant_id in participant_ids:
        count += 1
        problem_start = problem_id_start
        if count % 3 == 0:
            action0 = ActionChains(browser)
            from selenium.webdriver.common.keys import Keys

            action0.send_keys([Keys.DOWN] * 2)
            action0.perform()
            time.sleep(0.5)
        for problem_count in range(7):
            problem_id = problem_start + problem_count

            XML_PATH = "//div[@id='body']//div[@id='pageContent']/div[@class='datatable']//table[@class='standings']//tr[@participantid=" + participant_id + "]/td[@problemid=" + str(
            problem_id) + "]"
            # elem_temp = browser.find_element_by_xpath("//div[@id='body']//div[@id='pageContent']/div[@class='datatable']//table[@class='standings']//tr[@participantid='21001268']/td[@problemid='253927']")

            elem = browser.find_element_by_xpath(XML_PATH)
            #re_adjust(curr_pos=elem.location,browser=browser)

            if elem.get_attribute('acceptedsubmissionid') is None:
                continue
            action = ActionChains(browser)
            action.double_click(elem)

            action.perform()
            time.sleep(0.5)
            elem2 = browser.find_element_by_xpath("//div[@id='facebox']")

            add_parsed_accepted_ids(elem2.text)

            action2 = ActionChains(browser)

            elem3 = browser.find_element_by_xpath("//div[@id='facebox']//a[@class='close']")
            action2.click(elem3)

            action2.perform()
            time.sleep(0.5)


    print(accepted_ids)
    browser.close()