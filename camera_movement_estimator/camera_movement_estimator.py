import sys
import os
import pickle
import cv2
import numpy as np

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Correct way to import from parent directory using resource_path
utils_path = resource_path("..")
sys.path.insert(0, utils_path)
from utils import measure_distance, measure_xy_distance


class CameraMovementEstimator:
    def __init__(self, frame):
        self.minimum_distance = 5

        self.lk_params = dict(
            winSize = (15,15),
            maxLevel = 2,
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        ) 

        first_frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask_features = np.zeros_like(first_frame_grayscale)
        mask_features[:,0:20] = 1
        mask_features[:,900:1050] = 1

        self.features = dict(
            maxCorners = 100,
            qualityLevel = 0.3,
            minDistance = 3,
            blockSize = 7,
            mask = mask_features
        )

    def add_adjust_positions_to_tracks(self, tracks, camera_movement_per_frame):
        for object, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    position = track_info['position']
                    camera_movement = camera_movement_per_frame[frame_num]
                    position_adjusted = (position[0] - camera_movement[0], position[1] - camera_movement[1])
                    tracks[object][frame_num][track_id]['position_adjusted'] = position_adjusted

 
    def get_camera_movement(self, frames, read_from_stub = False, stub_path = None):
        # read the stub
        if read_from_stub and stub_path is not None:
            stub_path = resource_path(stub_path) #Use resource path here
            if os.path.exists(stub_path):
                with open(stub_path, 'rb') as f:
                    return pickle.load(f)


        camara_movement = [[0,0]]*len(frames)

        old_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        old_features = cv2.goodFeaturesToTrack(old_gray,**self.features)

        for frame_num in range(1,len(frames)):
            frame_gray = cv2.cvtColor(frames[frame_num], cv2.COLOR_BGR2GRAY)
            
            old_features = cv2.goodFeaturesToTrack(frame_gray, **self.features)
            if old_features is None:
                print('No features found in frame', frame_num)
                continue  # Skip this iteration of the loop

            print(old_features.dtype, old_features.shape)
            new_features,_,_ = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, old_features, None, **self.lk_params)
            print(old_gray.shape, frame_gray.shape)
            max_distance = 0
            camara_movement_x, camara_movement_y = 0, 0
            for i , (new,old) in enumerate(zip(new_features,old_features)):
                new_features_point = new.ravel()
                old_features_point = old.ravel()

                distance = measure_distance(new_features_point, old_features_point)

                if distance > max_distance:
                    max_distance = distance
                    camara_movement_x, camara_movement_y = measure_xy_distance(old_features_point, new_features_point)

            if max_distance > self.minimum_distance:
                camara_movement[frame_num] = [camara_movement_x, camara_movement_y]
            
            old_features = cv2.goodFeaturesToTrack(frame_gray, **self.features)
            old_gray = frame_gray

        if stub_path is not None:
            stub_path = resource_path(stub_path) #Use resource path here
            with open(stub_path, 'wb') as f:
                pickle.dump(camara_movement,f)

        return camara_movement
    
    
    def draw_camera_movement(self, frames, camera_movement_per_frame):
        output_frames = []
        
        for frame_num, frame in enumerate(frames):
            

            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (500, 100), (255, 255, 255), -1)
            alpha = 0.6
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            x_movement, y_movement = camera_movement_per_frame[frame_num]
            frame = cv2.putText(frame, f"Camera Movement X: {x_movement: .2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            frame = cv2.putText(frame, f"Camera Movement Y: {y_movement: .2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

            output_frames.append(frame)
        
        return output_frames

            
            