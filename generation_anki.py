import itertools
import random
from pathlib import Path
import uuid

import genanki
from tkinter import Tcl


class ModelCard:
    _count = 0

    def __init__(self, model_id=None):
        if model_id is None:
            model_id = random.randrange(1 << 30, 1 << 31)

        # Создаем модель
        self.model = genanki.Model(
            model_id,
            'Simple Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
                {'name': 'Audio'},
                {'name': 'Image'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Audio}}',
                    'afmt': '{{FrontSide}}<hr id="answer"><br>{{Image}}',
                },
            ],
            css='.card { font-family: arial; font-size: 20px; text-align: center; }',
        )

    def get_note(self, audio_path, image_path, answer=' ', question=' ') -> genanki.Note:
        # Создаем карточку
        note = genanki.Note(
            model=self.model,
            fields=[question, answer, f'[sound:{audio_path}]', f'<img src="{image_path}">']
        )
        return note


def create_package(audios_path, images_path, name_deck='Simple Deck', step=1, deck_id=None):
    if deck_id is None:
        deck_id = random.randrange(1 << 30, 1 << 31)
    # Создаем колоду
    my_deck = genanki.Deck(
        deck_id,
        name_deck
    )


    audios_list = [el for el in Path(audios_path).iterdir() if el.suffix == '.mp3']
    images_list = [el for el in Path(images_path).iterdir() if el.suffix == '.jpg']

    audios_list = Tcl().call('lsort', '-dict', audios_list)
    images_list = Tcl().call('lsort', '-dict', images_list)

    # Создаем пакет и сохраняем его
    my_package = genanki.Package(my_deck)
    my_model = ModelCard()
    import os

    out_list = list()
    for audio, image in itertools.islice(zip(audios_list, images_list), 1, None, step):

        # Добавляем карточку в колоду
        out_list.append(str(image_path))
        out_list.append(str(audio_path))

        my_deck.add_note(my_model.get_note(audio_path=audio_path.name, image_path=image_path.name))

    my_package.media_files = out_list
    my_package.write_to_file(f'{name_deck}.apkg')
