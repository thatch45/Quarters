import threading
import time
from queue import Queue

from quarters.state import State

import subprocess

import urllib.request

import os

import tarfile

class JobOverlord( threading.Thread ):
    '''

    controls all the poor joblings running on the server

    '''

    def __init__( self, max_jobs ):
        threading.Thread.__init__( self )
        self.max_jobs = max_jobs
        self.jobling_pool = []
        self.pending_jobs = Queue()

    def run( self ):
        for i in range( self.max_jobs ):
            job = Jobling( self )
            job.start()
            self.jobling_pool.append( job )

        for job in self.jobling_pool:
            job.join()

    def add_job( self, job_description ):
        self.pending_jobs.put( job_description )

class Jobling( threading.Thread ):
    '''

    does all the hardwork, will eventually die and return 42

    '''

    def __init__( self, job_overlord ):
        threading.Thread.__init__( self )
        self.job_overlord = job_overlord

    def run( self ):
        while 1:
            current_job = self.job_overlord.pending_jobs.get()

            # update state here (running)

            current_job.job()

            # update state here (done)

class JobDescription:
    '''

    a structure to store a job description

    '''

    # ujid - unique job id, given out by master
    def __init__( self, ujid, package_name, package_source ):
        self.ujid = ujid
        self.package_name = package_name
        self.package_source = package_source

    def job( self ):
        print( 'thread %s sleeping for 2 seconds' % ( self.package_name ) )

        time.sleep( 2 )

        job_path = '/var/tmp/quarters/' + self.ujid
        pkgsrc_path = job_path + '/' + self.package_name + '.tar.gz'

        #( return_code, output ) = subprocess.getstatusoutput( 'mkdir -p ' + job_path )
        try:
            os.makedirs( job_path )
        except os.error as e:
            print( 'warning: leaf directory already exists at ' + job_path )

        # need to make sure that urlretrieve overwrites if existing file with same name is found
        # "If the URL points to a local file, or a valid cached copy of the object exists, the object is not copied."
        # http://docs.python.org/py3k/library/urllib.request.html#urllib.request.urlretrieve
        urllib.request.urlretrieve( self.package_source, pkgsrc_path )

        #( return_code, output ) = subprocess.getstatusoutput( 'tar -xfz ' + self.package_name + '.tar.gz' )
        temp_tar = tarfile.open( pkgsrc_path )
        temp_tar.extractall( job_path )
