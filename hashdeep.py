"""
Build recursive hash of files in directory tree in hashdeep format.


Hashdeep format description:
http://md5deep.sourceforge.net/start-hashdeep.html

hashdeep.py differences from original hashdeep:

 - if called without arguments, automatically starts to build
   recursive hash starting from the current directory
   (original hashdeep waits for the output from stdin)
 - uses only sha256 (original uses md5 and sha256)
 - uses relative paths only (original works with absolute)


hashdeep.py output example:

$ hashdeep.py
%%%% HASHDEEP-1.0
%%%% size,sha256,filename
##
## $ hashdeep.py
## 
5584,28a9b958c3be22ef6bd569bb2f4ea451e6bdcd3b0565c676fbd3645850b4e670,dir/config.h
9236,e77137d635c4e9598d64bc2f3f564f36d895d9cfc5050ea6ca75beafb6e31ec2,dir/INSTALL
1609,343f3e1466662a92fa1804e2fc787e89474295f0ab086059e27ff86535dd1065,dir/README
"""

__author__ = 'anatoly techtonik <techtonik@gmail.com>'
__license__ = 'Public Domain'
__version__ = '1.0'

import os
import os.path as osp
import hashlib


# --- helpers ---

def write(text):
    """ helper for writing output, as a single point for replacement """
    print(text)

def filehash(filepath):
    blocksize = 64*1024
    md5 = hashlib.md5()
    with open(filepath, 'rb') as fp:
        while True:
            data = fp.read(blocksize)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest() 

# --- /helpers ---

file = open('filecheck.audit', 'w+')
file.write('<check_type:"Unix">\n\n')


ROOT = '.'
for root, dirs, files in os.walk(ROOT):
    for fpath in [osp.join(root, f) for f in files]:
    	file.write('<custom_item>\n')
    	file.write('\tsystem: "Linux"\n')
    	file.write('\ttype: FILE_CHECK\n')
    	
        size = osp.getsize(fpath)
        sha = filehash(fpath)
        name = osp.relpath(fpath, ROOT)
        
    	desc = '\tdescription: "' + os.getcwd() + '/' + name + ' has the proper md5 set"\n'
    	file.write(desc)
    	
    	file.write('\trequired: YES\n')
    	
    	fullpath = '\tfile: "' + os.getcwd() + '/' + name + '"\n'
    	file.write(fullpath)
    	
    	md5 = '\tmd5: "' + sha + '"\n'
    	file.write(md5)
        
        #write('%s,%s,%s' % (size, sha, name))

        #for ignored in ['.hg', '.svn', 'git']:
        #     if ignored in dirs:
        #         dirs.remove(ignored)
        
        file.write('</custom_item>\n\n')
        
file.write('</check_type>\n')
