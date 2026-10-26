#include <Receiver.h>
//#include <Cdrv8833.h>

//Create the Receiver object that your code will use to receive Robot commands.
//The first argument is the name of your robot, and the second is your robot's password.
//DO NOT set your robot's password to a password you use anywhere else.
//You should make it short.
Receiver receiver("My Robot", "12345678");

void setup()
{
    Serial.begin(9600);

    //This will start the receiver.
    //When the receiver starts, your robot will create a Wi-Fi network with the name of the robot you provided.
    //Use the robot password specified earlier to connect to the network.
    bool ret = receiver.begin();
    if (!ret) {
        Serial.print("There was an error configuring the Wi-Fi Access Point.");
        return;
    }

    Serial.print("Your robot '");
    Serial.print(receiver.getName());
    Serial.print("' will now listen on the Wi-Fi network '");
    Serial.print(receiver.getSSID());
    Serial.print("' with IP address ");
    Serial.println(receiver.getIpAddress());
    Serial.print("Connect to it with password '");
    Serial.print(receiver.getPassword());
    Serial.println("'");
}

void loop()
{
    //This will make sure that the gamepad values are as up-to-date as possible.
    //You should call this at the beginning of your loop()!
    receiver.receive();

    if (!receiver.getAlive()) 
    {
        //Write your robot's "safe mode" here!
        //Define the actions that your robot should take if the connection with the controller is lost.
        //For example: set motor speeds to zero, or set servos to a specific state.
        return;
    }

    //Write the controls for your robot here!
    //The code here will only run if the connection with the controller is good.

}