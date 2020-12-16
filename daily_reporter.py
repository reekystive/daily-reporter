from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome import options
from random import randint
from numpy.random import normal
import requests
import time
import config
import strings
import re


def send_wechat(user_index, msg):
    wechat_url = 'http://wxpusher.zjiecode.com/api/send/message/'
    wechat_url += '?appToken=' + config.app_token
    wechat_url += '&content=' + msg
    wechat_url += '&uid=' + config.users[user_index]['uid']
    requests.get(wechat_url)


def report(user_index):
    print('[Info] ' + 'Reporting for user ' + str(user_index + 1), end=', ')
    print('username: ' + config.users[user_index]['username'])

    today = time.localtime(time.time())
    print('[Info]', 'Now:', time.asctime(today))

    chrome_options = options.Options()
    if config.headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

    print('[Info] Launching Browser')
    if (config.driver_path != 'auto'):
        browser = webdriver.Chrome(
            config.driver_path, options=chrome_options)
    else:
        browser = webdriver.Chrome(options=chrome_options)

    browser.set_window_size(480, 720)

    print('[Info] Logging in')
    browser.get('https://id.sspu.edu.cn/cas/login')
    time.sleep(1)

    username_box = browser.find_element_by_id('username')
    username_box.send_keys(config.users[user_index]['username'])
    password_box = browser.find_element_by_id('password')
    password_box.send_keys(config.users[user_index]['password'])
    time.sleep(0.5)

    login_button = browser.find_element_by_class_name('submit_button')
    login_button.click()
    time.sleep(1)

    try:
        browser.find_element_by_class_name('success')
    except exceptions.NoSuchElementException:
        print('[Error] Login failed')
        if config.users[user_index]['use_wechat']:
            send_wechat(user_index, strings.get_msg_failed(user_index))
        browser.quit()
        return 1

    print('[Info] Login success')
    time.sleep(0.5)

    print('[Info] Jumping to HSM page')
    browser.get('https://hsm.sspu.edu.cn/selfreport/Default.aspx')
    time.sleep(0.5)
    print('[Info] Jumping to Daily Report page')
    browser.get('https://hsm.sspu.edu.cn/selfreport/DayReport.aspx')
    time.sleep(1)

    print('[Info] Starting auto fill')

    min_value = int(config.min_temperature * 10)
    max_value = int(config.max_temperature * 10)

    loc = int((min_value + max_value) / 2)
    scale = max_value - loc
    temperature = int(normal(loc=loc, scale=scale)) / 10

    if int(temperature * 10) < min_value or int(temperature * 10) > max_value:
        temperature = randint(min_value, max_value) / 10

    print('[Info] Auto generated temperature:', temperature)
    temperature_box = browser.find_element_by_id('p1_TiWen-inputEl')
    temperature_box.clear()
    temperature_box.send_keys(str(temperature))
    time.sleep(0.5)

    agree_box = browser.find_element_by_id('p1_ChengNuo-inputEl-icon')
    agree_box.click()
    time.sleep(0.5)

    condition_good = browser.find_element_by_id('fineui_2-inputEl-icon')
    condition_good.click()
    time.sleep(0.5)

    submit_button = browser.find_element_by_id('p1_ctl00') \
        .find_element_by_id('p1_ctl00_btnSubmit')
    submit_button.click()
    time.sleep(1)

    try:
        browser.find_element_by_id('fineui_27')
    except IndexError:
        print('[Error] Submit failed')
        if config.users[user_index]['use_wechat']:
            send_wechat(user_index, strings.get_msg_failed(user_index))
        browser.quit()
        return 1

    yes_button_1 = browser.find_element_by_id('fineui_27') \
        .find_element_by_id('fineui_30')
    yes_button_1.click()
    time.sleep(1)

    for i in range(int(config.timeout / 3)):
        time.sleep(3)
        try:
            browser.find_element_by_id('fineui_32')
        except exceptions.NoSuchElementException:
            print('[Info] Waiting: ' + str(i * 3) +
                  ' / ' + str(config.timeout) + ' seconds')
            continue
        break

    try:
        browser.find_element_by_id('fineui_32')
    except exceptions.NoSuchElementException:
        print('[Error] Submit timeout')
        if config.users[user_index]['use_wechat']:
            send_wechat(user_index, strings.get_msg_failed(user_index))
        browser.quit()
        return 1

    print('[Info] Reported successfully')

    yes_button_2 = browser.find_element_by_id('fineui_32') \
        .find_element_by_id('fineui_34') \
        .find_element_by_id('fineui_35')
    yes_button_2.click()
    time.sleep(1)

    browser.get('https://hsm.sspu.edu.cn/selfreport/ReportHistory.aspx')
    time.sleep(1)

    txt = browser.find_element_by_id('Panel1_DataList1') \
        .find_element_by_class_name('f-datalist-list') \
        .find_elements_by_class_name('f-datalist-item-inner')[0].text

    if txt.find(strings.msg['success_msg']) == -1:
        print('[Error] Check failed')
        if config.users[user_index]['use_wechat']:
            send_wechat(user_index, strings.get_msg_failed(user_index))
        browser.quit()
        return 1

    if re.match(r'^(\d+)-(\d+)-(\d+)\(.*?(\d+).*?\)$', txt) != None:
        datas = re.match(r'^(\d+)-(\d+)-(\d+)\(.*?(\d+).*?\)$', txt)
        rank = int(datas.group(4))
    else:
        print('[Warring] Check rank failed')
        datas = re.match(r'^(\d+)-(\d+)-(\d+)\(.*?\)$', txt)
        rank = None

    date = datas.group(1) + '-' + datas.group(2) + '-' + datas.group(3)

    print('[Info] ' + 'Date: ' + date + ', Rank: ' + str(rank))
    if config.users[user_index]['use_wechat']:
        send_wechat(user_index, strings.get_msg_success(
            user_index, date, rank, temperature))
    time.sleep(1)

    browser.quit()
    print('[Info] Browser closed')
    return 0


def run():
    print('[Info] Task started\n')

    for user_index in range(len(config.users)):
        for i in range(5):
            print('[Info] Trying # ' + str(i + 1))
            res = report(user_index)
            if res == 0:
                break
        print()
        time.sleep(5)

    print('[Info] Task done')


if __name__ == '__main__':
    run()
