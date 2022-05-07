#!/usr/bin/python3
import subprocess, os, signal, datetime


class DockerWechatHook:
    def __init__(self):
        signal.signal(signal.SIGINT, self.now_exit)
        signal.signal(signal.SIGHUP, self.now_exit)
        signal.signal(signal.SIGTERM, self.now_exit)

    def now_exit(self, signum, frame):
        self.exit_container()

    def run_vnc(self):
        # 根据VNCPASS环境变量生成vncpasswd文件
        os.makedirs('/root/.vnc', mode=755, exist_ok=True)
        passwd_output = subprocess.run(['/usr/bin/vncpasswd','-f'],input=os.environ['VNCPASS'].encode(),capture_output=True)
        with open('/root/.vnc/passwd', 'wb') as f:
            f.write(passwd_output.stdout)
        os.chmod('/root/.vnc/passwd', 0o700)
        self.vnc = subprocess.Popen(['/usr/bin/vncserver','-localhost',
            'no', '-xstartup', '/usr/bin/openbox' ,':5'])

    def run_wechat(self):
        # if not os.path.exists("/wechat_installed.txt"):
        #     self.wechat = subprocess.run(['wine','WeChatSetup.exe'])
        #     with open("/wechat_installed.txt", "w") as f:
        #         f.write("True\n")
        self.wechat = subprocess.run(['wine','/home/user/.wine/drive_c/Program Files/Tencent/WeChat/WeChat.exe'])

    def run_hook(self):
        if not os.path.exists("/home/user/.wine/drive_c/python3/python.exe"):
            print("当前 wine 内没有安装 python，正在安装中...")
            self.reg_hook = subprocess.run(['wine','python-3.8.10.exe', '/quiet', 'TargetDir=C:\\python3', 'Include_debug=1', 'Include_symbols=1'])
            # 安装完成 python 后建议重启一次容器，目前发现在部分情况下安装完成 python 后无法使用 pip ，重启容器后就好
            print("安装完成 python 后建议重启一次容器，目前发现在部分情况下 wine 安装完成 python 后无法使用 pip ，重启容器后就好")

        if "No module named pip" in str(subprocess.run(['wine', 'python', '-m', 'pip', '-V'], capture_output=True).stdout):
            print("正在 wine 内安装 pip ...")
            self.reg_hook = subprocess.run(['wine','python', '-m', 'ensurepip'])
            # 安装完成 python 后建议重启一次容器，目前发现在部分情况下安装完成 python 后无法使用 pip ，重启容器后就好
            print("安装完成 pip.exe 后建议重启一次容器，目前发现在部分情况下安装完成 python 后无法使用 pip ，重启容器后就好")

        if "comtypes" not in str(subprocess.run(['wine', 'python', '-m', 'pip', 'list'], capture_output=True).stdout):
            print("正在 wine 内安装 wxRobot 依赖...")
            self.reg_hook = subprocess.run(['wine', 'python', '-m', 'pip', 'install', '-r', 'Z:\\Python\\requirements.txt'])
            print("python 环境安装完成！建议重启一次容器！")
        self.reg_hook = subprocess.Popen(['wine','Release/CWeChatRobot.exe', '/regserver'])

    def exit_container(self):
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' 正在退出容器...')
        try:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' 退出Hook程序...')
            os.kill(self.reg_hook.pid, signal.SIGTERM)
        except:
            pass
        try:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' 退出微信...')
            os.kill(self.wechat.pid, signal.SIGTERM)
        except:
            pass
        try:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' 退出VNC...')
            os.kill(self.vnc.pid, signal.SIGTERM)
        except:
            pass

    def run_all_in_one(self):
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' 启动容器中...')
        self.run_vnc()
        self.run_hook()
        self.run_wechat()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ' 启动完成.')


if __name__ == '__main__' :
    print('---All in one 微信Hook容器---')
    hook = DockerWechatHook()
    hook.run_all_in_one()