import requests
import execjs

def auth(userinfo):
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

    def getLOG_JS():
        JSf = open("./log.js",'r',encoding = 'UTF-8')
        line = JSf.readline()
        Jstr = ''
        while line:
            Jstr = Jstr+line
            line = JSf.readline()
        return Jstr
    logJS = getLOG_JS()
    logOP = execjs.compile(logJS)


    def auth(challenge,srun):
        time = logOP.call('getTimeString')
        print(time)
        param_challenge = {"callback":"jQuery","username":user['username'],"ip":"","double_stack":"1","_":time}
        s = requests.session()
        s.cookies = requests.utils.cookiejar_from_dict(outcookie)
        s.headers = header

        r = s.get(challenge,params=param_challenge)
        strofr = str(r.content,encoding = 'UTF-8')
        strofr = strofr[7:-1]
        print(strofr)
        rdata = eval(strofr)

        result = logOP.call('getOutData',outdata,rdata)
        finaldict = {"callback":"jQuery"}
        finaldict.update(result)
        param_srun = {
            "callback":"jQuery",
            "action":"login",
            "username":userinfo['username'],
            "password":finaldict['password'],
            "ac_id":"1",
            "ip":"",
            "doublestack":"1",
            "info":finaldict['info'],
            "chksum":finaldict['chksum'],
            "n":"200",
            "type":"1",
            "_":time+1
        }
        print(param_srun)

        r2 = s.get(srun,params=param_srun)
        print(r2.url)
        print(r2.content)

    ipv4_challenge = "https://auth4.tsinghua.edu.cn/cgi-bin/get_challenge"
    ipv4_srun = "https://auth4.tsinghua.edu.cn/cgi-bin/srun_portal"
    ipv4 = auth(ipv4_challenge,ipv4_srun)

    ipv6_challenge = "https://auth6.tsinghua.edu.cn/cgi-bin/get_challenge"
    ipv6_srun = "https://auth6.tsinghua.edu.cn/cgi-bin/srun_portal"
    ipv6 = auth(ipv6_challenge,ipv6_srun)