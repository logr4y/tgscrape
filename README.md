# tgscrape
Quick and dirty public Telegram group message scraper

# Usage
## To dump messages from a public group
```bash
$ python3 tgscrape.py <groupname> [minid] [maxid]
```
### Examples
To dump all messages in the group _fun_with_friends_ type:
```bash
$ python3 tgscrape.py fun_with_friends
```
You can specify the message id you want to start and stop. For instance, to dump messages with id's 1000 through 2000 type:
```bash
$ python3 tgscrape.py fun_with_friends 1000 2000
```
If you want to start at message id 1000 and dump all messages after it, just skip the last parameter:
```bash
$ python3 tgscrape.py fun_with_friends 1000
```
Retrieved messages are stored in json format in the `conversations` folder.

## To read and search dumped messages
```bash
$ python3 tgscape_cli.py <groupname>
```

The following is the list and description of available commands:
```
Commands:
    search <terms>              search words or strings (in quotes) in messages and names
    all                         returns all dumped messages
    last <num>                  returns last <num> messages (default: 10)
    date <date>                 returns all messages for a date (format: YYYY-MM-DD)
    wordcloud                   returns the top 20 words (wordlen > 3)
    exit                        exits the program
    help                        this
```
### Examples
If you want to search all messages and names containing _either_ "foo" and "bar" type:
```
> search foo bar
```
If you want to search all messages and names containing the string "foo bar" type:
```
> search "foo bar"
```
To read all messages written on January 3rd, 2018, type:
```
> date 2018-03-01
```

# Requirements
```
BeautifulSoup4
```
To install dependencies:
```bash
$ pip install -r requirements.txt
```
