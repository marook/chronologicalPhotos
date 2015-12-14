#!/usr/bin/python2

import datetime
import exifread
import re
import os.path

def main(imgPaths):
    for path in imgPaths:
        if(os.path.isdir(path)):
            renameRecursive(path)
        elif(isImageFileName(path)):
            renameImage(path)

def renameRecursive(path):
    for name in os.listdir(path):
        if(os.path.isdir(name)):
            continue
        if(not isImageFileName(name)):
            continue
        
        renameImage(os.path.join(path, imgPath))

def isImageFileName(imgPath):
    imgFileName = os.path.basename(imgPath).lower()

    return imgFileName.endswith('.jpg') or imgFileName.endswith('.jpeg')

def renameImage(imgPath):
    imgDir, imgFileName = os.path.split(imgPath)
    
    imgTime = readImageDatetime(imgPath)
    imgName = parseImageName(imgFileName)

    newImgName = '%s %s' % (datetime.datetime.strftime(imgTime, '%Y-%m-%d %H_%M_%S'), imgName)

    if(newImgName != imgFileName):
        print '%s -> %s' % (imgFileName, newImgName)
        
        os.rename(imgPath, os.path.join(imgDir, newImgName))

IMAGE_NAME_PATTERN = re.compile('^(?:[0-9]+\-[0-9]+\-[0-9]+ [0-9]+_[0-9]+_[0-9]+ )?(.*)$')

def parseImageName(imgFileName):
    m = IMAGE_NAME_PATTERN.match(imgFileName)

    if(m):
        return m.group(1)
    else:
        return imgFileName

def readImageDatetime(imgPath):
    tags = None
    
    with open(imgPath, 'r') as f:
        tags = exifread.process_file(f, details=False)

    return datetime.datetime.strptime(tags['EXIF DateTimeOriginal'].values + ' UTC', '%Y:%m:%d %H:%M:%S %Z')

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
