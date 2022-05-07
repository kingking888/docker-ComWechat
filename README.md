# docker-ComWechat
A docker image for [ComWeChatRobot](https://github.com/ljc545w/ComWeChatRobot)


``` shell
docker run \
    --name comwechat  \
    -p 5905:5905 \
    -e VNCPASS=asdfgh123 \
    -dti  \
    --ipc=host \
    --privileged \
    -v $(pwd)/volume/WeChat\ Files/:'/home/user/.wine/drive_c/users/user/My Documents/WeChat Files/'  \
    -v $(pwd)/volume/Application\ Data:'/home/user/.wine/drive_c/users/user/Application Data/' \
    -v $(pwd)/volume/python3/:/home/user/.wine/drive_c/python3/ \
    tomsnow1999/docker-com_wechat_robot
```


## Issue
当前容器内 wine 用 python 调用 wxRobot 会提示内存不足，暂未发现解决方法。

wine 内也无法安装 .net framework 4.7.2 ，不知道上面提示内存不足是不是与此有关。

另外在初次运行镜像安装 python 时也会出现一些问题，需要重启一次或多次容器（建议 docker exec 进入容器测试 pip 等依赖是否正常）
