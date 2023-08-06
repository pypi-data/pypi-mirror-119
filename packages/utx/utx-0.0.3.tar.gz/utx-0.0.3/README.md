# UTX


## 安装
- 命令行执行
```
pip install utx
```


## 设计理念

很大程度上借鉴了HttpRunner（优秀的框架）。不同的是，utx更着重写python，而不是写YAML文件。

- 简单是更好的
- 每个人都能用python写自动化

这就是utx的设计理念。


## 项目结构
![](https://files.mdnice.com/user/17535/555b68ce-bc10-472b-a904-b0b17203f58a.png)

- utx提供了快速创建项目的能力，也就是脚手架。
```shell
utx startproject project_name
```
```
$ utx startproject demo
2021-09-01 12:39:16.491 | INFO     | utx.cli.scaffold:create_scaffold:51 - Create new project: demo
Project root dir: /PycharmProjects/demo

Created folder: demo
Created folder: demo/config
Created folder: demo/logs
Created folder: demo/packages
Created folder: demo/report/airtest
Created folder: demo/tests
Created folder: demo/suites
Created file: demo/.gitignore
Created file: demo/conftest.py
Created file: demo/pytest.ini
Created file: demo/run.py
Created file: demo/requirements.txt
Created file: demo/config/conf.py
Created file: demo/config/config.ini
Created file: demo/config/__init__.py
Created file: demo/tests/test_devices.py
Created file: demo/tests/__init__.py
Created file: demo/report/summary_template.html

```


## 专注于写脚本

- 项目结构很清晰。在conftest.py进行一些初始化/参数化/清理工作，在suites/写测试脚本。
>在AirtestIDE中写好.air脚本，然后将文件放到suites文件中。
- 更注重平铺写脚本的方式，这样就离“每个人都能用python写自动化”更近一步。毕竟封装之后看着容易晕，我也晕。
- 去除掉框架的约束，给每个人写python的自由，在测试脚本里你可以尽情发挥你的代码风格，代码能力，千人千面。代价呢，就是代码质量参差不齐。

大胆写，能写，写出来，跑通，就已经是在写自动化，就已经是在创造价值了！


## 轻封装

utx尊重原生用法。

airtest的封装只通过装饰器进行了运行方式的调整，没有做任何其他的冗余修改。

- faker，造数据工具
- pytest，测试框架
- airtest，自动化测试工具
- pandas、numpy，数据处理工具

安装utx，自动就把这些开源利器安装上了，无需单独安装。未来会集成更多实用工具到utx中。

utx本身是很轻的。



## 使用说明

- 只需在配置文件中填好相关内容，即可运行！
```
[device_info]
device = 10.237.224.160:5555
platform = android

[app_info]
package = com.longfor.yts.test
filename = AP_1.0.5.2108261134_pre.apk

[mode]
is_all = 0

[suites]
cases = test.air


```
- 启动命令
1. 普通启动
```
python run.py
```
2. 参数化启动
```
python run.py --platform=Android --device=127.0.0.1:5555
```
>参数优先级大于配置文件

## 运行结果
- 报告展示

![](https://files.mdnice.com/user/17535/29b7a536-9e30-45e3-b7ed-727a2091b910.png)
