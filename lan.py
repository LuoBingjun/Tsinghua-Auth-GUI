import requests
import execjs
from retrying import retry
from subprocess import run

def getLOG_OP():
    JSf = open("./log.js", 'r', encoding='UTF-8')
    line = JSf.readline()
    Jstr = ''
    while line:
        Jstr = Jstr + line
        line = JSf.readline()
    return execjs.compile(Jstr)

logOP = getLOG_OP()

def login(userinfo):
    outdata = {
        "action": "login",
        "username": userinfo['username'],
        "password": userinfo['password'],
        "ac_id": "1",
        "ip": "",
        "double_stack": "1"
    }
    header = {
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    outcookie = {
        "off_campus":"null"
    }

    challenge = "https://auth6.tsinghua.edu.cn/cgi-bin/get_challenge"
    srun = "https://auth6.tsinghua.edu.cn/cgi-bin/srun_portal"

    time = logOP.call('getTimeString')
    print(time)
    param_challenge = {"callback": "jQuery", "username": userinfo['username'], "ip": "", "double_stack": "1", "_": time}
    s = requests.session()
    s.cookies = requests.utils.cookiejar_from_dict(outcookie)
    s.headers = header

    r = s.get(challenge, params=param_challenge)
    strofr = str(r.content, encoding='UTF-8')
    strofr = strofr[7:-1]
    print(strofr)
    rdata = eval(strofr)

    result = logOP.call('getOutData', outdata, rdata)
    finaldict = {"callback": "jQuery"}
    finaldict.update(result)
    param_srun = {
        "callback": "jQuery",
        "action": "login",
        "username": userinfo['username'],
        "password": finaldict['password'],
        "ac_id": "1",
        "ip": "",
        "doublestack": "1",
        "info": finaldict['info'],
        "chksum": finaldict['chksum'],
        "n": "200",
        "type": "1",
        "_": time + 1
    }
    print(param_srun)

    r2 = s.get(srun, params=param_srun)
    print(r2.url)
    print(r2.content)

def logout(userinfo):
    header = {
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type":"application/x-www-form-urlencoded",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    outcookie = {
        "off_campus":"null"
    }

    srun = "https://auth6.tsinghua.edu.cn/cgi-bin/srun_portal"

    param_logout = {
            "action": "logout",
            "username": userinfo['username'],
            "ac_id": logOP.call('GetQueryString', 'ac_id'),
            "ip": "",
            "double_stack": "1"
        }
    s = requests.session()
    s.cookies = requests.utils.cookiejar_from_dict(outcookie)
    s.headers = header

    r = s.get(srun, params=param_logout)
    print(r)

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
    backinfo = run('ping -n 1 -w 1 auth.tsinghua.edu.cn',shell=True)
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