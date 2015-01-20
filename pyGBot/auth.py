

class AuthLevels:
    User = 0
    Mod = 100
    Admin = 200


class User:
    def __init__(self, host, level=AuthLevels.User):
        self.nick = host.split('!', 1)[0]
        #self.host = host.split('!', 1)[1]
        self.level = level


users = {}


def get_userlevel(user):
    if user in users:
        return users[user].level
    else:
        newuser = User(user)
        users[user] = newuser
        return newuser.level


def set_userlevel(user, level):
    if user in users:
        users[user].level = level
    else:
        newuser = User(user)
        newuser.level = level
        users[user] = newuser


def rename_user(oldname, newname):
    if oldname in users:
        level = get_userlevel(oldname)
        set_userlevel(newname, level)
        del users[oldname]


def delete_user(user):
    if user in users:
        del users[user]
