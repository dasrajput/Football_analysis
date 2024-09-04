from utils import read_video, save_video
from trackers import Tracker
import cv2
import numpy as np
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator   
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistance_Estimator

def main():
    # Read the video
    video_frames =  read_video('Input_Videos/1.mp4')
    
    
    #initialize the tracker
    tracker = Tracker('models/best.pt')
    print("Tracker initialized")

    tracks = tracker.get_object_tracks(video_frames,
                                       read_from_stub = True,
                                       stub_path = 'stubs/track_stubs_1.pkl')
    print("Object tracks obtained")

    # get object positions
    tracker.add_position_to_tracks(tracks)
    print("Positions added to tracks")
    
    #camera movement estimator
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames,
                                                                              read_from_stub = True,
                                                                              stub_path = 'stubs/camera_movement_stub_1.pkl')
    print("Camera movement estimated")

    camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)
    print("Adjusted positions added to tracks")


    # View transformer
    view_transformer = ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)
    print("Transformed positions added to tracks")
    
    #interpolate ball positions
    tracks["ball"] = tracker.interpolate_ball_positions(tracks["ball"])
    print("Ball positions interpolated")

    # Speed and Distance Estimator
    speed_and_distance_estimator = SpeedAndDistance_Estimator()
    speed_and_distance_estimator.add_speed_and_distance_to_tracks(tracks)
    print("Speed and distance added to tracks")
    
    # assign player teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
    print("Team colors assigned")

    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_num], track['bbox'], player_id)
            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]
    print("Player teams assigned")

    
        
    #Draw output
    ##Draw object tracks
    output_video_frames = tracker.draw_annotations(video_frames, tracks)
    print("Annotations drawn on video frames")

    # # # #Draw camera movement
    # output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)
    # print("Camera movement drawn on video frames")

    #Draw speed and distance
    speed_and_distance_estimator.draw_speed_and_distance(output_video_frames, tracks)
    print("Speed and distance drawn on video frames")

    
    

    # Save the video
    save_video(output_video_frames,'Output_Videos/1_out.avi')
    

if __name__ == '__main__':
    main()