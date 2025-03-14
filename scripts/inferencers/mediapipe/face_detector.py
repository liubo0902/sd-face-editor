from typing import List

import mediapipe as mp
import numpy as np
from PIL import Image

from scripts.entities.rect import Rect
from scripts.use_cases.face_detector import FaceDetector


class MediaPipeFaceDetector(FaceDetector):
    def name(self) -> str:
        return "MediaPipe"

    def detect_faces(self, image: Image, conf: float = 0.01, **kwargs) -> List[Rect]:
        face_detection = mp.solutions.face_detection.FaceDetection(min_detection_confidence=conf)
        results = face_detection.process(np.array(image.convert("RGB")))

        width = image.width
        height = image.height
        rects: List[Rect] = []

        if not results.detections:
            return rects

        for d in results.detections:
            relative_box = d.location_data.relative_bounding_box
            left = int(relative_box.xmin * width)
            top = int(relative_box.ymin * height)
            right = int(left + (relative_box.width * width))
            bottom = int(top + (relative_box.height * height))
            rects.append(Rect(left, top, right, bottom))
        return rects
