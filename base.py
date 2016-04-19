#-*- coding: utf-8 -*-
#这是一份默认的handler，用于替换掉默认的模板引擎为mako。
import tornado.web
import os.path
import tornado.ioloop
import mako.lookup
import tornado.httpserver
import mako.template


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        template_path = self.get_template_path()
        self.lookup = mako.lookup.TemplateLookup(directories=[template_path], input_encoding='utf-8', output_encoding='utf-8')

    def render_string(self, template_path, **kwargs):
        try:
            _debug=self.get_argument("debug","false")
            template = self.lookup.get_template(template_path)
            namespace = self.get_template_namespace()
            namespace.update(kwargs)

            env_kwargs = dict(
                    handler = self,
                    request = self.request,
                    locale = self.locale,
                    static_url = self.static_url,
                    xsrf_form_html = self.xsrf_form_html,
                    reverse_url = self.application.reverse_url,

            )
            env_kwargs.update(kwargs)
            return template.render(**env_kwargs)
        except Exception as e:
            print("服务端错误")
            print(e)

    def render(self, template_path, **kwargs):
        self.finish(self.render_string(template_path,**kwargs))

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return None
        else:
            return user
