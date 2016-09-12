from dborm import Dborm


class Videos(object):

    def __init__(self):
        self.orm = Dborm()
        self.table_name = "videos"
        self.cols = ['id', 'user_id', 'url']

    def get_playlist(self, user_id):
        state = 'where user_id={0}'.format(user_id)
        return self.orm.select(self.table_name,
                               self.cols,
                               state)

    def add_video(self, user_id, url):
        fields = {'user_id': user_id, 'url': url}
        return self.orm.insert(self.table_name,
                               fields)

    def delete_video(self, id):
        cols = {'id': id}
        return self.orm.delete(self.table_name, cols)
