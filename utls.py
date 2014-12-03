###########################################################################
#
#   File Name      Date        Owner           Description
#   ---------    -------     ---------        ------------
#   utls.py     12/1/2014   Archana Bahuguna  Utility fuctions 
#
###########################################################################

from sqlalchemy.exc import InvalidRequestError
import models
import views 

def display_tables():
    """ Displays db table entries after processing request """
    prompt = '__________________________________________\n'\
             'To view tables enter Yes/yes/y/No/no/n:'
    #i = raw_input(prompt)
    i = "yes"
    if i.lower() in ('yes','y'):
        import os
        os.system('clear')

        qry = models.User.query.all()
        print "========================================================="
        print "User Table\n=============:\nUserid Username    Email     Address\n"
        for i in qry:
            print i
        print "---------------------------------------------------------"
        qry = models.Podcast.query.all()
        print "Podcast Table\n=============:\nPodcastid Userid Podcastdata\n"
        for i in qry:
            print i

        print "---------------------------------------------------------"
    else:
        pass
    return None

