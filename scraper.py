#Script:    scraper.py
#Desc:      fetch data from webpages and gather informtion such as links,emailaddresses and phone numbers, md5 hashes, images,and check for known bad files and extension mismatches
#Author:    Steven Pyper (40319882)
#modified:  Nov 2018


#imports
import re,dict_crack,os,urllib,ssl
from webpage_get import wget
from file_hash import get_hash


#predefined variables
url = 'http://www.soc.napier.ac.uk/~40009856/CW/'
#url = 'http://www.napier.ac.uk/'
rainbow = {}
download_dir = 'downloadedfiles'
context = ssl._create_unverified_context()
file_signatures = {b'\xFF\xD8\xFF': ('jpeg', 'jpg'), b'\x47\x49\x46': ('gif'),b'PK\x03': ('zip','jar','odt','ods','odp','docx','xlsx','pptx','vsdx','apk','aar'),b'%PD':('pdf')}
bad_files = 'bad_files.txt'


def print_links(page):
    ''' find all hyperlinks on the webpage input and print(also returns it) '''
    # regex to match on hyperlinks
    #old regex that only looked for webpages which could be simplied instead of using two findalls, links = re.findall('(<a.*href=[\'"])(https?://.*|.*html)["\']', page)
    #first group looks for the the href which will always come before the hyperlink, it also looks for " and ' as they are both valid ways to contain the hyperlink in html,second group finds all of the information untill it reaches the next group which is another " or '
    #
    links = re.findall('(href=[\'"])(.+?)(["\'])', page,re.IGNORECASE)
    # sort and print the links
    links.sort()
    print(f'[+] {len(links)}Potential HyperLinks Found:')
    for link in links:
        #only prints the 2nd group(since it starts at 0)
        print(link[1])
    return links


def print_documents(page):
    """finds all documents on the webpage that was input as long as they are a comman document file type and prints them(also returns them)"""
    #first group looks for the href again as it should come before any document typed files, second group looks for anything that might come under comman document filetypes
    documents = re.findall('(href=[\'"])(.+?\.pdf|.+?\.docx?|.+?\.rtf|.+?\.opd|.+?\.pps|.+?\.pptx?|.+?\.txt)(["\'])', page,re.IGNORECASE)
    # sort and print the documents
    documents.sort()
    print(f'\n\n[+] {len(documents)}Potential Documents Found:')
    for document in documents:
        print(document[1])
    print('\n')
    return documents

      
def print_images(page):
    """find all images on the webpage input and prints(also returns them)"""
    #finds anything with the src tag which should contain a image,second group contains the actual image link
    images = re.findall('(src=["\'])(.+?)(["\'])', page,re.IGNORECASE)
    # sort and print the images
    images.sort()
    print(f'[+] {len(images)}Potential Images Found:')
    for image in images:
        print(image[1])
    print('\n')
    return images


def print_emails(page):
    """find all emails on the webpage input and prints(also returns them)"""
    #used this as a bases to find most emails that follow comman valid email formats  - https://www.regular-expressions.info/email.html (\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b)
    #the first section finds everything that should be valid before the @ including .%+- as they are allowed to be used, after the @ it stops allowing all of these apart from . and - but will find all characters and numbers after the @
    emails = re.findall('[A-Za-z0-9._%+-]+@[A-Za-z0-9-.]+',page,re.IGNORECASE)
    # sort and print the emails
    emails.sort()
    print(f'[+] {len(emails)}Potential Emails Found:')
    for email in emails:
        print(email)
    print('\n')
    return emails


def print_phoneNumbers(page):
    """find all phone numbers on the webpage input and prints(also returns them)"""
    #finds most comman formats as well, the first one looks for the correct amount of digits with spaces inbetween, the second looks for +44 numbers that could be split up with either -'s or with (0) inside and then looks for more -'s spaces and digits to fill the rest of the number,the third looks for just straight 11 digits for the number, and the final one looks for digits with spaces or -'s spliting it up(this one is more of a general catch all that will almost definately pick up none phone numbers at some point) 
    phones = re.findall('(\d{4}[\-\ ]\d{3}[\-\ ]\d{4}|\+44[\ \-\(\)0]{1,4}[\ \- \d]{10,15}|\d{11}|[\d -]{11,16})',page,re.IGNORECASE)
    #sort and print the phones
    phones.sort()
    print(f'[+] {len(phones)}Potential Phone numbers Found:')
    for phone in phones:
        print(phone)
    print('\n')
    return phones


def print_hashes(page):
    """find all hashes on the webpage input and prints(also returns them)"""
    #this is a fairly simple regex as you know it must be either digits or characters that are a-f and must have 32 of any combination of them
    hashes = re.findall('[\da-f]{32}',page,re.IGNORECASE)
    # sort and print the links
    hashes.sort()
    print(f'[+] {len(hashes)}Potential Hashes numbers Found:')
    for hash in hashes:
        print(hash)
    print('\n')    
    return hashes


def crack_hashes(hashes):
    """takes in a list of hashes and will attempt to crack them from a 'rainbow' of comman passwords that will be generated"""
    #updates the rainbow which will contain comman passwords, more effiecent because it only has to create the rainbow once not every time you try cracking a hash
    rainbow = dict_crack.updaterainbow()
    print(f'[+] Attempting to Crack all Found Hashes')
    for hash in hashes:
        #attempts to crack the single hash from the hashes list and this will print out if its found or not
        dict_crack.dict_attack(hash,rainbow)


#orgionally inside the download_files function but meant that it would remove the first set of files when it started downloading the second set
def downloaddirectory():
    """will create or clear the directory required for downloading files"""
    print(f'\n[+] Download Directory')
    # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python,answer by blair conrad nov 7 2018
    #checks if the download directory is already in the same foulder as the program and if it is not it creates the downloaded file directory, if it does exist it will look throughb all of the files in there and delete it
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f'created a directory in the programs directory called {download_dir}\n')
    else:
        print(f'directory {download_dir} exists in the program directory and all contents will be removed\n')
        #https://stackoverflow.com/questions/1995373/deleting-all-files-in-a-directory-with-python/1995397 correct answer, shows a way of deleting all files in a direcotry with a certain extension, i just removed the extension part as i ant to remove everything
        #creates a list of all file names in filelist
        filelist = [f for f in os.listdir(download_dir)]
        for f in filelist:
            #goes through each file and joins so that it has the full link to the file and removes it
            os.remove(os.path.join(download_dir, f))


def download_files(documents):
    """trys to download from the list of links passed in(from a website)"""
    print(f'[+] Attempting to download files')
    downloadlink = []
    #goes through item of the list that is passed in and creates a new list where it will contain the entire link that is retured for downloading
    try:
        for document in documents:
            #checks if it strarts with http(which means https would be included) this is used so that if a entire link has been added to the orgional list(maybe embedded link or offsite links) they can still be downloaded , and if they come from the website that is being scrapped it will add the rest of thje link correctly
            if document[1].startswith('http'):
                #checks if the second section of the link(for example facebook.com) is the same as the webpage you are scrapping
                if urllib.parse.urlparse(document[1]).netloc == urllib.parse.urlparse(url).netloc:
                    #if they are the same webpage but starts with the entire link only add the third part of the url, esensitally turning it into a relative link
                    downloadlink.append(urllib.parse.urlparse(document[1]).path)
                else:
                    #if it isnt the same that means that it is a offsite link(such as the regex-cheatsheet.pdf) and will just add the entire thing to the list
                    downloadlink.append(document[1])       
            else:
                #if it doesnt start with http it is likely a relative link and cna just be added
                downloadlink.append(document[1])
    except Exception as err:
                print(f'[-] {err}')
                sys.exit()

    #goes through each of the new list which has went through everything and tidied it up to make ti easier to deal with now
    for singlelink in downloadlink:
        #if it still starts with http it is a offsite link and can just be downloaded
        if singlelink.startswith('http'):
            try:
                #will read the link and try to request it, if it manages it will be read into contents
                file_contents = urllib.request.urlopen(singlelink,context=context)
                contents = file_contents.read()
                file_contents.close()
                #this plus the while loop will generate a name based on the nname of the actual file(this will deal with files with duplicated names)
                filename = download_dir+'/'+singlelink[singlelink.rindex('/')+1:]
                while os.path.exists(filename):
                    #if it already exists it will put notorginal at the end of the name but before the filetype
                    filename=os.path.splitext(filename)[0]+'notorignal'+os.path.splitext(filename)[1]
                with open(filename,'wb') as f:
                    #write sthe contents to the file and print that it worked
                    f.write(contents)
                    print(f'http thing {singlelink} was downloaded correctly in {filename}\n')
            except urllib.error.HTTPError as error:
                #should deal with most http errors
                print(f'{fulllink} is probably a broken link\n\n\n{error}\n\n\n')
            except Exception as err:
                print(f'[-] {err}')
                sys.exit()    

        else:
            #at this point the link should just be a relative link so it needs the rest ofthe url so this will join them
            fulllink = urllib.parse.urljoin(url,singlelink)
            try:
                #open the link and read contents into contents
                file_contents = urllib.request.urlopen(fulllink,context=context)
                contents = file_contents.read()
                file_contents.close()
                #checks if there is / in the name(like the subfolder/Martian.docx) because if it is it will only want to use everything after the last / as the name
                if '/' in singlelink:
                    #rindex finds the last occounrce of a character, this allows the name to only includef whats after the final /
                    filename = download_dir+'/'+singlelink[singlelink.rindex('/')+1:]
                    #same while as before for duplicate naming
                    while os.path.exists(filename):
                       filename=os.path.splitext(filename)[0]+'notorignal'+os.path.splitext(filename)[1]
                    with open(filename,'wb') as f:
                        f.write(contents)
                        print(f'{singlelink} was downloaded correctly in {filename}\n')
                else:
                    #if there is no / it can just use the full name
                    filename=download_dir+'/'+singlelink
                    while os.path.exists(filename):
                       filename=os.path.splitext(filename)[0]+'notorignal'+os.path.splitext(filename)[1]
                    with open(filename,'wb') as f:
                        f.write(contents)
                        print(f'{singlelink} was downloaded correctly in {filename}\n')
            except urllib.error.HTTPError as error:
                print(f'{fulllink} is a broken link\n')  
            except Exception as err:
                print(f'[-] {err}')
                sys.exit()



def check_filesigs(filelist):
    """checks if the list of files have the same extension as there file sigunature"""
    print(f'\n[+] Checking File Signatures')
    for file in filelist:
        filename = download_dir+'/'+file
        with open(filename,'rb') as f:
            #reads the first 3 bytes
            file_sig = f.read(3)
            #checks if those 3 bytes are in the file_signature list and prints if they arent
        if file_sig not in file_signatures:
            print(f'{file} is a unknown filetype:{file_sig}\n')
            continue
        #finds what the file extension is
        filetype = file[file.rindex('.')+1:]
        #checks if the file extension matches the file_signature, i put it to lower so that there is no need to have .jpeg and .JPEG as they are basically the same thing so this saves having such a long file_Signuature tuple
        if filetype.lower() in file_signatures.get(file_sig):
            #both prints say likely as this is not a foolproof way of doing it as for the docx one it could be other file types as well
            print(f'{file} claims to be a {filetype} and is likely correct\n')
        else:
            print(f'{file} claims to be a {filetype} but is actually likely to be one of the following {file_signatures.get(file_sig)}\n')


def check_badfiles(filelist):
    """ checks if any of the files in the list have the same filehash as any of of the hashes in the bad_file.txt file(which contains the hash and the file its linked with"""
    print(f'\n[+] Checking for bad files')
    rainbowbadfiles = {}
    with open(bad_files,'r') as badfilesfile:
        #read each line at a time as each line contains the hash and the file associated with the hash
        for line in badfilesfile.readlines():
            #split it on the : so that its easier ot access each individually
            tmp = line.split(':')
            #https://stackoverflow.com/questions/28090960/read-file-as-a-list-of-tuples Vivek Sable, used this as a template to clean up the badfiles so they would be easier to work with later
            #strips out the ''s as they are in the text file, this means that in the rainbowbadfiles it is just the hash matched with the file and nothing elkse
            rainbowbadfiles[tmp[0].strip().strip('\'')] = tmp[1].strip().strip('\'')
    #go through each file and get its hash from the file_hash.py script and print weather or not it was there was any match
    for file in filelist:
        filename = download_dir+'/'+file
        file_hashsig = get_hash(filename)
        if file_hashsig in rainbowbadfiles:
            print(f'{file} was found in the badlist file as {rainbowbadfiles.get(file_hashsig)}\n')
        else:
            print(f'{file} was not found in the badlist file\n')


def orginalfiles(filelist):
    """ will go through all of the files in the filelist and see if any of them had the same orgional name and will then compare there hashes to see if they have the same content"""
    print(f'[+] Checking for any files with the same orgiounal name and comparing them')
    for file in filelist:
        replaced = False
        filename = download_dir+'/'+file
        #requires two files that begin as the same so that one can be modified if they match and then compared later
        orginalname = filename
        #will go through eachb notorgional, that way if there was ltos of files with the same name it should still be bale to get back and find the orgional file
        while os.path.splitext(orginalname)[0].endswith('notorignal'):
            #https://stackoverflow.com/questions/37372603/how-to-remove-specific-substrings-from-a-set-of-strings-in-python no one program in there in particular jsut alot of reading from the page
            #i used this idea as a way to get back to the orgional string(opposite of what happened when dealinng with naming duplicate strings)
            orginalname = filename.replace('notorignal','')
            replaced = True
        #if there has been a change to the orgional name it will print saying so and then compare the hashes of both and print weather they are the same or not
        if replaced == True:
            print(f'{file} :this is a not orgional name')
            print(f'the orginal name and directory would have been {orginalname}')
            if get_hash(filename)== get_hash(orginalname):
                print(f'{file} is the same as {orginalname} and had the same origional name\n')
            else:
                print(f'{file} is not the same as {orginalname} even though they shared a name\n')

        
def get_content():
    """groups up all of the scraping from the actual webpage, returns links,documents,images,emails,phonenums and hashes"""
    file_contents = wget(url)
    links = print_links(file_contents)
    documents = print_documents(file_contents)
    images = print_images(file_contents)
    emails = print_emails(file_contents)
    phoneNums = print_phoneNumbers(file_contents)
    hashes = print_hashes(file_contents)
    crack_hashes(hashes)
    return links,documents,images,emails,phoneNums,hashes


def downloading_everything(documents,images):
    downloaddirectory()
    download_files(documents)
    download_files(images)


def checking_files():
    filelist = [file for file in os.listdir(download_dir)]
    check_filesigs(filelist)
    check_badfiles(filelist)
    orginalfiles(filelist)


def main():
    #gets all of the contents from the url from the wget script
    #links,dopcuments,images,emails,phonenums and hashes are all returned so that if you wanted to write them all to a file(for instance if this was used as a module) it would be easier to get stuff back from them not only whats printed
    links,documents,images,emails,phoneNums,hashes = get_content()
    downloading_everything(documents,images)
    checking_files()

    
if __name__ == '__main__':
	main()
