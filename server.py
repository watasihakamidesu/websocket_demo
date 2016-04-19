#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""

import logging
import os.path
import collections
from functools import reduce

import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.websocket
from tornado.options import define, options
from tornado.httpserver import HTTPServer

from base import BaseHandler

define("port", default=8888, help="run on the given port", type=int)




class LoginHandler(BaseHandler):
    "登录:记住名字"
    def get(self):
        if self.current_user:
            self.redirect("/rooms")
        else:
            self.render("login.mako")

    def post(self):
        name = self.get_argument("name", "admin")
        self.set_secure_cookie("user", name)
        self.redirect("/rooms")


class RoomsHandler(BaseHandler):
    "选择房间,num是房间数量"
    @tornado.web.authenticated
    def get(self):
        self.render("rooms.mako", num=5)


class MainHandler(BaseHandler):
    "id是房间号,cache是缓存"
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id",None)
        self.render("index.mako",messages=[c for c in ChatSocketHandler.cache if c["type"]=="0" or c["id"]==id], id=id, name=self.current_user.decode("ascii"))


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    "websocket处理函数"
    waiters = collections.defaultdict(set) #连接池
    cache = list()  #历史记录
    cache_size = 200 #历史记录长度

    def open(self):
        "websocket建立连接"
        self.name = self.get_argument("name","admin")
        self.id = self.get_argument("id",1)
        ChatSocketHandler.waiters[self.id].add(self)
        self.on_message('{"body":"welcome '+self.name+'","type":"1"}',cache=False)

    def on_close(self):
        "websocket关闭连接"
        ChatSocketHandler.waiters[self.id].remove(self)
        self.on_message('{"body":"exit !","type":"1"}',cache=False)

    @classmethod
    def update_cache(cls, chat):
        "更新缓存"
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache.pop(0)

    @classmethod
    def send_updates(cls, chat, cache):
        "按照type发个不同用户"
        logging.info("当前用户 %d ", len([waiter for x in cls.waiters.values() for waiter in x ]))
        if chat["type"] == "2":
            if chat["user"]:
                i = [waiter for waiter in cls.waiters[chat["id"]] if waiter.name==chat["user"]]
                if i:
                    chat["typename"] = "私密"
                    my = chat.pop("my")
                    i[0].write_message(chat)
                    my.write_message(chat)
                else:
                    my = chat.pop("my")
                    chat["typename"] = "系统"
                    chat["body"] = "没有用户"
                    my.write_message(chat)

            else:
                my = chat.pop("my")
                chat["typename"] = "系统"
                chat["body"] = "没有输入用户名"
                my.write_message(chat)
        else:
            if chat["type"] == "0":
                chat["typename"] = "所有"
                #users = reduce(lambda x,y: x | y,cls.waiters.values())
                #list(map(lambda waiter: waiter.write_message(chat), users))
                [waiter.write_message(chat) for x in cls.waiters.values() for waiter in x ]
            elif chat["type"] == "1":
                chat["typename"] = "当前"
                list(map(lambda waiter: waiter.write_message(chat), cls.waiters[chat["id"]]))
            if cache:
                tornado.ioloop.IOLoop.instance().add_callback(ChatSocketHandler.update_cache, chat)


    @tornado.gen.coroutine
    def on_message(self, message, cache=True):
        "websocket 客户端发消息时候"
        if message:
            parsed = tornado.escape.json_decode(message)
            parsed["id"] = self.id
            parsed["name"] = self.name
            if parsed["type"] == "2":
                parsed["my"] = self
            tornado.ioloop.IOLoop.instance().add_callback(ChatSocketHandler.send_updates, parsed, cache)


class Application(tornado.web.Application):
    "路由和server配置"
    def __init__(self):
        handlers = [
                (r"/", MainHandler),
                (r"/rooms", RoomsHandler),
                (r"/chatsocket", ChatSocketHandler),
                (r"/login", LoginHandler),
                ]
        settings = dict(
                cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies=True,
                login_url="/login",
                )
        super(Application, self).__init__(handlers, **settings)


def main():
    tornado.options.parse_command_line()
    app = Application()
    server = HTTPServer(app)
    server.bind(options.port)
    num = 1 #多进程
    server.start(num)
    logging.info('服务器已经运行 访问http://127.0.0.1:%s/' % options.port)
    logging.info('退出服务器按 Control-C')
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
