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


### Copies a given file f from archive ZIP to new folder with the same name as ZIP (without creating subfolders!)
def copyFile(archive, f, fName):

	targetPath = archive.filename[:-4]

	source = archive.open(f)
	target = open(os.path.join(targetPath, fName), "wb")

	with source, target:
		shutil.copyfileobj(source, target)

	target.close()
	source.close()


### Checks if type of the file's content already has its folder. If not, creates it
### Finally, moves the file to its relying folder
def classifyFile(typeName, targetPath, fName):
	
	if not (typeName in types):
		os.mkdir(targetPath + "/" + typeName)
		types.append(typeName)

	shutil.move(targetPath + "/" + fName, targetPath + "/" + typeName + "/" + fName)


### In case of HTML we use that function, which removes all HTML, CSS tags and JavaScript scripts
### Then saves it into the overall "texts.html"
def htmlFileParse(archive, f):

	targetPath = archive.filename[:-4]

	htmlContent = archive.read(f)
	
	soup = BeautifulSoup(htmlContent.decode("utf-8"), "lxml")
	
	for script in soup(["script", "style"]): # remove all javascript and stylesheet code
		script.extract()
	
	textContent = soup.get_text()

	with open(targetPath + '/texts.html', 'a+') as target:
		target.write(textContent)


### Extracts file from ZIP and save it in the folder it relies to (classifies it)
def copyAndClassify(f, archive):

	targetPath = archive.filename[:-4]

	### fName representes item's name with .extension (eg. mycoolimage.jpg)
	fName = os.path.basename(f)

	### skips directories and images
	### fName.split('.')[-1] represents file's extension

	if (not fName) or (fName.split('.')[-1].lower() in ['jpeg', 'jpg', 'png', 'gif']):
		return

	if fName.split('.')[-1].lower() in ['html', 'htm']:
		htmlFileParse(archive, f)
		return

	copyFile(archive, f, fName)

	### We request shell for finding the type of the file's content
	typeRequest = subprocess.check_output('file "%s/%s"' % (targetPath, fName), shell=True).decode("utf-8") 
	typeName = typeRequest.split(": ")[1].replace('/', ' ')

	classifyFile(typeName, targetPath, fName)


if __name__ == "__main__":

	### Creates ZipFile object from our argv input
	#archive = zipfile.ZipFile(sys.argv[1][:-4]+".zip", 'r')
	archive = zipfile.ZipFile("websoubory.zip", 'r')

	### By archive.filename we can find it's relative path, for ex. 'websoubory.zip'
	createTargetPath(archive.filename[:-4])

	### Goes through every item in ZIP
	for f in archive.namelist():
		copyAndClassify(f, archive)
