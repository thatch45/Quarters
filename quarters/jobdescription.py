import json

class JobDescription:
    ''' a structure to store a job description '''

    # ujid - unique job id, given out by master
    def __init__( self, ujid, package_name, sha256sum, architecture ):
        self.ujid = ujid
        self.package_name = package_name
        self.sha256sum = sha256sum
        self.architecture = architecture

    def dump_json( self ):
        d = {}
        d['ujid'] = self.ujid
        d['package_name'] = self.package_name
        d['sha256sum'] = self.sha256sum
        d['architecture'] = self.architecture

        return json.dumps( d )

    @staticmethod
    def load_json( json_string ):
        d = json.loads( json_string )
        return JobDescription( d['ujid'], d['package_name'], d['sha256sum'], d['architecture'] )
