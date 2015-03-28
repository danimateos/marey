import GeoBases
import datetime as dt

airports = GeoBases.GeoBase('airports', verbose = False)
dtFormat = "%Y-%m-%d %H:%M"

class Stop:
    def __init__(self, carrier, number, stopType, port, dateTime):
        self.carrier = carrier
        self.number = number
        self.stopType = stopType
        self.port = port
        self.dateTime = dateTime

    @classmethod
    def fromLine(cls, string):
        return cls(*string.split('^'))


class FlightOption:
    def __init__(self, price, *stops):
        self.price = price
        self.stops = stops
        self.totalDistanceCovered = sum([airports.distance(x.port, y.port) 
                                         for x, y in zip(self.stops, self.stops[1:])])

def stopsToPoints(stops):
    covered = 0.0
    time = dt.datetime.strptime(stops[0].dateTime, dtFormat)
    port = stops[0].port    
    res = [(port, covered, time)]
    
    for i in range(1, len(stops)):
        stop = stops[i]
        time = dt.datetime.strptime(stop.dateTime, dtFormat)
        covered += airports.distance(stops[i-1].port, stops[i].port)
        res.append((stop.port, covered, time))

    return res
