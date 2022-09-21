# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:26:27 2020

@author: Somil
"""

#import PIL
#from PIL.Image import core as _imaging
from PIL import Image
import os
import stat
import shutil
import datetime
import glob


class ImageOrganizer:
    def __init__(self,dirname=''):
        self.images = os.listdir(dirname)
         #recursive read
        self.images = [f for f in glob.glob(dirname + "**/*.jpg", recursive=True)]
        self.images = self.images + [f for f in glob.glob(dirname + "**/*.JPG", recursive=True)]
        self.dirname = dirname

    def preprocess_exif(self,data):
        data = data.strip()
        data = data.strip('\x00')

        return data

    def sort_by_device(self):
        for fname in self.images:
            with Image.open(os.path.join(self.dirname,fname)) as img:
                exif = img._getexif()

            manuf = self.preprocess_exif(exif[271])
            device = self.preprocess_exif(exif[272])
            merged = manuf + ' ' + device

            if not os.path.isdir(merged):
                os.mkdir(merged)

            shutil.move(os.path.join(self.dirname,fname),os.path.join(merged,fname))
            print("Image {} moved from {} to {} successfully\n".format(fname,os.path.join(self.dirname,fname),os.path.join(merged,fname)))


    def sort_by_year(self):
        for fname in self.images:
            with Image.open(os.path.join(self.dirname,fname)) as img:
                exif = img._getexif()

            ts = self.preprocess_exif(exif[306])
            date = ts.split(' ')[0]
            year = datetime.datetime.strptime(date, '%Y:%m:%d').strftime('%Y')

            if not os.path.isdir(year):
                os.mkdir(year)

            shutil.copy(os.path.join(self.dirname,fname),os.path.join(year,fname))
            print("Image {} moved from {} to {} successfully\n".format(fname,os.path.join(self.dirname,fname),os.path.join(year,fname)))


    def sort_by_yr_month(self):
        for fname in self.images:
            with Image.open(os.path.join(self.dirname,fname)) as img:
                exif = img._getexif()

            ts = self.preprocess_exif(exif[306])
            date = ts.split(' ')[0]
            year = datetime.datetime.strptime(date, '%Y:%m:%d').strftime('%Y')
            month = datetime.datetime.strptime(date, '%Y:%m:%d').strftime('%b')

            if not os.path.isdir(year):
                os.mkdir(year)

            if not os.path.isdir(os.path.join(year,month)):
                os.mkdir(os.path.join(year,month))

            shutil.copy(os.path.join(self.dirname,fname),os.path.join(year,month,fname))
            print("Image {} moved from {} to {} successfully\n".format(fname,os.path.join(self.dirname,fname),os.path.join(year,month,fname)))

    def sort_by_device_yr_month(self):
        current=0
        for fname in self.images:
            if os.path.isfile(fname) == True:
                #with Image.open(os.path.join(self.dirname,fname)) as img:
                current+=1
                try:
                    with Image.open(os.path.join(fname)) as img:
                        exif = img._getexif()
                    ts = self.preprocess_exif(exif[36867])
                    date = ts.split(' ')[0]
                    manuf = self.preprocess_exif(exif[271])
                    device = self.preprocess_exif(exif[272])
                    merged = manuf + ' ' + device
                    year = datetime.datetime.strptime(date, '%Y:%m:%d').strftime('%Y')
                    month = datetime.datetime.strptime(date, '%Y:%m:%d').strftime('%b')
                    formated_date = datetime.datetime.strptime(ts,"%Y:%m:%d %H:%M:%S")
                    Unix_timestamp = datetime.datetime.timestamp(formated_date)
                    if not os.path.isdir(merged):
                        os.mkdir(merged)
                    if not os.path.isdir(os.path.join(merged,year)):
                        os.mkdir(os.path.join(merged,year))
                    if not os.path.isdir(os.path.join(merged,year,month)):
                        os.mkdir(os.path.join(merged,year,month))
                    #shutil.copy(os.path.join(self.dirname,fname),os.path.join(merged,year,month,fname))

                    shutil.copy(os.path.join(fname),os.path.join(merged,year,month,os.path.basename(fname)))
                    #Update timestampt
                    os.utime(os.path.join(merged,year,month,os.path.basename(fname)),(Unix_timestamp,Unix_timestamp))
                    #Update timestpamt for folder
                    folder = os.path.dirname(os.path.abspath(os.path.join(merged,year,month,os.path.basename(fname))))
                    os.utime(folder,(Unix_timestamp,Unix_timestamp))
                    print("Image {} copied from {} to {} successfully\n".format(fname,os.path.join(fname),os.path.join(merged,year,month,os.path.basename(fname))), "  [", current," / ",len(self.images),"]")
                    os.chmod(os.path.join(merged,year,month,os.path.basename(fname)),stat.S_IRWXG )
                except:
                    print("Error metadata from ",fname)
                    merged = "Undefined"
                    if not os.path.isdir(merged):
                        os.mkdir(merged)
                    #os.chmod(os.path.join(fname), stat.S_IRWXG)
                    if os.path.join(fname) != os.path.join(merged,os.path.basename(fname)):
                        shutil.copy(os.path.join(fname),os.path.join(merged,os.path.basename(fname)))
                        os.chmod(os.path.join(merged,os.path.basename(fname)), stat.S_IRWXG)
                        print("Image without exif copied from {} to {} successfully\n".format(os.path.join(fname),os.path.join(merged,os.path.basename(fname))),  "  [", current," / ",len(self.images),"]")
