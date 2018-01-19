import redis

r = redis.Redis(
        host='localhost',
        port=6379,
        charset="utf-8", 
        decode_responses=True)
        

#r.hmset('Player:0', {'username': 'test', 'fname': 'test', 'lname': 'test', 'welcome': 'welcome test'})
def info(section):
    return r.info(section)

class user:
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
    
class welcome:
    class type:
        def set(msg_type, uid):
            if int(uid) >= 0:
                r.hmset(str('Player:{0}'.format(uid)), {'welcome_type': msg_type})
            else:
                r.hmset(str('Group:{0}'.format(uid)), {'welcome_type': msg_type})
        
        def get(uid):
            if int(uid) >= 0:
                return r.hget('Player:{0}'.format(uid), 'welcome_type')
            else:
                return r.hget('Group:{0}'.format(uid), 'welcome_type')


    def set(msg, uid):
        if int(uid) >= 0:
            r.hmset(str('Player:{0}'.format(uid)), {'welcome': msg})
        else:
            r.hmset(str('Group:{0}'.format(uid)), {'welcome': msg})

    def delete(uid):
        if int(uid) >= 0:
            r.hdel(str('Player:{0}'.format(uid)), 'welcome')
        else:
            r.hdel(str('Group:{0}'.format(uid)), 'welcome')

    class file_id:
        def set(file_id, uid):
            if int(uid) >= 0:
                r.hmset(str('Player:{0}'.format(uid)), {'file_id': file_id})
            else:
                r.hmset(str('Group:{0}'.format(uid)), {'file_id': file_id})

        def get(uid):
            if int(uid) >= 0:
                return r.hget('Player:{0}'.format(uid), 'file_id')
            else:
                return r.hget('Group:{0}'.format(uid), 'file_id')

    def exists(uid):
        if int(uid) >= 0:
            return r.hexists('Player:{0}'.format(str(uid)), 'welcome')
        else:
            return r.hexists('Group:{0}'.format(str(uid)), 'welcome')

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



def getwelc(uid):
    if int(uid) >= 0:
        return r.hget('Player:{0}'.format(uid), 'welcome')
    else:
        return r.hget('Group:{0}'.format(uid), 'welcome')

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

class groupList:
    def add(groupId):
        r.sadd('Groups', groupId)
    def get():
        return r.smembers('Groups')
