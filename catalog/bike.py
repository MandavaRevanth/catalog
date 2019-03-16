from flask import Flask, render_template, request
from flask import redirect, url_for, jsonify, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from showroom_database import Showroom, Bike, Base, User
from flask import session as login_session
import random
import string
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "showroom bikes item-catalog"
engine = create_engine(
    'sqlite:///bikewala.db',
    connect_args={'check_same_thread': False}, echo=True
    )
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# For User login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current state is %s" %login_session['state']
    showroom = session.query(Showroom).all()
    bike = session.query(Bike).all()
    return render_template('login.html', STATE=state, showroom=showroom,
                           bike=bike)


# If User already logged
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                                 json.dumps(
                                            'Current user already connected'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<center><h2><font color="green">Welcome '
    output += login_session['username']
    output += '!</font></h2></center>'
    output += '<center><img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; -webkit-border-radius: 200px;" '
    output += ' " style = "height: 200px;border-radius: 200px;" '
    output += ' " style = "-moz-border-radius: 200px;"></center>" '
    flash("you are now logged in as %s" % login_session['username'])
    print("Done")
    return output


def createUser(login_session):
        newUser = User(
            name=login_session['username'],
            email=login_session['email'],
            picture=login_session['picture']
            )
        session.add(newUser)
        session.commit()
        user = session.query(User)
        filter_by(email=login_session['email']).one()
        return user.id


# Getting information of user
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# Getting user email address
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        return None


# To read showroom JSON data on web browser
@app.route('/showroom/JSON')
def showroomJSON():
    showroom = session.query(Showroom).all()
    return jsonify(showroom=[s.serialize for s in showroom])


# To read showroom wise of bike JSON
@app.route('/showroom/<int:showroom_id>/menu/<int:bike_id>/JSON')
def showroomListJSON(showroom_id, bike_id):
    Bike_List = session.query(Bike).filter_by(id=bike_id).one()
    return jsonify(Bike_List=Bike_List.serialize)


# To read bikes JSON
@app.route('/showroom/<int:bike_id>/menu/JSON')
def bikeListJSON(bike_id):
    showroom = session.query(Showroom).filter_by(id=bike_id).one()
    bike = session.query(Bike).filter_by(bike_id=showroom.id).all()
    return jsonify(BikeLists=[i.serialize for i in bike])


# This is a home page of entire project
@app.route('/showroom/')
def showShowroom():
    showroom = session.query(Showroom).all()
    return render_template('showroom.html', showroom=showroom)


# Create new Showroom
@app.route('/showroom/new/', methods=['GET', 'POST'])
def newShowroom():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newShowroom = Showroom(
            name=request.form['name'],
            user_id=login_session['user_id']
            )
        session.add(newShowroom)
        session.commit()
        return redirect(url_for('showShowroom'))
    else:
        return render_template('newShowroom.html')


# To Editing existing showroom name
@app.route('/showroom/<int:showroom_id>/edit/', methods=['GET', 'POST'])
def editShowroom(showroom_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedShowroom = session.query(Showroom).filter_by(id=showroom_id).one()
    creater_id = getUserInfo(editedShowroom.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("You cannot edit this Showroom "
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showShowroom'))
    if request.method == 'POST':
        if request.form['name']:
            editedShowroom.name = request.form['name']
            flash(
                "Showroom Successfully Edited %s"
                % (editedShowroom . name)
                )
            return redirect(url_for('showShowroom'))
    else:
        return render_template('editShowroom.html', showroom=editedShowroom)


# To Deleting existing Showroom
@app.route('/showroom/<int:showroom_id>/delete/', methods=['GET', 'POST'])
def deleteShowroom(showroom_id):
    if 'username' not in login_session:
        return redirect('/login')
    showroomToDelete = session.query(Showroom).filter_by(id=showroom_id).one()
    creater_id = getUserInfo(showroomToDelete.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("You cannot delete this Showroom "
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showShowroom'))

    if request.method == 'POST':
        session.delete(showroomToDelete)
        flash("Successfully Deleted %s" % (showroomToDelete.name))
        session.commit()
        return redirect(url_for('showShowroom', showroom_id=showroom_id))
    else:
        return render_template(
            'deleteShowroom.html',
            showroom=showroomToDelete
            )


# It's Displays the total bike list of popular showroom
@app.route('/showroom/<int:showroom_id>/bikes/')
def showBikes(showroom_id):
    showroom = session.query(Showroom).filter_by(id=showroom_id).one()
    bike = session.query(Bike).filter_by(bike_id=showroom_id).all()
    return render_template('menu.html', showroom=showroom, bike=bike)


# Creating new bike
@app.route('/showroom/<int:bike_id>/new/', methods=['GET', 'POST'])
def newBikeList(bike_id):
    if 'username' not in login_session:
        return redirect('login')
    showroom = session.query(Showroom).filter_by(id=bike_id).one()
    creater_id = getUserInfo(showroom.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("you cannot add this Bike"
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showShowroom', showroom_id=bike_id))
    if request.method == 'POST':
        newList = Bike(
            bike_name=request.form['bike_name'],
            about=request.form['about'],
            millage=request.form['millage'],
            engine_capacity=request.form['engine_capacity'],
            max_power=request.form['max_power'],
            Transmission=request.form['Transmission'],
            kerb_weight=request.form['kerb_weight'],
            price=request.form['price'],
            bike_id=bike_id,
            user_id=login_session['user_id']
            )
        session.add(newList)
        session.commit()
        flash("New Bike List %s is created" % (newList))
        return redirect(url_for('showBikes', showroom_id=bike_id))
    else:
        return render_template('newbikelist.html', bike_id=bike_id)


# Editing to particlar showroom bike
@app.route(
    '/showroom/<int:showroom_id>/<int:b_id>/edit/',
    methods=['GET', 'POST']
    )
def editBikeList(showroom_id, b_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedList = session.query(Bike).filter_by(id=b_id).one()
    showroom = session.query(Showroom).filter_by(id=showroom_id).one()
    creater_id = getUserInfo(editedList.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("You cannot edit this Showroom "
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showBikes', showroom_id=showroom_id))

    if request.method == 'POST':
        editedList.name = request.form['name']
        editedList.about = request.form['about']
        editedList.millage = request.form['millage']
        editedList.engine_capacity = request.form['engine_capacity']
        editedList.max_power = request.form['max_power']
        editedList.Transmission = request.form['Transmission']
        editedList.kerb_weight = request.form['kerb_weight']
        editedList.price = request.form['price']
        editedList.place = request.form['place']
        session.add(editedList)
        session.commit()
        flash("bike List has been edited!!")
        return redirect(url_for('showBikes', showroom_id=showroom_id))
    else:
        return render_template(
            'editbikelist.html',
            showroom=showroom, bike=editedList
            )


# Deleting particular showroom of bike
@app.route(
    '/showroom/<int:bike_id>/<int:list_id>/delete/',
    methods=['GET', 'POST']
    )
def deleteBikeList(bike_id, list_id):
    if 'username' not in login_session:
        return redirect('/login')
    showroom = session.query(Showroom).filter_by(id=bike_id).one()
    listToDelete = session.query(Bike).filter_by(id=list_id).one()
    creater_id = getUserInfo(listToDelete.user_id)
    user_id = getUserInfo(login_session['user_id'])
    if creater_id.id != login_session['user_id']:
        flash("You cannot edit this Showroom "
              "This is belongs to %s" % (creater_id.name))
        return redirect(url_for('showBikes', showroom_id=bike_id))

    if request.method == 'POST':
        session.delete(listToDelete)
        session.commit()
        flash("Bike list has been Deleted!!!")
        return redirect(url_for('showBikes', showroom_id=bike_id))
    else:
        return render_template('deletebikelist.html', lists=listToDelete)


# Logout from application
@app.route('/disconnect')
def logout():
    access_token = login_session['access_token']
    print("In gdisconnect access token is %s", access_token)
    print("User Name is:")
    print(login_session['username'])

    if access_token is None:
        print("Access Token is None")
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(uri=url, method='POST', body=None,
                       headers={'content-type':
                                'application/x-www-form-urlencoded'})[0]

    print(result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successfully logged out")
        return redirect(url_for('showShowroom'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
