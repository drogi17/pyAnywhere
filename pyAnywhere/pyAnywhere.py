import requests, json

class Error_pyAnywhere(Exception):
    def __init__(self, text):
        self.txt = text


class console_class(object):
    def __init__(self, username, token, id_console):
        self.token      = token
        self.username   = username
        self.id_console = id_console
    def info(self):
        response = requests.get(
            'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{id_console}/'.format(username=self.username, id_console=self.id_console),
            headers={'Authorization': 'Token {token}'.format(token=self.token)}).content.decode()
        consoles_about = json.loads(response)
        return consoles_about
    def get_latest_output(self):
        if self.id_console:
            response = requests.get(
                'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{id_console}/get_latest_output/'.format(
                    username=self.username, 
                    id_console=self.id_console
                    ),
                headers={'Authorization': 'Token {token}'.format(token=self.token)}).content.decode()
            consoles_about = json.loads(response)
            return consoles_about
        else:
            return None
    def send_input(self, command):
        if self.id_console:
            data_send = requests.post('https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{id_console}/send_input/'.format(
                    username=self.username, 
                    id_console=self.id_console
                    ),
                headers={'Authorization': 'Token {token}'.format(token=self.token)},
                json={'input': str(command)})
            return data_send.text
        else:
            return None
        

class consoles_class(object):
    def __init__(self, username, token):
        self.token      = token
        self.username   = username

    def all(self):
        response = requests.get(
            'https://www.pythonanywhere.com/api/v0/user/{username}/consoles/'.format(
                    username=self.username),
            headers={'Authorization': 'Token {token}'.format(token=self.token)}
        ).content.decode()
        consoles_all = json.loads(response)
        return consoles_all
    def console(self, id_console=None): 
        if id_console:
            return console_class(self.username, self.token, id_console)

class pyAnywhere(object):
	__name__ = 'pyAnywhere'
	__vesrion__ = '1'
    def __init__(self, username, token):
        response = requests.get(
            'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(username=username),
            headers={'Authorization': 'Token {token}'.format(token=token)})
        if response.status_code == 200:
            self.token = token
            self.username = username
        else:
            raise Error_pyAnywhere("Incorrect data")
    def consoles(self):
        return consoles_class(self.username, self.token)
