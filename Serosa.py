import flask
from flask import request, jsonify
import inspect

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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

# closing the file.
f.close()

################################
##  DYNAMIC MODULE IMPORTS
################################
sensorModules = {}
actuatorModules = {}

###  https://www.oreilly.com/library/view/python-cookbook/0596001673/ch15s04.html
###  Import a named object from a module in the context of this function.
def importName(modulename, name):
    try:
        # Attempt to import the module as a "runtime" import...
        module = __import__(modulename, globals(), locals(), [name])
    except Exception as e:
        # Wuh-ohh.  Bad things happened.  Check to see if there was
        # a "ModuleNotFoundError" and handle it accordingly...
        if e.__class__.__name__ == 'ModuleNotFoundError':
            print('  -->  Could not load "' + modulename + '"!')
        else:
            # Looks like it was something else, so dump the whole
            # error to screen...
            print(e)
        return None

    #  Hand back the instantiated module that was loaded...
    return vars(module)[name]

### Dynamically loads a list of available modules...
def loadModules(jsonElementList, moduleType):
    #  Ready a return container...
    moduleDictionary = {};

    # Start looping through the list that was handed in...
    for element in jsonElementList:
        #  Grab the raw element info as a string...
        rawElement = str(element)
        #  Do some cleanup as necessary...
        elementData = json.loads(rawElement.replace("'", '"'))
        #  Grab the 'id' that corresponds to the module to load...
        elementId = str(elementData['id'])
        #  Attempt to dynamically import the module...
        modX = importName(elementId, elementId)
        #  If we got something back, then...
        if modX is not None:
            # Initialize the class (yes, you MUST hand in the 'self' reference!)...
            modX = modX.__init__(modX)
            # Set that dictionary reference to the instantiated module...
            moduleDictionary[elementId] = modX
            print('*** LOADED "' + elementId + '" ' + moduleType + '...')

    #  Return the dictionary...
    return moduleDictionary

#  Dynamically load all the sensor modules...
sensorModules = loadModules(sensors, 'sensor')

#  Dynam load all the actuator modules...
actuatorModules = loadModules(actuators, 'actuator')

################################
##  STATE COUNTDOWN THREADER
################################

import _thread, time

#  This is a work in progress, but the intent is to turn off things
#  like thrusters or lights so that power isn't drained in the event
#  tha communication with the external API controller is lost.
#  The idea is that if a particular actuator hasn't heard from the
#  external controller, it will power down so the device doesn't
#  wander off into the deep blue (in the case of thrusters) or
#  completely kill the batteries (in the case of a fan or light)...
def actuatorCountdown(fakeArg):
    while True:
        time.sleep(1)
        for actuatorItem in actuators:
            #print(str(actuatorItem['id']))
            actuator = actuatorModules.get(actuatorItem['id'])
            if actuator != None:
                actuator.decrementCountdown(actuator)
                # if actuator.decrementCountdown() != '0':
                #     ##print(actuator['id'])
                #     actuatorItem['countdown'] = str(int(actuatorItem['countdown']) - 1)
                #     if int(actuatorItem['countdown']) <= 0:
                #         actuatorItem['countdown'] == '0'

_thread.start_new_thread(actuatorCountdown, ('fake',))

################################
##  MACRO COMMANDS AND
##  SUPPORT FUNCTIONS
################################

#  Stops all thrusters...
def allStop():
    for actuator in actuators:
        if actuator['class'] == 'thruster':
            SetSingleActuator(actuator['id'], '0')
    return "All Stop"

#  All forward thrusters to full...
def aheadFull():
    setPortStarboardThrusters(100, 0)
    return "Ahead Full"

#  All reverse thrusters to full...
def asternFull():
    setPortStarboardThrusters(-100, 0)
    return "Astern Full"

#  Set all starboard thrusters to a particular value...
def setPortStarboardThrusters(portStarboardState, elseState):
    for actuator in actuators:
        if actuator['class'] == 'thruster':
            if ('port' in actuator['id']) or ('starboard' in actuator['id']):
                SetSingleActuator(actuator['id'], portStarboardState)
            else:
                SetSingleActuator(actuator['id'], elseState)

#  All vertical push thrusters should push full down...
def fullDive():
    setAllVerticalThrusters('-100', '0')
    return {'state' : 'Full Dive'}

#  All vertical push thrusters should push full up...
def fullAscent():
    setAllVerticalThrusters('100', '0')
    return {'state' : 'Full Ascent'}

#  Sets all vertical thrusters to a particular value...
def setAllVerticalThrusters(verticalState, elseState):
    for actuator in actuators:
        if actuator['class'] == 'thruster':
            if 'vertical' not in actuator['id']:
                SetSingleActuator(actuator['id'], elseState)
            else:
                SetSingleActuator(actuator['id'], verticalState)

#  Emergency forces all vertical thrusters upward, will eventually
#  cause emergency ballast release, which could be a compressed air release,
#  ditching any mechanically suspended ballast, etc...
def emergencyAscent():
    SetSingleActuator('globalThrottle', '100')
    print(fullAscent())
    return { "state" : "Emergency Ascent!  Blowing ballast!" }

#  Set the value of a single actuator as identified by 'id'...
def SetSingleActuator(id, state):
    #  Call the same setter as the API...
    print("SetSingleActuator: " + str(id))
    return setActuator(id, state)

#  Turn off all lights...
def allLightsOff():
    setAllLightsToState('off')
    return { "state" : "All Lights Off" }

#  Turn on all lights...
def allLightsOn():
    setAllLightsToState('on')
    return { "state" : "All Lights On" }

#  Sets all lights to a given state...
def setAllLightsToState(state):
        for actuator in actuators:
            if actuator['class'] == 'light':
                SetSingleActuator(actuator['id'], state)

#  Puts the sub into a low power mode by turning off all
#  lights, turning off the fan, and setting forward and
#  reverse thrusters to zero...
def lowPower():
    print(setPortStarboardThrusters('0', '0'))
    print(allLightsOff())
    print(SetSingleActuator('InternalFan', 'off'))
    return { "state" : "Low Power" }

################################
##  API ROUTING
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

    return api_actuatorsAll()

@app.route('/actuators/all', methods=['GET'])
def api_actuatorsAll():
    # Create an empty list for our results...
    results = []

    # Loop through the full sensor list...
    for actuatorName, actuator in actuatorModules.items():
        actuator = actuatorModules.get(actuatorName)
        results.append({actuatorName: {'value': actuator.getCurrentState(actuator)}})

    # Return the results...
    return jsonify(results)

@app.route('/actuators/list', methods=['GET'])
def api_actuatorsList():
    # Create an empty list for our results...
    results = []

    # Loop through the full sensor list...
    for actuatorName, actuator in actuatorModules.items():
        results.append({'id': actuatorName})

    # Return the results...
    return jsonify(results)

@app.route('/actuators', methods=['POST'])
def api_setActuatorState():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if not request.json or not 'id' in request.json:
        return {"error" : "Please format request in JSON and specify an ID."}
    else:
        id = request.json.get('id')

    # Check if an STATE was provided as part of the URL.
    # If STATE is provided, assign it to a variable.
    # If no STATE is provided, display an error in the browser.
    if not request.json or not 'state' in request.json:
        return {"error" : "Please format request in JSON and specify a STATE."}
    else:
        state = request.json.get('state')

    # Execute the set and return the results...
    return setActuator(id, state)

def setActuator(id, state):
    # Create an empty list for our results
    results = []

    # Grab the sensor reference that fits the requested ID...
    actuator = actuatorModules.get(id)

    if actuator != None:
        # Append the result state to the return object...
        results.append({id: {'state': actuator.setActuatorState(actuator, state)}})
    else:
        # Append the result state to the return object...
        results.append({id: {'state': 'actuator does not exist'}})

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/sensors/list', methods=['GET'])
def api_sensorsList():
        # Create an empty list for our results...
        results = []

        # Loop through the full sensor list...
        for sensorName, sensor in sensorModules.items():
            results.append({'id': sensorName})

        # Return the results...
        return jsonify(results)

@app.route('/sensors', methods=['GET'])
def api_sensors():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = request.args['id']
    else:
        return jsonify("Error: No ID field provided. Please specify an ID.")

    # Create an empty list for our results
    results = []

    # Grab the sensor reference that fits the requested ID...
    sensor = sensorModules.get(id)

    results.append({id: {'value': sensor.getSensorReading(sensor)}})

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/sensors/all', methods=['GET'])
def api_sensorsAll():
        # Create an empty list for our results...
        results = []

        # Loop through the full sensor list...
        for sensorName, sensor in sensorModules.items():
            sensor = sensorModules.get(sensorName)
            results.append({sensorName: {'value': sensor.getSensorReading(sensor)}})

        # Return the results...
        return jsonify(results)

################################
##  APP.RUN()
###############################

app.run()
