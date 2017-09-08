#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vk_api
import requests
import os
import json
import time
import random
import configparser
from antigate import AntiGate
from helpers import save_attachment

def get_auth():

    config = configparser.ConfigParser()
    config.read('auth/auth.ini')
    return config


def captcha_handler(captcha):

    config = get_auth()
    api_key = config.get('antigate', 'api_key')

    cap_img = captcha.get_image()
    print('Разгадываю капчу..')

    gate = AntiGate(api_key)
    captcha_id1 = gate.send(cap_img)
    key = gate.get(captcha_id1)
    print('Разгадал! Тут написанно:', key, 'Ввожу..')

    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key)


def vk_login():

    config = get_auth()
    login, password = config.get('vk', 'login'), config.get('vk', 'password')

    vk_session = vk_api.VkApi(
        login, password,
        captcha_handler=captcha_handler  # функция для обработки капчи
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    return vk_session


def get_dialogs():

    vk_session = vk_login()
    vk = vk_session.get_api()

    dialogs = vk.messages.getDialogs()


def core(user_id=None):

    if not user_id:
        return

    vk_session = vk_login()
    vk = vk_session.get_api()

    directory = "dump/{}".format(user_id)
    media_directory = directory + '/media'
    user_file = directory + '/user_{}.json'.format(str(user_id))

    if not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    else:
        print('Directory {} already exists'.format(user_id))
        return

    tools = vk_api.VkTools(vk_session)
    print('Getting messages..')
    messages = tools.get_all('messages.getHistory', 200, {'user_id': user_id})

    with open(user_file, 'w') as data_file:
        json.dump(messages, data_file)

    print('Getting media..')
    with open(user_file) as data_file:
        user_data = json.load(data_file)

    for i, msg in enumerate(user_data['items']):
        if "attachments" in msg:
            print('\nMessage {} from {}'.format(i, len(user_data['items'])))
            for attt in msg['attachments']:
                save_attachment(attt, media_directory)


if __name__ == "__main__":

    core(user_id=123)

