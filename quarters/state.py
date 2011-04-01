import multiprocessing

'''
{
 <ujid> : {
           status : <notdone,inprogress,done,failed>,
           packages : [
                       {
                        pkgname : "a.pkg.tar.xz",
                        sha256sum : <sha256sum>
                       },
                       ...
                      ]
          },
 ...
}
'''

class State:
    def __init__( self ):
        self.manager = multiprocessing.Manager()
        self.state = self.manager.dict()
        self.pending = self.manager.Queue()

    def set_status( self, ujid, status ):
        # need to do the following for mutable types in Manager.dict types
        temp = self.state[ ujid ]
        temp[ 'status' ] = status
        self.state[ujid] = temp

    def get_status( self, ujid ):
        return self.state[ ujid ][ 'status' ]

    def set_packages( self, ujid, packages ):
        # need to do the following for mutable types in Manager.dict types
        temp = self.state[ ujid ]
        temp[ 'packages' ] = packages
        self.state[ ujid ] = temp

    def get_packages( self, ujid ):
        return self.state[ ujid ][ 'packages' ]

    def get_pending_job( self ):
        return self.pending.get()

    def get_nowait_pending_job( self ):
        return self.pending.get_nowait()

    def put_pending_job( self, job_description ):
        # create the initial structure for the empty job in the state
        self.state[ job_description.ujid ] = {}
        self.set_status( job_description.ujid, 'notdone' )
        #print( self.state[ job_description.ujid ][ 'status' ] )
        self.state[ job_description.ujid ][ 'status' ] = 'notdone'
        print( self.state[ job_description.ujid ][ 'status' ] )
        self.set_packages( job_description.ujid, [] )

        self.pending.put( job_description )

    def size_pending_job( self ):
        return self.pending.qsize()

    def get_ujids( self ):
        return self.state.keys()

    def get_state_dict( self ):
        return dict( self.state )

    def remove_ujid( ujid ):
        del self.state[ ujid ]

def json_to_state( json ):
    ret = State()
    ret.state.update( new_dict )
    return ret
