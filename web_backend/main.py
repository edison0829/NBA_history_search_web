from firebase import FirebaseApplication
from firebase import firebase
from flask import Flask,render_template,request,session,redirect,jsonify,url_for
import flask
import re
import ast
import difflib

app = Flask(__name__)
firebase_search = FirebaseApplication('https://inf551-project-e0336.firebaseio.com', None)
firebase_register = FirebaseApplication('https://sign-up-d8e33.firebaseio.com', None)
firebase_savesSearch = FirebaseApplication('https://history-data.firebaseio.com/.json', None)

result = firebase_search.get('/', '')  # dict

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# global display
# global searchByFacet


def convert_keys_to_string(dictionary):
    if not isinstance(dictionary, dict):
        return dictionary
    return {str(k).replace("u",""): str(v) for k, v in dictionary.items()}

def convert(dictionary):
    if not isinstance(dictionary, dict):
        return dictionary
    return {str(k).replace("u",""): str(v).replace("u","") for k, v in dictionary.items()}

# def convert(dictionary):
#     if not isinstance(dictionary, dict):
#         return dictionary
#     for k, v in dictionary.items():
#         if str(k)[0] == 'u':
#             k = str(k)[1:]
#         if str(v)[0] == 'u':
#             v = str(v)[1:]
#         return {str(k): str(v)}

def facetSearch():
    facetByName = []
    facetByTeam = []
    facetByPos = []
    for i in range(len(result)):
        name = convert_keys_to_string(result[i]['Player'])
        team = convert_keys_to_string(result[i]['Tm'])
        pos = convert_keys_to_string(result[i]['Pos'])

        if facetByName == None or (name not in facetByName):
            facetByName.append(name)
        if facetByTeam == None or (team not in facetByTeam):
            facetByTeam.append(team)
        if facetByPos == None or (pos not in facetByPos):
            facetByPos.append(pos)
    facetByName = sorted(facetByName)
    facetByTeam = sorted(facetByTeam)
    facetByPos = sorted(facetByPos)
    facet = [facetByName,facetByTeam,facetByPos]
    return facet

facet = facetSearch()



@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', facet=facet, username=username)
    return render_template('index.html',facet=facet)





@app.route('/searchByFacet',methods=['POST','GET'])
def searchByFacet():
    if request.method == 'POST':
        playerName = request.form['playerName']
        playerTeam = request.form['playerTeam']
        playerPosition = request.form['playerPosition']

        display = [playerName,playerTeam,playerPosition]
        searchByFacet = []
        for i in range(len(result)):
            # 1
            if playerName != '' and playerTeam == '' and playerPosition == '' and result[i]['Player'].upper() == playerName.upper():
                searchByFacet.append(convert_keys_to_string(result[i]))
            if playerName == '' and playerTeam != '' and playerPosition == '' and result[i]['Tm'].upper() == playerTeam.upper() :
                searchByFacet.append(convert_keys_to_string(result[i]))
            if playerName == '' and playerTeam == '' and playerPosition != ''  and result[i]['Pos'].upper() == playerPosition.upper():
                searchByFacet.append(convert_keys_to_string(result[i]))

            # 2
            if playerName != '' and playerTeam != '' and playerPosition == '' and result[i]['Player'].upper() == playerName.upper() and result[i]['Tm'].upper() == playerTeam.upper():
                searchByFacet.append(convert_keys_to_string(result[i]))
            if playerName != '' and playerTeam == '' and playerPosition != '' and result[i]['Player'].upper() == playerName.upper() and result[i]['Pos'].upper() == playerPosition.upper():
                searchByFacet.append(convert_keys_to_string(result[i]))
            if playerName == '' and playerTeam != '' and playerPosition != '' and result[i]['Tm'].upper() == playerTeam.upper() and result[i]['Pos'].upper() == playerPosition.upper():
                searchByFacet.append(convert_keys_to_string(result[i]))

            # 3
            if playerName != '' and playerTeam != '' and playerPosition != '' and result[i]['Player'].upper() == playerName.upper() and result[i]['Tm'].upper() == playerTeam.upper() and result[i]['Pos'].upper() == playerPosition.upper():
                searchByFacet.append(convert_keys_to_string(result[i]))

        if 'username' in session:
            username = session['username']
            username = username.replace('.', '')
            loves = []
            saved = firebase_savesSearch.get('/' + username, None)
            if saved != None:
                savedSearch = saved.values()
                for s in savedSearch:
                    for i  in searchByFacet:
                        if convert(s) == convert(i):
                            loves.append(i)
            session['search'] = searchByFacet[:20]
            session['display'] = display
            session['loves'] = loves
            session['label'] = 'face'
            return render_template('index-searchByFacet.html',searchByFacet = searchByFacet,facet=facet,display=display, username=username,loves=loves)

        return render_template('index-searchByFacet.html',searchByFacet = searchByFacet,facet=facet,display=display)


@app.route('/searchByKeyword',methods=['POST','GET'])
def searchByKeyword():
    if request.method == 'POST':
        display = request.form['searchByKey']
        searchByKeyword = []
        outKey = []
        for item in result:
            flag = 0
            for key, value in item.items():
                if display != '':
                    if str(display.upper()) in str(value.upper()):
                        flag = 2
                    else:
                        for i in display:
                            if str(i.upper()) in str(value.upper()):
                                flag = 1
            if flag == 1:
                outKey.append(convert_keys_to_string(item))
            if flag == 2:
                searchByKeyword.append(convert_keys_to_string(item))

        searchByKeyword = sorted(searchByKeyword,
                                 key=lambda z: (difflib.SequenceMatcher(None, str(z.values()), display).ratio()),
                                 reverse=True) + \
                          sorted(outKey,
                                 key=lambda z: (difflib.SequenceMatcher(None, str(z.values()), display).ratio()),
                                 reverse=True)
        if 'username' in session:
            username = session['username']
            username = username.replace('.', '')
            loves = []
            saved = firebase_savesSearch.get('/' + username, None)
            if saved != None:
                savedSearch = saved.values()
                for s in savedSearch:
                    for i  in searchByKeyword:
                        if convert(s) == convert(i):
                            loves.append(i)

            session['search'] = searchByKeyword[:20]
            session['display'] = display
            session['loves'] = loves
            session['label'] = 'key'
            return render_template('index-searchByKeyword.html',display=display,searchByKeyword=searchByKeyword,username=username,loves=loves)

        return render_template('index-searchByKeyword.html',display=display,searchByKeyword=searchByKeyword)

    return render_template('index-searchByKeyword.html')


@app.route('/logInAndSignUp', methods=['GET', 'POST'])
def logInAndSignUp():
    register_Data = {'Email' : request.form.get('email'),'User name' : request.form.get('username'),'Password' : request.form.get('currentPassword')}
    firebase_register.post('/',register_Data)
    print request.form
    login_Data = [request.form.get('emailnow'),request.form.get('password')]
    check = firebase_register.get('/',None)
    keyword=[]

    for key, value in check.iteritems():
        keyword.append([value['Email'],value['Password']])

    if login_Data in keyword:
        session['username'] = login_Data[0]
        username = session['username']
        return render_template('index.html', facet=facet, username=username)
    else:
        flask.flash('Log-in failed.')
        return render_template('logInAndSignUp.html')


@app.route('/savedSearch',methods=['POST','GET'])
def savedSearch():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            item = request.form.get('searchItem')
            item = ast.literal_eval(item)
            username = username.replace('.','')
            flag = 0
            saved = firebase_savesSearch.get('/' + username, None)
            rm_data = ''
            rm_key = ''
            if saved != None:
                savedSearch = saved.values()
                for s in savedSearch:
                    if s == item:
                        rm_data = s
                        flag = 1
            else:
                flag = 0
            if flag == 0:
                firebase_savesSearch.post('/'+username,item)
            if flag == 1:
                for key, value in saved.iteritems():
                    if value == rm_data:
                        print key
                        firebase_savesSearch.delete('/' + username +'/'+key, None)
            saved = firebase_savesSearch.get('/' + username, None)
            if saved != None:
                savedSearch = saved.values()
            else:
                savedSearch = []
            if session['label'] == 'key':
                loves = []
                for s in savedSearch:
                    for i  in session['search']:
                        if convert(s) == convert(i):
                            loves.append(i)
                session['loves'] = loves
                return render_template('index-searchByKeyword.html',display=session['display'],searchByKeyword=session['search'],username=username,loves=session['loves'])
            else:
                loves = []
                for s in savedSearch:
                    for i  in session['search']:
                        if convert(s) == convert(i):
                            loves.append(i)
                session['loves'] = loves
                return render_template('index-searchByFacet.html',searchByFacet = session['search'],facet=facet,display=session['display'], username=username,loves=session['loves'])
    else:
        return render_template('logInAndSignUp.html')


@app.route('/usersCenter')
def usersCenter():
    if 'username' in session:
        username = session['username'].replace('.', '')
        saved = firebase_savesSearch.get('/'+username, None)
        if saved != None:
            savedSearch = saved.values()
            return render_template('usersCenter.html',savedSearch=savedSearch)
        else:
            return render_template('usersCenter.html')


@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('loves', None)
    session.pop('search', None)
    return render_template('index.html',facet=facet)


if __name__ == "__main__":
    app.run(debug=True)
