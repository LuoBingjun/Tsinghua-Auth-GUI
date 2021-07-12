import sys
import os
import threading
import json
import net
import MainWindow
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
        timer.cancel()
        if config['general']['save'] == False:
            config['info']['username'] = ''
            config['info']['password'] = ''
        save_settings()
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
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
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
    ui.statusBar.showMessage('状态：正在登录中')
    ret = net.login(config['info'])
    if ret == 1:
        ui.statusBar.showMessage('状态：登录成功')
    else:
        ui.statusBar.showMessage('错误：' + ret)


def logout():
    ui.checkBox_2.setChecked(False)
    ret = net.logout(config['info'])
    if ret == 1:
        ui.statusBar.showMessage('状态：断开成功')
    else:
        ui.statusBar.showMessage('错误：' + ret)


def attempt_to_login():
    ret = net.checklogin(config['info'])
    if ret == 1:
        ui.statusBar.showMessage('状态：在线')
    elif ret == 0:
        ui.statusBar.showMessage('状态：离线')
        if config['general']['automode'] == True:
            login()
    else:
        ui.statusBar.showMessage('错误：' + ret)

    global timer
    timer = threading.Timer(10, attempt_to_login)
    timer.start()


def sync_settings():
    config['info']['auth'] = ui.comboBox.currentIndex()
    config['info']['username'] = ui.lineEdit.text()
    config['info']['password'] = ui.lineEdit_2.text()
    config['general']['save'] = str(ui.checkBox.isChecked())
    config['general']['automode'] = str(ui.checkBox_2.isChecked())


def save_settings():
    with open("config.json", "w") as f:
        json.dump(config, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    if(os.path.exists("config.json")):
        with open("config.json", 'r') as config_f:
            config = json.load(config_f)
    else:
        config = {
            'info': {
                'auth': 0,
                'username': '',
                'password': ''
            },
            'general': {
                'save': False,
                'automode': False
            }
        }

    app = QApplication(sys.argv)
    mainWindow = AuthWindow()
    ui = MainWindow.Ui_MainWindow()
    ui.setupUi(mainWindow)

    for i in ['net', 'auth4', 'auth6']:
        ui.comboBox.addItem(i)
    ui.comboBox.setCurrentIndex(config['info']['auth'])
    ui.lineEdit.setText(config['info']['username'])
    ui.lineEdit_2.setText(config['info']['password'])
    ui.checkBox.setChecked(config['general']['save'] == True)
    ui.checkBox_2.setChecked(config['general']['automode'] == True)

    ui.comboBox.currentIndexChanged.connect(sync_settings)
    ui.lineEdit.textChanged.connect(sync_settings)
    ui.lineEdit_2.textChanged.connect(sync_settings)
    ui.checkBox.stateChanged.connect(sync_settings)
    ui.checkBox_2.stateChanged.connect(sync_settings)

    ui.pushButton.clicked.connect(
        lambda: threading.Thread(target=login).start())
    ui.pushButton_2.clicked.connect(
        lambda: threading.Thread(target=logout).start())

    timer = threading.Timer(10, attempt_to_login)
    timer.start()

    mainWindow.show()
    sys.exit(app.exec_())
