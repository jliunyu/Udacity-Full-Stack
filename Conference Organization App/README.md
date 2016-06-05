App Engine application for the Udacity training course.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
1. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
1. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
1. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
1. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
1. (Optional) Generate your client library(ies) with [the endpoints tool][6].
1. Deploy your application.


[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://console.developers.google.com/
[5]: https://localhost:16080/
[6]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool

1. The project is "Conference" which have the following function: user authentication, user profiles, conference information and various manners in which to query the data

2. The python version 2.7.6 should be installed before running the program, the Google App Engine version is 1.9.30.

3. Function detail : 
[1] User can login with their gmail account and set the size of the T-shirts. The app will remember, they can also change this at any time.
[2] User can create conference, query conference, register conference and unregister conference. 


3. List of Author: Jane

All the task listed below:

1. 1)For the session part, each conference has many one or more sessions. So the most import thing for this is in the _createSessionObject() function, when create the session, also get the conference_key and let the conference_key as the parent of the session_key. When the server got the create session request, the createSession() function will be called. Then it will call the _createSessionObject() function and return the sessionForm created from the _copySessionToForm function.

2) what’s more, a getConferenceSessions() function is designed. this will query out all the conference sessions. When a get conference session request sent from the client.

3) getConferenceSessionsByType() is also designed. This is used to query all the sessions by a special type from the database.

4) getSessionsBySpeaker() is designed. This is used to query all the sessions by a special speaker.

2. Add Sessions to User Wishlist

1) use a list to store the wishlist. In the function _wishlistSession(), if a session is been requested to add to the wish list, check if the session is in the wish list, throw an exception, otherwise add the session to the wishlist. When the server received a request that add session to wish list, the function addSessionToWishlist will be called. Then it will call the function of _wishlistSession()

2) In the function of getSessionsInWishlist(), all the sessions in a wish list will be queried.

3. Additional queries:

1) getSessionsBeforeCurrentTime(), this will query out all the sessions that start before current time.

2) getSessionsWithSpecialDurationTime() ,this will query out all the sessions that between 20-30 mins.

4. Add a task:

_cacheFeaturedSpeaker() is designed. When add a new session to the conference, check the speaker first. When the server received this query, the function of getFeaturedSpeaker() will be called.

5. Query problem:

The query for the non-workspace is query by type. But for the session before 7pm is query by time. These two are different types. Inequality filter can be applied at most one property. So my solution for this is query out the non-workspace first and then query the session before 7pm from the result.

6. For the models.py,

the definitions of Session, SessionForm and SessionForms are defined. The session extends the ndb.model and define the Session. SessionForm extends messages.Message and define the SessionForm. SessionForms extends the messages.Message and define the SessionForms.

7. For the reference, are listed below:

https://cloud.google.com/appengine/docs/python/ndb/modelclass

https://cloud.google.com/appengine/docs/python/tools/protorpc/messages/messageclass

https://cloud.google.com/appengine/docs/python/endpoints/create_api