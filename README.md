# API測試項目

## 下載Repo
`$ git clone https://github.com/Kouei-Lin/my-python-api`

## 進文件夾
`$ cd my-python-api`


`$ cd add_api`

## Server 安裝套件

`$ pip install -r requirements.txt`

[沒Python於此下載](https://www.python.org/downloads/)

## Server 跑項目
`$ python3 app.py`

## Server .env
如果有`.env_example`則需要編輯各項目所需`.env`

`$ cp .env_example .env`

`$ vim .env`

## Client 跑指令
複製貼上`command.txt`中的範例指令，`IP`改成伺服器，執行。


## Systemd排程
`/etc/systmed/system`，建立`xxx.service`。

```
[Unit]
Description=My Python App Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/your/folder
ExecStart=/usr/bin/python3 /path/to/your/folder/app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

`sudo systemd enable xxx.service`
