import tunet

def login(info):
    # 1为成功，其他为错误信息
    try:
        if info['auth'] == 0:
            ret = tunet.net.login(info['username'],info['password'])
            if ret['msg'] == 'Login is successful.':
                return 1
            else:
                return ret['msg']
        elif info['auth'] == 1:
            ret = tunet.auth4.login(info['username'], info['password'], net=True)
            if ret['ecode']==0:
                return 1
            else:
                return ret['error']
        elif info['auth'] == 2:
            ret = tunet.auth6.login(info['username'], info['password'], net=True)
            if ret['ecode'] == 0:
                return 1
            else:
                return ret['error']
    except Exception as e:
         return str(e)

def checklogin(info):
    # 0为未认证，1为已认证
    try:
        ret={}
        if info['auth'] == 0:
            ret=tunet.net.checklogin()
        elif info['auth'] == 1:
            ret=tunet.auth4.checklogin()
        elif info['auth'] == 2:
            ret=tunet.auth6.checklogin()

        if 'username' in ret.keys():
            return 1
        else:
            return 0
    except Exception as e:
         return str(e)

def logout(info):
    # 1为成功，其他为错误信息
    try:
        if info['auth'] == 0:
            ret=tunet.net.logout()
            if ret['msg'] == 'Logout is successful.':
                return 1
            else:
                return ret['msg']
        elif info['auth'] == 1:
            ret=tunet.auth4.logout()
            if ret['ecode']==0:
                return 1
            else:
                return ret['error']
        elif info['auth'] == 2:
            ret=tunet.auth6.logout()
            if ret['ecode']==0:
                return 1
            else:
                return ret['error']
    except Exception as e:
        return str(e)