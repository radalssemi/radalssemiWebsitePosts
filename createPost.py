import zipfile  # zipping files for download
import pathlib  # to zip folder structure
import os  # directories and stuff
import cv2  # making thumbnails and medium images
import re  # searching for
import json  # writing json file
import easygui  # selecting source folder and adding comments
import shutil  # copying files



# -------------------------------------------------------
# |  This is a script I made for creating a new post    |
# |  for this website.                                  |
# |                                                     |
# |  It's based around a folder structure I use         |
# |  for my photos. I have batch script in this folder  |
# |  that creates the proper folders.                   |
# |                                                     |
# -------------------------------------------------------





# check if posts.json exists:
if not os.path.isfile("posts.json"):
    open("./posts.json", "w")









#
# ----- VARIABLES -----
#



with open("./posts.json", "r+") as f:
    try:
        data = json.load(f)
        data["numberOfPosts"] = data["numberOfPosts"] + 1
        currentPostID = data["numberOfPosts"]
        currentPostName = "post" + str(currentPostID)
        initialNumberOfImages = data["numberOfImages"]
        currentImageID = data["numberOfImages"]
        currentSrcID = currentImageID
        allPostsData = data["posts"]
    except:
        print("error reading file! starting from 1 \n")
        currentPostID = 1
        currentPostName = "post" + str(currentPostID)
        initialNumberOfImages = 0
        currentImageID = 0
        currentSrcID = currentImageID
        allPostsData = {}
        pass


postsDirectory = ".\\" + currentPostName

directoryToMake = [postsDirectory + "\\edit", postsDirectory + "\\edit\\fullsize", postsDirectory + "\\edit\\medium", postsDirectory + "\\edit\\thumbnail", postsDirectory + "\\src", postsDirectory + "\\download"]

path = easygui.diropenbox()
imagesDate = re.search("\d\d[-]\d\d[-]\d\d\d\d", path)[0]



dictionarySrc = {} 
dictionaryImages = {}
comment = {}

defaultJson = {
    "numberOfPosts": 0,
    "numberOfImages": 0,
    "posts": {}
}
#
# ----- END OF VARIABLES -----
#











#
# ----- FUNCTIONS -----
#



def writeComment(commentText, commentImageID):
    with open(".\\posts.json", "r+") as f:
        data = json.load(f)
        rangeStart = data["posts"][currentPostName]["edit"]["rangeStart"]
        commentImageID += rangeStart
        if str(comment) is not None or "":
            data["posts"][currentPostName]["info"]["imgComments"]["img" +
                                                                str(commentImageID)] = str(commentText)
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f, indent=2)
            f.truncate()
            print(f"comment for img{commentImageID} written:    {commentText}\n")
        else:
            print(f"no comment for img{commentImageID}")

def addComments():
    commentImageID = 0
    for filename in os.listdir(".\\" + currentPostName + "\\edit\\thumbnail"):
        commentText = easygui.enterbox(
            "add comment", image=".\\" + currentPostName + "\\edit\\thumbnail\\" + filename)
        writeComment(commentText, commentImageID)
        commentImageID += 1




def makeZipFile(toZip, zipTo):
    with zipfile.ZipFile(zipTo, mode="w") as archive:
        for file_path in toZip.iterdir():
            archive.write(file_path, arcname=file_path.name)

def writeFilesToZips():
    makeZipFile(pathlib.Path(f"./{currentPostName}/edit/"),
                f"./{currentPostName}/download/{currentPostName}-edit.zip")
    makeZipFile(pathlib.Path(f"./{currentPostName}/src/"),
                f"./{currentPostName}/download/{currentPostName}-src.zip")




def createThumbnail(filename):
    im = cv2.imread(path + "\\picks\\edit\\" + filename, cv2.IMREAD_UNCHANGED)
    h = im.shape[0]
    w = im.shape[1]
    dim = (int(480 * w / h), 480)
    resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(postsDirectory + "\\edit\\thumbnail\\" +
                filename.rsplit(".", 1)[0] + ".jpg", resized, [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(f"thumbnail        {filename}")

def createMedium(filename):
    im = cv2.imread(path + "\\picks\\edit\\" + filename, cv2.IMREAD_UNCHANGED)
    h = im.shape[0]
    w = im.shape[1]
    dim = (int(1920 * w / h), 1920)
    resized = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
    cv2.imwrite(postsDirectory + "\\edit\\medium\\" +
                filename.rsplit(".", 1)[0] + ".jpg", resized, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(f"medium           {filename}")

def copyFullsize(filename):
    shutil.copy2(path + "\\picks\\edit\\" + filename,
                 postsDirectory + "\\edit\\fullsize\\")
    print(f"fullsize         {filename}")

def copySrc(filename):
    shutil.copy2(path + "\\picks\\" + filename, postsDirectory + "\\src\\")
    print(f"srcimage          {filename}")




def writeJsonData():
    with open(".\\posts.json", "r+") as f:
        data = json.load(f)
        data["posts"] = writeThis | allPostsData
        data["numberOfPosts"] = currentPostID
        data["numberOfImages"] = currentImageID
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
        if (easygui.ynbox("do you wanna add comments?")):
            addComments()
        print("\n-------------------------------------------------------")
        print(f"written {currentPostName} to posts.json")
        print("-------------------------------------------------------\n")
#
# ----- END OF FUNCTIONS -----
#











#
# ----- WORKING SCRIPT -----
#



print(f"\n\n\nsource path:   {path}\n\n\n\n")

# printing info about post
print("-------------------------------------------------------")
print(f"date read:          {imagesDate}")
print(f"images exist:       {currentImageID}")
print(f"making post:        {currentPostName}")
print("-------------------------------------------------------\n")




# create folders for post
for i in directoryToMake:
    if not os.path.isdir(i):
        os.makedirs(i)
        print(f"created dir:     {i}")


open(".\\posts.json", "w")
print("\n")

# find edited images and create thumbnails and  medium; copy fullsize
for filename in os.listdir(path + "\\picks\\edit"):
    if filename.endswith(".jpg" or ".jpeg" or ".png" or "JPG" or "JPEG" or "PNG"):
        currentImageID += 1
        print(currentImageID)
        dictionaryImages["img" + str(currentImageID)] = filename
        createThumbnail(filename)
        createMedium(filename)
        copyFullsize(filename)
        print()
print()
# find src images and copy
for filename in os.listdir(path + ".\\picks\\"):
    if filename.endswith(".CR2"):
        currentSrcID += 1
        dictionarySrc["img" + str(currentSrcID)] = filename
        copySrc(filename)
print()


# create download zip files with: src, edit
writeFilesToZips()



# I declare this here because currentImageID has to be updated
writeThis = {
    currentPostName: {
        "edit": {
            "rangeStart": initialNumberOfImages + 1,
            "rangeEnd": currentImageID,
            "name": dictionaryImages
        },
        "info":
        {
            "contentType": "photos",
            "date": imagesDate,
            "imgComments": {}
        },
        "src": dictionarySrc
    }
}
# write data to json file: if can't read create new
try:
    writeJsonData()
except:
    open(".\\posts.json", "w").write("{\n}")
    with open(".\\posts.json", "r+") as f:
        data = json.load(f)
        data = defaultJson
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=2)
        f.truncate()
        print("default json loaded")
    writeJsonData()
#
# ----- WORKING SCRIPT -----
#