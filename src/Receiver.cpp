/*
 * Receiver.cpp - Library for controlling robots with a gamepad.
 * Created by Mac Coleman, 10/26/2026
 */


#include "Arduino.h"
#include "WiFi.h"
#include "Receiver.h"

Receiver::Receiver(Stream output, const char* robot_name, const char* robot_password)
{
  _stream = output;
  _robot_name = robot_name;
  _robot_password = robot_password;
  _leftStickX = 0.0f;
  _leftStickY = 0.0f;
  _rightStickX = 0.0f;
  _rightStickY = 0.0f;
  _buttonY = false;
  _buttonB = false;
  _buttonA = false;
  _buttonX = false;
  _bumperLeft = false;
  _bumperRight = false;
  _triggerLeft = false;
  _triggerRight = false;
  WifiServer _server(80);
}

void Receiver::begin()
{
  WiFi.softAP(_robot_name, _robot_password);
  WiFi.softAPsetHostname(_robot_name);
  IPAddress ip = Wifi.softAPIP();
  _stream.print("Your robot ");
  _stream.print(_robot_name);
  _stream.print(" will now listen on the Wi-Fi network '");
  _stream.print(_robot_name);
  _stream.print("' with IP address ");
  _stream.println(ip);
}

void Receiver::receive()
{
}
