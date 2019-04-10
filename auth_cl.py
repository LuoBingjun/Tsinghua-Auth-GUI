import sys, os, threading, json, signal
import net

online=False

def save_config():
  with open("config.json", "w") as f:
    json.dump(config, f, sort_keys=True, indent=4, separators=(',', ': '))

def first_config():
  print('未检测到config.json！')
  while True:
    str=input('请输入认证服务器类型：0-net 1-auth4 2-auth6\n')
    if int(str) in [0,1,2]:
      config['info']['auth']=int(str)
      break
  config['info']['username']=input('请输入用户名：\n')
  config['info']['password']=input('请输入密码：\n')
  save_config()
  print('设置成功')

def login():
    print('状态：正在登录中')
    ret = net.login(config['info'])
    if ret == 1:
        print('状态：登录成功')
    else:
        print('错误：' + ret)

def attempt_to_login():
    if net.checklogin(config['info'] and online==False):
      online=True
      print('状态：在线')
    else:
      print('状态：离线')
      if config['general']['automode']=='True':
        login()

    global timer
    timer = threading.Timer(10, attempt_to_login)
    timer.start()


if __name__ == '__main__':
  if(os.path.exists("config.json")):
    with open("config.json", 'r') as config_f:
      config = json.load(config_f)
  else:
    config={
            'info':{
                'auth':0,
                'username':'',
                'password':''
            },
            'general':{
                'save':True,
                'automode':True
            }
    }
    first_config()
  
  print('开始自动认证')
  timer = threading.Timer(10, attempt_to_login)
  timer.start()
        