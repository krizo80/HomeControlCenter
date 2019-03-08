from xml.dom import minidom
import ActionThread
import EventClass
import ConfigClass
import CalendarClass
import RadioClass
import SprinklerClass
import HeaterClass



class ActionClass(object):
    ActionEventAll       = 1 << 0
    ActionEventGeneric   = 1 << 1
    ActionEventCalendar  = 1 << 2
    ActionEventRadio     = 1 << 3

    def __init__(self):
        self.__config = ConfigClass.ConfigClass()
        self.__actionEvents = []

    def __isEventEnable(self, events, eventID):
        if (events & eventID <> 0) or (events & ActionClass.ActionEventAll <> 0):
            return True
        else:
            return False

    def __updateEvents(self, events, filters):
        if (filters & ActionClass.ActionEventAll <> 0):
            self.__actionEvents = events
        elif len(events) > 0:
            # find events in global event list and update them, if not exist then add
            for item in events:                
                exist = False
                for global_event_item in self.__actionEvents:
                    if global_event_item.id == item.id:                                                
                        self.__actionEvents.remove(global_event_item)                        
                        break                    
                                                            
                self.__actionEvents.insert(0, item)
        else:
            for global_event_item in self.__actionEvents:
                if global_event_item.id & filters <> 0:
                    self.__actionEvents.remove(global_event_item)
                    

    def actionOnDoor(self, param = ""):
        url = self.__config.getSwitchURL("door")
        threadTask = ActionThread.ActionThread()

        threadTask.addTask("set","door", "Otwieranie furtki")
        threadTask.addTask("request",url)
        threadTask.addTask("delay",5)
        threadTask.addTask("clear","door", "No action")
        threadTask.start()
        threadTask.suspend()

    def actionOnGate0(self, param = ""):
        url = self.__config.getSwitchURL("garage")
        threadTask = ActionThread.ActionThread()

        threadTask.addTask("set","garage", "Otwieranie/Zamykanie bramy garazowej")
        threadTask.addTask("request",url)
        threadTask.addTask("delay",20)
        threadTask.addTask("clear","garage", "No action")
        threadTask.start()
        threadTask.suspend()
        
    def actionOnGate1(self, param = ""):
        url = self.__config.getSwitchURL("mainGate")
        threadTask = ActionThread.ActionThread()

        threadTask.addTask("set","mainGate", "Otwieranie bramy wjazdowej")
        threadTask.addTask("request",url)
        threadTask.addTask("delay",20)
        threadTask.addTask("clear","mainGate", "No action")
        threadTask.start()
        threadTask.suspend()

    def actionOnGate1Perm(self, param = ""):
        url = self.__config.getSwitchURL("mainGate")
        threadTask = ActionThread.ActionThread()

        threadTask.addTask("set","mainGate", "Otwieranie bramy wjazdowej")
        threadTask.addTask("request",url)
        threadTask.addTask("delay",25)
        threadTask.addTask("request",url)
        threadTask.addTask("delay",2)
        threadTask.addTask("request",url)
        threadTask.addTask("clear","mainGate", "No action")
        threadTask.start()
	threadTask.suspend()

                
    def actionOnSprinklerOn(self, param = ""):
	sprinkler = SprinklerClass.SprinklerClass()
	sprinkler.setSprinklerOn(param)

    def actionOnSprinklerOff(self, param = ""):
	sprinkler = SprinklerClass.SprinklerClass()
	sprinkler.setSprinklerOff()

    def actionOnPlay(self, param = ""):
        radio = RadioClass.RadioClass()
        radio.getRadioPlayRequest(param)

    def actionOnPlayMp3(self, param = ""):
        player = RadioClass.RadioClass()
        player.playMp3File(param)

    def actionOnStop(self, param = ""):
        radio = RadioClass.RadioClass()
        radio.getRadioStopRequest()

    def actionOnVolumeUp(self, param = ""):
        radio = RadioClass.RadioClass()
        radio.getRadioVolumeUpRequest() 

    def actionOnVolumeDown(self, param = ""):
        radio = RadioClass.RadioClass()
        radio.getRadioVolumeDownRequest() 

    def actionOnGetActiveEvents(self, param = ""):
        # perform on timer tick from browser - currently do nothing
	pass

#---------------------------------------------------------------------------------------------------------------
    def __getSwitchEvents(self):
	try:
	    status = -1
	    config = ConfigClass.ConfigClass()
	    status_url = config.getSwitchURL("Status")
	    threadStatus = ActionThread.ActionThread()
	    threadStatus.addTask("request",status_url)
    	    threadStatus.addTask("delay",1)
	    threadStatus.addTask("notify")
	    threadStatus.start()
	    threadStatus.suspend()
	    status = int(threadStatus.getResponse())
	except:
	    # report error
	    status = -1
	self.__config.updateEvents(status)

    def getEventsData(self,actionName="", param = "", filters = ActionEventAll, returnOnlyRequestedEvents = False, returnOnlyActivateEvents = True):
        events = []

        calendarEvents = CalendarClass.CalendarClass()
        radioEvents = RadioClass.RadioClass()

        if actionName <> "":
            method_name = 'actionOn' + actionName
            method = getattr(self, method_name)
            method(param)

        if self.__isEventEnable(filters, ActionClass.ActionEventGeneric) == True:
	    self.__getSwitchEvents()
            events = events + self.__config.getEvents(self.ActionEventGeneric, returnOnlyActivateEvents)

        if self.__isEventEnable(filters, ActionClass.ActionEventRadio) == True:
            events = events + radioEvents.getEventsData(self.ActionEventRadio)

        if self.__isEventEnable(filters, ActionClass.ActionEventCalendar) == True:
            events = events + calendarEvents.getEventsData(self.ActionEventCalendar)

        self.__updateEvents(events, filters)

        if returnOnlyRequestedEvents == True:
            return events
        else:
            return self.__actionEvents


