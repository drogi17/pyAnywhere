import argparse
import requests
import os
import json
import sys
import base64

from colors.colors import ok_text, error_text
from pyAnywhere.pyAnywhere import pyAnywhere

def get_user():
    if not os.path.exists('.pyAnywhere/config.cfg'):
        print('Log in first: --login')
        sys.exit()
    with open('.pyAnywhere/config.cfg', 'r') as f:
        user_data = f.read()
    user_data = json.loads(user_data)
    user = pyAnywhere(user_data.get('username'), user_data.get('token'))
    return user

def dir_files(dir_link, directory):
    response = requests.get(dir_link)
    paths = response.json()
    files = []
    for path in paths:
        path_link = [path.get('url'), path.get('type')]
        if path_link[1] == 'dir':
            get_dir = dir_files(path_link[0], directory + '/' + path.get('path'))
            files.append(get_dir)
        elif path_link[1] == 'file':
            content = base64.b64decode(requests.get(path_link[0]).json().get('content')).decode()
            files.append([path.get('path'), directory, content])
    return files

def save_files(link_array):
    for file in link_array:
        if isinstance(file[0], list):
            save_files(file)
        else:
            if file[1] != '.':
                try:
                    os.mkdir(file[1])
                except FileExistsError:
                    pass
            with open(file[0], 'w') as f:
                f.write(file[2])
            print('[%s] %s' % (ok_text('OK'), file[0]))
    sys.exit()

def update_program():
    update_links = dir_files('https://api.github.com/repos/drogi17/pyAnywhere/contents', '.')
    save_files(update_links)

parser = argparse.ArgumentParser(description='pyAnywhere')
parser.add_argument('--login', action='store_true', help='Log in system. Token: https://www.pythonanywhere.com/user/{username}/account/#api_token')
parser.add_argument('--consoles', action='store_true', help='All user consoles')
parser.add_argument('--console-info', help='Get console info')
parser.add_argument('--console', help='Connect to console')
# parser.add_argument('--update', action='store_true', help='Get a new version of the program.')
parser.add_argument('--upload', action='store_true', help='Upload file to your server. -f <path> -s <server path>\nExample: --upload -f files.txt -s /files/files.txt')
parser.add_argument('-f', action='store', help='File to upload')
parser.add_argument('-s', action='store', help='The path to be loaded')

parser.add_argument('--webapps', action='store_true', help='All user webapps')
parser.add_argument('--webapp', help='Web application control. (argument: domain)\n-e/-d/-r')
parser.add_argument('-e', action='store_true', help='Enable webapp')
parser.add_argument('-d', action='store_true', help='Disable webapp')
parser.add_argument('-r', action='store_true', help='Reload the webapp')

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
            if not server_response or server_response.get('detail'):
                print('Console not found.')
                sys.exit()
            elif server_response.get('error'):
                print('[ERROR]: ' + server_response.get('error'))
                sys.exit()
            get_latest_output = server_response.get('output')
            user.consoles().console(get_console_id).send_input(input(get_latest_output)+'\n')
    except KeyboardInterrupt:
        print('Stopped')

# elif args.update:
#     response = requests.get('https://api.github.com/repos/drogi17/pyAnywhere/contents/VERSION')
#     if response.status_code == 403:
#         print('Update limit exceeded.')
#         sys.exit()
#     version_base64 = response.json().get('content')
#     version_new  = json.loads(base64.b64decode(version_base64).decode())
#     with open('VERSION', 'r') as f:
#         version_now = json.loads(f.read())
#     cli_version  = version_now.get('pyAnywhere_cli')
#     lib_version  = version_now.get('pyAnywhere_lib')
#     if lib_version != version_new.get('pyAnywhere_lib') or cli_version != version_new.get('pyAnywhere_cli'):
#         print('Found a new version of the program. (client: %s, lib: %s)' % (version_new.get('pyAnywhere_cli'), version_new.get('pyAnywhere_lib')))
#         if input('Would you like to update?(y, n): ') in ['y', 'Y', 'Д', 'д']:
#             update_program()
#         else:
#             print('Ok...')
#     else:
#         print('You have the latest version of the program.')

elif args.upload:
    if args.f and args.s:
        file_path   = args.f
        server_path = args.s
        user = get_user()
        print(user.upload_file(file_path, server_path))

elif args.webapps:
    user = get_user()
    webapps_all = user.webapps().all()
    if not webapps_all:
        print('You have no running consoles')
    else:
        print('\tID\tDOMAIN\t\t\t\tSource Sirectory')
        for console_info in webapps_all:
            print('    %s |\t%s |\t%s' % (console_info.get('id'), console_info.get('domain_name'), console_info.get('source_directory')))

elif args.webapp:
    user = get_user()
    webapp_name = args.webapp
    if args.e:
        if user.webapps().webapp(webapp_name).enable():
            print('[%s] %s: Enabled' % (ok_text('OK'), webapp_name))
        else:
            print('[%s] %s: Enabled' % (error_text('ERROR'), webapp_name))
    if args.d:
        if user.webapps().webapp(webapp_name).disable():
            print('[%s] %s: Disabled' % (ok_text('OK'), webapp_name))
        else:
            print('[%s] %s: Enabled' % (error_text('ERROR'), webapp_name))
    if args.r:
        if user.webapps().webapp(webapp_name).reload():
            print('[%s] %s: Restarted' % (ok_text('OK'), webapp_name))
        else:
            print('[%s] %s: Enabled' % (error_text('ERROR'), webapp_name))

else:
    print('''usage: main.py [-h] [--login] [--consoles] [--console-info CONSOLE_INFO]
[--console CONSOLE]''')
