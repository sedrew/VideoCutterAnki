import uuid
from itertools import islice
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip


class CutterSilence:

    def __init__(self, video_clip: VideoFileClip):
        self.video_clip = video_clip

    @staticmethod
    def smooth(y, box_pts):
        box = np.ones(box_pts) / box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth

    def get_frame_fragment(self, slice_frame=None, step=10000, f=1000):
        vid_fps = self.video_clip.audio.fps

        stun_loop = False
        count = 0
        for item in self.video_clip.audio.iter_chunks(chunksize=step):
            count += step
            mean_res = np.mean(np.abs(item)) * f

            if mean_res <= 0.001 and not stun_loop:
                stun_loop = True
            elif mean_res > 0.00 and stun_loop:
                res = (count - step - 5000) / vid_fps
                print(f'#{int(count/step)} Cut point - Time sec: {res}')
                stun_loop = False
                yield res

            # mean_list = np.array([])
            if slice_frame is not None and count >= slice_frame:
                break

    def get_video_fragment(self, frame_fragments: iter):
        last_el = 0
        for el in frame_fragments:
            if el == last_el:
                print(f'Skip time sec: {el}')
                continue
            res_cut = (self.video_clip.subclip(t_start=last_el, t_end=el).
                       set_audio(self.video_clip.audio.subclip(t_start=last_el, t_end=el)))
            last_el = el
            yield res_cut

        end_audio = self.video_clip.audio.end
        if last_el < end_audio:
            yield (self.video_clip.subclip(t_start=last_el, t_end=end_audio).
                   set_audio(self.video_clip.audio.subclip(t_start=last_el, t_end=end_audio)))

    def get_audio_fragment(self, frame_fragments: Iterable[VideoFileClip]):
        for video in self.get_video_fragment(frame_fragments):
            yield video.audio

    @staticmethod
    def get_screenshot_video(vide_clips: Iterable[VideoFileClip]) -> Image:
        for video_clip in vide_clips:
            frame = video_clip.get_frame(video_clip.end * 0.5)
            # Преобразуем массив пикселей кадра в изображение PIL
            pil_image = Image.fromarray(frame)
            yield pil_image

    @staticmethod
    def save_videos_in_folder(dir_name, list_video: Iterable[VideoFileClip]):
        for idx, el in enumerate(list_video):
            file_uuid = str(uuid.uuid4()).split('-')[0]
            el.write_videofile(f"{dir_name}/vid-{file_uuid}-{idx}.mp4")

    @staticmethod
    def save_audios_in_folder(dir_name, list_video: Iterable[VideoFileClip]):
        for idx, el in enumerate(list_video):
            file_uuid = str(uuid.uuid4()).split('-')[0]
            el.audio.write_audiofile(f"{dir_name}/aud-{file_uuid}-{idx}.mp3")

    @staticmethod
    def save_images_in_folder(dir_name, list_images: Iterable[VideoFileClip]):
        for idx, el in enumerate(list_images):
            file_uuid = str(uuid.uuid4()).split('-')[0]
            el.save(f"{dir_name}/img-{file_uuid}-{idx}.jpg")


def split_video(input_video, output_folder):
    # Загрузка видео
    video_clip = VideoFileClip(input_video)

    cutter = CutterSilence(video_clip=video_clip)
    list_audio = cutter.get_frame_fragment()
    list_video = list(cutter.get_video_fragment(frame_fragments=list_audio))
    list_image = cutter.get_screenshot_video(list_video)

    dir_videos = f'{output_folder}/audio'
    dir_images = f'{output_folder}/images'
    Path(dir_videos).mkdir(parents=True, exist_ok=True)
    Path(dir_images).mkdir(parents=True, exist_ok=True)

    cutter.save_audios_in_folder(dir_videos, list_video)
    cutter.save_images_in_folder(dir_images, list_image)
    print('Successful')


if __name__ == '__main__':
    # Пример использования
    video_path = "/Users/sedrew/Downloads/tomp3.cc - 500 Common English Idioms and Examples.mp4"
    output_folder = "/Users/sedrew/PycharmProjects/VideoCutterAnki"
    split_video(video_path, output_folder)
