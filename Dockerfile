FROM docker.io/zixia/wechat:3.3.0.115

USER root
WORKDIR /

ENV WINEPREFIX=/home/user/.wine \
    LANG=zh_CN.UTF-8 \
    LC_ALL=zh_CN.UTF-8 \
    DISPLAY=:5 \
    VNCPASS=YourSafeVNCPassword


EXPOSE 5905


RUN apt update &&  \
    apt install wget -y && \
    apt autoremove -y && \
    apt clean && \
    rm -fr /tmp/*

RUN apt update && \
    apt --no-install-recommends install winbind samba tigervnc-standalone-server tigervnc-common openbox -y && \
    wget --no-check-certificate -O /bin/dumb-init "https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64"


COPY run.py /run.py
COPY ComWeChatRobot/Python Python
# https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.6.0.18/WeChatSetup-3.6.0.18.exe
# COPY WeChatSetup-3.6.0.18.exe WeChatSetup.exe
# https://repo.anaconda.com/miniconda/Miniconda3-py37_4.11.0-Windows-x86.exe
# COPY Miniconda3-py37_4.11.0-Windows-x86.exe Miniconda3.exe
# https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe
COPY python-3.8.10.exe python-3.8.10.exe
# https://bootstrap.pypa.io/get-pip.py
# COPY get-pip.py get-pip.py
# .net FrameWork 4.7.2
# https://dotnet.microsoft.com/en-us/download/dotnet-framework/thank-you/net472-offline-installer
COPY ndp472-kb4054530-x86-x64-allos-enu.exe ndp472-kb4054530-x86-x64-allos-enu.exe
COPY wine/Tencent.zip /Tencent.zip
COPY wine/微信.lnk /home/user/.wine/drive_c/users/Public/Desktop/微信.lnk
COPY wine/system.reg  /home/user/.wine/system.reg
COPY wine/user.reg  /home/user/.wine/user.reg
COPY wine/userdef.reg /home/user/.wine/userdef.reg

RUN chmod a+x /bin/dumb-init && \
    chmod a+x /run.py && \
    rm -rf "/home/user/.wine/drive_c/Program Files/Tencent/" && \
    unzip Tencent.zip && \
    cp -rf /wine/Tencent "/home/user/.wine/drive_c/Program Files/" && \
    chown root:root -R /home/user/.wine && \
    rm -rf /wine/Tencent Tencent.zip && \
    apt autoremove -y && \
    apt clean && \
    rm -fr /tmp/*

# RUN wine Miniconda3.exe /InstallationType=JustMe /AddToPath=1 /RegisterPython=1 /S /D=C:\\Miniconda3
# RUN wine python-3.8.10.exe /quiet InstallAllUsers=1 TargetDir=C:\\python3 Include_debug=1 Include_symbols=1 

# RUN wine python -m pip install -r Z:\\Python\\requirements.txt

COPY ComWeChatRobot/Release /Release

ENTRYPOINT [ "/bin/dumb-init" ]
CMD ["/run.py", "start"]
