import cv2
import os
import tornado
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop
from logic.video_server import VideoServer, Frame


class ServerApp(Application):
    def __init__(self, cam_server):
        handlers = [
        (r"/", MainHandler),
        (r"/cam_server1", CameraHandler, dict(cam_server=cam_server, cam_id=0)),
        (r"/cam_server2", CameraHandler, dict(cam_server=cam_server, cam_id=1)),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        )
        Application.__init__(self, handlers, **settings)



class MainHandler(RequestHandler):
    async def get(self):
        self.render('index.html')



class CameraHandler(WebSocketHandler):
    def initialize(self, cam_server: VideoServer, cam_id: int):
        self.cam_server: VideoServer = cam_server
        self.cam_id = cam_id
        self._ioloop = tornado.ioloop.IOLoop.current()

    def open(self):
        print("connection opened", self.cam_id)
        self._ioloop.call_later(0.001, self.loop)


    def loop(self):
        if self.cam_server.exist_camera(self.cam_id):
            img, is_ok = self.cam_server.get_image(self.cam_id)
            if is_ok:
                self.write_message(img, binary=True)
        self._ioloop.call_later(0.001, self.loop)


def main():
    cam_server = VideoServer()
    cam_server.setDaemon(True)
    cam_server.start()
    app = ServerApp(cam_server)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()