import os
import time
import schedule


def job():
    print('Starting job...')
    os.system("python3 ./daily_reporter.py")
    print('Job done\n')


schedule.every().day.at('00:30').do(job)
schedule.every().day.at('07:30').do(job)

print('Started scheduler')

while True:
    schedule.run_pending()
    time.sleep(20)
