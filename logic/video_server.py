import cv2
from threading import Thread, Lock
import os
import json
import time

class Frame:
    def __init__(self, cam_id, frame):
        self.cam_id = cam_id
        self.frame = frame

    def to_json(self):
        res = { 'cam_id': self.cam_id, 'frame': self.frame }
        return json.loads(res)



class VideoServer(Thread):
    def __init__(self, width: int = 1920, height: int = 1080):
        Thread.__init__(self)
        self._cameras = dict()
        self._camera_mutex = Lock()
        self._width = width
        self._height = height


    def exist_camera(self, cam_id: int):
        return cam_id in self._cameras.keys() and os.path.exists("/dev/video" + str(cam_id))

    
    def get_frames(self):
        res = []
        self._camera_mutex.acquire()
        cam_keys = self._cameras.keys()
        self._camera_mutex.release()

        for cam_id in cam_keys:
            img, is_ok = self.get_image(cam_id)
            if is_ok:
                res.append(Frame(id, img))
        return res


    def get_image(self, cam_id):
        self._camera_mutex.acquire()
        if cam_id in self._cameras.keys() and os.path.exists("/dev/video" + str(cam_id)):
            _, img = self._cameras[cam_id].read()
            self._camera_mutex.release()
            return cv2.imencode(".jpg", img)[1].tostring(), True
        self._camera_mutex.release()
        return [], False


    def update_cam_list(self):
        self._camera_mutex.acquire()

        dev_files: list = os.listdir('/dev/')
        video_src_names = list(filter(lambda x: x.startswith('video'), dev_files))
        video_src_ids = [ int(x.replace('video', '')) for x in video_src_names]

        add_list = list(set(video_src_ids) - set(self._cameras.keys()))
        remove_list = list(set(self._cameras.keys()) - set(video_src_ids))
        
        for cam_id in remove_list:
            self._cameras.pop(cam_id)
        for cam_id in add_list:
            print('add camera', cam_id)
            camera = cv2.VideoCapture(cam_id)
            cv2.VideoCapture.set(camera, cv2.CAP_PROP_FRAME_WIDTH, self._width)
            cv2.VideoCapture.set(camera, cv2.CAP_PROP_FRAME_HEIGHT, self._height)
            self._cameras[cam_id] = camera

        self._camera_mutex.release()


    def run(self):
        while True:
            self.update_cam_list()
            time.sleep(1)
