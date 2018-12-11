# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 20:44:18 2018

@author: Administrator
"""

import requests
import threading

class PointWithAttr():
    def __init__(self,id,lon,lat):
        self.id=id
        self.lon=lon
        self.lat=lat
        self.name=""

def createpoint(filename,idindex,lonindex,latindex):
    doc = open(filename, 'r')
    lines = doc.readlines()
    doc.close()
    points=[]
    for line in lines:
        linesplit = line.split(',')
        id=linesplit[idindex]
        lon=linesplit[lonindex]
        lat=linesplit[latindex].replace("\n", "")
        point=PointWithAttr(id,lon,lat)
        points.append(point)
    return points

def ExtractWalkInformation(walkmydata,opoint,dpoint,outputfile):
    if walkmydata['status'] == '1':
        #还可以提取出租车出行费用，驾车收费，收费路段长度等信息
        distance = walkmydata['route']['paths'][0]['distance']
        duration = walkmydata['route']['paths'][0]['duration']
        print(duration,distance)
        usefuldata = [opoint.id, opoint.lon, opoint.lat, dpoint.id, dpoint.lon, dpoint.lat, duration, distance]
        doc = open(outputfile, 'a')
        # 用分号分隔每一个信息
        for data in usefuldata:
            doc.write(data)
            doc.write(';')
        doc.write('\n')  # 记住换行
  
    else:
        print('Status wrong' + walkmydata['infocode'])




def ExtractCarInformation(carmydata,opoint,dpoint,outputfile):
    if carmydata['status'] == '1':
        #还可以提取出租车出行费用，驾车收费，收费路段长度等信息
        distance = carmydata['route']['paths'][0]['distance']
        duration = carmydata['route']['paths'][0]['duration']
        print(duration,distance)
        usefuldata = [opoint.id, opoint.lon, opoint.lat, dpoint.id, dpoint.lon, dpoint.lat, duration, distance]
        doc = open(outputfile, 'a')
        # 用分号分隔每一个信息
        for data in usefuldata:
            doc.write(data)
            doc.write(';')
        doc.write('\n')  # 记住换行
  
    else:
        print('Status wrong' + carmydata['infocode'])
        
def ExtractBikeInformation(bikemydata,opoint,dpoint,outputfile):
    if bikemydata['errcode'] == 0:
        distance = bikemydata['data']['paths'][0]['distance']
        duration = bikemydata['data']['paths'][0]['duration']
        print(duration,distance)
        usefuldata = [opoint.id, opoint.lon, opoint.lat, dpoint.id, dpoint.lon, dpoint.lat, duration, distance]
        doc = open(outputfile, 'a')
        # 用分号分隔每一个信息
        for data in usefuldata:
            doc.write(str(data))
            doc.write(';')
        doc.write('\n')  # 记住换行
  
    else:
        print('BIKE Status wrong')
        
        
def ExtractBusInformation(busmydata,opoint,dpoint,outputfile):
    if busmydata['info'] == "OK":
        rounts = busmydata['route']
        transits = rounts['transits']
        if transits!=[]:
            project1 = transits[0]
            # important data
            cost = project1['cost']
            if cost==[]:
                cost='0'
                print("该路线未提供价格")
            duration = project1['duration']
            distance = project1['distance']
            usefuldata = [opoint.id,opoint.lon,opoint.lat,dpoint.id,dpoint.lon,dpoint.lat,cost, duration, distance]
            doc = open(outputfile, 'a')
            # 用分号分隔每一个信息
            for data in usefuldata:
                doc.write(data)
                doc.write(';')
            doc.write('\n')  # 记住换行
            doc.close()
        else:
            print("距离太近，无需换乘")#换用步行API
            cost='0'
            distance=rounts['distance']
            if distance==[]:
                distance=0
                return
            else:
                duration=distance #步行速度1m/s
                usefuldata = [opoint.id, opoint.lon, opoint.lat, dpoint.id, dpoint.lon, dpoint.lat, cost, duration,distance]
                doc = open(outputfile, 'a')
                # 用分号分隔每一个信息
                for data in usefuldata:
                    doc.write(data)
                    doc.write(';')
                doc.write('\n')  # 记住换行
                doc.close()
    else:
        print('Bus爬取错误' + 'Status wrong' + busmydata['infocode'])
        
class get_data(threading.Thread):
    def __init__(self,threadID,starti,endi,outputpathbus,outputpathcar,outputpathbike,outputpathwalk):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.starti=starti
        self.endi=endi
        self.ak = 'eb876dfcab39a4e89df3738186edee29'
         #需要更改的参数
        self.date = "2018-11-20"
        self.time = "10:40"
        self.ofile = "C:\\Users\\Administrator\\Desktop\\untitled2\\O.csv"
        self.dfile = "C:\\Users\\Administrator\\Desktop\\untitled2\\D.csv"
        #共四个date,time,ofile,dfile
        self.outputpathbus = outputpathbus
        self.outputpathcar = outputpathcar
        self.outputpathbike = outputpathbike
        self.outputpathwalk = outputpathwalk
        self.opointslist = createpoint(self.ofile, 0, 1, 2)
        self.dpointslist = createpoint(self.dfile, 0, 1, 2)
    def run(self):
        i=0
        j=0
        for i in range(self.starti,self.endi):
            opoint=self.opointslist[i]
            busoutputfile = busoutputpath + "bus_" + str(i) + ".txt"
            caroutputfile = caroutputpath + "car_" + str(i) + ".txt"
            bikeoutputfile = bikeoutputpath + "bike_" + str(i) + ".txt"
            walkoutputfile = walkoutputpath + "walk_" + str(i) + ".txt"
            doc = open(busoutputfile, 'w')
            doc.close()
            doc = open(caroutputfile, 'w')
            doc.close()
            doc = open(bikeoutputfile, 'w')
            doc.close()
            doc = open(walkoutputfile, 'w')
            doc.close()            
            for j in range(0, len(self.dpointslist)):
            #for j in range(self.originj, 2872):
                dpoint=self.dpointslist[j]
#                print "线程%s:O_ID是%s,D_ID是 %s" % (self.xiancheng,opoint.id, dpoint.id)
                #bus
                busrequesturl = "http://restapi.amap.com/v3/direction/transit/integrated?key=" + self.ak + "&origin=" + opoint.lon + "," + opoint.lat + "&destination=" + dpoint.lon + "," + dpoint.lat + "&city=昆山&cityd=昆山&strategy=0&nightflag=0&date=" + self.date + "&time=" + self.time
                busjson_obj = requests.get(busrequesturl)
                busmydata = busjson_obj.json()
                #car
                carrequesturl = "http://restapi.amap.com/v3/direction/driving?key=" + self.ak + "&origin=" + opoint.lon + "," + opoint.lat + "&destination=" + dpoint.lon + "," + dpoint.lat
#                carrequesturl = "http://restapi.amap.com/v3/direction/driving?key=" + 'eb876dfcab39a4e89df3738186edee29' + "&origin=" + "116.481028,39.989643" + "&destination=" + "116.465302,40.004717"
                carjson_obj = requests.get(carrequesturl)
                
                carmydata = carjson_obj.json()
                
                #bike
                bikerequesturl = "https://restapi.amap.com/v4/direction/bicycling?key=" + self.ak + "&origin=" + opoint.lon + "," + opoint.lat + "&destination=" + dpoint.lon + "," + dpoint.lat
                bikejson_obj = requests.get(bikerequesturl)
                bikemydata = bikejson_obj.json()
                #walk
                walkrequesturl = "https://restapi.amap.com/v3/direction/walking?key=" + self.ak + "&origin=" + opoint.lon + "," + opoint.lat + "&destination=" + dpoint.lon + "," + dpoint.lat
                walkjson_obj = requests.get(walkrequesturl)
                walkmydata = walkjson_obj.json()
                #提取并写入outputfile
                ExtractBusInformation(busmydata, opoint,dpoint,busoutputfile)
                ExtractCarInformation(carmydata, opoint,dpoint,caroutputfile)
                ExtractBikeInformation(bikemydata, opoint,dpoint,bikeoutputfile)
                ExtractWalkInformation(walkmydata, opoint,dpoint,walkoutputfile)


if __name__ == '__main__':
    print('-'*50 + '\n' + '*'*50 + '\n' + '*'*50) 
    #公交存储路径
    busoutputpath="C:/Users/Administrator/Desktop/untitled2/output/bus/"
    #小汽车存储路径
    caroutputpath="C:/Users/Administrator/Desktop/untitled2/output/car/"
    #自行车储存路径
    bikeoutputpath="C:/Users/Administrator/Desktop/untitled2/output/bike/"
    #步行储存路径
    walkoutputpath="C:/Users/Administrator/Desktop/untitled2/output/walk/"
    
    thread0 = get_data('No0',0, 24, busoutputpath,caroutputpath,bikeoutputpath,walkoutputpath)
    thread0.start()
    thread1 = get_data('No1',24, 48, busoutputpath,caroutputpath,bikeoutputpath,walkoutputpath)
    thread1.start()
    thread2 = get_data('No2',48, 72, busoutputpath,caroutputpath,bikeoutputpath,walkoutputpath)
    thread2.start()