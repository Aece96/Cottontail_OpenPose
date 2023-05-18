from IPython.display import HTML
from settings import VIDEO_PATH


def display_video(video_name):
    video_path = VIDEO_PATH + video_name + '.mp4'
    video_tag = f"""
    <video width="640" height="480" controls>
        <source src="{video_path}" type="video/mp4">
    </video>
    """
    return HTML(video_tag)
