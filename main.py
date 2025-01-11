from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import read_video, save_video
from trackers import Tracker
from team_assigner import TeamAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistance_Estimator
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def initialize_tracker(video_frames, video_number):
    model_path = resource_path("models/best.pt")  # Use resource_path
    tracker = Tracker(model_path)
    tracks = tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                       stub_path=f'stubs/track_stubs_{video_number}.pkl')
    tracker.add_position_to_tracks(tracks)
    return tracks, tracker

def estimate_camera_movement(video_frames, video_number):
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames,
                                                                              read_from_stub=True,
                                                                              stub_path=f'stubs/camera_movement_stub_{video_number}.pkl')
    return camera_movement_per_frame

def transform_view(tracks):
    view_transformer = ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)
    
def interpolate_ball_positions(tracker, tracks):
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])

def estimate_speed_and_distance(tracks):
    speed_and_distance_estimator = SpeedAndDistance_Estimator()
    speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)
    
def assign_team(video_frames, tracks):
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num], track['bbox'], player_id)
            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]

def process_video(input_path, output_path):
    video_number = os.path.basename(input_path).split('.')[0]
    yield f"Processing video: {video_number}"
    
    # Read the video
    print("Reading video...")
    video_frames = read_video(input_path)
    if isinstance(video_frames, tuple):
        video_frames = video_frames[0]  # Assuming frames are the first element
    yield f"Video read successfully. Total frames: {len(video_frames)}"
    
    with ThreadPoolExecutor() as executor:
        # Initialize tracker and estimate camera movement concurrently
        futures = {
            executor.submit(initialize_tracker, video_frames, video_number): 'tracker',
            executor.submit(estimate_camera_movement, video_frames, video_number): 'camera_movement'
        }
        
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
                if task == 'tracker':
                    tracks, tracker = result
                elif task == 'camera_movement':
                    camera_movement_per_frame = result
            except Exception as e:
                print(f"Error occurred during {task}: {e}")
                return

        # Continue processing
        camera_movement_estimator = CameraMovementEstimator(video_frames[0])
        camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)
        yield "Camera movement estimation completed."
        
        transform_view(tracks)
        yield "View transformation completed."
        
        interpolate_ball_positions(tracker, tracks)
        yield "Ball position interpolation completed."
        
        estimate_speed_and_distance(tracks)
        yield "Speed and distance estimation completed."
        
        assign_team(video_frames, tracks)
        yield "Team assignment completed."
        
        # Draw annotations and save the video
        output_video_frames = tracker.draw_annotations(video_frames, tracks)
        speed_and_distance_estimator = SpeedAndDistance_Estimator()
        speed_and_distance_estimator.draw_speed_and_distance(output_video_frames, tracks)
        
        yield "Annotations drawn successfully."
        yield f"Saving video to {output_path}..."
        save_video(output_video_frames, output_path)
        yield "Video saved successfully."

if __name__ == '__main__':
    input_path = resource_path('Input_Videos/2.mp4')  # Use resource_path here!
    output_path = resource_path('Output_Videos/2_out.avi')

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

        
    for message in process_video(input_path, output_path):
        print(message)