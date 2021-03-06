# -*- coding:utf-8 -*-
import json
import os
import urllib2

import threading




'''import sys
stdo = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout= stdo'''


class PointWithAttr(object):
    def __init__(self,id,lon,lat):
        self.id=id
        self.lon=lon
        self.lat=lat
        self.name=""
# 有o,d点的信息，只爬取小汽车属性信息
def ExtractCarInformation(carmydata,opoint,dpoint,outputfile):
    if carmydata['info']=="OK":
        route=carmydata['route']
        path=route['paths'][0]
        tolls=path['tolls']
        distance=path['distance']
        duration=path['duration']
        usefuldata = [opoint.id, opoint.lon, opoint.lat, dpoint.id, dpoint.lon, dpoint.lat, tolls, duration, distance]
        doc = open(outputfile, 'a')
        # 用分号分隔每一个信息
        for data in usefuldata:
            doc.write(data)
            doc.write(';')
        doc.write('\n')  # 记住换行
        doc.close()
        #print "car", opoint.id, dpoint.id
#    else:
#        print "your url has probelems" + '\n'
#        print  carmydata['info']

#爬取自行车属性信息
def ExtractBikeInformation(bikemydata,opoint,dpoint,outputfile):
    if bikemydata['errmsg']=="OK":
        route=bikemydata['data']
        path=route['paths'][0]
        distance=path['distance']
        duration=path['duration']
        usefuldata = [opoint.id, opoint.lon, opoint.lat, dpoint.id, dpoint.lon, dpoint.lat, duration, distance]
        
#        print bikemydata
#        print '#'*50
        
        doc = open(outputfile, 'a')
        # 用分号分隔每一个信息
        for data in usefuldata:
            doc.write(str(data))
            doc.write(';')
        doc.write('\n')  # 记住换行
        doc.close()
#    else:
#        print "your url has probelems" + '\n'
#        print bikemydata['errmsg']

#爬取步行相关信息
def ExtractWalkInformation(walkmydata,opoint,dpoint,outputfile):
    if walkmydata['status']=='1':
        route=walkmydata['route']
        path=route['paths'][0]
        distance=path['distance']
        duration=path['duration']
        usefuldata = [opoint.id, opoint.lon, opoint.lat, dpoint.id, dpoint.lon, dpoint.lat, duration, distance]

        doc = open(outputfile, 'a')
        # 用分号分隔每一个信息
        for data in usefuldata:
            doc.write(data)
            doc.write(';')
        doc.write('\n')  # 记住换行
        doc.close()
#    else:
#        print "your url has probelems" + '\n'
#        print walkmydata
#        print '#'*50
#        print walkmydata['info']

#有o,d点的信息，只爬取公交属性信息
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
#                print "该路线未提供价格"
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
#            print "距离太近，无需换乘"#换用步行API
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
        #print "bus",opoint.id,dpoint.id  # Print url to see if there is a bug
#    else:
#        print "your url has probelems" + '\n'
#        print  busmydata['info']

#根据文件，返回point的列表
def createpoint(filename,idindex,lonindex,latindex,nameindex):
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
        if nameindex!=0:
            name=linesplit[nameindex]
            point.name=name
        points.append(point)
    return points

class myThreadDown(threading.Thread):
    def __init__(self, xiancheng,starti,endi,outputpathbus,outputpathcar,outputpathbike,outputpathwalk):
        threading.Thread.__init__(self)
        self.xiancheng=xiancheng
        self.starti=starti
        self.endi=endi
        #self.ak="fb607477f41fafe380dff9394cdadabb"
#        self.ak="350b3b1ae4aa853d54294b521069a638"
#        self.ak="b7b322bc0da342c84402c7e75aa379f4"
#        self.ak = '2533c243ca84b5a37611f91b10a3d917'
#        self.ak = '00dd95d3bd1ec265c837a98d3a7b05ad'
        self.ak = 'eb876dfcab39a4e89df3738186edee29'
        #需要更改的参数
        self.date = "2018-11-20"
        self.time = "10:40"
        self.ofile = "C:\Users\Administrator\Desktop\untitled2\O.csv"
        self.dfile = "C:\Users\Administrator\Desktop\untitled2\D.csv"
        #共四个date,time,ofile,dfile
        self.outputpathbus = outputpathbus
        self.outputpathcar = outputpathcar
        self.outputpathbike = outputpathbike
        self.outputpathwalk = outputpathwalk
        self.opointslist = createpoint(self.ofile, 0, 1, 2, 0)
        self.dpointslist = createpoint(self.dfile, 0, 1, 2, 0)
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
                busjson_obj = urllib2.urlopen(busrequesturl)
                busmydata = json.load(busjson_obj)
                #car
                carrequesturl = "http://restapi.amap.com/v3/direction/driving?key=" + self.ak + "&origin=" + opoint.lon + "," + opoint.lat + "&destination=" + dpoint.lon + "," + dpoint.lat + "&originid=&destinationid=&extensions=all&strategy=0&waypoints=&avoidpolygons=&avoidroad="
                carjson_obj = urllib2.urlopen(carrequesturl)
                carmydata = json.load(carjson_obj)
                #bike
                bikerequesturl = "https://restapi.amap.com/v4/direction/bicycling?key=" + self.ak + "&origin=" + opoint.lon + "," + opoint.lat + "&destination=" + dpoint.lon + "," + dpoint.lat
                bikejson_obj = urllib2.urlopen(bikerequesturl)
                bikemydata = json.load(bikejson_obj)
                #walk
                walkrequesturl = "https://restapi.amap.com/v3/direction/walking?key=" + self.ak + "&origin=" + opoint.lon + "," + opoint.lat + "&destination=" + dpoint.lon + "," + dpoint.lat
                walkjson_obj = urllib2.urlopen(walkrequesturl)
                walkmydata = json.load(walkjson_obj)
                #提取并写入outputfile
                ExtractBusInformation(busmydata, opoint,dpoint,busoutputfile)
                ExtractCarInformation(carmydata, opoint,dpoint,caroutputfile)
                ExtractBikeInformation(bikemydata, opoint,dpoint,bikeoutputfile)
                ExtractWalkInformation(walkmydata, opoint,dpoint,walkoutputfile)  
if __name__ == '__main__':
#    print "begin"
    #公交存储路径
    busoutputpath="C:/Users/Administrator/Desktop/untitled2/output/bus/"
    #小汽车存储路径
    caroutputpath="C:/Users/Administrator/Desktop/untitled2/output/car/"
    #自行车储存路径
    bikeoutputpath="C:/Users/Administrator/Desktop/untitled2/output/bike/"
    #步行储存路径
    walkoutputpath="C:/Users/Administrator/Desktop/untitled2/output/walk/"
    
#    thread0 = myThreadDown("No.0", 0, 24, busoutputpath,caroutputpath,bikeoutputpath,walkoutputpath)
#    thread0.start()
#    thread1 = myThreadDown("No.1", 24, 48, busoutputpath,caroutputpath,bikeoutputpath,walkoutputpath)
#    thread1.start()
    thread2 = myThreadDown("No.2", 48, 72, busoutputpath,caroutputpath,bikeoutputpath,walkoutputpath)
    thread2.start()
print('-'*50 + '\n' + '*'*50 + '\n' + '-'*50)

