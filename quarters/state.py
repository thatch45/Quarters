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

    def get_pending_job( self )
        return self.pending.get()

    def put_pending_job( self, job_description )
        return self.pending.put( job_description )
