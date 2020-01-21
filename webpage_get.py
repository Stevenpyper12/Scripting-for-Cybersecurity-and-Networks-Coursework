# Script:   webpage_get.py
# Desc:     Fetches data from a webpage.
# Author:   PL & RM
# Modified: nov 2018 by SP(40319882)

import sys, urllib.request,ssl
        
def wget(url):
    ''' Retrieve a webpage via its url, and return its contents'''
    #opts out of certificate verification allowing pages with no valid certificate to be opened
    try:
        context = ssl._create_unverified_context()
        #opens a webpage even if it doesnt have a valid certficiate
        webpage = urllib.request.urlopen(url, context=context)
        #gets the contents from the webpage
        page_contents = webpage.read().decode("utf-8")
        webpage.close()
        return page_contents
    except Exception as err:
        print(f'{err}')
        sys.exit()

def main():
    # set test url argument
    #sys.argv.append('http://www.facefacefacebook.com/')
    sys.argv.append('https://moodle.napier.ac.uk/')
    # Check args
    if len(sys.argv) != 2:
        print ('[-] Usage: webpage_get URL')
        return

    # Get web page
    print (wget(sys.argv[1]))

if __name__ == '__main__':
	main()
