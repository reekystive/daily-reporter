import time
import schedule
import config
import daily_reporter as reporter


def job():
    print()
    print('[Info] [Scheduler] Starting scheduled job')
    reporter.run()
    print('[Info] [Scheduler] Scheduled job done')


for item in config.report_times:
    schedule.every().day.at(item).do(job)

print('[Info] [Scheduler] Started scheduler')

while True:
    schedule.run_pending()
    time.sleep(20)
