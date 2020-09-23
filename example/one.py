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


def direction(start, end):
    if start > end:
        return "DOWN"
    else:
        return "UP"


# def adjElevator(elevators, start, direction):
#     for elevator,index in enumerate(elevators):
#         if direction=="UP":
#             start = elevator['floor']
#         else:
def check(es, person):
    d = direction(person['start'], person['end'])
    if d=="UP":
        if es['status']=="UP" and es['floor']<person['start']:
            return True
        elif es['status']=="STOP":
            return True
        else:
            return False
    else:
        if es['status'] == "UP" and es['floor'] > person['start']:
            return True
        elif es['status'] == "STOP":
            return True
        else:
            return False
def setLoop(es,call):

    el = call['elevators'][0]

    es['floor'] = el['floor']
    es['status'] = el['status']
def p0_simulator():
    # for i in range(3):
    user = 'tester'
    problem = 0
    count = 1

    ret = start(user, problem, count)
    token = ret['token']
    elevator_status = [{"id": i, "yetPassenger":[], "passenger": [], "status": "STOP", "floor": 1, "dest": 10000}.copy() for i in
                       range(count)]
    es = {"id": 0, "passengers": [],"direction":"UPWARD", "status": "STOP", "floor": 1, "dest": 1,"call_ids":[],"action":""}
    yetPassenger = []

    while True:
        call_result = oncalls(token)
        calls = call_result['calls']
        es['call_ids'] = []
        elevators = call_result['elevators']
        setLoop(es,call_result)
        if call_result['is_end'] == "true":
            flag = False
            for i in range(count):
                if len(elevators['passengers']) != 0:
                    flag = True
            if not flag:
                break
        yetPassenger+=calls
        print(es)
        if len(es['passengers'])==0:
            m=11110
            ind= -1
            for j,i in enumerate(yetPassenger):
                if m>abs(es['floor']-i['start']):
                    m = abs(es['floor']-i['start'])
                    ind = j
            if ind!=-1:
                es['passengers'].append(yetPassenger[ind])
                es['dest'] = yetPassenger[ind]['start']
                yetPassenger.pop(ind)
            if es['dest']>es['floor']:
                es['direction']="UPWARD"
                es['action']="UP"
            else:
                es['direction']="DOWNWARD"
                es['action'] = "DOWN"


        elif es['direction']=="UPWARD":
            if es['status']=="STOPPED":
                flag = False
                for i in yetPassenger:
                    if i['start']==es['floor']:
                        flag=True
                for i in es['passengers']:
                    if i['end']==es['floor']:
                        flag=True
                if flag:
                    es['status'] = "OPENED"
                    es['action'] = "OPEN"


            elif es['status']=="OPENED":
                plist = []
                idxlist = []
                for idx,i in enumerate(es['passengers']):

                    if es['floor']==i['end']:
                        plist.append(i['id'])
                        idxlist.append(idx)
                for i in reversed(idxlist):
                    es['passengers'].pop(i)
                if len(plist)>0:
                    es['action']="EXIT"
                    es['call_ids']+=plist

                else:
                    for idx,i in enumerate(yetPassenger):
                        if es['floor']==i['start']:
                            plist.append(i['id'])
                            idxlist.append(idx)
                    for i in reversed(idxlist):
                        yetPassenger.pop(i)
                    if len(plist)>0:
                        es['action']="ENTER"
                        es['call_ids']+=plist

            else:
                flag = False
                for i in yetPassenger:
                    if i['start']==es['floor']:
                        flag=True
                for i in es['passengers']:
                    if i['end']==es['floor']:
                        flag=True
                if flag:
                    es['action']="STOP"

        elif es['direction']=="DOWNWARD":
            if es['status']=="STOPPED":
                plist = []
                for i in es['passengers']:
                    if es['floor']==i['end']:
                        plist.append(i['id'])
                if len(plist)>0:
                    es['status']="OPENED"
                    es['action']="OPEN"

            elif es['status']=="OPENED":
                plist = []
                idxlist = []
                for idx,i in enumerate(es['passengers']):
                    if es['floor']==i['end']:
                        plist.append(i['id'])
                        idxlist.append(idx)
                for i in reversed(idxlist):
                    es['passengers'].pop(i)
                if len(plist)>0:
                    es['action']="EXIT"
                    es['call_ids']+=plist

                else:
                    for idx,i in enumerate(yetPassenger):
                        if es['floor']==i['start']:
                            plist.append(i['id'])
                            idxlist.append(idx)
                    for i in reversed(idxlist):
                        yetPassenger.pop(i)
                    if len(plist)>0:
                        es['action']="ENTER"
                        es['call_ids']+=plist

            else:
                flag = False
                for i in yetPassenger:
                    if i['start']==es['floor']:
                        flag=True
                for i in es['passengers']:
                    if i['end']==es['floor']:
                        flag=True
                if flag:
                    es['action']="STOP"

        action(token, [{'elevator_id': 0, 'command': es['action'], 'call_ids': es['call_ids']}])




if __name__ == '__main__':
    p0_simulator()
