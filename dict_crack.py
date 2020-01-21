#Script: dict_crack.py
#Description: Takes hashes and cracks them using a dictionary attack(MD5 only)
#author: Steven Pyper
#modified Nov 2018
#imports
import sys,hashlib

#
dic = []
hashes = []
finaldict= []
rainbow = {}
dictionaryFile = 'commanpasswords.txt'


def readdic():
    """reads all words in from commanpasswords.txt and and returns a list of all the words"""
    #strips the newline character and all the words in the dic list
    try:
        dic = [s.strip("\n").lower() for s in open(dictionaryFile)] 
        dic.sort() # sort the list
        return dic
    except Exception as err:
        print(f'[-] {err}')
        sys.exit()

def finaldictionary(dic):
    """takes in a list and will add them to a new list but in more formats(the orgional password,upper,lower and a titled version and title version) which is returned"""
    for password in dic:
        finaldict.append(password)
        if(password.isdigit()):
            continue
        if not(password.islower()):
            finaldict.append(password.lower())
        if not(password.isupper()):
            finaldict.append(password.upper())
        if not(password.istitle()):
            finaldict.append(password.title())
    return finaldict

def createhashes(finaldict):
    """takes in a list and creates a list of hashes(hexdigested) for each item in that list and returns that list """
    try:
        hashes = [hashlib.md5(pwd.encode('utf-8')).hexdigest() for pwd in finaldict]
        return hashes
    except Exception as err:
        print(f'[-] {err}')
        sys.exit()
        
def createrainbow(hashes,finaldict):
    """takes in a list of hashes and a list of values(that are the ones turned into) and zips them together into a dictionary which is returned"""
    rainbow = dict(zip(hashes,finaldict))
    return rainbow

def updaterainbow():
    """updates a rainbow of comman passwords and hashes from the dictionaryFile(commanpasswords.txt by default) and returns it"""
    dic = readdic()
    finaldict = finaldictionary(dic)
    hashes = createhashes(finaldict)
    rainbow = createrainbow(hashes,finaldict)
    return rainbow

    
def dict_attack(passwd_hash,rainbow):
    """Checks password hash against a dictionary of common passwords"""
    print (f'[*] Cracking hash: {passwd_hash}')
    #looks in the dictionary for the saame hash value and if it finds it prints that it did and the value it found
    passwd_found = rainbow.get(passwd_hash)
    if passwd_found:
        print (f'[+] Password recovered: {passwd_found}\n')
    else:
        print (f'[-] Password not recovered \n')

def main():
    print('[dict_crack] Tests')
    passwd_hash = '4297f44b13955235245b2497399d7a93'
    rainbow = updaterainbow()
    dict_attack(passwd_hash,rainbow)
        

if __name__ == '__main__':
    main()
