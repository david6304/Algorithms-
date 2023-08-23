class Bike:
    all_bikes = []
    
    def __init__(self,co,br,yr):
        self._color = co
        self._brand = br
        self._year = yr
        self._current_year = 2023
        Bike.all_bikes.append(self)
        
        
    def get_bike_age(self):
        return (self._current_year - self._year)

  

class Engine(Bike):
    def __init__(self,etech, eng_spd = 80):
        self._engine_speed = eng_spd #RPM
        self._engine_tech = etech   #Technology used in engine

    def get_engine_speed(self):
        return self._engine_speed


class Motorbike(Engine, Bike):
    def __init__(self,fl,fe,yr,br,co):
        self._fuel_level = fl #How many miles are left in tank
        self._fuel_efficiency = fe   #Capacity of engine
        self._year = yr
        self._brand = br
        self._color = co
        self._engine_speed= 80

    def get_max_speed(self):
        return self._engine_speed
    
    def __str__(self):
        return self.get_max_speed
   
    def cal_travel_time(self,distance):
        return (distance / 80)

class Bicycle(Bike):
    def __init__(self,ps,co,br,yr,):
        self.ped_speed = ps
        self._color = co
        self._brand = br
        self._year = yr
    
    def check_speed(self):
        return (self._distance / self.cal_travel_time) 
        '''potentially might need string command'''
 
    def get_pedal_speed(self):
        return self.ped_speed

    def cal_travel_time(self,distance):
        return distance / self.ped_speed
        '''t = d/s'''

class Ebike(Bicycle,Engine,Bike):
    def __init__(self,bt,co,br,yr,ps):
        self.battery_time = bt
        self._color = co
        self._brand = br
        self._year = yr
        self.ped_speed = ps

    def get_max_speed(self):
        return self.ped_speed + self.battery_time
    
    def cal_travel_time(self, distance):
      return distance / (self.ped_speed + self.battery_time)

    





'''Print statement'''


bike1=Bike(co='Black', br='Trek', yr=2012)
engine1=Engine(etech='gas')
print(engine1.get_engine_speed())

  # arguments: co - color, br - brand, yr - year, ps - pedal speed
bicycle1=Bicycle(co='Red', br='GIANT', yr=2015, ps=15)
bicycle2=Bicycle(co='Red', br='GIANT', yr=2015, ps=30)
print(bicycle1.get_pedal_speed())
print(bicycle2.get_pedal_speed())
print(bicycle1.cal_travel_time(300))

  # arguments: co - color, br - brand, yr - year, ps - pedal speed, bt - battery time 
ebike1=Ebike(co='Blue', br='Basis', yr=2018, ps=15, bt=10)
print(ebike1.get_max_speed())
print(ebike1.cal_travel_time(350))
print(ebike1.cal_travel_time(650))

  # arguments: co - color, br - brand, yr - year, fl - fuel level, fe - fuel efficiency
motorbike1= Motorbike(co='Silver', br='YAMAHA', yr=2013, fl=40, fe=12)
print(motorbike1.get_max_speed())
print(motorbike1.cal_travel_time(300))
print(motorbike1.cal_travel_time(600))

  # get the age of all bikes created
for b in Bike.all_bikes:
    print(b.get_bike_age)

















