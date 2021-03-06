from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app.secret_key = 'why would I tell you my secret key?'


@app.route('/login')
def showLogin():
    """
    show the login page

    Returns:
        The render of the login page
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/logout')
def showLogout():
    """
    show the logout page

    Returns:
        The render of the logout page
    """
    if 'username' not in login_session:
        return redirect(url_for('showRestaurants'))
    result = disconnect()
    return render_template('logout.html', result=result)


# show the restaurent menu accordingt to the restaurant id
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    """
    show the restaurent menu accordingt to the restaurant id

    Args:
        restaurant_id : restaurant id
    Returns:
        if the user is creator of the restaurant, return the menu that the
        user can edit it
        else return the public menu
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = getUserInfo(restaurant.user_id)
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicmenu.html', items=items, restaurant=restaurant, creator=creator)
    else:
        return render_template('menu.html', items=items, restaurant=restaurant, creator=creator)


# create a new user
def createUser(login_session):
    """
    Create a user

    Args:
        login_session : login session
    Returns:
        New User's id
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """
    Get user's information

    Args:
        user_id : user id
    Returns:
        user object
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """
    Get user's information according to email

    Args:
        email : user email
    Returns:
        user id
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# google accounts login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Use google account to login

    Returns:
        login information
    """
    if (request.args.get('state') != login_session['state']):
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        # print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google+'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    userid = getUserID(login_session['email'])
    if not userid:
        userid = createUser(login_session)
    login_session['user_id'] = userid

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Now logged in as %s" % login_session['username'])
    return output


# google account logout, but currently this function not be called
@app.route('/gdisconnect')
def gdisconnect():
    """
    Use google account to disconnect

    Returns:
        response
    """
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# login using facebook account
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """
    Use facebook account to login

    Returns:
        login information
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


# facebook account logout
@app.route('/fbdisconnect')
def fbdisconnect():
    """
    Use facebook account to logout

    Returns:
        "you have been logged out"
    """
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Show all restaurants
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    """
    Show all restaurants

    Returns:
        Restaurants list
    """
    restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
    if 'username' not in login_session:
        return render_template('publicrestaurants.html', restaurants=restaurants)
    else:
        return render_template('restaurants.html', restaurants=restaurants)


# Create a new restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    """
    create a new restaurent

    Returns:
        if a new restaurant is created, return the restaurants lists
        else return the create new restaurants page
    """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newRestaurant)
        flash('New Restaurant %s Successfully Created' % newRestaurant.name)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


# Edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    """
    edit a restaurent

    Args:
        restaurant_id : restaurant id
    Returns:
        if a restaurant is edited, return the restaurants lists
        else return the edit restaurants page
    """
    editedRestaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=editedRestaurant)


# Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    """
    delete a restaurent
    Args:
        restaurant_id: restaurent id
    Returns:
        if a restaurant is deleted, return the restaurants lists
        else return the delete restaurants page
    """
    restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        flash('%s Successfully Deleted' % restaurantToDelete.name)
        session.commit()
        return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)


# Show a restaurant menu
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    """
    create a restaurant menu to json
    Args:
        restaurant_id: restaurent id
    Returns:
        json of a restaurant menu
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    """
    create a item of restaurant menu to json
    Args:
        restaurant_id: restaurent id
        menu_id : menu id
    Returns:
        json of an item in a restaurant menu
    """
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


# show the menu of a restaurant according to its id
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    """
    Show menu of restaurant
    Args:
        restaurant_id: restaurent id
    Returns:
        render of menu of restaurant
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items, restaurant_id=restaurant_id)


# add a new item to a menu
@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    """
    create new menu item of restaurant
    Args:
        restaurant_id: restaurent id
    Returns:
        if new menu item is created, return the render of menu of current
        restaurant
        else return new menu create page
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id, user_id=restaurant.user_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# edit item in a menu
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    """
    edit menu item of restaurant
    Args:
        restaurant_id: restaurent id
        menu_id : menu id
    Returns:
        if menu item is edit, return the render of menu of current restaurant
        else return menu edit page
    """
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# detete a item in a menu accoring to restaurant id and menu_id
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    """
    delete menu item of restaurant
    Args:
        restaurant_id: restaurent id
        menu_id : menu id
    Returns:
        if menu item is deleted, return the render of menu of current
        restaurant
        else return menu delete page
    """
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    """
    logout account
    Args:
        restaurant_id: restaurent id
        menu_id : menu id
    Returns:
        Render of the show restaurants lists page
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        login_session.pop('access_token', None)
        flash("You have successfully been logged out.")
        return redirect(url_for('showRestaurants'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showRestaurants'))

if __name__ == '__main__':
    # app.secret_key = super_secret_key
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
