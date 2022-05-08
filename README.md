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

## 如何使用
1. 运行上方命令启动镜像
2. 查看容器实时日志（也可以在运行上面启动镜像命令时先去掉 -d 参数），若发现提示 python 安装完成建议重启则可以 exec 进入容器运行 `wine python -m pip` 检查 pip 是否正常（参考 run.py 文件内 run_hook 方法），如果不正常建议重启容器
3. 若发现 pip 已经可以正常使用并且 `ComWeChatRobot/Python/requirements.txt` 中的依赖均已安装成功可以进行下一步操作
4. vnc 连接上容器登陆微信
5. exec 进入容器运行 `wine python Z:\\Python\\test.py` 文件进行测试（如果能用可以修改 `/Python/test.py` 主函数测试其他功能是否正常）



## Known Issues
当前我测试时容器内 wine 用 python 调用 wxRobot 会提示内存不足，暂未发现解决方法。

wine 内也无法安装 .net framework 4.7.2 ，不知道上面提示内存不足是不是与此有关。

另外在初次运行镜像给 wine 内安装 python 时可能也会出现一些问题，需要重启一次或多次容器（建议 docker exec 进入容器测试 pip 等依赖是否正常）
