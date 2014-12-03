###########################################################################
#
#   File Name      Date        Owner           Description
#   ---------    -------     ---------        ------------
#   views.py     12/1/2014   Archana Bahuguna  View functions
#
###########################################################################
from flask import Flask, request, render_template, make_response
from flask.ext.sqlalchemy import SQLAlchemy, get_debug_queries
import models
import utls

app=Flask(__name__)

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        app.logger.info("SQL QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n\n" % (query.statement, query.parameters, query.duration, query.context))
    return response

@app.route('/index', methods = ['GET'])
@app.route('/', methods = ['GET'])
def index():

    # GET /
    if request.method == 'GET':
        app.logger.info(request)
        err=""
        utls.display_tables()
        return render_template('index.html',err=err)

@app.route('/api', methods = ['GET'])
def api():

    # GET /
    if request.method == 'GET':
        app.logger.info(request)
        err=""
        utls.display_tables()
        return render_template('api.html',err=err)

@app.route('/users', methods = ['GET','POST'])
def users():

    # GET
    if request.method == 'GET':
        app.logger.info(request)
        err=""

        user_obj = models.User.query.all()
        if not user_obj:
            err="No user"

        utls.display_tables()
        response = render_template('list_of_users.html',
                                   user_obj=user_obj,
                                   err=err
                                   )
        return response

    # POST
    if request.method == 'POST':
        app.logger.info(request)
        err=""
        username = request.form["username"]
        email = request.form["email"]
        address = request.form["address"]
        podcast1 = request.form["podcast1"]
        podcast2 = request.form["podcast2"]
        podcast3 = request.form["podcast3"]

        user_obj = models.User.query.filter_by(username=username).all()
        if (not user_obj):
            user_obj = models.User(username,email,address)
            models.db.session.add(user_obj)

            query_obj = models.User.query.filter_by(username=username).first()
            userid = query_obj.userid
            if (podcast1):
                pod_obj1 = models.Podcast(podcast1,userid)
                models.db.session.add(pod_obj1)
            if (podcast2):
                pod_obj2 = models.Podcast(podcast2, userid)
                models.db.session.add(pod_obj2)
            if (podcast3):
                pod_obj3 = models.Podcast(podcast3, userid)
                models.db.session.add(pod_obj3)
            models.db.session.commit()

        else:
            err = "User already exists"

        utls.display_tables()
        response = render_template('api.html', 
                                   user_obj=user_obj, 
                                   err=err)
        return response


@app.route('/users/<userid>/podcasts', methods = ['GET'])
def podcasts(userid):

    # GET
    if request.method == 'GET':
        app.logger.info(request)
        err=""

        user_obj = models.User.query.join(models.Podcast).filter_by(userid=userid).all()
        if not user_obj:
            err="No such user"

        utls.display_tables()
        response = render_template('alluserdata.html',
                                   user_obj=user_obj,
                                   err=err
                                   )
        return response


if __name__ == '__main__':

    app.debug = False

    models.db.drop_all()
    models.db.create_all()
    
    utls.display_tables()

    if not app.debug:
        import logging
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('tmp/ormppt.log', 'a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('App startup')
    app.run('192.168.33.10', 5001)

