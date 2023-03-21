import wikipedia
import requests
import json
import datetime

from apscheduler.schedulers.background import BackgroundScheduler

returnData = []

months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
        31]


class Event:
    def __init__(self, eventName, date, subtitle, title, link):
        self.eventName = eventName
        self.date = date
        self.subtitle = subtitle;
        self.title = title
        self.link = link


class AllEvents:
    def __init__(self, eventName, date, subtitle, title, link, text, image):
        self.eventName = eventName
        self.date = date
        self.subtitle = subtitle;
        self.title = title
        self.link = link
        self.text = text
        self.image = image

    # a method to convert AllEvents object to json
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def getDataFromApi():
    print("New Data's are taking..")
    filtered = []
    events = []
    for x in months:
        for y in days:
            z = requests.get('https://history.muffinlabs.com/date/' + str(x) + "/" + str(y))
            if z.status_code == 200:
                try:
                    eventsAll = list(filter(lambda itemEvent: int(itemEvent['year']) >= 2020,
                                            json.loads(z.content)["data"]['Events']))
                    birthsAll = list(filter(lambda itemEvent: int(itemEvent['year']) >= 2020,
                                            json.loads(z.content)["data"]['Births']))
                    deathsAll = list(filter(lambda itemEvent: int(itemEvent['year']) >= 2020,
                                            json.loads(z.content)["data"]['Deaths']))
                    if len(eventsAll) > 0:
                        for event in eventsAll:
                            try:
                                Item = Event("Event", str(y) + "/" + str(x) + "/" + event['year'], event['text'],
                                             event['links'][0]['title'], event['links'][0]['link'])
                                filtered.append(Item)
                            except:
                                pass

                    if len(birthsAll) > 0:
                        for birth in birthsAll:
                            try:
                                Item = Event("Birth", str(y) + "/" + str(x) + "/" + birth['year'], birth['text'],
                                             birth['links'][0]['title'], birth['links'][0]['link'])
                                filtered.append(Item)
                            except:
                                pass

                    if len(deathsAll) > 0:
                        for death in deathsAll:
                            try:
                                Item = Event("Death", str(y) + "/" + str(x) + "/" + death['year'], death['text'],
                                             death['links'][0]['title'], death['links'][0]['link'])
                                filtered.append(Item)
                            except:
                                pass
                except:
                    pass
            else:
                print("Api Error - Status Code:", z.status_code)
    # Each event is calling with its title name again and taking the summary and image information
    for eventFiltered in filtered:
        try:
            ny = wikipedia.page(eventFiltered.title, auto_suggest=False)
            summary = str(ny.summary)
            # filtered .jpg images bcz svg images cannot appear in web and taken only one image
            if len(list(filter(lambda line: '.jpg' in line, ny.images))) > 0:
                image = list(filter(lambda line: '.jpg' in line, ny.images))[0]
            else:
                image = "No Image Found As Jpg Format"

            ItemAll = AllEvents(eventFiltered.eventName, eventFiltered.date, eventFiltered.subtitle,
                                eventFiltered.title,
                                eventFiltered.link,
                                summary, image)
            events.append(ItemAll)
        except Exception as e:
            print(str(e))
    if len(events) > 0:
        returnData.clear()
        for i in events.copy():
            temp = AllEvents(i.eventName, i.date, i.subtitle, i.title, i.link, i.text, i.image)
            returnData.append(temp)
        returnData.sort(key=lambda element: datetime.datetime.strptime(element.date, "%d/%m/%Y"))
        print("returnData has been filled.")


# The scheduled method works once a day at 23:59
scheduler = BackgroundScheduler()
scheduler.add_job(func=getDataFromApi, trigger='cron', hour='23', minute='59')
scheduler.start()
