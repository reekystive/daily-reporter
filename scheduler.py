import time
import schedule
import daily_reporter as reporter


def job():
    print()
    print('[Info] [Scheduler] Starting scheduled job')
    reporter.run()
    print('[Info] [Scheduler] Scheduled job done')


schedule.every().day.at('00:30').do(job)
schedule.every().day.at('07:30').do(job)

print('[Info] [Scheduler] Started scheduler')

while True:
    schedule.run_pending()
    time.sleep(20)
