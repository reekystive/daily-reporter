from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome import options
from random import randint
from random import normalvariate
import requests
import time
import config
import strings
import re


def send_wechat(user_index, msg):
    """Send messeage to WeChat"""
    wechat_url = 'http://wxpusher.zjiecode.com/api/send/message/'
    wechat_url += '?appToken=' + config.app_token
    wechat_url += '&content=' + msg
    wechat_url += '&uid=' + config.users[user_index]['uid']
    requests.get(wechat_url)


def report(user_index, try_times):
    """Report for one user"""
    today = time.localtime(time.time())
    print('[Info]', 'Now:', time.asctime(today))

    chrome_options = options.Options()
    if config.browser_path != 'auto':
        chrome_options.binary_location = config.browser_path
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

    # Login
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

    # Detect login status
    try:
        browser.find_element_by_class_name('success')
    except exceptions.NoSuchElementException:
        print('[Error] Login failed')
        if config.users[user_index]['use_wechat']:
            if try_times == config.retry_times:
                send_wechat(user_index, strings.get_msg_failed(user_index, try_times))
        browser.quit()
        return 1

    print('[Info] Login success')
    time.sleep(0.5)

    # Jump to HSM page
    print('[Info] Jumping to HSM page')
    browser.get('https://hsm.sspu.edu.cn/selfreport/Default.aspx')
    time.sleep(0.5)

    # Jump to Daily Report page
    print('[Info] Jumping to Daily Report page')
    browser.get('https://hsm.sspu.edu.cn/selfreport/DayReport.aspx')
    time.sleep(1)

    # Start filling
    print('[Info] Starting auto fill')

    min_value = int(config.min_temperature * 10)
    max_value = int(config.max_temperature * 10)

    # Generate temperature using normal distribution
    loc = int((min_value + max_value) / 2)
    scale = max_value - loc
    temperature = int(normalvariate(loc, scale))
    if int(temperature * 10) < min_value or int(temperature * 10) > max_value:
        temperature = randint(min_value, max_value) / 10

    print('[Info] Auto generated temperature:', temperature)

    # Fill temperature
    temperature_box = browser.find_element_by_id('p1_TiWen-inputEl')
    temperature_box.clear()
    temperature_box.send_keys(str(temperature))
    time.sleep(0.5)

    # Health Condition
    condition_good = browser.find_element_by_id('p1_DangQSTZK') \
        .find_element_by_id('fineui_2-inputEl-icon')
    condition_good.click()
    time.sleep(0.5)

    # Dangerous Area
    dangerous_area = browser.find_element_by_id('p1_CengFWH') \
        .find_element_by_id('fineui_13-inputEl-icon')
    dangerous_area.click()
    time.sleep(0.5)

    # Dangerous People
    dangerous_people = browser.find_element_by_id('p1_JieChu') \
        .find_element_by_id('fineui_15-inputEl-icon')
    dangerous_people.click()
    time.sleep(0.5)

    # In Shanghai
    if config.users[user_index]['in_shanghai']:
        in_shanghai = browser.find_element_by_id('p1_Shanghai') \
            .find_element_by_class_name('f-field-body-cell') \
            .find_element_by_class_name('f-field-checkbox-switch')
        in_shanghai.click()
        time.sleep(0.5)

    # Check Address
    check_address = browser.find_element_by_id('p1_CheckAddress') \
        .find_element_by_id('p1_CheckAddress-inputEl-icon')
    check_address.click()
    time.sleep(0.5)

    # Submit
    submit_button = browser.find_element_by_id('p1_ctl00') \
        .find_element_by_id('p1_ctl00_btnSubmit')
    submit_button.click()
    time.sleep(1)

    # Detect submit status
    try:
        browser.find_element_by_id('fineui_36')
    except IndexError:
        print('[Error] Submit failed')
        if config.users[user_index]['use_wechat']:
            if try_times == config.retry_times:
                send_wechat(user_index, strings.get_msg_failed(user_index, try_times))
        browser.quit()
        return 1

    # Confirm submit
    yes_button_1 = browser.find_element_by_id('fineui_36') \
        .find_element_by_id('fineui_38') \
        .find_element_by_id('fineui_39')
    yes_button_1.click()
    time.sleep(1)

    # Waiting for submit result
    for i in range(int(config.timeout / 3)):
        time.sleep(3)
        try:
            browser.find_element_by_id('fineui_41')
        except exceptions.NoSuchElementException:
            print('[Info] Waiting: ' + str(i * 3) +
                  ' / ' + str(config.timeout) + ' seconds')
            continue
        break

    try:
        browser.find_element_by_id('fineui_41')
    except exceptions.NoSuchElementException:
        print('[Error] Submit timeout')
        if config.users[user_index]['use_wechat']:
            if try_times == config.retry_times:
                send_wechat(user_index, strings.get_msg_failed(user_index, try_times))
        browser.quit()
        return 1

    print('[Info] Reported successfully')

    # Confirm the success message
    yes_button_2 = browser.find_element_by_id('fineui_41') \
        .find_element_by_id('fineui_43') \
        .find_element_by_id('fineui_44')
    yes_button_2.click()
    time.sleep(1)

    # Check rank
    browser.get('https://hsm.sspu.edu.cn/selfreport/ReportHistory.aspx')
    time.sleep(1)

    # Get rank data text
    txt = browser.find_element_by_id('Panel1_DataList1') \
        .find_element_by_class_name('f-datalist-list') \
        .find_elements_by_class_name('f-datalist-item-inner')[0].text

    # Check whether report is successful
    if txt.find(strings.msg['success_msg']) == -1:
        print('[Error] Check failed')
        if config.users[user_index]['use_wechat']:
            if try_times == config.retry_times:
                send_wechat(user_index, strings.get_msg_failed(user_index, try_times))
        browser.quit()
        return 1

    # Get rank data
    if re.match(r'^(\d+)-(\d+)-(\d+)\(.*?(\d+).*?\)$', txt) != None:
        datas = re.match(r'^(\d+)-(\d+)-(\d+)\(.*?(\d+).*?\)$', txt)
        rank = int(datas.group(4))
    else:
        print('[Warning] Check rank failed')
        datas = re.match(r'^(\d+)-(\d+)-(\d+)\(.*?\)$', txt)
        rank = None

    date = datas.group(1) + '-' + datas.group(2) + '-' + datas.group(3)

    print('[Info] ' + 'Date: ' + date + ', Rank: ' + str(rank))
    if config.users[user_index]['use_wechat']:
        send_wechat(user_index, strings.get_msg_success(
            user_index, date, rank, temperature, try_times))
    time.sleep(1)

    browser.quit()
    print('[Info] Browser closed')
    return 0


def run():
    print('[Info] Task started\n')

    for user_index in range(len(config.users)):
        print('[Info] Reporting for user ' + str(user_index + 1), end=', ')
        print('username: ' + config.users[user_index]['username'])
        for i in range(config.retry_times):
            print('[Info] Trying # ' + str(i + 1))
            res = report(user_index, i + 1)
            if res == 0:
                break
        print()
        time.sleep(5)

    print('[Info] Task done')


if __name__ == '__main__':
    run()
