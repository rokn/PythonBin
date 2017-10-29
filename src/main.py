#!/home/rokner/anaconda3/bin/python3.6
import fileinput
import pyperclip
import sys, getopt, os
from pastebin_connection import paste_create, login_user
from formats import FORMATS


def add_paste(content, title, syntax, expiry, succ, error):
    if content:
        result = paste_create(content, title, syntax, expiry)
        if result['success']:
            succ.append(result['data'])
        else:
            error.append(result['data'])
        paste_content = ""

def handle_input(args, title, syntax, expiry, clip):
    paste_content = ""
    succ = []
    error = []

    for line in fileinput.input(args):
        if fileinput.isfirstline():
            add_paste(paste_content, title, syntax, expiry, succ, error)

        paste_content += line

    add_paste(paste_content, title, syntax, expiry, succ, error)
    if succ:
        print("Succesful paste")
        for url in succ:
            print(url)

        print()

        if clip and len(succ) == 1:
            pyperclip.copy(succ[0])

    if error:
        print("Error")
        for url in error:
            print(url)

def print_help():
    print()
    print("Uploading files to pastebin. Usage similar to `cat` program.")
    print("[-u|--username] [-p|--password] - for username and password")
    print("[-t|--title] for title")
    print("[-s|--syntax] for syntax")
    print("[-e|--expiry] for expiry time")
    print("[-c] for auto copy to clipboard when only one input is used")
    print("[-m] for silent mode(no prints)")
    print("[-f|--format] for printing available formats and searching for a format")
    print()

def print_formats(search):
    if search:
        formats = [line for line in FORMATS.splitlines() if search in line]
        print('\n'.join(formats))
    else:
        print(FORMATS)

def main(argv):
    username = ''
    password = ''
    syntax = ''
    title = ''
    expiry = ''
    clip = False
    silent = False
    try:
        opts, args = getopt.gnu_getopt(argv, 'hu:p:t:s:e:cmf:', ["username=", "password=", "title=", "syntax=", "expiry=", "format="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ('-f', '--format'):
            print_formats(arg)
            sys.exit()
        elif opt in ('-u', '--username'):
            username = arg
        elif opt in ('-p', '--password'):
            password = arg
        elif opt in ('-t', '--title'):
            title = arg
        elif opt in ('-s', '--syntax'):
            syntax = arg
        elif opt in ('-e', '--expiry'):
            expiry = arg
        elif opt == '-c':
            clip = True
        elif opt == '-m':
            silent = True

    if silent:
        f = open(os.devnull, 'w')
        sys.stdout = f

    if username and password:
        res = login_user(username, password)
        if res['success']:
            print('Successful login')
        else:
            print(res['data'])

    handle_input(args, title, syntax, expiry, clip)

if __name__ == "__main__":
    main(sys.argv[1:])
