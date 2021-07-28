class User():
    user_id = None
    def __init__(self,user_id):
        self.user_id = user_id

    def getUserId(self):
        return self.user_id

user = User(1000000001)
