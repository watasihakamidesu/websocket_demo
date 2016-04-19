mako + tornado

websocket
├── base.py             渲染mako的handler
├── server.py           后台事件
├── static              网站css和js
│   ├── chat.css
│   ├── chat.js         里面js有websocket操作
│   └── jquery.min.js
├── templates           里面是模板
│   ├── index.mako      聊天模板
│   ├── login.mako      登录模板
│   └── rooms.mako      房间选择模板
├── test.txt 		说明文件
└── test_websocket.py   测试脚本
