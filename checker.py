from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import json
from datetime import datetime

LOGIN_URL = 'https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1'
SLACK_HOOK = 'https://hooks.slack.com/services/.../.../...'
CHROME_PATH = '/path/to/chromedriver'


def login(d):
    # Login and navigate to the delivery window page
    d.get(LOGIN_URL)
    print('please login and navigate to the delivery window page'); time.sleep(30)
    print('30 seconds left'); time.sleep(30)


def get_fresh_slot(d):
    open_slots = False
    while not open_slots:
        d.refresh()
        print('refreshed page...let load')
        time.sleep(5)
        unavailable = d.find_elements_by_xpath("//*[contains(text(),'No doorstep delivery windows are available')]")
        open_slots = False if len(unavailable) == 4 else True

        if open_slots:
            msg = '{} THERE ARE SLOTS OPEN ON {} DAY(S)'.format(datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
                                                                4 - len(unavailable))
            print(msg)
            for n in range(30):
                requests.post(
                    SLACK_HOOK,
                    data=json.dumps({'text': msg}),
                    headers={'Content-Type': 'application/json'}
                )
                # print(msg)
                time.sleep(1)
        else:
            msg = '{} no open slots'.format(datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
            print(msg)
            # requests.post(
            #     SLACK_HOOK,
            #     data=json.dumps({'text': msg}),
            #     headers={'Content-Type': 'application/json'}
            # )
        time.sleep(55)


driver = webdriver.Chrome(executable_path=CHROME_PATH)

login(driver)
get_fresh_slot(driver)
