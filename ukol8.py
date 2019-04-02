import zipfile
import sys
import os
import shutil
import subprocess

### We are using types[] for keeping all possible types in ZIP
types = []

### Remove folder with the same ZIP name, if already exists and create once again
def createTargetPath(path):
	if os.path.exists(path):
		print("Folder with the same name detected...\nRemoving...")
		shutil.rmtree(path)

	os.mkdir(path)
	print ("Successfully created the directory %s " % path)


### Copies a given file f from archive ZIP to new folder path (without creating subfolders!)
def copyFile(archive, f, path, fName):
	source = archive.open(f)
	target = open(os.path.join(path, fName), "wb")

	with source, target:
		shutil.copyfileobj(source, target)

	target.close()

### Checks if type of the file's content already has its folder. If not, creates it
### Finally, moves the file to its relying folder
def classifyFile(typeName, path, fName):
	if not (typeName in types):
		os.mkdir(path + "/" + typeName)
		types.append(typeName)

	shutil.move(path + "/" + fName, path + "/" + typeName + "/" + fName)


### Extracts file from ZIP and save it in the folder it relies to (classifies it)
def copyAndClassify(f, path, archive):
	fName = os.path.basename(f)
	fType = fName.split('.')[-1]

	### skips directories and images
	if not fName or fType.lower() in ['jpeg', 'jpg', 'png', 'gif']:
		return

	copyFile(archive, f, path, fName)

	### We request shell for finding the type of the content
	typeRequest = subprocess.check_output('file "%s/%s"' % (path, fName), shell=True).decode("utf-8") 
	typeName = typeRequest.split(": ")[1].replace('/', ' ')

	classifyFile(typeName, path, fName)


if __name__ == "__main__":

	path = "websoubory.zip"[:-4]

	### Path to our ZIP without .zip ending
	# path = sys.argv[1][:-4]

	archive = zipfile.ZipFile(path+".zip", 'r')

	createTargetPath(path)


	for f in archive.namelist():

		copyAndClassify(f, path, archive)
