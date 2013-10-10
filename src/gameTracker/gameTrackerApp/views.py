# main definition of view code

from django.http import HttpResponse

def login( request ):
    return HttpResponse( "login" )

def register( request ):
    return HttpResponse( "register" )
