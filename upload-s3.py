#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import os
import sys
import atexit
import random
import string
import mimetypes
import subprocess
import tempfile
from subprocess import call
from os.path import expanduser, exists, basename, getsize
from workflow import Workflow

def get_random_bit(length):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length))

def capture_text(extension):
    # global name 'subprocess' is not defined
    text_file = subprocess.check_output("pbpaste", shell=True)
    random_bit = get_random_bit(10)
    file_name = 'clip-'+random_bit+'.'+extension
    file_path = os.path.join(tempfile.mkdtemp(), file_name)
    with open(file_path, "wb") as f:
        f.write(text_file)

    # return content type based on extension.
    content_type = mimetypes.MimeTypes().guess_type(file_path)[0]
    return file_path, file_name, content_type

def capture():
    random_bit = get_random_bit(5)
    file_name = datetime.datetime.now().strftime('%S'+random_bit+'.png')
    content_type = 'image/png'
    if (sys.argv[1] != ""):
        file_path = sys.argv[1]
        content_type = mimetypes.MimeTypes().guess_type(file_path)[0]
        _head, file_name = os.path.split(file_path)
        file_names = file_name.split('.')
        file_names.insert(1,'-' + random_bit + '.')
        file_name = "".join(file_names)
    else:
        file_path = os.path.join(tempfile.mkdtemp(), file_name)
        atexit.register(lambda x: os.remove(x) if os.path.exists(x) else None, file_path)
        save = call(['./pngpaste', file_path])
        if save == 1:
            sys.exit()
    tinypng_key = os.getenv('tinypng_api_key')
    # If content type starts with 'image/' then compress.
    if content_type.startswith('image/') and tinypng_key:
        import tinify
        tinify.key = tinypng_key
        tinify.from_file(file_path).to_file(file_path)
    return file_path, file_name, content_type

def main(wf):
    import boto3
    # print all arguments for debug.
    #for arg in sys.argv:
     #   print (arg)
    #exit()
    # if cmd is pressed we assume it is text capture.
    if sys.argv[1] == "text":
        # extension in 2nd argument
        extension = sys.argv[2] if len(sys.argv) > 2 else 'txt'
        file_path, file_name, content_type = capture_text(extension)
    else:
        file_path, file_name, content_type = capture()
    account_id = os.getenv('cf_account_id')
    bucket_name = os.getenv('cf_bucket_name')
    region_name = os.getenv('cf_region')
    s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=os.getenv('cf_access_key'),
        aws_secret_access_key=os.getenv('cf_secret_key'),
        endpoint_url="https://%s.r2.cloudflarestorage.com/%s" %(account_id, bucket_name),
        region_name=region_name
    )
    # Set explicit content type with UTF-8 encoding for text files
    extra_args = {'ContentType': content_type}
    if content_type and content_type.startswith('text/'):
        extra_args['ContentType'] = content_type + '; charset=utf-8'

    s3.upload_file(file_path, bucket_name, file_name, ExtraArgs=extra_args)
    shorturl = os.getenv('shorturl')
    # if short url is not empty and exists.
    if shorturl:
        if shorturl[len(shorturl)-1] != "/":
            shorturl = shorturl + "/"
        output = "%s%s" %(shorturl,file_name)
    else:
        output = 'https://pub-%s.r2.dev/%s/%s' %(account_id,bucket_name,file_name)
    print (output,end='')

if __name__ == '__main__':
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))
