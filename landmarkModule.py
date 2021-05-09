import paddlehub as hub

class landmarker():
    def __init__(self,debug=False):
        self.face_landmark = hub.Module(name="face_landmark_localization")
        self.debug=debug
    def run(self, img):
        landmarks = []
        # print('begin baidu landmark')
        results = self.face_landmark.keypoint_detection(images=[img],
                                                        paths=None,
                                                        batch_size=1,
                                                        use_gpu=False,
                                                        output_dir='face_landmark_output',
                                                        visualization=self.debug)
        # print('emoi baidu landmark',landmarks)
        for result in results:
            landmarks = result['data']
            break  # one pic one result
        # print('emoi baidu landmark', landmarks[0], len(landmarks[0]))
        return landmarks