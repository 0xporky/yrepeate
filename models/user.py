from dborm import Dborm


class User(object):

    def __init__(self):
        self.orm = Dborm()
        self.table_name = "users"
        self.cols = ['id', 'name']

    def get_user(self, id):
        return self.orm.select(self.table_name,
                               self.cols,
                               'where id={0}'.format(id))

    def get_users(self):
        return self.orm.select(self.table_name,
                               self.cols)

    def create_user(self, name):
        cols = {'user': name}
        return self.orm.insert(self.table_name, cols)

    def delete_user(self, id):
        cols = {'id': id}
        return self.orm.delete(self.table_name, cols)
