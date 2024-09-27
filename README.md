本项目在Efficient Dynamic Proof of Retrievability for Cold Storage论文的基础上进行修改
# 需要的库文件
1. [NTL v11.5.1](http://www.shoup.net/ntl/download.html)

2. [ZeroMQ v4.8.1](https://github.com/zeromq/cppzmq/releases/tag/v4.8.1)

3. [Secp256k1](https://github.com/bitcoin-core/secp256k1/tree/423b6d19d373f1224fd671a982584d7e7900bc93) (**Note: checkout the correct branch as listed here**)

4. [Gnark-crypto v0.6.0](https://github.com/ConsenSys/gnark-crypto/releases/tag/v0.6.0)

一键安装脚本
```
sudo ./auto_setup.sh
```
或者可以在makefile中修改安装路径
```
porla/Makefile
```
# 构建和编译
KZG模式需要gnark-crypto库，使用go生成并放在/usr/lib下
```
go build -buildmode=c-shared -o libmultiexp.so main.go
```
使用make进行编译
```
make -j8
```
## 测试
在Server目录下创建三个子文件夹 **H_X**, **H_Y** and **U**. 

1. 启动 server:
```
$ cd porla/Server
$ ./Server
```
2. 启动 client:
```
$ cd porla/Client
$ ./Client
```

使用上面方式生成配置文件后在porla_app/app.py中修改文件路径

3. 启动后端
```
$ cd porla_app
$ pyhton app.py
```

