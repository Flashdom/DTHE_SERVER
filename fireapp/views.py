import pyrebase
from django.shortcuts import render
from django.views import View
import requests
import os

config = {
    "apiKey": "AIzaSyDdjxZi5Fw8qiJVcWMnawfImtnf3uMFGQM",
    "authDomain": "dthe-980e8.firebaseapp.com",
    "databaseURL": "https://dthe-980e8-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "dthe-980e8",
    "storageBucket": "dthe-980e8.appspot.com",
    "messagingSenderId": "381524571258",
    "appId": "1:381524571258:web:1ef2567a345f3806a6b7c3",
    "measurementId": "G-WWS9MQDG5C",
    "serviceAccount": "C:/Users/arr98\PycharmProjects\pythonProject/venv/fireapp/dthe-980e8-firebase-adminsdk-iom8x-7d9a521033.json"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()


class MlUserData(View):

    def get(self, request, uid) -> render:
        template = 'mluserdata.html'
        audios = storage.child("audios").child(uid)
        data = database.child("audio").child(uid).get()
        keys = []
        paths = []
        for pyre in data.pyres:
            keys.append(pyre.key())
        for key in keys:
            storage.child("audios").child(uid).child(key).download(
               path="C:/Users/arr98/PycharmProjects/pythonProject/venv/fireapp/", filename=key + ".wav")
            r = requests.get(storage.child("audios").child(uid).child(key).get_url(None), timeout=5)

            # save response data to disk
            if r.status_code == 200:
                path = 'C:/Users/arr98/PycharmProjects/pythonProject/venv/fireapp/' + key
                with open(path + ".wav", 'wb') as f:
                    f.write(r.content)
                paths.append(path)

        context = {

        }
        return render(request, template, context)


class HomePage(View):
    """Главная страница"""

    def get(self, request) -> render:
        template = 'index.html'

        data = database.child('users').shallow().get().val()
        userData = []
        for obj in data:
            tmp = []
            userid = obj
            username = database.child('users').child(
                userid).child('name').get().val()
            tmp.append(userid)
            tmp.append(username)
            userData.append(tmp)

        print(userData)

        context = {
            'userdata': userData,
        }

        return render(request, template, context)


class UserData(View):
    """Страница пользователя"""

    def get(self, request, uid) -> render:
        template = 'userdata.html'

        # data = database.child('users').shallow().get().val()
        name = database.child('users').child(uid).child('name').get().val()
        location = UserData.exeptions('location', uid)
        notes = UserData.exeptions('notes', uid)
        photo = UserData.exeptions('photo', uid)
        video = UserData.exeptions('video', uid)
        audio = UserData.exeptions('audio', uid)
        sumdata = len(location) + len(notes) + len(photo) + len(video)
        time_set = [
            # [start_datatime, end_datatime]
            [2312442134, 2423424234]
        ]
        time_location = [
            'ул. Кремлевская, 35, Kazan, Respublika Tatarstan, Russia, 420111'
        ]

        # объееняем списки строк
        text = ' '.join(notes)
        # и т.д.
        lst_no = ['.', ',', ':', '!', '"', "'", '[', ']', '-', '—', '(', ')']
        lst = []
        for word in text.lower().split():
            if not word in lst_no:
                _word = word
                if word[-1] in lst_no:
                    _word = _word[:-1]
                if word[0] in lst_no:
                    _word = _word[1:]
                lst.append(_word)

        _dict = dict()
        for word in lst:
            _dict[word] = _dict.get(word, 0) + 1
        # сортируем словарь посредством формирования списка (значение, ключ)
        _list = []
        for key, value in _dict.items():
            _list.append((value, key))
            _list.sort(reverse=True)
        # печатаем первые 3 самых используемых слов
        sumstr = []
        for freq, word in _list[0:3]:
            sumstr.append(f'{word:>3} -> {freq:>3}')

        timeset = ''
        print(location)
        if len(location) > 0:
            for item in location:
                for local in time_location:
                    if item['name'] == str(local):
                        for timepar in time_set:
                            if (item['time'] >= timepar[0]) and (item['time'] <= timepar[1]):
                                timeset = timeset + 'Занятие №' + str(location.index(item) + 1) + ' посещено, '
                            else:
                                timeset = timeset + 'Занятие №' + str(location.index(item) + 1) + ' не посещено, '
                    else:
                        timeset = timeset + 'Занятие №' + str(location.index(item) + 1) + ' не посещено, '
        else:
            timeset = ''

        context = {
            'name': name,
            'sumdata': sumdata,
            'sumstr': sumstr,
            'timeset': timeset
        }

        return render(request, template, context)

    def exeptions(variable, uid):
        data = database.child(variable).child(uid).get().val()
        try:
            var = list(filter(None, data))
            return var
        except:
            var = []
            return var
