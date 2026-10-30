# 2026 Cornell College Engineering Club Robotics Challenge

:)
Not at all finished, I'm kind of making stuff up right now.
This project allows a robot to be programmed in Arduino IDE with C++, but in the future I want to offer a CircuitPython version too so that people can use python to program their robots as well. However, Arduino C++ is really not that bad, and the hard parts have already been taken care of.

#####
# Example
There is an example of a basic Arduino robot created with this project in <./examples/BasicRobot/BasicRobot.ino>.
This is not a real robot as I do not have one available, but this would be about as complicated as you would need it to be in order to have a functioning robot controlled by a game controller.

First, you need to create a `Receiver` class. Give your robot a name, and a password. **MAKE SURE THAT THIS PASSWORD IS NOT A PASSWORD YOU USE FOR ANYTHING ELSE.** It only needs to be 8 characters long. When the robot is running, it will create a Wi-Fi network for you to connect to with the name set to your robot's name and the password set to the password you specify here.
You should call this function outside of your `void setup() {...}` function.
```cpp
Receiver receiver("My awesome robot", "123456789");
```

Within your setup function, call `Receiver::begin()` to create the Wi-Fi network and begin listening for control commands.
```cpp
bool wifi_okay = receiver.begin();
```

`Receiver::begin()` will return `true` if the Wi-Fi network was successfully created. I recommend checking the value just in case the Wi-Fi network couldn't be created for some reason.
```cpp
if (!wifi_okay) {
    log_e("The Wi-Fi network could not be created :(");
    while(1); //Loop forever
}
```

Within your `void loop() { ... }` function, call `Receiver::receive()` at the beginning of the function. This will allow you to read the latest values of the connected gamepad.

## Recommended: call `Receiver::getAlive()` to check whether your robot is healthy.
`Receiver::getAlive()` returns a boolean value to let you know if the robot has received a valid command within the last 100 milliseconds. Use this to test if your robot is still connected to your computer. You don't want your robot to spiral out of control just because the connection was lost!
Within your `void loop() { ... }` function, test the value of `Receiver::getAlive()` so you can define a "safe state" for your robot. For example: Turn off any motors, apply brakes, set servos to known positions, or turn on/off LEDs.

```cpp
//Guard clause to exit function early if the robot has not received a valid control packet in the last 100 milliseconds.
if (!receiver.getAlive()) {})
{
    log_i("The robot hasn't received any valid commands for a while.");
    log_i("Now would be a good time to set the robot to a safe state so it doesn't go out of control.");
    return; //IMPORTANT: Return here so that the loop() function exits and does not continue running the "healthy" code below.
}

//We can write the code for our robot when it is healthy right here!
```

I will probably rename `Receiver::getAlive()` to something like `Receiver::isAlive()` at some point, I don't know why that didn't occur to me earlier.

After the `Receiver::getAlive()` guard clause, we can write the "healthy" code of our robot here! This is where we should set things like motor speeds, servo positions, and lights. This is also probably where you want to read the state of the gamepad.

Now, you can safely read the values of buttons and axes on your joystick/gamepad!

For example, if we want to know whether the Y button is pressed on our gamepad, we can use `Receiver::buttonY()`. This will return a boolean value that is `true` if the Y button is being held down.

For example, say we want to turn on an LED when the Y button is pressed. Doing so is as simple as this:
```cpp
//Assuming that LED_PIN is defined elsewhere and that it has already been setup with pinMode(LED_PIN, OUTPUT)
if (receiver.buttonY())
{
    //The Y button is being pressed. We should turn on the LED!
    digitalWrite(LED_PIN, HIGH);
}
else
{
    digitalWrite(LED_PIN, LOW);
}```

Or, in even simpler terms:

```cpp
digitalWrite(LED_PIN, receiver.buttonY());
```

#####
# Controlling your robot with the client
There is a python client for controlling your robot. I have not written the setup instructions for it yet, but it requires `pygame`.
```
py -m pip install pygame
```
To use it, connect to the Wi-Fi network created by your robot with the password you specified earlier.
**Important**: Make sure that there is no other internet connection available on the device you want to control the robot from. If your laptop tries connecting to another Wi-Fi network, you will lose connection to your robot.
Then, start the controller client.
```
$ py client/Transmitter.py
```
It should display the current state of your joystick on the screen to assist you with debugging.
I haven't tested it with an actual joystick yet.

#####
# Arduino Server Library
This entire repository is an Arduino library. To install it, compress the repository into a .zip file.
Then, in Arduino IDE, go to `Sketch` -> `Include Library` -> `Add .ZIP Library`. Whenever you want to update the library, just do this process again, and agree to overwrite the library if it asks you if you want to.