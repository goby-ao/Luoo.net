import urllib2
import os
import re
import time

print '------------------------------------'
print 'Name:   Luoo.net-Mp3 crawler '
print 'author: Chen Yao'
print 'version: v1.0'
print '------------------------------------'

headers = {'Referer':'http://www.luoo.net/'}
charInSongName = ['?',  '!' , '\\' , '/'  , '#' ,'%' , '*', '^' , '~']
sourUrl = 'http://www.luoo.net/radio/radio'
rawPath = "./Luoo.net/"
coverRaw = 'http://www.luoo.net/wp-content/uploads/'
htmlRaw = 'http://www.luoo.net/'

#sourUrl_296  = 'http://www.luoo.net/radio/radio296/mp3.xml'
#sourUrl_1 = 'http://www.luoo.net/radio/radio1/mp3player.xml'

#To do : file name
#luoo = file('luoo.txt')
#li = luoo.readlines()

# request mp3 jpg ...
def requestResource(sourcePath, url):
	# file do not exist, download
    if (os.path.isfile(sourcePath) == False):
        timeStart = time.time()
        req = urllib2.Request(
            url = url,
            headers = headers
            )
        try:
        	# catch the exception, example HTTP_404 
            response = urllib2.urlopen(req, timeout = 10)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason 
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
        	# write to the file
            with open(sourcePath, "wb") as code:
                code.write(response.read())
            
            # print the download time
            timeEnd = time.time()
            spendTime = time.strftime('%M:%S',time.localtime(timeEnd - timeStart))
            print '### Download Time:  [%s]' % spendTime
    # file exist
    elif(os.path.isfile(sourcePath)):
    	# then check wether file is empty
        if((os.path.getsize(sourcePath)) == 0L):
        	# Empyt, then reomove it and retry
            os.remove(sourcePath)
            requestResource(sourcePath, url)
        # file exist and is not empty
        else:
            print "### file already exist!!! "
            pass

# print the download detail infomation
def print_info(songName, fileNum):
    print '### Downloading >>> [%s].'%fileNum + songName

# remove the special char in songName
def removeChar(songName):
    for i in charInSongName:
        songName = songName.replace(i,' ')
    return songName
    
# start download
def download(start,end):
    for x in range(start,end):
        startTime = time.time()
        if x < 296:
            Url = sourUrl + str(x) +'/mp3player.xml'
        else:
            Url = sourUrl + str(x) +'/mp3.xml'
        folderPath = rawPath + 'Luoo_' + str(x) + '/'
        #folderPath = rawPath + li[x-2].rstrip() + '\\'
        # new a fold in path
        if os.path.isdir(folderPath): 
            pass 
        else: 
            os.mkdir(folderPath)
        # read the xml 
        lines = urllib2.urlopen(Url, timeout = 10 ).readlines()
        # total songs
        songs = len(lines) - 3
        print '****************'
        print 'Radio: radio' + str(x)
        print 'Total: ' + str(songs) + ' songs'
        print '****************'
        print('----------------------------------')

        # Download the cover
        coverUrl = coverRaw + str(x) + '.jpg'
        coverPath = folderPath + 'cover.jpg'
        print '### Downlonding >>> Cover.jpg'
        requestResource(coverPath,coverUrl)

        # Download the HTML
        htmlUrl = htmlRaw + str(x)
        htmlPath = folderPath + 'VOL.' + str(x) + '.html'
        print '### Downloading >>> HTML'
        requestResource(htmlPath,htmlUrl)

        print('----------------------------------')
        print '------------------------------------------------------'
        fileNum = 1
        for line in lines[2:-1]:
            line = line.strip()
            a = re.findall(r'http.*.mp3',line)
            if a == []:
                continue
            realUrl = str(a[0])
            b = re.findall(r'(?<=title=").*(?="\s*/)',line)
            if b == []:
                continue
            songName = str(b[0]).decode('utf-8')
            songName = removeChar(songName)
            print_info(songName,fileNum)
           
           	# Download mp3 
            musicUrl = realUrl
            musicPath = folderPath + songName + ".mp3"
            requestResource(musicPath,musicUrl)
            fileNum += 1
            print '------------------------------------------------------'
        lines = []
        endTime = time.time()
        date = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
        during = time.strftime('%M:%S',time.localtime(endTime - startTime))
        
        print('----------------------------------')
        print "### Total time: " , during       
        print "### Date: " ,  date
        print('----------------------------------')
        print('\n')

if __name__ == '__main__':
    startNum = input('input the start number(start from 1): ')
    endNum = input('input the end(end with the last Vol): ')
    if(os.path.isdir(rawPath) == False):
    	os.mkdir(rawPath)
    download(startNum,endNum)
 
