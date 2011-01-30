import urllib.request

def download( url ):
    filename = url.split('/')[-1]
    try:
        urllib.request.urlretrieve( url, filename )
    except ContentTooShortError as e:
        print( 'failed to retrieve %s' % url )
