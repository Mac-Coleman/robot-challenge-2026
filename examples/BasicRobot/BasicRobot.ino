/* +--------------------------------------------------------------+
 * |                 Basic Robot Example Code                     |
 * |                                                              |
 * |   This example is a basic robot, named "The Flippinator".    |
 * |    It has two motors controlled by a DRV8833-based motor     |
 * |  controller, a servo for flipping its opponents, and an LED  |
 * | to make it easy to tell when the robot is on and connected.  |
 * |                                                              |
 * | The robot's left and right motors are controlled by the left |
 * |   and right joysticks, and the flipper is raised when the A  |
 * |                     button is held.                          |
 * +--------------------------------------------------------------+
 */

#include <Receiver.h>

//Install these from the library manager:
#include <Cdrv8833.h>
#include <Servo.h>

#define MOTOR_L_PIN_1 2
#define MOTOR_L_PIN_2 3
#define MOTOR_L_PWM_CHANNEL 0
#define MOTOR_L_REVERSE false

#define MOTOR_R_PIN_1 4
#define MOTOR_R_PIN_1 5
#define MOTOR_R_PWM_CHANNEL 1
#define MOTOR_R_REVERSE true

#define SERVO_PIN 6
#define LED_PIN 7

//Create the Receiver object that your code will use to receive Robot commands.
//The first argument is the name of your robot, and the second is your robot's password.
//DO NOT set your robot's password to a password you use anywhere else.
//You should make it short.
//Here, we are making a robot called "The Flippinator"
Receiver receiver("The Flippinator", "0987654321");

Servo flipper;
Cdrv8833 motorLeft(MOTOR_L_PIN_1, MOTOR_L_PIN_2, MOTOR_L_PWM_CHANNEL, MOTOR_L_REVERSE);
Cdrv8833 motorRight(MOTOR_R_PIN_1, MOTOR_R_PIN_2, MOTOR_R_PWM_CHANNEL, MOTOR_R_REVERSE);

void setup()
{
    Serial.begin(115200);
    Serial.println("Starting robot.");

    //This will start the receiver.
    //When the receiver starts, your robot will create a Wi-Fi network with the name of the robot you provided.
    //Use the robot password specified earlier to connect to the network.
    bool ret = receiver.begin();
    if (!ret) {
        log_e("There was an error configuring the Wi-Fi Access Point.");
        while (1);
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

    pinMode(LED_PIN, OUTPUT); //Setup the LED pin to be used as an output.
    digitalWrite(LED_PIN, LOW); //Turn off the LED.

    // Make sure both motors are not turning/
    motorLeft.stop();
    motorRight.stop();

    // set the motors to slow decay (high torque) mode.
    motorLeft.setDecayMode(drv8833DecaySlow);
    motorRight.setDecayMode(drv8833Decayslow);

    // Set up the flipper servo to the correct pin, and set the angle to zero degrees.
    flipper.attach(SERVO_PIN);
    flipper.write(0);
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
        motorLeft.stop();
        motorRight.stop();

        //Lower the flipper.
        flipper.write(0);

        //Makes the LED flash twice a second.
        digitalWrite(LED_PIN, (millis() % 250) % 2 == 0);

        return;
    }

    //Write the controls for your robot here!
    //The code here will only run if the connection with the controller is good.

    //Turn on the LED to a steady brightness so we know the robot is connected.
    digitalWrite(LED_PIN, HIGH);
    
    //Set the speeds of each motor to be based on the position of the left and right joysticks.
    //The motors take an integer speed between -100 (full speed backwards) and 100 (full speed forwards).
    motorLeft.move((int) (100.0f * receiver.leftstickY()));
    motorRight.move((int) (100.0f * receiver.rightStickY()));

    //Set the flipper angle. It should be raised (90 degrees) when the A button is pressed.
    //Otherwise, it should be zero.
    flipper.write(receiver.buttonA() ? 90 : 0);
}