from utils import read_video, save_video
from trackers import Tracker
def main():
    # Read the video
    video_frames =  read_video('Input_Videos/08fd33_4.mp4')


    #initialize the tracker
    tracker = Tracker('models/best.pt')

    tracks = tracker.get_object_tracks(video_frames,
                                       read_from_stub = True,
                                       stub_path = 'stubs/track_stubs.pkl')
    
    #draw output
    #draw object tracks

    output_video_frames = tracker.draw_annotations(video_frames, tracks)

    # Save the video
    save_video(output_video_frames,'Output_Videos/output_video.avi')

if __name__ == '__main__':
    main()