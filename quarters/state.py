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
        manager = multiprocessing.Manager()
        self.state = manager.dict()
        self.pending = manager.Queue()

    def set_status( self, ujid, status ):
        self.state[ ujid ][ 'status' ] = status

    def get_status( self, ujid ):
        return self.state[ ujid ][ 'status' ]

    def set_packages( self, ujid, packages ):
        self.state[ ujid ][ 'packages' ] = packages

    def get_packages( self, ujid ):
        return self.state[ ujid ][ 'packages' ]

    def get_pending_job( self ):
        return self.pending.get()

    def get_nowait_pending_job( self ):
        return self.pending.get_nowait()

    def put_pending_job( self, job_description ):
        self.pending.put( job_description )

    def size_pending_job( self ):
        return self.pending.qsize()

    def get_ujids( self ):
        return self.state.keys()

    def get_state_dict( self ):
        return dict( self.state )

    def create_ujid( ujid ):
        self.state[ ujid ] = {}
        self.set_status( job_description.ujid, 'notdone' )
        self.set_packages( job_description.ujid, [] )

    def remove_ujid( ujid ):
        del self.state[ ujid ]

def json_to_state( json ):
    ret = State()
    ret.state.update( new_dict )
    return ret
