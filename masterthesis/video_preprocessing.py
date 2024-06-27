import cv2
import os
def do_grayscale(input_video_path, output_video_path):
    # Capture the input video
    cap = cv2.VideoCapture(input_video_path)
    
    # Get the width, height, and frames per second (fps) of the input video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Define the codec and create a VideoWriter object to write the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height), isColor=False)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Write the grayscale frame to the output video
        out.write(gray_frame)
    
    # Release the video capture and writer objects
    cap.release()
    out.release()
    #cv2.destroyAllWindows()
    print(f'Video saved as {output_video_path}')

def reduce_frame_rate(input_video_path, output_video_path, target_fps):
    # Capture the input video
    cap = cv2.VideoCapture(input_video_path)
    
    # Get the original frame rate of the input video
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate the frame interval
    frame_interval = int(original_fps / target_fps)
    
    # Get the width and height of the input video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Define the codec and create a VideoWriter object to write the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, target_fps, (frame_width, frame_height))
    
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Write every nth frame to achieve the target frame rate
        if frame_count % frame_interval == 0:
            out.write(frame)
        
        frame_count += 1
    
    # Release the video capture and writer objects
    cap.release()
    out.release()
    #cv2.destroyAllWindows()
    print(f'Video saved as {output_video_path}')


output_path = "./processed_vid"
input_path = "./Non_move_vid"
try:
    os.makedirs(output_path,exist_ok=True)
    print(f'Created output directory: {output_path}')
except OSError as error:
    print(f'Error creating directory: {error}')
FPS = 10
for vid in os.listdir(input_path):
    input_vid_path = input_path+'/'+vid
    output_vid_path = output_path+'/'+ vid
    do_grayscale(input_vid_path,output_vid_path)
    #reduce_frame_rate(input_vid_path,output_vid_path, FPS)
    print(f'Processed video:{vid}')

# Example usage
#reduce_frame_rate('input_video.mp4', 'output_lower_fps_video.mp4', target_fps=15)
# Example usage
#do_grayscale('input_video.mp4', 'output_grayscale_video.mp4')
