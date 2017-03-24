import redis

r = redis.Redis(
        host='localhost',
        port=6379,
        charset="utf-8", 
        decode_responses=True)
        

#r.hmset('Player:0', {'username': 'test', 'fname': 'test', 'lname': 'test', 'welcome': 'welcome test'})

class User:
    def __init__(self, uid):
        self.fname = r.hget(str('Player:{0}'.format(uid)), "fname")

    def all(uid):
        if int(uid) >= 0:
            return r.hgetall(str('Player:{0}'.format(uid)))
        else:
            return r.hgetall(str('Group:{0}'.format(uid)))
        
    def name(uid):
        if int(uid) >= 0:
            return r.hget(str('Player:{0}'.format(uid)), "fname")
        else:
            return r.hget(str('Group:{0}'.format(uid)), "title")
    
#    class welcome:
#        def set
#        r.hmset(str('Player:{0}'.format(uid)), {'welcome': msg})
#
#class group:
#    def setwelc(msg, uid):
#            r.hmset(str('Group:{0}'.format(uid)), {'welcome': msg})
#
#    def remwelc(uid):
#        if int(uid) >= 0:
#            r.hdel(str('Player:{0}'.format(uid)), 'welcome')
#        else:
#            r.hdel(str('Group:{0}'.format(uid)), 'welcome')
#
#    def getwelc(uid):
#        if int(uid) >= 0:
#            return r.hget('Player:{0}'.format(uid), 'welcome')
#        else:
#            return r.hget('Group:{0}'.format(uid), 'welcome')

def setwelc(msg, uid):
    if int(uid) >= 0:
        r.hmset(str('Player:{0}'.format(uid)), {'welcome': msg})
    else:
        r.hmset(str('Group:{0}'.format(uid)), {'welcome': msg})

def remwelc(uid):
    if int(uid) >= 0:
        r.hdel(str('Player:{0}'.format(uid)), 'welcome')
    else:
        r.hdel(str('Group:{0}'.format(uid)), 'welcome')

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

class superadmin:
    def add(uid):
        r.sadd('superadmins', uid[0])

    def check(uid):
        if r.sismember("superadmins", uid) == 1:
            return True
        else: 
            return False
    def get():
        return r.smembers('superadmins')

class blocked:
    def add(uid):
        r.sadd('blocked', uid)

    def check(uid):
        if r.sismember("blocked", uid) == 1:
            return True
        else: 
            return False
    def get():
        return r.smembers('blocked')
    def rem(uid):
        r.srem('blocked', uid)
