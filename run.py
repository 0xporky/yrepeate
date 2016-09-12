from flask import Flask
from flask import render_template
from flask import request
from flask import session
import string
import random

from models.user import User
from models.videos import Videos
from config import IP as ip
from config import PORT as port

secret = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
app = Flask(__name__)
app.config['SECRET_KEY'] = secret


@app.route('/')
def index():
    if 'id' not in session:
        user = User()
        user_id = user.create_user(id_generator())
        session['id'] = user_id

    return render_template('index.html', url='', msg='empty', result=dict())


@app.route('/play', methods=['POST'])
def form_result():
    result = request.form
    url = result.get('url')
    add = result.get('add')
    play = result.get('play')
    delete = result.get('delete')
    urls = list()

    if isinstance(play, (str, unicode)) and len(play) != 0:
        session['code'] = play
        return render_template('index.html',
                               url=decode_url(play),
                               msg='ok',
                               result=load_video_urls(session))

    if isinstance(delete, (str, unicode)) and len(delete) != 0:
        videos = Videos()
        if isinstance(delete, unicode):
            delete = delete.encode('ascii')
        videos.delete_video(delete)
        return render_template('index.html',
                               url=decode_url(session['code']),
                               msg='ok',
                               result=load_video_urls(session))

    if add == '1':
        user_id = session['id']
        code = session['code']
        videos = Videos()

        cur_videos = videos.get_playlist(user_id)
        if (len(cur_videos) < 6):
            videos.add_video(user_id, code)
        return render_template('index.html',
                               url=decode_url(code),
                               msg='ok',
                               result=load_video_urls(session))

    urls = load_video_urls(session)

    if len(url) == 0:
        if 'code' in session:
            code = session['code']
            return render_template('index.html',
                                   url=decode_url(code),
                                   msg='ok',
                                   result=urls)

    msg, code = handle_url(url)
    if msg == 'error':
        return render_template(index.html, url='', msg=msg, result=urls)

    session['code'] = code
    return render_template('index.html',
                           url=decode_url(code),
                           msg=msg,
                           result=urls)


def handle_url(url):
    tpl = 'watch?v='
    ridx = url.rfind(tpl)
    lidx = url.rfind('&')
    if ridx == -1:
        return ['error', '']
    if lidx == -1:
        return ['ok', url[ridx+len(tpl):]]
    return ['ok', url[ridx+len(tpl):lidx]]


def decode_url(code):
    return ''.join(['https://www.youtube.com/embed/',
                    code,
                    '?enablejsapi=1'])


def load_video_urls(my_session):
    urls = list()
    if 'id' in my_session:
        vid = Videos()
        video_list = vid.get_playlist(session['id'])
        for video in video_list:
            urls.append({video[0]: video[2]})
    return urls


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    app.run(host=ip, port=port)
