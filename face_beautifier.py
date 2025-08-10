# face_beautifier.py

import cv2
import mediapipe as mp
import numpy as np

class FaceBeautifier:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=2,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def beautify(self, image):
        results = self.face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h, w, _ = image.shape
                face_outline_idx = list(range(0, 468))
                points = []
                for idx in face_outline_idx:
                    pt = face_landmarks.landmark[idx]
                    x, y = int(pt.x * w), int(pt.y * h)
                    points.append((x, y))

                # 建立凸包 (convex hull) 當作完整遮罩
                hull = cv2.convexHull(np.array(points, dtype=np.int32))
                mask = np.zeros(image.shape[:2], dtype=np.uint8)
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (55, 55))
                mask = cv2.dilate(mask, kernel, iterations=1)
                mask = cv2.GaussianBlur(mask, (15, 15), 0)
                cv2.fillConvexPoly(mask, hull, 255)

                # 提取臉部區域
                face_area = cv2.bitwise_and(image, image, mask=mask)
                hsv = cv2.cvtColor(face_area, cv2.COLOR_BGR2HSV)

                # 提亮：提高飽和度與亮度
                h_, s, v = cv2.split(hsv)
                s = cv2.add(s, 15)  # 飽和度 +15
                v = cv2.add(v, 30)  # 亮度 +30
                s = np.clip(s, 0, 255)
                v = np.clip(v, 0, 255)
                enhanced_hsv = cv2.merge([h_, s, v])

                # 轉回 BGR
                brightened = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)

                # 將提亮的區域貼回原圖
                result = image.copy()
                result[mask == 255] = brightened[mask == 255]
                image = result
        return image
