import time
import schedule
import daily_reporter as reporter


def job():
    print('[Info] Starting scheduled job')
    reporter.run()
    print('[Info] Scheduled job done\n')


schedule.every().day.at('00:30').do(job)
schedule.every().day.at('07:30').do(job)

print('[Info] Started scheduler')

while True:
    schedule.run_pending()
    time.sleep(20)
