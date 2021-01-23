min_temperature = 35.5
max_temperature = 36.9

timeout = 120
retry_times = 20

driver_path = 'auto'
browser_path = 'auto'
headless = False

app_token = 'AT_ABCDEF0123456789abcdef0123456789'
# app_token = None if do not use WeChat push

report_times = [
    '00:30',
    '07:30'
]

users = [
    {
        'username': '20201234567',
        'password': '123456',
        'use_wechat': True,
        'uid': 'UID_ABCDEF0123456789abcdef012345'
    },
    {
        'username': '20201234568',
        'password': '654321',
        'use_wechat': False,
        'uid': None
    }
]
