import json

class JobDescription:
    ''' a structure to store a job description '''

    # ujid - unique job id, given out by master
    def __init__( self, ujid, package_name, package_source ):
        self.ujid = ujid
        self.package_name = package_name
        self.package_source = package_source

    def dump_json( self ):
        d = {}
        d['ujid'] = self.ujid
        d['package_name'] = self.package_name
        d['package_source'] = self.package_source

        return json.dumps( d )

    def load_json( self, json_string ):
        d = json.loads( json_string )
        
        self.ujid = d['ujid']
        self.package_name = d['package_name']
        self.package_source = d['package_source']
