import pprint
import os
from googleapiclient.discovery import build

def main():

  ## change developerKey into your own key
  keys = []
  keyFile = open('keyFile','r')
  for line in keyFile.readlines():
    devKey = line.split('\t')[0]
    cxKey = line.split('\t')[1].strip()
    keys.append([devKey,cxKey])
  for keyIndex in range(len(keys)):
    print keys[keyIndex][0]
    service = build("customsearch", "v1",developerKey=keys[keyIndex][0])
    ## change shx to your name
    addressFile = open('city_st_clean_gjq','r')
    querys=[]
    for address in addressFile.readlines()[0:10]:
      querys.append(address.strip())
    # 10 addressIndex can be searched per day for each Google account, change range(0,1) to range(0,10)
    # there should be at most 1000 more links added to the file 'zillow'
    addressIndex = 0
    exceed = 1
    #try:
    for addressIndex in range(0,10):
      print "search for: "+ querys[addressIndex]
      for queryIndex in range(0,10):
        print "search page "+str(queryIndex+1)

        ## change the value of cx to your own search engine ID
        try:
          res = service.cse().list(q=querys[addressIndex],cx=keys[keyIndex][1],start=1+queryIndex*10).execute()
          file = open('zillow','a')
          for item in res['items']:
            file.write(item['link']+"\n")
        except Exception,e:
          print e
          exceed = 0
    # except Exception,e: 
    #   print e
    #   exceed = 0

    ## change file name to your own -- jxs -- gjq
    addressFile = open('city_st_clean_gjq','r')
    addressFile_new = open('city_st_clean_gjq_new','w')

    # drop the 10 addresses that have been searched
    for address in addressFile.readlines()[addressIndex+exceed:]:
      addressFile_new.write(address)
    addressFile.close()

    ## change shx to your name
    os.remove('city_st_clean_gjq')
    os.rename('city_st_clean_gjq_new','city_st_clean_gjq')

if __name__ == '__main__':
  main()