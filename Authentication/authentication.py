import getpass
from user import user as User


class auth:
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    
    def __init__(self):
        self.logged_in = False
        
    def login(self, username, password):
        user = User().where_equal('username', username).first()
        if user == None:
            print('user do not exists!')
            return
        match = User.check_hashed_pass(password, user.password)
        if match:
            self.logged_in = True
            print('logged in')
        else:
            print('wrong credential!')


    def register(self, username, password):
        User().create(username, password)
        print('User registered')
        self.login(username, password)


def take_creadential():
    name = input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    return name, password


def login_case():
    auth().login(*take_creadential())


def register_case():
    auth().register(*take_creadential())


def take_input():
    print("[1]: login")
    print("[2]: register")
    return input("Select an option: ")


cases = {
    '1': login_case,
    '2': register_case
}

user_input = take_input()

cases.get(user_input)()