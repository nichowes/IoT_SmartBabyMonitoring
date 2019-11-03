class Car:
    def __init__(self, speed=0):
        self.speed = speed
        self.odometer = 0
        self. time = 0

    def say_state(self):
        print("I'm going {} kph!".format(self.speed))

    def accelarate(self):
        self.speed+=5

    def brake(self):
        self.speed-=5

    def step(self):
        self.odometer += self.speed
        self.time+=1

    def avg_speed(self):
        if (self.time != 0):
            return self.odometer/self.time
        else:
            pass

if __name__ == '__main__':

    my_car = Car()
    print("I'm a Car!")

    while True:
        action = input("What should I do? [A]ccelerate, [B]reak, "
                       "show [O]dometer, show average [S]peed").upper()

        if (action not in "ABOS" or len(action)!=1):
            print("I don't know how to do that")
            continue
        if(action == 'A'):
            my_car.accelarate()
        elif(action=='B'):
            my_car.brake()
        elif(action=='S'):
            print("The average speed of the car is {} kph".format(my_car.avg_speed()))
        elif(action=='O'):
            print("The car has driven {} km.".format(my_car.odometer))

        my_car.step()
        my_car.say_state()