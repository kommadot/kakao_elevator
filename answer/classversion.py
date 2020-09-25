import requests
import time
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
    return requests.post(uri, headers={'X-Auth-Token': token}, json={'commands': cmds}).text


def selection(call,elevators):

    result = elevators[0]
    m=10000

    for elevator in elevators:
        if elevator.floor > elevator.dest:
            if call['start']<=elevator.floor:
                if m>elevator.floor - call['start']:
                    result=elevator
                    m = elevator.floor -call['start']
        else:
            if call['start']>=elevator.floor:
                if m>call['start']-elevator.floor:
                    result=elevator
                    m = call['start']-elevator.floor
    return result
class Elevator:
    def __init__(self,floor,bottom,loof):
        self.to_up = True
        self.passengers = []
        self.status = "STOPED"
        self.floor = bottom
        self.bottom = bottom
        self.max_floor = loof
        self.src = 0
        self.dest = 0
        self.call_ids = []
        self.call = []

    def set_info(self,elevator):
        self.status = elevator['status']
        self.floor = elevator['floor']
        self.passengers = elevator['passengers']

    def add_call(self,call):
        if self.src == 0 and self.dest == 0 :
            self.src = self.floor
            self.dest = call['start']
        self.call.append(call)

    def set_dest(self):
        if self.dest!=self.floor:
            return
        if not self.passengers and self.call:
            mi = 10000
            c = None
            for call in self.call:
                if mi>abs(self.floor-call['start']):
                    mi = abs(self.floor-call['start'])
                    c = call
            self.dest = c['start']
        elif not self.call and self.passengers:
            mi = 10000
            c = None
            for passenger in self.passengers:
                if mi>abs(self.floor-passenger['end']):
                    mi = abs(self.floor-passenger['end'])
                    c = passenger
            self.dest = c['end']
        elif self.call and self.passengers:
            mi = 10000
            c = None
            for passenger in self.passengers:
                if mi>abs(self.floor-passenger['end']):
                    mi = abs(self.floor-passenger['end'])
                    c = passenger
            self.dest = c['end']
        else:
            if self.floor<self.max_floor:
                self.dest = self.max_floor
            else:
                self.dest = self.bottom
    def action(self):

        to_enter = [call for call in self.call if call['start']==self.floor]
        to_exit = [passenger for passenger in self.passengers if passenger['end']==self.floor]

        if len(to_enter)>0:
            if self.status=="STOPPED":
                return "OPEN"
            elif self.status=="OPENED":
                ret = {}
                ret['ACTIONS'] = "ENTER"
                self.passengers.extend(to_enter)
                temp = []
                for i in self.call:
                    if not i in to_enter:
                        temp.append(i)
                self.call=temp
                ret['CALLID'] = [x['id'] for x in to_enter]
                return ret
            else:
                return "STOP"
        if len(to_exit)>0:

            if self.status=="STOPPED":
                return "OPEN"
            elif self.status=="OPENED":
                ret = {}
                ret['ACTIONS'] = "EXIT"
                temp = []
                for i in self.passengers:
                    if not i in to_exit:
                        temp.append(i)
                self.passengers = temp
                ret['CALLID'] = [x['id'] for x in to_exit]
                return ret
            else:
                return "STOP"
        if self.status=="OPENED":
            return "CLOSE"
        if self.floor ==self.dest:
            self.set_dest()
        if self.status=="STOPPED":
            if self.floor>self.dest:
                return "DOWN"
            elif self.floor<self.dest:
                return "UP"
        #올라가거나 내려가는 상황일때

        if self.floor<self.dest:
            if self.status=="DOWNWARD":
                return "STOP"
            return "UP"
        else:
            if self.status=="UPWARD":
                return "STOP"
            return "DOWN"
        # return self.status
    def __str__(self):
        return f"콜수 : {len(self.call)} , 승객수 : {len(self.passengers)} , 출발층 : {self.src}, 도착층 : {self.dest} , 현재층 : {self.floor} , 상태 {self.status}"

def p0_simulator():

    user = 'komad'
    floor = [5,25,25]
    for i in range(3):
        count = 4
        ret = start(user, i, count)
        elevators = [Elevator(1, 1, floor[i]) for e in range(count)]
        token = ret['token']
        timestamp = 0
        idval = -1
        k = []
        print(f"{i} problem start")
        while True:
            #명령을 전달한다. 엘리베이터의

            calls = oncalls(token)
            if calls['is_end']:
                timestamp = calls['timestamp']
                break
            command = []

            percall = calls['calls']


            for a in percall:
                if a['id']>idval:
                    k.append(a)
                    idval=a['id']

            for idx,elevator in enumerate(elevators):
                elevator.set_info(calls['elevators'][idx])


            for call in k:
                el = selection(call,elevators)
                if len(el.passengers)+len (el.call)>=8:
                    continue
                el.add_call(call)
                k.remove(call)

            for idx,elevator in enumerate(elevators):
                ret = elevator.action()
                if type(ret) == dict:
                    command.append({'elevator_id':idx,'command':ret['ACTIONS'],'call_ids':ret['CALLID']})
                else:
                    command.append({'elevator_id':idx,'command':ret})
            # print(command)
            action(token,command)

        print(f"result : {timestamp}")
        print()
if __name__ == '__main__':
    p0_simulator()
