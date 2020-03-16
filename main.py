from pyAnywhere.pyAnywhere import pyAnywhere
import argparse
import os
import json
import sys

def get_user():
    if not os.path.exists('.pyAnywhere/config.cfg'):
        print('Log in first: --login')
        sys.exit()
    with open('.pyAnywhere/config.cfg', 'r') as f:
        user_data = f.read()
    user_data = json.loads(user_data)
    user = pyAnywhere(user_data.get('username'), user_data.get('token'))
    return user

parser = argparse.ArgumentParser(description='Great Description To Be Here')
parser.add_argument('--login', action='store_true', help='Log in system. Token: https://www.pythonanywhere.com/user/{username}/account/#api_token')
parser.add_argument('--consoles', action='store_true', help='All user consoles')
parser.add_argument('--console-info', help='Get console info')
parser.add_argument('--console', help='Connect to console')

args = parser.parse_args()

if args.login:
    print('\t--LOGIN--')
    username = input('Username: ')
    token    = input('Token: ')
    try:
        os.mkdir('.pyAnywhere')
    except FileExistsError:
        pass
    with open('.pyAnywhere/config.cfg', 'w') as f:
        f.write('{"token": "%s", "username": "%s"}' % (token, username))

elif args.consoles:
    user = get_user()
    consoles_all = user.consoles().all()
    if not consoles_all:
        print('You have no running consoles')
    else:
        print('\tID\tNAME\t\t\tURL')
        for console_info in consoles_all:
            print('    %s |\t%s |\t%s' % (console_info.get('id'), console_info.get('name'), 'https://www.pythonanywhere.com/' + console_info.get('console_url')))

elif args.console_info:
    user = get_user()
    console_info = user.consoles().console(args.console_info).info()
    if console_info.get('detail'):
        print('Console not found.')
        sys.exit()
    print("""  --Console: %s--
id: %s
user: %s
executable: %s
working_directory: %s
name: %s
console_url: %s
console_frame_url: %s""" % (args.console_info,
                            console_info.get('id'), 
                            console_info.get('user'), 
                            console_info.get('executable'), 
                            console_info.get('working_directory'), 
                            console_info.get('name'), 
                            console_info.get('console_url'), 
                            console_info.get('console_frame_url')))

elif args.console:
    user = get_user()
    get_console_id = args.console
    try:
        while True:
            server_response = user.consoles().console(get_console_id).get_latest_output()
            if server_response.get('detail'):
                print('Console not found.')
                sys.exit()
            elif server_response.get('error'):
                print('[ERROR]: ' + server_response.get('error'))
                sys.exit()
            get_latest_output = server_response.get('output')
            user.consoles().console(get_console_id).send_input(input(get_latest_output)+'\n')
    except KeyboardInterrupt:
        print('Stopped')

else:
    print('''usage: main.py [-h] [--login] [--consoles] [--console-info CONSOLE_INFO]
[--console CONSOLE]''')