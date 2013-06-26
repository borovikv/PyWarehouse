'''
Created on Apr 6, 2013

@author: vb
'''
import re
import os
import shutil
import urllib
import urlparse
import urllib2
import filecmp

def delete_files(dir_path, filter_function):
    for _, _, files in os.walk(dir_path):
        for f in files:
            if filter_function(f):
                os.remove(os.path.join(dir_path, f))

def render_template(template, context):
        reg = re.compile(r'{{\s*(\w+)\s*}}')
        return reg.sub(lambda x: context.get(x.group(1)), template)
    
def make_dir_if_not_exist(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

def is_image(path):
    return os.path.splitext(path)[1] in (".png", ".jpg", ".gif", ".bmp", ".jpeg")

def get_name(path):
    if not isinstance(path, basestring):
        path = unicode(path, 'utf-8')
    return os.path.split(path)[1]
       
def copy_folder(src, dest, pred=lambda name: True):
    print src, dest, pred
    def func(arg, dirname, names):
        for name in names:
            path = os.path.join(dest, name)
            if not os.path.exists(path) and pred(name):
                src = os.path.join(dirname, name)
                shutil.copy(src, path)
                
    if not os.path.exists(dest):
        shutil.copytree(src, dest)
    else:
        os.path.walk(src, func, None)
#---------------------------------------------------------------------------------------------       
# copy_img_html
#---------------------------------------------------------------------------------------------       
def copy_img_html(html, dest, source_path=None):
    """
    get text html
    return {'<img src=old>': '<img src=new>'}
    """
    img_reg = re.compile("<img\s[^>]*?>")
    imgs = img_reg.findall(html)
    
    old_new_imgs = {}
    for i in imgs:
        old_new_imgs[i] = make_img(i, dest, source_path)
    
    return old_new_imgs      
    
def make_img(img, dest, source_path):
    img_reg = re.compile("src\s*=\s*[\"']([^\"']*?)[\"']")
    #get path to original file
    old_path = img_reg.search(img).groups()[0]

    path = copy_file(old_path, dest, source_path)
    if path:
        img = "" + img     
        # replace src="xxx/yyy/zzz.abc" - src="IMG/zzz.abc"
        img.replace(old_path, path)
        return img
    else:
        return None      
           
def copy_file(path, dest, source_path, rel=True):
    if not os.path.exists(dest):
        os.mkdir(dest) 
    
    link = getFullPathFromStr(linkPreparation(path), source_path)
    new_path = None
    if link:
        path = link["link"]
        if link["type"] == "http":
            folder = os.path.split(dest)[1] if rel else dest
            new_path = os.path.join(folder, download_file(path, dest))
            
        if link["type"] == "local":
            new_path = copy_local_file(path, dest) 
    return new_path

def copy_local_file(src, dest, rel=True):
    
    fileName = os.path.split(src)[1]        
    newFile = os.path.join(dest, fileName)

    try:

        if os.path.exists(newFile) and not filecmp.cmp(src, newFile):
            f, ext = os.path.splitext(fileName)
            s = re.search("(.*)\(([0-9]+)\)$", f)

            if s:
                counter = int(s.group(2))
                counter = "(" + str(counter + 1) + ")"
                fn = s.group(1) + counter + ext
            else:
                fn = f + "(1)" + ext
            
            dst = os.path.join(dest, fn)
            shutil.copyfile(src, dst)
        elif not os.path.exists(newFile):
            shutil.copy(src, dest)
        
        folder = os.path.split(dest)[1] if rel else dest    
        newPath = os.path.join(folder, fileName)
    except:
        print("exept copyFile")
        newPath = None
    
    return newPath

def download_file(url, destination):
    _filepath, filename = os.path.split(urlparse.urlparse(url).path)
    urllib.urlretrieve(url, destination + os.sep + filename)
    return filename
    


def linkPreparation(link):
    link = link.replace("&amp;", "&") 
    if isinstance(link, unicode):
        return link
    try:
        link = link.toUtf8()
    except:
        print('link.toUtf8() error')
    link = unicode(link, 'utf-8')

    try:
        link = decodeURI(link)
    except:
        print("bad decode")
    
    return link
    

def decodeURI(uri):
    return urllib.unquote(uri.encode('ascii'))    

def getFullPathFromStr(link, source_path):
    
    objUrl = urlparse.urlparse(link)
    
    if objUrl.scheme == 'file' and os.path.exists(objUrl.path):
        return {"type": "local", "link" : objUrl.path}
    
    if objUrl.scheme == 'http':
        return {"type": "http", "link" : link}
    
    if objUrl.netloc:
        try:
            fullpath = 'http' + link
            urllib2.urlopen(fullpath)
            return {"type": "http", "link" : fullpath}
        except:
            print("bad location 1")
            
            
    if objUrl.path.startswith('www.'):
        #try to open file on http if false fale may by local
        try:
            fullpath = "http://" + link
            urllib2.urlopen(fullpath)
            return {"type": "http", "link" : fullpath}
        except:
            print("bad location 2")
                
    
    # Might be a file
    if os.path.exists(link):
        return {"type": "local", "link" : link}
    
    # Might be a shorturl 
    if source_path:
        #print(link, objUrl, self.urlForCopy)
        par = os.path.dirname(source_path)
        fullpath = os.path.join(par, link)
        return {"type" : "local", "link" : fullpath}
    
    # Might be a shorturl from www or other surces
        
    return None    