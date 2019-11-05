class User:
    def __init__(self, id, username, followers):
        self.id = id
        self.username = username
        self.followers = followers

    def __repr__(self):
        return "User [id=" + self.id + ", username=" + self.username + ", followers=" + str(len(self.followers)) + "]"

    def __str__(self):
        # return "User [id=" + self.id + ", username=" + self.username + ", followers=" + str(len(self.followers)) + "]"
        return self.username
