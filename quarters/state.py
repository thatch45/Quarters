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
        self.state = multiprocessing.Manager().dict

    def set_status( self, ujid, status ):
        self.state[ ujid ][ 'status' ] = status

    def get_status( self, ujid ):
        return self.state[ ujid ][ 'status' ]

    def set_packages( self, ujid, packages ):
        self.state[ ujid ][ 'packages' ] = packages

    def get_packages( self, ujid ):
        return self.state[ ujid ][ 'packages' ]
