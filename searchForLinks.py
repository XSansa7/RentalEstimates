import pprint

from googleapiclient.discovery import build

def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",developerKey="AIzaSyBxnwBAgKwvVWNfYQu7dnSPi4KZL7O105w")
  addressFile = open('city_st_clean','r')
  querys=[]
  for address in addressFile.readlines():
    querys.append(address)
  for addressIndex in range(0,1):
    for queryIndex in range(0,10):
      res = service.cse().list(q=querys[addressIndex],cx='017594452969038394662:re2jac33guq',start=1+queryIndex*10).execute()
      file = open('zillow','a')
      for item in res['items']:
        file.write(item['link']+"\n")

if __name__ == '__main__':
  main()