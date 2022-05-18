class Database:
    def __init__(self):
        users = {}

    def get_user(self, id):
        if id not in self.users:
            return None

        return self.users[id]

    def update_user(self, id, user):
        self.users[id] = user
  


