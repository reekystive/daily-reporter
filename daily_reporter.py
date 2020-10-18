from selenium import webdriver
from selenium.common import exceptions
from random import randint
from numpy.random import normal
import time
import config

today = time.localtime(time.time())
print('Now:', time.asctime(today))

print('Launching Browser')
driver_path = '/Users/reekystive/Workspace/bin/chromedriver'
browser = webdriver.Chrome(driver_path)
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
    browser.close()
    quit()

print('Login success')

print('Jumping to HSM page')
browser.get('https://hsm.sspu.edu.cn/selfreport/Default.aspx')
time.sleep(0.5)
print('Jumping to Daily Report page')
browser.get('https://hsm.sspu.edu.cn/selfreport/DayReport.aspx')

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
time.sleep(1)

submit_button = browser.find_elements_by_class_name('f-btn-text')[0]
submit_button.click()
time.sleep(1)

try:
    browser.find_elements_by_class_name('f-btn-text')[2]
except IndexError:
    print('Submit failed')
    browser.close()
    quit()

yes_button = browser.find_elements_by_class_name('f-btn-text')[2]
yes_button.click()
time.sleep(1.5)

try:
    browser.find_element_by_class_name('f-messagebox-message')
except exceptions.NoSuchElementException:
    print('Submit failed')
    browser.close()
    quit()

print('Congratulations! You have reported successfully!')
time.sleep(1)

browser.close()
print('Browser closed')
