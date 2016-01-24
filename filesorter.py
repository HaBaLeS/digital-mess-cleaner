import exifread
import os
import shutil


import dmcutils
from dmcutils import mylog


report = {}

def processVideo(candidate):
    vp = os.path.join(inputDir,'videos')
    if not os.path.exists(vp):
        os.mkdir(vp)

    outPath = os.path.join(vp,os.path.split(candidate)[1])

    while os.path.exists(outPath) :
        print outPath + " exists geenrating new name"
        outPath = os.path.join(vp,"dif_" + os.path.split(candidate)[1])

    move(candidate, outPath);

def processFile(file):
    print(file)
    if str(file).lower().endswith(('.jpg', '.jpeg')):
        processImage(file)
        report["processImageCount"] = report["processImageCount"] + 1
    elif 'mp4' in str(file).lower():
        #processVideo(candidate)
        pass
    elif 'avi' in str(file).lower():
        #processVideo(candidate)
        pass
    elif 'mov' in str(file).lower():
        #processVideo(candidate)
        pass
    else:
        mylog("Unhandled %s " % file)


def scanAndProcessFolders(inputDir):
    mylog("Starting in " + inputDir)
    fileList = []
    for root, dirs, files in os.walk(inputDir):
        for file in files:
            candidate = os.path.join(root, file)
            fileList.append(candidate);

    for candidate in fileList:
            processImage(candidate);





def processImage(img):
    with open(img, "rb") as f:
        tags = exifread.process_file(f, stop_tag='EXIF DateTimeOriginal')
        datestr = "0"
        if "EXIF DateTimeOriginal" in tags:
            datestr = str(tags["EXIF DateTimeOriginal"])
        elif "Image DateTime" in tags:
            datestr = str(tags["Image DateTime"])

        if not datestr == "0" and not datestr == " ":
            moveImage(img, datestr)
        else:
            report["processNoExif"] = report["processNoExif"] +1
            if(args.requireExif):
                mylog("Skip %s due missing EXIF Date" % img)
                return
            mylog("%s - No EXIFDate Found" % img)
            ndd = os.path.join(args.targetFolder,"nodate") #maybe old directory structure could be preserved
            if(not os.path.exists(ndd)):
                    os.mkdir(ndd)
            move(img,os.path.join(ndd,os.path.split(img)[1]))


def moveImage(image,datestr):
    dateList = datestr.split(':')
    year, month = createDirsIfNotExist(dateList)
    filename = os.path.split(image)[1]

    newPath = os.path.join(args.targetFolder, year,month,filename)
    if(os.path.exists(newPath)):
        if(not checkForDublette(image,newPath)):
            newPath = os.path.join(args.targetFolder, year, month, "dif_" + filename)
            mylog("New filename for conflicting file generated %s" % newPath)
            move(image,newPath)
        else:
            if not args.copyonly:
                mylog("Deleting %s it already exists in %s" % (image,newPath))
                os.remove(image)
    else:
        move(image,newPath)


def move(srcFile, toDir):
    if args.copyonly:
        mylog("copy %s to direcotry %s" % (srcFile,toDir))
        shutil.copy(srcFile,toDir)
    else:
        mylog("move %s to direcotry %s" % (srcFile,toDir))
        shutil.move(srcFile,toDir)



def checkForDublette(image,newPath):
    imageHash =  dmcutils.fileSha265Sum(image)
    copyedHash = dmcutils.fileSha265Sum(newPath)
    if(imageHash == copyedHash):
        return True
    else:
        return False





def createDirsIfNotExist(dateList):
    year = os.path.join(args.targetFolder,dateList[0].strip())
    month = os.path.join(year,dateList[1].strip())
    if(not os.path.exists(year)):
        mylog("Create new Folder %s" % year)
        os.mkdir(year)

    if(not os.path.exists(month)):
        mylog("Create new Folder %s" % month)
        os.mkdir(month)
    return year, month


def init(commandArgs):

    global args

    report["processImageCount"] = 0;
    report["processNoExif"] = 0;

    mylog("Init FileUtils")
    args = commandArgs

if __name__ == '__main__':

    dmcutils.init()
    init(dmcutils.commandArgs)
    scanAndProcessFolders(args.inputFolder)

    mylog("Images processed %s" % report["processImageCount"])
    mylog("Images without valid EXIF Date %s" % report["processNoExif"])


