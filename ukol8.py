import zipfile
import sys
import os
import shutil
import subprocess
from bs4 import BeautifulSoup


### We are using types[] for keeping all possible types in ZIP
types = []


### Remove folder with the same ZIP name, if already exists and create once again
def createTargetPath(archivePath):
	if os.path.exists(archivePath):
		print("Folder with the same name detected...\nRemoving...")
		shutil.rmtree(archivePath)

	os.mkdir(archivePath)
	print ("Successfully created the directory %s " % archivePath)


### Copies a given file f from archive ZIP to new folder archivePath (without creating subfolders!)
def copyFile(archive, f, archivePath, fName):
	source = archive.open(f)
	target = open(os.path.join(archivePath, fName), "wb")

	with source, target:
		shutil.copyfileobj(source, target)

	target.close()
	source.close()


### Checks if type of the file's content already has its folder. If not, creates it
### Finally, moves the file to its relying folder
def classifyFile(typeName, archivePath, fName):
	if not (typeName in types):
		os.mkdir(archivePath + "/" + typeName)
		types.append(typeName)

	shutil.move(archivePath + "/" + fName, archivePath + "/" + typeName + "/" + fName)


### In case of HTML we use that function, which removes all HTML, CSS tags and JavaScript scripts
### Then saves it into the overall "texts.html"
def htmlFileParse(archive, f, archivePath):

	htmlContent = archive.read(f)
	
	soup = BeautifulSoup(htmlContent.decode("utf-8"), "lxml")
	
	for script in soup(["script", "style"]): # remove all javascript and stylesheet code
		script.extract()
	
	textContent = soup.get_text()

	with open(archivePath + '/texts.html', 'a+') as target:
		target.write(textContent)


### Extracts file from ZIP and save it in the folder it relies to (classifies it)
def copyAndClassify(f, archivePath, archive):
	fName = os.path.basename(f)
	fType = fName.split('.')[-1]

	### skips directories and images
	if not fName or fType.lower() in ['jpeg', 'jpg', 'png', 'gif']:
		return

	if fType.lower() in ['html', 'htm']:
		htmlFileParse(archive, f, archivePath)
		return

	copyFile(archive, f, archivePath, fName)

	### We request shell for finding the type of the content
	typeRequest = subprocess.check_output('file "%s/%s"' % (archivePath, fName), shell=True).decode("utf-8") 
	typeName = typeRequest.split(": ")[1].replace('/', ' ')

	classifyFile(typeName, archivePath, fName)


if __name__ == "__main__":

	archivePath = "websoubory.zip"[:-4]

	### Path to our ZIP without .zip ending
	# archivePath = sys.argv[1][:-4]

	archive = zipfile.ZipFile(archivePath+".zip", 'r')

	createTargetPath(archivePath)

	for f in archive.namelist():

		copyAndClassify(f, archivePath, archive)
