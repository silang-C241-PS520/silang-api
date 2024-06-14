import math
import os
import tempfile
from os.path import dirname, abspath, join
from pathlib import Path
from typing import Tuple

import aiofiles as aiofiles
from fastapi import UploadFile
import mediapipe as mp
import cv2
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import numpy as np

model_path = join(dirname(dirname(abspath(__file__))), 'resource', 'test_video8.h5')
model = tf.keras.models.load_model(model_path, )
model.summary()

dirs_path = join(dirname(dirname(abspath(__file__))), 'resource', '60_words.txt')
dirs = open(dirs_path, 'r').read().split('\n')
dirs.sort()

enc = LabelEncoder()
labels = enc.fit_transform(dirs)
labels = tf.keras.utils.to_categorical(labels)

holistic = mp.solutions.holistic.Holistic(static_image_mode=False,
                                          smooth_segmentation=True,
                                          refine_face_landmarks=False,
                                          min_detection_confidence=0.5,
                                          min_tracking_confidence=0.5)


class MLServices:
    def __init__(self):
        self.model = model
        self.dirs = dirs
        self.holistic = holistic
        self.temp_file_path = ""

    def do_translation(self, file: UploadFile) -> str:
        # TODO
        self._save_file_tmp(file)
        print("temp file: ", self.temp_file_path)
        cap = cv2.VideoCapture(self.temp_file_path)

        if not cap.isOpened():
            raise ValueError("Error opening video file.")

        fps = cap.get(cv2.CAP_PROP_FPS)

        frames = self._get_frames(cap)
        cap.release()

        reduced_frames = self._reduce_frames(frames, fps)
        print("reduced frames: ", len(reduced_frames))

        translation_text = self._predict(reduced_frames)

        return translation_text

    def _save_file_tmp(self, file: UploadFile):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(file.file.read())
            self.temp_file_path = temp_file.name
            file.file.seek(0)
            print("temp file path: ", self.temp_file_path)

    def _get_frames(self, cap):
        frames = []
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frames.append(frame)

        return frames

    def _reduce_frames(self, frames, fps):
        new_frames = []
        for i in range(0, len(frames), math.floor(fps / 14)):
            new_frames.append(frames[i])

        return new_frames

    def _predict(self, frames):
        results = []
        j = 0
        for i in range(14, len(frames)):
            res = frames[j:i]
            res = self._preprocessing(res)
            res = np.array(res, dtype='float32')
            res = np.expand_dims(res, axis=0)
            result = self.model.predict(res, verbose=0)[0]
            i = np.argmax(result)
            mx = result[i]
            if mx > 0.9:
                results.append(enc.inverse_transform([i])[0])
        print("results: ", results)
        return " ".join(results)

    def _preprocessing(self, frames):
        # TODO
        frames = np.array(frames)
        mediapipe_preprocessed_data = []
        for frame in frames:
            image, results = self._mediapipe_detection(frame, self.holistic)
            landmarks = []
            if results.right_hand_landmarks is not None:
                for landmark in results.right_hand_landmarks.landmark:
                    landmarks = landmarks + [landmark.x, landmark.y, landmark.z]
            else:
                landmarks = landmarks + [0, 0, 0] * 21

            if results.left_hand_landmarks is not None:
                for landmark in results.left_hand_landmarks.landmark:
                    landmarks = landmarks + [landmark.x, landmark.y, landmark.z]
            else:
                landmarks = landmarks + [0, 0, 0] * 21

            if results.pose_landmarks is not None:
                nose_landmark = results.pose_landmarks.landmark[0]
                nose_landmarks = [nose_landmark.x, nose_landmark.y, nose_landmark.z] * 59
                for i in range(0, 17):
                    landmark = results.pose_landmarks.landmark[i]
                    landmarks = landmarks + [landmark.x, landmark.y, landmark.z]
            else:
                nose_landmarks = [0, 0, 0] * 59
                landmarks = landmarks + [0, 0, 0] * 17
            mediapipe_preprocessed_data.append(np.array(landmarks) - np.array(nose_landmarks))
        return mediapipe_preprocessed_data

    def _mediapipe_detection(self, image, holistic_model):
        # TODO
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
        image.flags.writeable = False  # Image is no longer writable
        results = holistic_model.process(image)  # Make prediction
        image.flags.writeable = True  # Image is now writable
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR CONVERSION RGB 2 BGR
        return image, results
