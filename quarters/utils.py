import urllib.request

def download( url ):
    filename = url.split('/')[-1]
    try:
        # FIXME: the following function doesn't actually check if an ssl cert is good
        urllib.request.urlretrieve( url, filename )
    except ContentTooShortError as e:
        print( 'failed to retrieve %s' % url )
