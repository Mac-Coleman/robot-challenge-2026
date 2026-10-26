/*
 * Receiver.cpp - Library for controlling robots with a gamepad.
 * Created by Mac Coleman, 10/26/2026
 */


#include "Arduino.h"
#include "WiFi.h"
#include "Receiver.h"

Receiver::Receiver(const char* robot_name, const char* robot_password)
{
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
  _alive = false;
  _lastReceive = 0;
  WiFiServer _server(80);
}

const char* Receiver::getName()
{
  return _robot_name;
}

const char* Receiver::getPassword()
{
  return _robot_password;
}

String Receiver::getSSID()
{
  return WiFi.softAPSSID();
}

IPAddress Receiver::getIpAddress()
{
  return WiFi.softAPIP();
}

bool Receiver::begin()
{
  bool ret = WiFi.softAP(_robot_name, _robot_password);
  if (!ret) {
    return ret;
  }
  ret = WiFi.softAPsetHostname(_robot_name);
  return ret;
}

void Receiver::receive()
{
}

bool Receiver::getAlive()
{
  return _alive;
}
