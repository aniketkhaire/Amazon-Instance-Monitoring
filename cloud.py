import sys
import json
import boto.ec2.cloudwatch 
import time
import datetime
import requests
import re
from random import randint
from bs4 import BeautifulSoup
#import urllib2
#import urllib.request as urllib2

#import urllib, urllib2
cw = boto.ec2.cloudwatch.connect_to_region('us-east-1',aws_access_key_id ='###',aws_secret_access_key = '###')
conn = boto.ec2.connect_to_region('us-east-1',aws_access_key_id ='###',aws_secret_access_key = '###')

existingInstances = []

def getListOfAllInstances():
	global existingInstances
	instances = conn.get_only_instances()
	
	print (instances)
	for instance in instances :
			if (instance.state_code == 16):
				instance = str(instance)[9:]
				existingInstances.append(instance) 
		

def getMemoryUsageForThisMinute():
	
	for instance in existingInstances :
			print (instance)
			time.sleep(2)
			now = datetime.datetime.now()
			uniqueIdentifier = now.hour+now.minute+now.second+randint(0,9999)
			uniqueIdentifier=str(uniqueIdentifier)
			print(uniqueIdentifier)
			url = "http://52.20.175.246:9200/memory/MemoryUtilization/id"+uniqueIdentifier
	
			NetworkInresponce = cw.get_metric_statistics(
			300,
			datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
			datetime.datetime.utcnow(),
			'MemUsage',
			'EC2/Memory',
			statistics = ['Maximum','Average','Sum','Minimum','SampleCount'],
			dimensions={'InstanceId':[instance]}
		)

			headers = {'Content-Type': 'application/json'}

			for item in NetworkInresponce:
		
				Average = item['Average']
				SampleCount =item['SampleCount']
				Timestamp =item['Timestamp']
				Sum =item['Sum']
				Unit =item['Unit']
				Maximum =item['Maximum']
				Minimum =item['Minimum']
		
				#print(Timestamp)
				newTime = str(Timestamp)

				output = re.sub(' ', 'T', newTime.rstrip())
				print(instance)
				payload = {'Instance-ID':instance,'Average':Average,'SampleCount':SampleCount,'@timestamp':output,'Sum':Sum,'Unit':Unit,'Maximum':Maximum,'Minimum':Minimum,'Network':'NetworkOut'}

				#print(payload)
				
				
				response = requests.post(url, data=json.dumps(payload),headers=headers)
				
				print(response.status_code, response.reason)

			
def getNetWorkInForThisMinute():
	
	for instance in existingInstances :
			print (instance)
			time.sleep(2)
			now = datetime.datetime.now()
			date = time.strftime("%d")+time.strftime("%m")+time.strftime("%Y")
			uniqueIdentifier = now.hour+now.minute+now.second+randint(0,9999)
			uniqueIdentifier=str(uniqueIdentifier)
			print(uniqueIdentifier)
			url = "http://52.20.175.246:9200/network/NetworkUtilization/id"+uniqueIdentifier
	
			NetworkInresponce = cw.get_metric_statistics(
			300,
			datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
			datetime.datetime.utcnow(),
			'NetworkIn',
			'AWS/EC2',
			statistics = ['Maximum','Average','Sum','Minimum','SampleCount'],
			dimensions={'InstanceId':[instance]}
		)

			headers = {'Content-Type': 'application/json'}

			for item in NetworkInresponce:
		
				Average = item['Average']
				SampleCount =item['SampleCount']
				Timestamp =item['Timestamp']
				Sum =item['Sum']
				Unit =item['Unit']
				Maximum =item['Maximum']
				Minimum =item['Minimum']
		
				print(Timestamp)
				newTime = str(Timestamp)

				output = re.sub(' ', 'T', newTime.rstrip())
				print(instance)
				payload = {'Instance-ID':instance,'Average':Average,'SampleCount':SampleCount,'@timestamp':output,'Sum':Sum,'Unit':Unit,'Maximum':Maximum,'Minimum':Minimum,'Network':'NetworkIn'}

				#print(payload)
				
				
				response = requests.post(url, data=json.dumps(payload),headers=headers)
				
				print(response.status_code, response.reason)

def getNetWorkOutForThisMinute():
	
	for instance in existingInstances :
			print (instance)
			time.sleep(2)
			print (time.strftime("%d/%m/%Y"))
			now = datetime.datetime.now()
			date = time.strftime("%d")+time.strftime("%m")+time.strftime("%Y")
			uniqueIdentifier = now.hour+now.minute+now.second+randint(0,9999)
			uniqueIdentifier=str(uniqueIdentifier)
			print(uniqueIdentifier)
			url = "http://52.20.175.246:9200/network/NetworkUtilization/id"+uniqueIdentifier
	
			NetworkInresponce = cw.get_metric_statistics(
			300,
			datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
			datetime.datetime.utcnow(),
			'NetworkOut',
			'AWS/EC2',
			statistics = ['Maximum','Average','Sum','Minimum','SampleCount'],
			dimensions={'InstanceId':[instance]}
		)

			headers = {'Content-Type': 'application/json'}

			for item in NetworkInresponce:
		
				Average = item['Average']
				SampleCount =item['SampleCount']
				Timestamp =item['Timestamp']
				Sum =item['Sum']
				Unit =item['Unit']
				Maximum =item['Maximum']
				Minimum =item['Minimum']
		
				#print(Timestamp)
				newTime = str(Timestamp)

				output = re.sub(' ', 'T', newTime.rstrip())
				print(instance)
				payload = {'Instance-ID':instance,'Average':Average,'SampleCount':SampleCount,'@timestamp':output,'Sum':Sum,'Unit':Unit,'Maximum':Maximum,'Minimum':Minimum,'Network':'NetworkOut'}

				#print(payload)
				
				
				response = requests.post(url, data=json.dumps(payload),headers=headers)
				
				print(response.status_code, response.reason)


def main():		
	getListOfAllInstances()
	getMemoryUsageForThisMinute()
	getNetWorkInForThisMinute()
	getNetWorkOutForThisMinute()
if __name__ == '__main__':
	sys.exit(main())

	
'''
NetworkInresponce = cw.get_metric_statistics(
        300,
        datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
        datetime.datetime.utcnow(),
        'NetworkIn',
        'AWS/EC2',
         statistics = ['Maximum','Average','Sum','Minimum','SampleCount'],
        dimensions={'InstanceId':['i-9936693a']}
   )

print ("\n NetWork Input Output")
print (NetworkInresponce)
'''	