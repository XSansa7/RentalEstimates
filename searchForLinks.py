import pprint
import os
from googleapiclient.discovery import build

def main():

  ## change developerKey into your own key
  service = build("customsearch", "v1",developerKey="AIzaSyCHNsNCSOz6ervN6_zHdJaoDqW-mXac_-o")
  ## change file name
  addressFile = open('city_st_clean_shx','r')
  querys=[]
  for address in addressFile.readlines()[0:10]:
    querys.append(address.strip())
  # 10 addressIndex can be searched per day for each Google account, change range(0,1) to range(0,10)
  # there should be at most 1000 more links added to the file 'zillow'
  addressIndex = 0
  try:
    for addressIndex in range(0,10):
      print "search for: "+ querys[addressIndex]
      for queryIndex in range(0,10):
        print "search page "+str(queryIndex+1)

        ## change the value of cx to your own search engine ID
        res = service.cse().list(q=querys[addressIndex],cx='010195169098183863802:9s71hhrm6em',start=1+queryIndex*10).execute()
        
        file = open('zillow','a')
        for item in res['items']:
          file.write(item['link']+"\n")
  except:
    print 'quota use up?'

  ## change file name to your own -- jxs -- gjq
  addressFile = open('city_st_clean_shx','r')
  addressFile_new = open('city_st_clean_shx_new','w')

  # drop the 10 addresses that have been searched
  for address in addressFile.readlines()[addressIndex+1:]:
    addressFile_new.write(address)
  addressFile.close()

  os.remove('city_st_clean_shx')
  os.rename('city_st_clean_shx_new','city_st_clean_shx')

if __name__ == '__main__':
  main()