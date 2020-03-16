import requests, json

class Error_pyAnywhere(Exception):
    def __init__(self, text):
        self.txt = text


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
            ).content.decode()
        consoles_about = json.loads(response)
        return consoles_about
    def get_latest_output(self):
        if self.console_id:
            response = self.session.get(
                'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{console_id}/get_latest_output/'.format(
                    username=self.username, 
                    console_id=self.console_id
                    )
                ).content.decode()
            consoles_about = json.loads(response)
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
        ).content.decode()
        all_consoles = json.loads(response)
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
            # self.token    = token
            self.username = username
            self.session  = requests.Session()
            self.session.headers.update({'Authorization': 'Token {token}'.format(token=token)})
        else:
            raise Error_pyAnywhere("Incorrect data")
    def consoles(self):
        return Consoles(self.username, self.session)
