/*
 * Receiver.cpp - Library for controlling robots with a gamepad.
 * Created by Mac Coleman, 10/26/2026
 */


#include "Arduino.h"
#include "WiFi.h"
#include "WiFiUDP.h"
#include "Receiver.h"
#include "base64.hpp"

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
  WiFiUDP _udpSocket;
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
    log_e("Could not configure soft AP.");
    return ret;
  }
  ret = WiFi.softAPsetHostname(_robot_name);
  if (!ret) {
    log_e("Failed to set hostname.");
    return ret;
  }
  ret = _udpSocket.begin(1853); //Year Cornell was founded. I'm bad at choosing numbers.
  if (!ret) {
    log_e("No sockets available.");
  }
  return ret;
}

void Receiver::receive()
{
  size_t ret = _udpSocket.parsePacket();
  if (ret == 0) {
    log_i("No packet available.");
    return;
  }

  unsigned char readbuffer[256];
  unsigned char writebuffer[256];

  IPAddress remote = _udpSocket.remoteIP();
  int port = _udpSocket.remotePort();
  log_i("Packet received from %s:%d.", remote.toString().c_str(), port);

  size_t read_len = _udpSocket.readBytesUntil('\n', readbuffer, 255);
  readbuffer[read_len] = 0; //Add null terminator.
  log_i("Packet content: '%s'", readbuffer);

  unsigned char decoded_buffer[256];
  unsigned int decoded_length = decode_base64(readbuffer, decoded_buffer);
  if (decoded_length < 256) {
    decoded_buffer[decoded_length] = '\0';
  };
  log_i("Decoded content: '%s'",(char *) decoded_buffer);
}

bool Receiver::getAlive()
{
  return _alive;
}
