from cutter import split_video
from generation_anki import create_package


if __name__ == '__main__':

    # Пример использования
    # video_path = "/Users/sedrew/Downloads/tomp3.cc - 500 Common English Idioms and Examples.mp4"
    # output_folder = "/Users/sedrew/PycharmProjects/VideoCutterAnki"
    # # split_video(video_path, output_folder)
    #
    # create_package(audios_path=f'{output_folder}/audio', images_path=f'{output_folder}/images', step=2,
    #                name_deck='500 Common English Idioms and Examples (Man)')

    video_path = "/Users/sedrew/Downloads/1000 Most Common English Sentences in Present Simple Tense for Daily Life.mp4"
    output_folder = "/Users/sedrew/PycharmProjects/VideoCutterAnki"
    split_video(video_path, output_folder)

    create_package(audios_path=f'{output_folder}/audio', images_path=f'{output_folder}/images', step=4,
                   name_deck='1000 Most Common English Sentences in Present Simple')


