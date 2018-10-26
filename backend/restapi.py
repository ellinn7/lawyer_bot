import os.path
import BackEnd.tornado.auth as TornadoAuth
import BackEnd.tornado.httpserver as TornadoServer
import BackEnd.tornado.ioloop as TornadoIoloop
import BackEnd.tornado.options as TornadoOptions
import BackEnd.tornado.web as TornadoWeb
import unicodedata
import random
import string

from BackEnd.tornado.options import define, options

define("port", default=8080, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1", help="api database host")
define("mysql_database", default="tornado_api", help="tornado_api database name")
define("mysql_user", default="root", help="tornado_api database user")
define("mysql_password", default="", help="tornado_api database password")


class Application(TornadoWeb.Application):
    def __init__(self):
        handlers = [
            (r"/demo", IndexHandler),
            (r"/upload/", DocsVerification)
        ]
        settings = dict(
            #autoescape=None,
        )
        TornadoWeb.Application.__init__(self, handlers, **settings)

class IndexHandler(TornadoWeb.RequestHandler):
    def get(self):
        self.render("TPL/upload_form.html")

class DocsVerification(TornadoWeb.RequestHandler):
    def post(self):
        try:
            print("Get Etalon Document")
            etalonDocument = self.request.files['etalonDocument'][0]
            if etalonDocument['filename'] == '':
                return self.write({"success":False})
            original_fname = etalonDocument['filename']
            extension = os.path.splitext(original_fname)[1]
            filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
            final_filename = filename + extension
            output_file = open("uploads/" + final_filename, 'wb')
            output_file.write(etalonDocument['body'])

            print("Get Compared Document")
            comparedDocument = self.request.files['comparedDocument'][0]
            if not comparedDocument or not len(comparedDocument):
                return self.write({"success":False})
            original_fname = comparedDocument['filename']
            extension = os.path.splitext(original_fname)[1]
            filename = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
            final_filename = filename + extension
            output_file = open("uploads/" + final_filename, 'wb')
            output_file.write(comparedDocument['body'])

            print("Start to veryfing documents")

            fname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
            resultDocument = fname + extension

            self.write({"success": True, "resultDocument": resultDocument})
        except Exception as ex:
            print(ex)
            self.write({"success": False})

def main():
    TornadoOptions.parse_command_line()
    http_server = TornadoServer.HTTPServer(Application())
    http_server.listen(options.port)
    TornadoIoloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()