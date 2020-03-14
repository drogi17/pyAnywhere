from pyAnywhere.pyAnywhere import pyAnywhere


username = ''
token = ''

user = pyAnywhere(username, token)

consoles_all = user.consoles().all()
get_console_id = consoles_all[0].get('id')
console_by_id = user.consoles().console(get_console_id).info()
send_input = user.consoles().console(get_console_id).send_input('echo hello\n')
get_latest_output = user.consoles().console(get_console_id).get_latest_output()

print(consoles_all)
print(console_by_id)
print(send_input)
print(get_latest_output)