#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility methods"""

def print_error(error_msg):
    """Prints an error"""
    print('ERROR: {}'.format(error_msg))

def print_object(lobj):
    """ Print a message object """
    if 'deleted' in lobj.keys() and lobj['deleted'] == '1':
        print('[deleted]')
        return

    outputline = '[{}] {}{}: '.format(lobj['datetime'],
                                      lobj['name'],
                                      ' (@{})'.format(lobj['username']) if lobj['username'] else '')

    if lobj['fwd_name'] or lobj['fwd_username']:
        outputline += '{ '
        outputline += '{}{}: '.format(lobj['fwd_name'],
                                      ' (@{})'.format(lobj['fwd_username'])
                                      if lobj['fwd_username']
                                      else '')

    if lobj['quote']:
        outputline += '{{ {} }} '.format(lobj['quote'])

    outputline += lobj['msg']

    if lobj['photo']:
        outputline += ' {}'.format(lobj['photo'])

    if lobj['video']:
        outputline += ' {}'.format(lobj['video'])

    if lobj['voice']:
        outputline += ' {}'.format(lobj['voice'])

    if lobj['link']['title'] or lobj['link']['description'] or lobj['link']['preview']:
        link_msg = [
            lobj['link']['title'],
            lobj['link']['description'],
            lobj['link']['preview']
            ]
        link_msg = list(filter(None, link_msg))
        link_msg = ' - '.join(link_msg)
        outputline += ' <{}>'.format(link_msg)

    if lobj['fwd_name'] or lobj['fwd_username']:
        outputline += ' }'

    print(outputline)