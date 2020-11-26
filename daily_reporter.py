from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome import options
from random import randint
from numpy.random import normal
import requests
import time
import config
import re

wechat_url = 'https://sc.ftqq.com/' + config.sckey + '.send'


def send_wechat(msg):
    send_url = wechat_url + '?text=' + msg
    response = requests.get(send_url)


today = time.localtime(time.time())
print('Now:', time.asctime(today))

chrome_options = options.Options()
if config.headless:
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

print('Launching Browser')
if (config.driver_path != 'auto'):
    browser = webdriver.Chrome(
        config.driver_path, chrome_options=chrome_options)
else:
    browser = webdriver.Chrome(chrome_options=chrome_options)

browser.set_window_size(480, 720)

print('Logging in')
browser.get('https://id.sspu.edu.cn/cas/login')
time.sleep(1)

username_box = browser.find_element_by_id('username')
username_box.send_keys(config.username)
password_box = browser.find_element_by_id('password')
password_box.send_keys(config.password)
time.sleep(0.5)

login_button = browser.find_element_by_class_name('submit_button')
login_button.click()
time.sleep(1)

try:
    browser.find_element_by_class_name('success')
except exceptions.NoSuchElementException:
    print('Login failed')
    send_wechat('Login_Failed')
    browser.quit()
    quit(1)

print('Login success')
time.sleep(0.5)

print('Jumping to HSM page')
browser.get('https://hsm.sspu.edu.cn/selfreport/Default.aspx')
time.sleep(0.5)
print('Jumping to Daily Report page')
browser.get('https://hsm.sspu.edu.cn/selfreport/DayReport.aspx')
time.sleep(1)

print('Starting auto fill')

min_value = int(config.min_temperature * 10)
max_value = int(config.max_temperature * 10)

loc = int((min_value + max_value) / 2)
scale = max_value - loc
temperature = int(normal(loc=loc, scale=scale)) / 10

if int(temperature * 10) < min_value or int(temperature * 10) > max_value:
    temperature = randint(min_value, max_value) / 10

print('Auto generated temperature:', temperature)
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
    print('Submit failed')
    send_wechat('Submit_Failed')
    browser.quit()
    quit(0)

yes_button_1 = browser.find_element_by_id('fineui_27') \
    .find_element_by_id('fineui_30')
yes_button_1.click()
time.sleep(1)

for i in range(100):
    time.sleep(3)
    try:
        browser.find_element_by_id('fineui_32')
    except exceptions.NoSuchElementException:
        print('Waiting')
        continue
    break

try:
    browser.find_element_by_id('fineui_32')
except exceptions.NoSuchElementException:
    print('Submit timeout')
    send_wechat('Submit_Timeout')
    browser.quit()
    quit(0)

print('Reported successfully')

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

datas = re.match(r'^(\d+)-(\d+)-(\d+).*?(\d+).*?$', txt)
res_date = datas.group(1) + '-' + datas.group(2) + '-' + datas.group(3)
res_date_wechat = datas.group(1) + '.' + datas.group(2) + '.' + datas.group(3)
rank = int(datas.group(4))

print('Date: ' + res_date + ', Rank: ' + str(rank))
send_wechat('Successfully' + '_' + res_date_wechat +
            '_' + str(temperature) + '_' + str(rank))
time.sleep(1)

browser.quit()
print('Browser closed')
