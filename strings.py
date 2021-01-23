import config
import time

msg = {}

# WeChat message strings
msg['success'] = '报送成功！'

msg['retry_1'] = '第'
msg['retry_2'] = '次尝试'

msg['number'] = '报送学号：'
msg['date'] = '报送日期：'
msg['time'] = '成功时间：'
msg['rank'] = '当日排名：'
msg['temperature'] = '报送体温：'

msg['failed_msg'] = '报送失败，请手动报送！'
msg['failed_time'] = '失败时间：'

# Website strings
msg['success_msg'] = '已填报'


def get_msg_success(user_index, date, rank, temp, try_times):
    now = time.localtime(time.time())
    res = msg['success']
    res += msg['retry_1'] + ' ' + str(try_times) + ' ' + msg['retry_2'] + '%0a' + '%0a'
    res += msg['number'] + str(config.users[user_index]['username']) + '%0a'
    res += msg['date'] + date + '%0a'
    res += msg['time'] + str(now[3]) + ':' + str(now[4]) + '%0a'
    res += msg['rank'] + str(rank) + '%0a'
    res += msg['temperature'] + str(temp)
    return res


def get_msg_failed(user_index, try_times):
    now = time.localtime(time.time())
    res = msg['failed_msg'] + '%0a'
    res += msg['retry_1'] + ' ' + str(try_times) + ' ' + msg['retry_2'] + '%0a' + '%0a'
    res += msg['number'] + str(config.users[user_index]['username']) + '%0a'
    res += msg['date'] + str(now[0]) + '-' + \
        str(now[1]) + '-' + str(now[2]) + '%0a'
    res += msg['failed_time'] + str(now[3]) + ':' + str(now[4])
    return res
