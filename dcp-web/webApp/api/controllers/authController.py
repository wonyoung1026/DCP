import json
import firebase_admin
import datetime

from firebase_admin import auth
from requests import exceptions
from flask import abort, request, Response, redirect, jsonify, make_response

from ..models.userModel import User

def getUserWithHeader():
    bearer = request.headers.get('Authorization')
    
    try:
        if bearer is None or not isinstance(bearer, str):
            raise AssertionError('header Authorization missing')
        uid = getUIDByFirebaseToken(bearer[7:])
        
        user = User(id=uid)
        user.reload()
        return user

    except:
        return abort(500)


def getUIDByFirebaseToken(token: str):
    decoded_token= auth.verify_id_token(token)
    return decoded_token['uid']

def getUserWithSessionCookie():
    session_cookie = request.cookies.get('session')
    if not session_cookie:
        # Force user to log in if session cookie is unavailable
        return redirect('/')

    try: 
        # decoded claims contain user info such as email, signinprovider, uid etc
        decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
        uid = decoded_claims['uid']
        
        user = User(id=uid)
        user.reload()

        return user

    except auth.InvalidSessionCookieError as e:
        print(e)
        return redirect('/')
    except:
        return abort(500)

def sessionLogout():
    response = make_response(redirect('/'))
    response.set_cookie(key='session', expires=0)
    return response

def sessionLogin():
    # Get the ID token sent by the client
    id_token = request.json.get('idToken')
    # Set session expiration to 5 days.
    expires_in = datetime.timedelta(days=5)
    try:
        # Create the session cookie to verify the token
        # The session cookie will have the same claims as the ID token.
        session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
        response = make_response(jsonify({'status': 'success'}))
        # Set cookie policy for session cookie.
        expires = datetime.datetime.now() + expires_in
        response.set_cookie(
            key='session', value=session_cookie, expires=expires)
        return response
    except exceptions.FirebaseError:
        return make_response(jsonify({'message': 'Failed to create a session cookie'}), 401)
    except:
        abort(500)

def preregisterCheck():
    email = request.get_json().get("email")
    buyer_flag = request.get_json().get("buyerFlag")
    triplets = [('email', '==', email)]
    user_list = User.getByQuery(triplets=triplets)
    
    if len(user_list) == 1:
        user = user_list[0]
        if user.isBuyer == buyer_flag and user.isProvider != buyer_flag:
            return make_response(jsonify({'message': 'User already exists'}), 400)
        else:
            # Update user type
            if buyer_flag:
                user.isBuyer = buyer_flag
            else:
                user.isProvider = not buyer_flag
            user.save()
            return make_response(jsonify({'message': 'User type has been updated.'}), 211)
    elif len(user_list) > 1:
        return make_response(jsonify({'message' : "Unknown error from database."}), 400)
    else:
        return make_response(jsonify({'message': 'User does not exist. Adding to database.'}),201)


    
def createUser():
    email = request.get_json().get("email")
    buyer_flag = request.get_json().get("buyerFlag")
    id = request.get_json().get("id")

    user = User(id=id, email=email, isBuyer=buyer_flag, isProvider=not buyer_flag)
    user.save()

    return make_response(jsonify({'message': "New user has been added to database."}), 201)


