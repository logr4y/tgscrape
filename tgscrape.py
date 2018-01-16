#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick and dirty public Telegram group message scraper

Usage:
    $ python3 tgscrape.py <groupname> [minid] [maxid]

Example:
    $ python3 tgscrape.py fun_with_friends 1 1000
        - dumps messages 1 through 1000 from the group @fun_with_friends

The loop stops when it finds 20 consecutive empty messages (defined by max_err in config.py)
"""

import sys
import time
import copy
import urllib.request
from bs4 import BeautifulSoup
from util import *
import config
import db

def usage(pyfile):
    """ Usage """
    return 'Usage: {} <groupname> [minid] [maxid]'.format(pyfile)


def get_sender(obj, lclass):
    """ Retrieves the sender of a message """
    author = obj.find('', class_=lclass)
    return_name = ''
    return_username = ''
    if author:
        return_name = author.text
    if author.name == 'a':
        return_username = author['href'].split('/')[3]
    return (return_name, return_username)


def parse_message(soup):
    """ Parses a message, returns object """
    datetime = soup.find_all('time')[-1]['datetime']
    if datetime:
        return_object = copy.deepcopy(config.message_object)
        (return_object['name'], return_object['username']) = \
            get_sender(soup, config.author_class)
        return_object['datetime'] = datetime

        msg = soup.find_all('', class_=config.text_class)
        if msg:
            if len(msg) == 2:
                quote = msg[0].text
                msg = msg[1].text
            else:
                quote = None
                msg = msg[0].text

            return_object['msg'] = msg
            if quote:
                return_object['quote'] = quote

        service_msg = soup.find('', class_=config.service_class)
        if service_msg:
            return_object['msg'] = \
                '|{}|'.format(service_msg.text
                              if service_msg.text
                              else 'SERVICE MESSAGE')

        fwd = soup.find('', class_=config.forward_class)
        if fwd:
            (return_object['fwd_name'], return_object['fwd_username']) = \
                get_sender(soup, config.forward_class)

        media = soup.find('', class_=config.photo_class) or \
            soup.find('', class_=config.video_class) or \
            soup.find('', class_=config.voice_class) or \
            soup.find('', class_=config.link_class) or \
            soup.find('', class_=config.sticker_class)

        if media:
            if media['class'][0] == config.photo_class:
                return_object['photo'] = media['style'].split("'")[1]

            if media['class'][0] == config.video_class:
                return_object['video'] = media.video['src']

            if media['class'][0] == config.voice_class:
                return_object['voice'] = media['src']

            if media['class'][0] == config.link_class:
                title_class = soup.find('', class_=config.link_title_class)
                description_class = soup.find('', class_=config.link_description_class)
                preview_class = soup.find('', class_=config.link_preview_class)

                if title_class:
                    return_object['link']['title'] = title_class.text
                if description_class:
                    return_object['link']['description'] = description_class.text
                if preview_class:
                    return_object['link']['preview'] = preview_class['style'].split("'")[1]

            if media['class'][0] == config.sticker_class:
                return_object['photo'] = media['style'].split("'")[1]

        return return_object


def scrape_run(lgroupname, lmin_id, lmax_id, ldb):
    """ Main logic """
    msg_id = lmin_id
    cnt_err = 0
    url = 'https://t.me/{}/'.format(lgroupname)
    while True:
        if msg_id not in ldb.keys():
            r_url = url + str(msg_id) + '?embed=1'
            with urllib.request.urlopen(r_url) as response:
               response = response.read()
            if len(response) > 3000:
                cnt_err = 0
                soup_object = BeautifulSoup(response, 'html.parser')
                ldb[msg_id] = parse_message(soup_object)
            else:
                ldb[msg_id] = copy.deepcopy(config.message_object)
                ldb[msg_id]['deleted'] = '1'
                cnt_err += 1
                if cnt_err == config.max_err:
                    for id_to_delete in range(msg_id, msg_id - config.max_err, -1):
                        del ldb[id_to_delete]
                    return '{} consecutive empty messages. Current ID: {}. Exiting...'.format(config.max_err, msg_id)
            time.sleep(config.sleeptime)

            if (msg_id - lmin_id + 1) % config.messages_dump_cnt == 0:
                dh.write_data(ldb)

        print_object(ldb[msg_id])

        if msg_id == lmax_id:
            return 'All messages retrieved. Exiting...'

        msg_id += 1

try:
    print('> Telegram Public Groups Scraper', end='\n\n')
    argnum = len(sys.argv)

    if argnum < 2:
        print(usage(sys.argv[0]))
        raise ValueError('Not enough parameters')

    groupname = sys.argv[1]
    min_id = int(sys.argv[2]) if argnum >= 3 else config.min_id
    max_id = int(sys.argv[3]) if argnum >= 4 else config.max_id

    dh = db.DB(groupname)
    database = dh.load_data()
    exit_msg = scrape_run(groupname, min_id, max_id, database)
    exit_code = 0
except KeyboardInterrupt:
    (exit_code, exit_msg) = 1, 'Stopped. Exiting...'
except Exception as e:
    (exit_code, exit_msg) = 1, 'ERROR: {}'.format(e)
finally:
    print('\r  ')
    try:
        dh.write_data(database)
    except NameError:
        pass
    print(exit_msg)
    exit(exit_code)
