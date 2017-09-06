#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import shutil
import urllib.request


def save_attachment(attachment, media_folder_path):

    if not attachment:
        return

    media_type = attachment['type']

    if media_type == 'doc':

        download_media(
            dwnld_src = attachment['doc']['url'],
            media_id = attachment['doc']['id'],
            media_ext = attachment['doc']['ext'],
            media_folder_path = media_folder_path
        )

    elif media_type == 'photo':

        dwnld_src = None

        if "photo_2560" in attachment['photo']:
            dwnld_src = attachment['photo']['photo_2560']

        elif "photo_1280" in attachment['photo']:
            dwnld_src = attachment['photo']['photo_1280']

        elif "photo_807" in attachment['photo']:
            dwnld_src = attachment['photo']['photo_807']

        elif "photo_604" in attachment['photo']:
            dwnld_src = attachment['photo']['photo_604']

        elif "photo_130" in attachment['photo']:
            dwnld_src = attachment['photo']['photo_130']

        elif "photo_75" in attachment['photo']:
            dwnld_src = attachment['photo']['photo_75']

        download_media(
            dwnld_src = dwnld_src,
            media_id = attachment['photo']['id'],
            media_ext = "jpg",
            media_folder_path = media_folder_path
        )

    elif media_type == 'video':

        if not "player" in attachment['video']:
            return

        download_media(
            dwnld_src = attachment['video']['player'],
            media_id = attachment['video']['id'],
            media_ext = "mp4",
            media_folder_path = media_folder_path
        )

    elif media_type == 'audio':

        download_media(
            dwnld_src = attachment['audio']['url'],
            media_id = attachment['audio']['id'],
            media_ext = "mp3",
            media_folder_path = media_folder_path
        )


def download_media(dwnld_src, media_id, media_ext, media_folder_path):

    if not os.path.isdir(media_folder_path):
        try:
            os.makedirs(media_folder_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    print("--> Downloading {}.{}".format(media_id, media_ext))

    file_name = '{}.{}'.format(media_id, media_ext)
    if os.path.isfile(media_folder_path + '/' + file_name):
        print("Already exist")
        return

    try:
        urllib.request.urlretrieve(dwnld_src, file_name)
    except:
        print("Error")

    if os.path.isfile(file_name):
        shutil.move(file_name, media_folder_path + '/' + file_name)
        print("Success")
