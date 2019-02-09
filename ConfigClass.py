from xml.dom import minidom
import EventClass


class ConfigClass(object):
    __xmldoc = None
    
    
    def __init__(self):
        self.iterator = 0
        if ConfigClass.__xmldoc == None:
            ConfigClass.__xmldoc = minidom.parse('data/config.xml')
            
    def initializeConfigData(self):
            # clear statuses
            itemsList = ConfigClass.__xmldoc.getElementsByTagName('status')[0].getElementsByTagName('element')
            for item in itemsList:
                    item.setAttribute("state","0")
                    item.setAttribute("desc", "No action")
            ConfigClass.__xmldoc.writexml( open('data/config.xml', 'w'))
            
    def getSwitchURL(self,name):
        ip = ConfigClass.__xmldoc.getElementsByTagName('switch')[0].getAttribute('ip')
        url = ConfigClass.__xmldoc.getElementsByTagName('switch')[0].getElementsByTagName(name)[0].getAttribute('url')
        url = "http://"+ ip + url
        return url

    def getSwitchItemDesc(self, name):
        return ConfigClass.__xmldoc.getElementsByTagName('switch')[0].getElementsByTagName(name)[0].getAttribute('desc')
        
    def getRadioURL(self,name):
        for item in ConfigClass.__xmldoc.getElementsByTagName('radio')[0].getElementsByTagName('element'):
            if item.getAttribute('name') == name:
                break
        return item.getAttribute('url');
                                
    def getRadioSettings(self):
        ip = ConfigClass.__xmldoc.getElementsByTagName('radio')[0].getAttribute('ip')
        port = ConfigClass.__xmldoc.getElementsByTagName('radio')[0].getAttribute('port')
        device = ip + ":" + port 
        return device

    def getRadioStationsName(self):
        names = []                
        for item in ConfigClass.__xmldoc.getElementsByTagName('radio')[0].getElementsByTagName('element'):
            names.append(item.getAttribute('name'))            
        return names

    def getAlarmSetting(self, name):
        return ConfigClass.__xmldoc.getElementsByTagName('alarm')[0].getElementsByTagName(name)[0].getAttribute('value')

    def getCalendarKey(self):
        return ConfigClass.__xmldoc.getElementsByTagName('calendar')[0].getElementsByTagName('key')[0].getAttribute('value')

    def getCalendarsList(self):
        names = []
        for item in ConfigClass.__xmldoc.getElementsByTagName('calendar')[0].getElementsByTagName('calendars_list')[0].getElementsByTagName('element'):
            names.append(item.getAttribute('name'))
        return names

    def getCalendarRange(self):
        return int(ConfigClass.__xmldoc.getElementsByTagName('calendar')[0].getElementsByTagName('range')[0].getAttribute('value'))

    def getCurrentWeatherReq(self):
        return ConfigClass.__xmldoc.getElementsByTagName('weather')[0].getElementsByTagName('current')[0].getAttribute('url')

    def getHourlyWeatherForecastReq(self):
        return ConfigClass.__xmldoc.getElementsByTagName('weather')[0].getElementsByTagName('hourly')[0].getAttribute('url')

    def getDailyWeatherForecastReq(self):
        return ConfigClass.__xmldoc.getElementsByTagName('weather')[0].getElementsByTagName('daily')[0].getAttribute('url')

    def getDS18B20file(self):
	return ConfigClass.__xmldoc.getElementsByTagName('ds18b20')[0].getElementsByTagName('device')[0].getAttribute('file')

    def getDS18B20offset(self):
	return ConfigClass.__xmldoc.getElementsByTagName('ds18b20')[0].getElementsByTagName('offset')[0].getAttribute('value')


    def getlocalIPmask(self):
	return ConfigClass.__xmldoc.getElementsByTagName('passwd')[0].getAttribute('localIPmask')

    def getmd5passwd(self):
	return ConfigClass.__xmldoc.getElementsByTagName('passwd')[0].getAttribute('value')

#-------------------------- Heater settings -----------------------------
    def getThermMode(self):
        return ConfigClass.__xmldoc.getElementsByTagName('heater')[0].getElementsByTagName('thermometer')[0].getAttribute('mode')

    def getFirstThermDevices(self):
        self.iterator = 0
        return ConfigClass.__xmldoc.getElementsByTagName('heater')[0].getElementsByTagName('thermometer')[0].getElementsByTagName('ds18b20')[0].getAttribute('file'), ConfigClass.__xmldoc.getElementsByTagName('heater')[0].getElementsByTagName('thermometer')[0].getElementsByTagName('ds18b20')[0].getAttribute('offset')

    def getNextThermDevices(self):
        self.iterator = self.iterator + 1
        return ConfigClass.__xmldoc.getElementsByTagName('heater')[0].getElementsByTagName('thermometer')[0].getElementsByTagName('ds18b20')[self.iterator].getAttribute('file'), ConfigClass.__xmldoc.getElementsByTagName('heater')[0].getElementsByTagName('thermometer')[0].getElementsByTagName('ds18b20')[self.iterator].getAttribute('offset')

    def getDayTemp(self):
	return ConfigClass.__xmldoc.getElementsByTagName('heater')[0].getElementsByTagName('day_temperature')[0].getAttribute('value')

    def geTempThreshold(self):
        return ConfigClass.__xmldoc.getElementsByTagName('heater')[0].getElementsByTagName('threshold')[
            0].getAttribute('value')

    def getNightTemp(self):
	return ConfigClass.__xmldoc.getElementsByTagName('heater')[0].getElementsByTagName('night_temperature')[0].getAttribute('value')

    def isDayMode(self,dayNumber, hour):
	hours = int(ConfigClass.__xmldoc.getElementsByTagName('heater')[0].getElementsByTagName('days')[0].getElementsByTagName('element')[dayNumber].getAttribute('hours'))
	if (hours & (1 << hour) != 0):
	    return True
	else:
	    return False
#-------------------------- Heater settings -----------------------------

    def getMp3Directory(self):
	return ConfigClass.__xmldoc.getElementsByTagName('radio')[0].getAttribute('mp3_directory')

    def getEvent(self, name):
        xmldoc = minidom.parse('data/config.xml')
        eventData = None
        itemsList = xmldoc.getElementsByTagName('status')[0].getElementsByTagName('element')        
        for item in itemsList:
	    if item.getAttribute('name') == name:
		break
	return EventClass.EventClass(item.getAttribute('desc'),"",item.getAttribute('name'), item.getAttribute('state'))

    def getEvents(self, id, onlyActiveEvents = True):
        xmldoc = minidom.parse('data/config.xml')
        eventsData = []
        itemsList = xmldoc.getElementsByTagName('status')[0].getElementsByTagName('element')        
        for item in itemsList:
            if (item.getAttribute('state') == "1" and onlyActiveEvents == True) or (onlyActiveEvents == False):
                event = EventClass.EventClass(item.getAttribute('desc'),"",id, item.getAttribute('state'))
                try:
                    event.setEventIcon(item.getAttribute('icon'))
                except:
                    event.setEventIcon('gate')
                eventsData.append(event)
        return eventsData


    def changeStatus(self, name, value, desc = ""):
        ret_val = "Conf_Change_ok"

        xmldoc = minidom.parse('data/config.xml')
        itemsList = xmldoc.getElementsByTagName('status')[0].getElementsByTagName('element')
        for item in itemsList:
            if item.getAttribute('name') == name:
                break


        item.setAttribute("state", value)
        if len(desc) > 0:
            item.setAttribute("desc", desc)
        xmldoc.writexml( open('data/config.xml', 'w'))

        return ret_val

