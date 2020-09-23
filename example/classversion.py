import requests

url = 'http://localhost:8000'


def start(user, problem, count):
    uri = url + '/start' + '/' + user + '/' + str(problem) + '/' + str(count)
    return requests.post(uri).json()


def oncalls(token):
    uri = url + '/oncalls'
    data = requests.get(uri, headers={'X-Auth-Token': token}).json()
    return data


def action(token, cmds):
    uri = url + '/action'
    requests.post(uri, headers={'X-Auth-Token': token}, json={'commands': cmds})
class Elevator:
    def __init__(self,floor,bottom,loof):
        self.to_up = True
        self.passengers = []
        self.status = "STOPED"
        self.floor = bottom
        self.bottom = bottom
        self.max_floor = loof
        self.call_ids = []
    def
def p0_simulator():

    user = 'tester'
    problem = 0
    count = 1
    elevators = []

    ret = start(user, problem, count)
    token = ret['token']

if __name__ == '__main__':
    p0_simulator()
