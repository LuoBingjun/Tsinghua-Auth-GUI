import sys, threading, configparser
import MainWindow
import wireless, lan
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AuthWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AuthWindow, self).__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(":/ico/icon.ico"))
        ti = TrayIcon(self)
        ti.show()

    def closeEvent(self, event):
        if config['general']['save']=='False':
            config['info']['username']=''
            config['info']['password']=''
        save_settings()
        timer.cancel()
        event.accept()

    def changeEvent(self, event):
        if self.isMinimized():
            self.hide()

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.showMenu()
        self.activated.connect(self.iconClicked)
        self.setIcon(QIcon(":/ico/icon.ico"))
        self.icon = self.MessageIcon()

    def showMenu(self):
        self.menu = QMenu()
        self.showAction = QAction("显示/隐藏", self, triggered=self.actionClicked)
        self.quitAction = QAction("退出", self, triggered=self.quit)
        self.menu.addAction(self.showAction)
        self.menu.addAction(self.quitAction)
        self.setContextMenu(self.menu)

    def iconClicked(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            pw = self.parent()
            if pw.isVisible():
                pw.hide()
            else:
                pw.showNormal()

    def actionClicked(self):
        pw = self.parent()
        if pw.isVisible():
            pw.hide()
        else:
            pw.showNormal()

    def quit(self):
        self.parent().close()

def login():
    ui.statusBar.showMessage('正在连接')
    result = wireless.login(config['info'])
    if result == 1:
        ui.statusBar.showMessage('连接成功')
    elif result == 2:
        ui.statusBar.showMessage('您已在线了')
    elif result==3:
        ui.statusBar.showMessage('用户名或密码错误')
    else:
        ui.statusBar.showMessage('连接失败')

def logout():
    ui.checkBox_2.setChecked(False)
    result = wireless.logout()
    if result == 1:
        ui.statusBar.showMessage('断开成功')
    elif result == 2:
        ui.statusBar.showMessage('您不在线上')
    else:
        ui.statusBar.showMessage('断开失败')

def attempt_to_login():
    if config['general']['automode']=='True':
        result, data = wireless.networktest()
        if result==0:
            ui.statusBar.showMessage('状态：未连接到网络')
        elif result==1:
            login()
        elif result==2:
            ui.statusBar.showMessage('状态：在线 本月已用流量：%.2f GB' % (data))
        elif result == 3:
            ui.statusBar.showMessage('状态：未在校园网内')
    global timer
    timer = threading.Timer(10, attempt_to_login)
    timer.start()

def sync_settings():
    config['info']['username']=ui.lineEdit.text()
    config['info']['password']=ui.lineEdit_2.text()
    config['general']['save']=str(ui.checkBox.isChecked())
    config['general']['automode']=str(ui.checkBox_2.isChecked())

def save_settings():
    with open("settings.ini", 'w') as configfile:
        config.write(configfile)

if __name__ == '__main__':
    config=configparser.ConfigParser()
    config.read("settings.ini")

    app = QApplication(sys.argv)
    mainWindow = AuthWindow()
    ui = MainWindow.Ui_MainWindow()
    ui.setupUi(mainWindow)

    ui.lineEdit.setText(config['info']['username'])
    ui.lineEdit_2.setText(config['info']['password'])
    ui.checkBox.setChecked(config['general']['save']=='True')
    ui.checkBox_2.setChecked(config['general']['automode'] == 'True')

    ui.lineEdit.textChanged.connect(sync_settings)
    ui.lineEdit_2.textChanged.connect(sync_settings)
    ui.checkBox.stateChanged.connect(sync_settings)
    ui.checkBox_2.stateChanged.connect(sync_settings)
    ui.pushButton.clicked.connect(lambda: threading.Thread(target=login).start())
    ui.pushButton_2.clicked.connect(lambda: threading.Thread(target=logout).start())

    timer = threading.Timer(5, attempt_to_login)
    timer.start()

    mainWindow.show()
    sys.exit(app.exec_())