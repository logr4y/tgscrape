#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tgscrape cli to search and read scraped conversations
"""
import sys
import re
import db
from util import *

def usage(pyfile):
    """ Usage """
    return 'Usage: {} <groupname>'.format(pyfile)


def print_help():
    """Prints program's help"""
    print("""
    Commands:
        search <terms>              search words or strings (in quotes) in messages and names
        all                         returns all dumped messages
        last <num>                  returns last <num> messages (default: 10)
        date <date>                 returns all messages for a date (format: YYYY-MM-DD)
        wordcloud                   returns the top 20 words (wordlen > 3)
        exit                        exits the program
        help                        this
    """)

def search_cmd(search_args):
    """ Search text in conversation """
    if search_args[0] in ["'", '"']:
        search_entries = search_args.strip('"\'')
    else:
        search_entries = search_args.split(' ')

    results = []
    for entry_key in sorted(DATABASE.keys()):
        msg = DATABASE[entry_key]
        search_content = msg['msg'] + \
                         msg['quote'] + \
                         msg['name'] + \
                         msg['username'] + \
                         msg['fwd_name'] + \
                         msg['fwd_username']
        if isinstance(search_entries, str):
            if search_entries.lower() in search_content.lower():
                results.append(entry_key)
        else:
            for search_entry in search_entries:
                if search_entry.lower() in search_content.lower():
                    results.append(entry_key)

    results = set(results)
    for db_id in results:
        print_object(DATABASE[db_id])
    print("- Total Entries: {}".format(len(results)))

def print_wordcloud():
    """ Generate wordcloud from messages """
    wcloud = {}
    for entry_key in DATABASE.keys():
        msg = DATABASE[entry_key]['msg']
        if msg and msg[0] == '|':
            continue
        msg = re.sub(r'[^\w ]', '', msg, flags=re.IGNORECASE)
        if msg:
            msg = msg.split(' ')
            msg = [m for m in msg if len(m) > 3]
            for word in filter(None, msg):
                if word in wcloud.keys():
                    wcloud[word] += 1
                else:
                    wcloud[word] = 1

    wcloud = sorted(wcloud.items(), key=lambda v: v[1], reverse=True)
    for word in wcloud[0:20]:
        print(word, end='')
    print()


def print_all_messages():
    """Prints all dumped messages"""
    for entry_key in sorted(DATABASE.keys()):
        print_object(DATABASE[entry_key])


def print_last_messages(num=20):
    """Prints last dumped messages"""
    for entry_key in sorted(DATABASE.keys())[-num:]:
        print_object(DATABASE[entry_key])


def print_date(ldate):
    """Prints all messages on ldate"""
    date_regex = r'\d{4}-\d{2}-\d{2}'
    results = []
    if re.match(date_regex, ldate):
        for entry_key in sorted(DATABASE.keys()):
            msg = DATABASE[entry_key]
            if msg['datetime'][0:10] == ldate:
                results.append(entry_key)
    else:
        print_error("Invalid date format. Expected: YYYY-MM-DD")

    for result in results:
        print_object(DATABASE[result])
    print("- Total Entries: {}".format(len(results)))    


def main():
    """Main code"""
    while True:
        cmd = input('> ')
        try:
            (cmd, args) = cmd.split(' ', 1)
        except ValueError:
            (cmd, args) = cmd, None

        if cmd == 'search':
            if args:
                search_cmd(args)
            else:
                print_error("Enter search terms")

        elif cmd == 'wordcloud':
            print_wordcloud()
        
        elif cmd == 'help':
            print_help()
        
        elif cmd == 'all':
            print_all_messages()
        
        elif cmd == 'last':
            if not args:
                args = 20
            print_last_messages(int(args))

        elif cmd == 'date':
            date = args.split(' ')[0]
            print_date(date)

        elif cmd in ['exit', 'quit']:
            break

        else:
            print_error('Command not valid')

if __name__ == '__main__':
    try:
        print('> tgscrape console\n')
        ARGNUM = len(sys.argv)
        if ARGNUM < 2:
            print(usage(sys.argv[0]))
            raise ValueError('Not enough parameters')

        (EXIT_CODE, EXIT_MSG) = 0, 'Goodbye!'

        GROUPNAME = sys.argv[1]
        DH = db.DB(GROUPNAME)
        DATABASE = DH.load_data(False)
        if not DATABASE:
            raise FileNotFoundError("No conversations found")

        main()
    except KeyboardInterrupt:
        (exit_code, exit_msg) = 1, 'Stopped'
        print('\b\b', end='')
    except BaseException as exception_msg:
        (EXIT_CODE, EXIT_MSG) = 1, 'ERROR: {}'.format(exception_msg)
    finally:
        print('{}\nExiting...'.format(EXIT_MSG))
        exit(EXIT_CODE)
