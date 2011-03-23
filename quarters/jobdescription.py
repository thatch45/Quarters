import json

class JobDescription:
    ''' a structure to store a job description '''

    # ujid - unique job id, given out by master
    def __init__( self, ujid, package_name, package_source, sha256sum, architecture ):
        self.ujid = ujid
        self.package_name = package_name
        self.package_source = package_source
        self.sha256sum = sha256sum
        self.architecture = architecture

    def dump_json( self ):
        d = {}
        d['ujid'] = self.ujid
        d['package_name'] = self.package_name
        d['package_source'] = self.package_source
        d['sha256sum'] = self.sha256sum
        d['architecture'] = self.architecture

        return json.dumps( d )

    @staticmethod
    def load_json( self, json_string ):
        d = json.loads( json_string )
        return JobDescription( d['ujid'], d['package_name'], d['package_source'], d['sha256sum'], d['architecture'] )
