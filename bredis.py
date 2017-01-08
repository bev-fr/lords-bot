import redis

r = redis.Redis(
        host='localhost',
        port=6379,
        charset="utf-8", 
        decode_responses=True)
        

#r.hmset('Player:0', {'username': 'test', 'fname': 'test', 'lname': 'test', 'welcome': 'welcome test'})

def setwelc(msg, uid):
    if int(uid) >= 0:
        r.hmset(str('Player:{0}'.format(uid)), {'welcome': msg})
    else:
        r.hmset(str('Group:{0}'.format(uid)), {'welcome': msg})

def getwelc(uid):
    if int(uid) >= 0:
        return r.hget('Player:{0}'.format(uid), 'welcome')
    else:
        return r.hget('Group:{0}'.format(uid), 'welcome')

def exists(uid):
    return r.exists('Player:{0}'.format(str(uid)))

def adduser(uid, fname, lname, uname):
    r.hmset('Player:{0}'.format(uid), {'username': uname, 'fname': fname, 'lname': lname})

def addgroup(gid, title, uname):
    r.hmset('Group:{0}'.format(gid), {'title': title, 'username': uname})

def info(uid):
    if int(uid) >= 0:
        return r.hgetall(str('Player:{0}'.format(uid)))
    else:
        return r.hgetall(str('Group:{0}'.format(uid)))

def addsuperadmin(uid):
    r.sadd('superadmins', uid[0])

def isSuperAdmin(uid):
    if r.sismember(superadmins, uid) == 1:
        return True
    else: 
        return False
