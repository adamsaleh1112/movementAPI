from flask import Flask, request, render_template, jsonify # importing flask to allow for creation of api webserver
from adafruit_motorkit import MotorKit # motorkit library to allow for motor function on robot
from time import sleep # time library allows sleep function, which pauses code to allow for rests
tank = MotorKit(0x40) # setting the variable tank to a 0x40 gpio board

app = Flask(__name__) # assigning api name


@app.route("/", methods=['GET', 'POST']) # main route that will display the html
def gui():
    return render_template('gui.html', results=request.form) # displays html file

@app.route("/move", methods=["POST"]) # route that takes in posts requests and runs movement code
def move():
    command = request.json['command'] # gets "command" varible from json script posted from gui.html
    if command == 'forward': # checking for name of command, either forward, backwards, left, right, go, or stop
       moveForward()
    elif command == 'backward':
        moveBackward()
    elif command == 'left':
        moveLeft()
    elif command == 'right':
        moveRight()
    elif command == 'go':
        go()
    elif command == 'stop':
        stop()
    else: # returns invalid if none of the above options
        return jsonify({'status': 'error', 'message': 'Invalid command'})

    return jsonify({'status': 'error', 'message': 'Invalid command'}) # function must end in a return command

def go(): # function for entire movement course
    def forward(throttle, time):
        tank.motor1.throttle = throttle * -1
        tank.motor2.throttle = throttle + 0.069
        sleep(time)
        tank.motor1.throttle = 0.0
        tank.motor2.throttle = 0.0

    def left90(throttle):
        tank.motor1.throttle = throttle * -1
        tank.motor2.throttle = (throttle + 0.069) * -1
        sleep(1.195)
        tank.motor1.throttle = 0.0
        tank.motor2.throttle = 0.0

    def reverse(throttle, time):
        tank.motor1.throttle = throttle
        tank.motor2.throttle = (throttle + 0.0665) * -1
        sleep(time)
        tank.motor1.throttle = 0.0
        tank.motor2.throttle = 0.0


    forward(0.75, 4.8)
    sleep(0.2)
    left90(0.75)
    sleep(0.2)
    forward(0.75, 3.4)
    sleep(0.2)
    reverse(0.75, 5.8)


def stop(): # stops any movement for any movement function
    tank.motor1.throttle = 0
    tank.motor2.throttle = 0

def moveForward(): # goes forwards
    tank.motor1.throttle = 0.75 * -1
    tank.motor2.throttle = 0.75 + 0.069


def moveRight(): # goes backwards
    tank.motor1.throttle = 0.75 * 1
    tank.motor2.throttle = (0.75 + 0.069) * 1


def moveLeft(): # goes left
    tank.motor1.throttle = 0.75 * -1
    tank.motor2.throttle = (0.75 + 0.069) * -1

def moveBackward(): # goes right
    tank.motor1.throttle = 0.75
    tank.motor2.throttle = (0.75 + 0.0665) * -1


if __name__ == "__main__": # runs api
    app.run(host = '0.0.0.0', port = 5000) # gives the webserver the port :5000