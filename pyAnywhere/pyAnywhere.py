import requests, json

class ErrorOutput(Exception):
    def __init__(self, text):
        self.txt = text

def checking_server_response(response):
    if response.status_code < 200:    # 1xx
        return (True, 'info')
    elif response.status_code < 300: # 2xx
        return (True, 'successfully')
    elif response.status_code < 400: # 3xx
        return (True, 'redirection')
    elif response.status_code < 500: # 4xx
        return (False, 'client_error')
    elif response.status_code < 600: # 5xx
        return (False, 'server_error')

class ConsoleSession(object):
    def __init__(self, username, session, console_id):
        self.username   = username
        self.session    = session
        self.console_id = console_id

    def info(self):
        response = self.session.get(
            'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{console_id}/'.format(
                username=self.username, 
                console_id=self.console_id
                )
            )
        if checking_server_response(response)[0]:
            consoles_about = response.json()
            return consoles_about
    def get_latest_output(self):
        if self.console_id:
            response = self.session.get(
                'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{console_id}/get_latest_output/'.format(
                    username=self.username, 
                    console_id=self.console_id
                    )
                )
            if checking_server_response(response)[0]:
                consoles_about = response.json()
                return consoles_about
        else:
            return None
    def send_input(self, command):
        if self.console_id:
            send_status = self.session.post('https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{console_id}/send_input/'.format(
                    username=self.username, 
                    console_id=self.console_id
                    ),
                json={'input': str(command)}
            )
            if checking_server_response(send_status)[0]:
                return send_status.text
        else:
            return None
        

class Consoles(object):
    def __init__(self, username, session):
        self.session  = session
        self.username = username
    def all(self):
        response = self.session.get(
            'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/'.format(
                username=self.username
                )
        )
        if checking_server_response(response)[0]:
            all_consoles = response.json()
            return all_consoles
    def console(self, console_id=None): 
        if console_id:
            return ConsoleSession(self.username, self.session, console_id)

class pyAnywhere(object):
    def __init__(self, username, token):
        response = requests.get(
            'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(username=username),
            headers={'Authorization': 'Token {token}'.format(token=token)})
        if response.status_code == 200:
            self.username = username
            self.session  = requests.Session()
            self.session.headers.update({'Authorization': 'Token {token}'.format(token=token)})
        else:
            raise ErrorOutput("Incorrect data")
    def consoles(self):
        return Consoles(self.username, self.session)
