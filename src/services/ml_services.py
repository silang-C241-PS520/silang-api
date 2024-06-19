import math
import tempfile
import os
from os.path import dirname, abspath, join

from fastapi import UploadFile
import mediapipe as mp
import cv2
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import numpy as np

model_path = join(dirname(dirname(abspath(__file__))), 'resource', 'ml_model.h5')
model = tf.keras.models.load_model(model_path, )

dirs_path = join(dirname(dirname(abspath(__file__))), 'resource', 'words.txt')
file = open(dirs_path, 'r')
dirs = file.read().split('\n')
print(dirs)
file.close()

holistic = mp.solutions.holistic.Holistic(model_complexity=2,
                                          min_detection_confidence=0.5,
                                          min_tracking_confidence=0.5)


class MLServices:
    def __init__(self):
        self.model = model
        self.dirs = dirs
        self.holistic = holistic
        self.temp_file_path = ""

    def do_translation(self, file: UploadFile) -> str:
        self._save_file_tmp(file)

        cap = cv2.VideoCapture(self.temp_file_path)

        if not cap.isOpened():
            raise ValueError("Error opening video file.")

        frames = self._get_frames(cap)

        cap.release()

        translation_text = self._predict(frames)

        os.remove(self.temp_file_path)

        return translation_text

    def _save_file_tmp(self, file: UploadFile):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(file.file.read())
            self.temp_file_path = temp_file.name
            file.file.seek(0)

    def _get_frames(self, cap):
        frames = []
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frames.append(frame)

        return frames

    def _predict(self, frames):
        results = []
        i = 30
        j = 0
        while i <= len(frames):
            res = frames[j:i]
            res = self._preprocessing(res)
            res = np.array(res, dtype='float32')
            res = np.expand_dims(res, axis=0)
            result = self.model.predict(res, verbose=0)[0]
            index = np.argmax(result)
            print(index)
            print(result[index])

            j = i
            i += 30
            results.append(self.dirs[index])

        return " ".join(results)

    def _preprocessing(self, frames):
        frames = np.array(frames)
        mediapipe_processed_data = []
        for frame in frames:
            image, results = self._mediapipe_detection(frame, self.holistic)
            landmark_data = []

            pose_landmarks = results.pose_landmarks
            left_hand_landmarks = results.left_hand_landmarks
            right_hand_landmarks = results.right_hand_landmarks

            if pose_landmarks:
                base_x = pose_landmarks.landmark[0].x
                base_y = pose_landmarks.landmark[0].y
                base_z = pose_landmarks.landmark[0].z

                for landmark in pose_landmarks.landmark:
                    landmark_data.extend(
                        [landmark.x - base_x, landmark.y - base_y, landmark.z - base_z, landmark.visibility])
            else:
                landmark_data.extend([0] * (33 * 4))

            if left_hand_landmarks:
                base_x = left_hand_landmarks.landmark[0].x
                base_y = left_hand_landmarks.landmark[0].y
                base_z = left_hand_landmarks.landmark[0].z

                for landmark in left_hand_landmarks.landmark:
                    landmark_data.extend([landmark.x - base_x, landmark.y - base_y, landmark.z - base_z])
            else:
                landmark_data.extend([0] * (21 * 3))

            if right_hand_landmarks:
                base_x = right_hand_landmarks.landmark[0].x
                base_y = right_hand_landmarks.landmark[0].y
                base_z = right_hand_landmarks.landmark[0].z

                for landmark in right_hand_landmarks.landmark:
                    landmark_data.extend([landmark.x - base_x, landmark.y - base_y, landmark.z - base_z])
            else:
                landmark_data.extend([0] * (21 * 3))

            mediapipe_processed_data.append(landmark_data)

        return mediapipe_processed_data

    def _mediapipe_detection(self, image, holistic_model):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
        results = holistic_model.process(image)  # Make prediction
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR CONVERSION RGB 2 BGR
        return image, results
