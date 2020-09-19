#!/usr/bin/python


import HeaterClass
import WeatherClass
import CalendarClass
import ActionClass
import ConfigClass
import RadioClass
import SprinklerClass
import HeaterClass
import ScheduleClass
import HccDeamonClass
import InfoClass
import os
import json




class APIClass:
    methods = {}
    def __init__(self):
	pass

    def APItemperature(self,json_req):
	obj = HeaterClass.HeaterClass()
	response = obj.getCurrentTemperatureInside()
	return json.dumps(response)

    def APIversion(self,json_req):
	response = {}
	response['name'] = "Home Control Center"
	response['version'] = "1.0"
	return json.dumps(response)

    def APIgetMediaChannels(self,json_req):
        obj = RadioClass.RadioClass()
        response = obj.getPVRStations()
	return json.dumps(response)

    def APIinfo(self,json_req):
	infoObj = InfoClass.InfoClass()
	response = infoObj.getInfoData()
	return json.dumps(response)

    def APIweather(self,json_req):
        obj = WeatherClass.WeatherClass()
        response = obj.getCurrentWeather()
	return json.dumps(response)

    def APIschedule(self,json_req):
	obj = ScheduleClass.ScheduleClass()
	response = {}
	response['DirectionA'] = obj.getJsonFromKoleo('A', 0)
	response['DirectionB'] = obj.getJsonFromKoleo('B', 0)
	return json.dumps(response)

    def APIheaterCharts(self,json_req):
	obj = HeaterClass.HeaterClass()
	response = obj.getCharts()
	return json.dumps(response)

    def APIgetGardenSettings(self,json_req):
	obj = SprinklerClass.SprinklerClass()
	response = obj.getSettings()
	return json.dumps(response)

    def APIplayMediaChannel(self,json_req):
	obj = RadioClass.RadioClass()
	response = obj.playPVRChannel(param)
	return json.dumps(response)

    def APItoggleCec(self,json_req):
	obj = RadioClass.RadioClass()
	response = obj.toggleCEC()
	return json.dumps(response)

    def APIsetGardenSettings(self,json_req):
	response = {}
	config = ConfigClass.ConfigClass()
	config.saveSettingsData(2, json_req)
	response['state'] = "OK"
	return json.dumps(response)

    def APIsetHeaterSettings(self,json_req):
	response = {}
	config = ConfigClass.ConfigClass()
	config.saveSettingsData(1, json_req)
	response['state'] = "OK"
	return json.dumps(response)

    def APIsetAlarmSettings(self,json_req):
	response = {}
	config = ConfigClass.ConfigClass()
	config.saveSettingsData(0, json_req)
	response['state'] = "OK"
	return json.dumps(response)

    def APIevents(self,json_req=""):
	obj = ActionClass.ActionClass()
	events = obj.getEvents()
	response = {}
	resEvents = []
	duration = 0
	for event in events:
	    row = {}
	    row['eventType'] = event.id
	    row['eventDesc'] = event.desc
	    row['eventIcon'] = event.icon
	    row['eventDate'] = event.date
	    resEvents.append(row)
	response['events'] = resEvents
	response['eventDuration'] = duration
	return json.dumps(response)

    def APIGenericCMD(self,cmd, param=""):
	action = ActionClass.ActionClass()
	duration = action.performAction(cmd,param)
	return self.APIevents()

    def APIVolumeSet(self,json_req):
	param=json_req['volume']
	return self.APIGenericCMD(json_req['action'],param)

    def APIPlayPVR(self,json_req):
	param=json_req['channel']
	return self.APIGenericCMD(json_req['action'],param)

    def APISprinklerOn(self,json_req):
	param=json_req['id']
	return self.APIGenericCMD(json_req['action'],param)

    def APIDoor(self,json_req):
	return self.APIGenericCMD(json_req['action'])

    def APItoggleCec(self,json_req):
	return self.APIGenericCMD(json_req['action'])

    def APIGate1(self,json_req):
	return self.APIGenericCMD(json_req['action'])

    def APIGate0(self,json_req):
	return self.APIGenericCMD(json_req['action'])

    def APIGate1Perm(self,json_req):
	return self.APIGenericCMD(json_req['action'])

    def APIStop(self,json_req):
	return self.APIGenericCMD(json_req['action'])

    def APIVolumeUp(self,json_req):
	return self.APIGenericCMD(json_req['action'])

    def APIVolumeDown(self,json_req):
	return self.APIGenericCMD(json_req['action'])

    def APISprinklerOff(self,json_req):
	return self.APIGenericCMD(json_req['action'])

    def invoke(self, json_req):
	try:
	    method_name = 'API' + json_req['action']
	    method = getattr(self, method_name)
	    response = method(json_req)
	except:
	    response = {"error" : "invalid command"}
	    response = json.dumps(response)

	return response
