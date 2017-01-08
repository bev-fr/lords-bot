import redis

r = redis.Redis(
        host='localhost',
        port=6379,
        charset="utf-8", 
        decode_responses=True)
        

r.hmset('Player:0', {'username': 'test', 'fname': 'test', 'lname': 'test', 'welcome': 'welcome test'})
val = r.hmget('Player:0', 'welcome')

def setwelc(msg, uid):
    if uid >= 0:
        r.hmset(str('Player:{0}'.format(uid)), {'welcome': msg})
    if else:
        r.hmset(str('Group:{0}'.format(uid)), {'welcome': msg})

def getwelc(uid):
    if uid >= 0:
        return r.hget('Player:{0}'.format(uid), 'welcome')
    if else:
        return r.hget('Group:{0}'.format(uid), 'welcome')

def exists(uid):
    return r.exists('Player:{0}'.format(str(uid)))

def adduser(uid, fname, lname, uname):
    r.hmset('Player:{0}'.format(uid), {'username': uname, 'fname': fname, 'lname': lname})

def addgroup(gid, title, uname):
    r.hmset('Group:{0}'.format(gid), {'title': title, 'username': uname})

