#data_script_v2.py Eric Peltola 11.2018
import pycurl
import pymongo
import time
import re

# curl -H "Authorization: Bearer 65bb9f5f762c30c7899f802bb7eb6cd522cfb6b9" https://api.particle.io/v1/devices/360057000351353530373132
# curl -H "Authorization: Bearer 65bb9f5f762c30c7899f802bb7eb6cd522cfb6b9" https://api.particle.io/v1/devices/360057000351353530373132/events/weight

def save(data):
    '''save weight data to mLab'''
    uri = 'mongodb://root:toor@ds155577.mlab.com:55577/limby'
    # uri = 'mongodb://root:toor@ds155577.mlab.com:55577/LAMBO'
    client = pymongo.MongoClient(uri)
    db = client.get_database()
    col = db.Data
    # userid = 143744072
    userid = -470610416
    doc = {}
    doc["userid"]=userid
    doc["time"] = int(round(time.time() * 1000))
    doc["value"] = int(float(data))
    print(doc)
    col.insert_one(doc)  

def on_receive(data):
    #extract sensor reading from particle published bytes
    data_str = str(data)
    r = re.search('"data":"(.*)","ttl', data_str) #find the substring we want
    if r is not None:
        print(r.group(1))
        save(r.group(1))

def sync(deviceId, accessToken):
	"""sync data from Particle to mLab of given device id
	"""
	conn = pycurl.Curl()
	conn.setopt(pycurl.URL, 'https://api.particle.io/v1/devices/'+deviceId+'/events/weight')
	conn.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer '+accessToken])
	conn.setopt(pycurl.WRITEFUNCTION, on_receive)
	try:
		conn.perform()
	except pycurl.error as error:
		errno, errstr = error
		print(errstr)

def main():
    # deviceId = '3e002d000e47363336383437' #sparkling_badger
    #deviceId = '360034001847343438323536' #hamster_wizard
    deviceId = '360057000351353530373132' #bird_girder
    #accessToken = 'c4fbea34670f7726445924aac6ac3fa89f31d7f1'
    accessToken = '412d6c5b6ff724d409f5494ea4f52ed748bf5ba6' #Eric Peltola
    # accessToken = '65bb9f5f762c30c7899f802bb7eb6cd522cfb6b9'
    sync(deviceId, accessToken)

if __name__ == "__main__":
    main()
