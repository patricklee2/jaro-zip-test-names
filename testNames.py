from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import subprocess
import os
import requests
import datetime
from time import sleep

def cleanup(name):
    # print("cleaning up")
    deleteFolder = subprocess.run(["rm", "-r", name])
    deleteZip = subprocess.run(["rm", "{0}.zip".format(name)])

def rename(name):
    # print("creating directory")
    # copy template
    copy = subprocess.run(["cp","-r", "template", name])
    # rename
    rename = subprocess.run(["mv", "{0}/renameMe".format(name), "{0}/{1}".format(name, name)])

def createZip(name):
    # print("zipping")
    # zip
    zip = subprocess.run(["7z","a", "-mx=0", "{0}.zip".format(name), ".\\{0}\\*".format(name)], stdout=subprocess.PIPE)

def upload(filename):
    print("uploading")
    blobName = 'zip-test-name.zip'

    # get service
    block_blob_service = BlockBlobService(account_name='ziptestpatrick', account_key='MRVydk0ZxMuzwbkc/GyKg/276knpogjDP6q99Sr0cjVu9mez6T4LV/QpSNDu+vkVN7dlEu6kZ+reBS8es0s/bA==')
    # delete
    # block_blob_service.delete_blob('ziptestpatrick', blobName)
    # create
    block_blob_service.create_blob_from_path(
        'ziptestpatrick',
        blobName,
        "{0}.zip".format(filename),
        content_settings=ContentSettings(content_type='application/zip'))
    # list
    # generator = block_blob_service.list_blobs('ziptestpatrick')
    # for blob in generator:
    #     print(blob.name)
    
def stopApp(url):
    cmd="az functionapp stop --ids {0}".format(url)
    os.system(cmd)

def startApp(url):
    cmd="az functionapp start --ids {0}".format(url)
    os.system(cmd)

def waitUntilStopped(site):
    print("stopping")
    while True:
        r = requests.get(site)
        if r.status_code == 403:
            print("stopped")
            break
        else:
            print(".")
            sleep(1)

def waitUntilStarted(url):
    print("Starting")
    while True:
        r = requests.get(url)
        if r.status_code == 200:
            print("started")
            break
        else:
            print(".")
            sleep(1)

def testName(filename):
    siteId='/subscriptions/02c9e5be-fbd7-4d45-9c13-e9a82eed2003/resourceGroups/zip-test-name/providers/Microsoft.Web/sites/zip-test-name'
    appUrl='https://zip-test-name.azurewebsites.net/'
    functionUrl='https://zip-test-name.azurewebsites.net/api/{0}?name=world'.format(filename)
    rename(filename)
    createZip(filename)
    upload(filename)
    cleanup(filename)

    print("stopping app")
    stopApp(siteId)
    waitUntilStopped(appUrl)
    print("starting app")
    startApp(siteId)
    waitUntilStarted(appUrl)

    print("testing")
    r = requests.get(functionUrl, timeout=300) # 5 min timeout
    if r.status_code != 200:
        print("status code: {0}".format(r.status_code))
        return False
    else:
        return True

###############################################################################################################


passed = open('passed.txt', 'w')
failed = open('failed.txt', 'w')

# common english words
commonWords = open('common-english-usa-1000.txt', 'r')
for word in commonWords:
    filename = word.strip()
    print(filename)
    result = testName(filename)
    if (not result):
        failed.write("{0}\n".format(filename))
        failed.flush()
    else:
        passed.write("{0}\n".format(filename))
        passed.flush()


passed.close()
failed.close()

# passed2 = open('passed2.txt', 'w')
# failed2 = open('failed2.txt', 'w')

# # common english words
# commonWords = open('failed.txt', 'r')
# for word in commonWords:
#     filename = word.strip()
#     print(filename)
#     result = testName(filename)
#     if (not result):
#         failed2.write("{0}\n".format(filename))
#         failed2.flush()
#     else:
#         passed2.write("{0}\n".format(filename))
#         passed2.flush()


# passed2.close()
# failed2.close()


# passed3 = open('passed3.txt', 'w')
# failed3 = open('failed3.txt', 'w')

# # common english words
# commonWords = open('failed2.txt', 'r')
# for word in commonWords:
#     filename = word.strip()
#     print(filename)
#     result = testName(filename)
#     if (not result):
#         failed3.write("{0}\n".format(filename))
#         failed3.flush()
#     else:
#         passed3.write("{0}\n".format(filename))
#         passed3.flush()


# passed3.close()
# failed3.close()

# passed4 = open('passed4.txt', 'w')
# failed4 = open('failed4.txt', 'w')

# # common english words
# commonWords = open('failed3.txt', 'r')
# for word in commonWords:
#     filename = word.strip()
#     print(filename)
#     result = testName(filename)
#     if (not result):
#         failed4.write("{0}\n".format(filename))
#         failed4.flush()
#     else:
#         passed4.write("{0}\n".format(filename))
#         passed4.flush()


# passed4.close()
# failed4.close()


failed = ''
passed = ''

# ascii symbols
# do not use 
# 0-31 (0x00-0x1F)
# < (less than)
# > (greater than)
# : (colon)
# " (double quote)
# / (forward slash)
# \ (backslash)
# | (vertical bar or pipe)
# ? (question mark)
# * (asterisk)
#   (space at end)
# . (period at end)

# The name must be unique within a Function App. It must start with a letter and can contain letters, numbers (0-9), dashes ("-"), and underscores ("_").

# forbidden = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
# forbidden = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', ' ', '.', '\'', '-']

# # # test '\'', '-' manually

# for i in range(32, 127+1):
#     filename = chr(i)
#     if filename not in forbidden:
#         filename = "a{0}a".format(filename)
#         print(filename)
#         result = testName(filename)
#         if (not result):
#             failed = "{0}\n {1}".format(failed, filename).strip()
#         else:
#             passed = "{0}\n {1}".format(passed, filename).strip()

# filenames = ['space space', 'period.period', 'dash-dash', 'underscore_underscore']
# for filename in filenames:
#     print(filename)
#     result = testName(filename)
#     if (not result):
#         failed = "{0}\n {1}".format(failed, filename).strip()
#     else:
#         passed = "{0}\n {1}".format(passed, filename).strip()

# extended ascii

# for i in range(129, 256+1):
#     filename = chr(i)    
#     filename = "a{0}a".format(filename)
#     print(i)
#     print(filename)
#     result = testName(filename)
#     if (not result):
#         failed = "{0}\n {1} {2}".format(failed, filename, i).strip()
#     else:
#         passed = "{0}\n {1} {2}".format(passed, filename, i).strip()


# unicode
# for i in range(256, 65535, 1000):
#     filename = chr(i)    
#     print(i)
#     print(filename)
#     result = testName(filename)
#     if (not result):
#         failed = "{0}\n {1} {2}".format(failed, filename, i).strip()
#     else:
#         passed = "{0}\n {1} {2}".format(passed, filename, i).strip()

#     filename = "a{0}a".format(filename)
#     print(i)
#     print(filename)
#     result = testName(filename)
#     if (not result):
#         failed = "{0}\n {1} {2}".format(failed, filename, i).strip()
#     else:
#         passed = "{0}\n {1} {2}".format(passed, filename, i).strip()



#sanity check
# filename = 'A'
# print(filename)
# result = testName(filename)
# if (not result):
#     failed = "{0}\n {1}".format(failed, filename).strip()
# else:
#     passed = "{0}\n {1}".format(passed, filename).strip()


# manual test
# filenames = ["working"]
# for filename in filenames:
#     print(filename)
#     result = testName(filename)
#     if (not result):
#         failed = "{0}\n {1}".format(failed, filename).strip()
#     else:
#         passed = "{0}\n {1}".format(passed, filename).strip()


print("passed\n{0}".format(passed))
print("failed\n{0}".format(failed))
