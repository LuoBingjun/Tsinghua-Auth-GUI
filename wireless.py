import requests
from retrying import retry
from subprocess import run
import hashlib
import os

def login(userinfo):
    md = hashlib.md5()
    pwd = userinfo['password']
    md.update(pwd.encode('UTF-8'))
    code = md.hexdigest()

    topost = "action=login&username=" + userinfo['username'] + "&password={MD5_HEX}" + str(code) + "&ac_id=1"

    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "Keep-Alive",
        "Host": "net.tsinghua.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    s = requests.session()
    s.headers = header

    try:
        r = s.post("https://net.tsinghua.edu.cn/do_login.php", topost, timeout=5)
    except:
        return 0

    # 结果代码
    if r.content==b'Login is successful.':
        return 1
    elif r.content==b'IP has been online, please logout.':
        return 2
    elif r.content==b'E2553: Password is error.' or r.content==b'E2531: User not found.':
        return 3
    else:
        print(r.content)

def logout():
    topost = "action=logout"

    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "Keep-Alive",
        "Host": "net.tsinghua.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    s = requests.session()
    s.headers = header
    try:
        r = s.post("https://net.tsinghua.edu.cn/do_login.php", topost, timeout=5)
    except:
        return 0

    if r.content==b"Logout is successful.":
        return 1
    elif r.content==b'You are not online.':
        return 2
    else:
        print(r.content)

@retry(stop_max_attempt_number=3)
def get_userinfo():
    header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "Keep-Alive",
        "Host": "net.tsinghua.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    s = requests.session()
    s.headers = header

    r = s.post("https://net.tsinghua.edu.cn/rad_user_info.php", timeout=2)
    if len(r.content) == 0:
        return -1
    else:
        data = int(str(r.content).split(',')[6])
        return data / 1000000000

def networktest():
    #0为未连接上网,1为在内网(未登录),2为在内网(已登录),3为在外网
    backinfo = run('ping -4 -n 1 -w 1 www.tsinghua.edu.cn',shell=True)
    if backinfo.returncode:
        return 0, 0
    else:
        try:
            result = get_userinfo()
            if result==-1:
                return 1, 0
            else:
                return 2, result
        except:
            return 3, 0