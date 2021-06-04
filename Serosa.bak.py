from pyfladesk import init_gui
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

################################
##  STATE COUNTDOWN THREADER
################################

import _thread, time

def actuatorCountdown(fakeArg):
    while True:
        time.sleep(1)
        for actuator in actuators:
            if (actuator['countdown'].isnumeric()) and actuator['state'] != '0':
                print(actuator['id'])
                actuator['countdown'] = str(int(actuator['countdown']) - 1)
                if int(actuator['countdown']) <= 0:
                    actuator['countdown'] == '0'
                    actuator['state'] = '0'

_thread.start_new_thread(actuatorCountdown, ('fake',))

################################
##  SUB STATE ARRAYS
################################

import json 

# Opening JSON file...
f = open('SerosaConfig.json')

# returns JSON object as a dictionary...
data = json.load(f)

# reads in each given path of the json file...
actuators = data['actuators']
sensors = data['sensors']
commands = data['commands']

#  closing the file.
f.close()

################################
##  MACRO COMMANDS AND
##  SUPPORT FUNCTIONS
################################

def allStop():
    for actuator in actuators:
        if actuator['class'] == 'thruster':
            SetSingleActuator(actuator['id'], '0')
    return "All Stop"

def aheadFull():
    setPortStarboardThrusters(100, 0)
    return "Ahead Full"

def asternFull():
    setPortStarboardThrusters(-100, 0)
    return "Astern Full"

def setPortStarboardThrusters(portStarboardState, elseState):
    for actuator in actuators:
        if actuator['class'] == 'thruster':
            if ('port' in actuator['id']) or ('starboard' in actuator['id']):
                SetSingleActuator(actuator['id'], portStarboardState)
            else:
                SetSingleActuator(actuator['id'], elseState)

def fullDive():
    setAllVerticalThrusters('-100', '0')
    return 'Full Dive'

def fullAscent():
    setAllVerticalThrusters('100', '0')
    return 'Full Ascent'

def setAllVerticalThrusters(verticalState, elseState):
    for actuator in actuators:
        if actuator['class'] == 'thruster':
            if 'vertical' not in actuator['id']:
                SetSingleActuator(actuator['id'], elseState)
            else:
                SetSingleActuator(actuator['id'], verticalState)

def emergencyAscent():
    SetSingleActuator('globalThrottle', '100')
    print(fullAscent())
    return "Emergency Ascent!  Blowing ballast!"

def SetSingleActuator(id, state):
    for actuator in actuators:
        if actuator['id'] == id:
            actuator['state'] = state
            actuator['countdown'] = actuator['defaultCountdown']

def allLightsOff():
    setAllLightsToState('off')
    return "All Lights Off"

def allLightsOn():
    setAllLightsToState('on')
    return "All Lights On"

def setAllLightsToState(state):
        for actuator in actuators:
            if actuator['class'] == 'light':
                SetSingleActuator(actuator['id'], state)

def lowPower():
    print(setPortStarboardThrusters('0', '0'))
    print(allLightsOff())
    print(SetSingleActuator('internalFan', 'off'))
    return 'Low Power'

################################
##  ROUTING
################################

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Serosa Class ROV Web Service</h1>
<p>API for controlling the movement and recording sensor readings of any Serosa class ROV.</p>'''

@app.route('/commands/list', methods=['GET'])
def api_commandsList():
    return jsonify(commands)

@app.route('/commands', methods=['POST'])
def api_commands():
    if not request.json or not 'id' in request.json:
        return "Error: Please format request in JSON and specify an ID."
    else:
        id = request.json.get('id')

    for command in commands:
        if command['id'] == id:
            functionList = globals().copy()
            functionList.update(locals())
            for cmd in functionList:
                if cmd == command['id']:
                    execCmd = functionList.get(cmd)
                    print(execCmd())
                    break

    return jsonify(actuators)

@app.route('/actuators/list', methods=['GET'])
def api_actuatorsList():
    return jsonify(actuators)

@app.route('/actuators', methods=['POST'])
def api_setActuatorState():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if not request.json or not 'id' in request.json:
        return "Error: Please format request in JSON and specify an ID."
    else:
        id = request.json.get('id')

    # Check if an STATE was provided as part of the URL.
    # If STATE is provided, assign it to a variable.
    # If no STATE is provided, display an error in the browser.
    if not request.json or not 'state' in request.json:
        return "Error: Please format request in JSON and specify a STATE."
    else:
        state = request.json.get('state')

    for actuator in actuators:
        if actuator['id'] == id:
            actuator['state'] = state
            actuator['countdown'] = '10'
            break

    return jsonify(actuators)

@app.route('/sensors/list', methods=['GET'])
def api_sensorsList():
    return jsonify(sensors)

@app.route('/sensors', methods=['GET'])
def api_sensors():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No ID field provided. Please specify an ID."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for sensor in sensors:
        if sensor['id'] == id:
            results.append(sensor)
            break

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/sensors/all', methods=['GET'])
def api_sensorsAll():
        # Create an empty list for our results...
        results = []
        # Loop through the full sensor list...
        for sensor in sensors:
            results.append(sensor)
        # Return the results...
        return jsonify(results)

################################
##  APP.RUN()
###############################

app.run()
# if __name__ == '__main__':
#     init_gui(app)
#init_gui(app)
