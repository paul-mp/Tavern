from models import User
class UserRepository:

    def get_all_post(self):
        pass

    def get_post_by_id(self, post_id):
        pass

    def create_post(self, title, author, tag):
        pass

    def get_profile(self, user_id):
        pass

    def get_char(self, user_id):
        pass

    def create_comment(self, post_id, comment):
        pass

    def get_comment(self, post_id):
        pass

    def ____(self,):
        pass

user_repository_singleton = UserRepository()