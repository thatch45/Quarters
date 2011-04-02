#!/usr/bin/python3

from bottle import get, post, request, run
from pymongo import Connection
import json
import uuid
import urllib.request

@get('/')
def main_form():
    return '''<form method="POST">
              <input name="packages" type="text" />
              </form>'''

@post('/')
def main_submit():
    packages = request.forms.get('packages')

    package_list = []

    for package in packages.split():
        package_list.append( { 'uuid' : str( uuid.uuid4() ), 'pkgname' : package } )

    packages_collection.insert( package_list )
    
    return '<p> %s </p>' % packages

@get('/stat')
def stat():
    jobs = []
    # query the list of todo packages
    for package in packages_collection.find():
        jobdescription = { 'uuid' : package[ 'uuid' ], 'pkgname' : package[ 'pkgname' ] }
        jobs.append( jobdescription )
    return json.dumps( jobs )

@get('/mstat')
def mstat():
    content = '<table>'
    url = 'http://76.191.31.83:1337/global_status'
    states = json.loads( bytes.decode( urllib.request.urlopen( url ).read() ) )
    for k in states:
        content += '<tr>'
        content += '<td>' + k + '</td>'
        content += '<td>' + states[ k ][ 'status' ] + '</td>'
        if states[ k ][ 'status' ] == 'done':
            url = 'http://76.191.31.83:1337/' + k + '/build_log'
            content += '<td> <a href="' + url + '">' + url + '</a> </td>'
        if states[ k ][ 'status' ] == 'failed':
            url = 'http://76.191.31.83:1337/' + k + '/build_log'
            content += '<td> <a href="' + url + '">' + url + '</a> </td>'
        content += '</tr>'
    content += '</table>'
    return content
    

mongo_connection = Connection()
quarters_database = mongo_connection[ 'quarters' ]
packages_collection = quarters_database[ 'packages' ]
# clear out crud since it's all a test
packages_collection.drop()

run(host='localhost', port=1000)

