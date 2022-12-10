import os  # directories and stuff
import cv2  # making thumbnails and medium images (pip install opencv-python)
import re  # searching for date in selected path
import json  # writing json file
import easygui  # selecting source folder and adding comments 
import shutil  # copying files and zipping for download
# ! PIL needs to be installed to view image while adding comments (pip install pillow)



# ==== nyuballs ================================= - □ x =
# |                                                     |
# |  This is a script I made for creating a new post    |
# |  for this website.                                  |
# |                                                     |
# |  It's based around a folder structure I use         |
# |  for my photos. I have batch script in this folder  |
# |  that creates the proper folders.                   |
# |                                                     |
# -------------------------------------------------------





# check if posts.json exists:
if not os.path.isfile(".\\posts.json"):
    open(".\\posts.json", "w")
    print()
    print("posts.json didn't exist, making file")









#
# ----- VARIABLES -----
#



with open(".\\posts.json", "r+") as f:
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
        print()
        print("error reading from file! starting from defaults \n")
        currentPostID = 1
        currentPostName = "post" + str(currentPostID)
        initialNumberOfImages = 0
        currentImageID = 0
        currentSrcID = currentImageID
        allPostsData = {}
        pass


postsDirectory = ".\\posts\\" + currentPostName

directoryToMake = [postsDirectory + "\\edit", postsDirectory + "\\edit\\fullsize", postsDirectory + "\\edit\\medium", postsDirectory + "\\edit\\thumbnail", postsDirectory + "\\src", postsDirectory + "\\download"]

path = easygui.diropenbox()
imagesDate = re.search("([0-9]+(-[0-9]+)+)", path)[0]



dictionarySrc = {} 
dictionaryImages = {}

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





def writeFilesToZips():
    shutil.make_archive(f".\\posts\\{currentPostName}\\download\\{currentPostName}-edit", 'zip', f".\\posts\\{currentPostName}\\edit\\")
    shutil.make_archive(f".\\posts\\{currentPostName}\\download\\{currentPostName}-src", 'zip', f".\\posts\\{currentPostName}\\edit\\")
    print("images zipped")





def writeComment(commentText, commentImageID):
    with open(".\\posts.json", "r+") as f:
        data = json.load(f)
        rangeStart = data["posts"][currentPostName]["edit"]["rangeStart"]
        commentImageID += rangeStart
        if commentText == "None" or bool(commentText):
            data["posts"][currentPostName]["info"]["imgComments"]["img" + str(commentImageID)] = str(commentText)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
            print(f"comment for img{commentImageID} written:    {commentText}")
        else:
            print(f"no comment for img{commentImageID}")

def addComments():
    print("\n")
    print(f"adding comments to post {currentPostName}")
    print()
    commentImageID = 0
    for filename in os.listdir(postsDirectory + "\\edit\\thumbnail\\"):
        commentText = easygui.enterbox(f"add comment for img{commentImageID}", image = f"{postsDirectory}\\edit\\thumbnail\\{filename}")
        writeComment(commentText, commentImageID)
        commentImageID += 1



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
        print(f"img{currentImageID}")
        dictionaryImages["img" + str(currentImageID)] = filename
        createThumbnail(filename)
        createMedium(filename)
        copyFullsize(filename)
        print()
print()
# find src images and copy
for filename in os.listdir(path + "\\picks\\"):
    if filename.endswith(".CR2"):
        currentSrcID += 1
        print(f"src{currentSrcID}")
        dictionarySrc["src" + str(currentSrcID)] = filename
        copySrc(filename)
        print()
print("\n")


# create download zip files with: src, edit
writeFilesToZips()
print()

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
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
        print("default json loaded")
    writeJsonData()
#
# ----- END OF WORKING SCRIPT -----
#