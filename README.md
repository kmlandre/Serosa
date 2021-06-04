# Serosa
<b> Submerge, Explore, Research, Observe, Sample, Ascend </b>
#
<b> RaspberryPi based REST interface for aquatic research vehicles and data stations in Python. </b>
#

Works on a "duck typing" model and commands are sent to the REST Api, where components abstracted behind one of two categories:
  * sensors
  * actuators.

Sensors are things that get information about the outside world, like thermometers, pressure sensors, light detectors, pH sensors, etc.

Actuators are things that actually do things in the outside world.  Examples are thrusters and motors, lights, relay-controlled devices, robotic claws and grippers, etc.

Additionally, there is a "command" component.  A command component is a module that either functions in one of two ways:
  * a "macro" - sends multiple commands to actuators or thrusters, such as a "full stop" command to shut down all thrusters, or rapidly take multiple readings from a sensor
  * internal action - typically a hard-coded function which may reset a software timer, reboot the operating system, change configurations, etc
