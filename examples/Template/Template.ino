#include <Receiver.h>

void setup()
{
    Serial.begin(115200);
    Serial.println("Starting robot.");

    //Write your setup code here!
    //For example, define output/input pins, set initial speed and positions of motors/servos, and initial values of any output pins.

    //This will start the receiver.
    //When the receiver starts, your robot will create a Wi-Fi network with the name of the robot you provided.
    //Use the robot password specified earlier to connect to the network.
    bool ret = receiver.begin();
    if (!ret) {
        log_e("There was an error configuring the Wi-Fi Access Point.");
        while (1);
    }
}

void loop()
{
    //This will make sure that the gamepad values are as up-to-date as possible.
    //You should call this at the beginning of your loop()!
    receiver.receive();

    if (!receiver.isAlive()) 
    {
        //Write your robot's "safe mode" here!
        //Define the actions that your robot should take if the connection with the controller is lost.
        //For example: set motor speeds to zero, or set servos to a specific state.

        return;
    }

    //Write the controls for your robot here!
    //The code here will only run if the connection with the controller is good.

}