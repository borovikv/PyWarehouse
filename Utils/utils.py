'''
Created on Apr 6, 2013

@author: vb
'''
import re
import os
import shutil
import urllib2
import filecmp
from BeautifulSoup import BeautifulSoup
import traceback
from PyWarehouse import Settings

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
# copy_imgs
#---------------------------------------------------------------------------------------------    
def copy_imgs(html, dest, start=None):
    soup = BeautifulSoup(unicode(html))
    imgs = soup('img')
    if imgs:
        make_dir_if_not_exist(dest)
    
    for img in imgs:
        src = dict(img.attrs).get('src')
        new_path = copy_img(src, dest, start)
        if not new_path:
            img.extract()
        img['src'] = new_path
    
    return unicode(soup)

def copy_img(src, dest, start=None):
    if os.path.isfile(src):
        new_path = copy_file(src, dest)
    else:
        new_path = download_file(dest, src)
    if new_path and start:
        new_path = os.path.relpath(new_path, start)
    return new_path
        
    
def copy_file(src, dest):
    try:
        new_path = get_path(src, dest)
        shutil.copyfile(src, new_path)
        return new_path
    except:
        print("exept copyFile")

def get_path(src, dest):
    basename = os.path.basename(src)
    new_path = os.path.join(dest, basename)
    if os.path.exists(new_path) and (not os.path.isfile(src) or not filecmp.cmp(src, new_path)):
        fn = increment_file_name(basename)
        new_path = os.path.join(dest, fn)
    return new_path
           
def increment_file_name(file_name):
    name, ext = os.path.splitext(file_name)
    s = re.search("(.*)\(([0-9]+)\)$", name)
    if s:
        counter = int(s.group(2))
        counter = "(" + str(counter + 1) + ")"
        fn = s.group(1) + counter + ext
    else:
        fn = name + "(1)" + ext
    return fn

def download_file(dest, src):
    install_opener(Settings.PROXY)
    try:
        req = urllib2.urlopen(src)
        new_path = get_path(src, dest)
        f = open(new_path, 'w')
        f.write(req.read())
        return new_path
    except:
        print 'error download', src
        print traceback.format_exc()
     
def install_opener(proxy=None):
    if proxy:
        proxy_support = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)   


    
