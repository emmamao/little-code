# encoding: UTF-8
#

import httplib, mimetypes
import urllib
import urllib2
import os
import sys
import optparse
import hashlib
import time

# The key for examples.
API_KEY = " "#"PUT YOUR APIKEY"

class ThreatBook(object):

    def __init__(self, api_key):

        super(ThreatBook, self).__init__()

        self.api_key = api_key

    def __repr__(self):
        return "<ThreatBook proxy>"

    def get(self, hash):
        print "Getting the report ...\r\n"
        #time.sleep(10)

        url = "https://x.ThreatBook.cn/api/v1/file/report"
        parameters = {"resource": hash,
                       "apikey": self.api_key}
        data = urllib.urlencode(parameters)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        ret_json = response.read()

        print "Report(in JSON):\r\n"

        print ret_json
        return 1;

def main():
    parser = optparse.OptionParser(usage = """
    %prog <hash>
Samples:
    %prog b76280c2b71b369c8e013651d66d599c615cf83096388c1ad76be6c9725a26db
    """)

    (options, arguments) = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_usage()
        return -1

    hash = arguments.pop(0)
	
    try:
        v = ThreatBook(API_KEY)
        v.get(hash)

    except Exception, e:
        print "ThreatBook returned a non correct response. See the parameter -l"

if __name__ == "__main__":
    main()
