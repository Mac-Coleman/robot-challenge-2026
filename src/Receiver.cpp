/*
 * Receiver.cpp - Library for controlling robots with a gamepad.
 * Created by Mac Coleman, 10/26/2026
 */


#include "Arduino.h"
#include "WiFi.h"
#include "WiFiUDP.h"
#include "Receiver.h"
#include "base64.hpp"

const uint16_t right_bumper_mask = 1 << 0;
const uint16_t left_bumper_mask  = 1 << 1;
const uint16_t start_mask        = 1 << 2;
const uint16_t back_mask         = 1 << 3;
const uint16_t ba_mask           = 1 << 4;
const uint16_t bb_mask           = 1 << 5;
const uint16_t bx_mask           = 1 << 6;
const uint16_t by_mask           = 1 << 7;
const uint16_t right_stick_mask  = 1 << 8;
const uint16_t left_stick_mask   = 1 << 9;

const uint8_t D_NONE      = 0;
const uint8_t D_EAST      = 1 << 0;
const uint8_t D_NORTHEAST = 1 << 1;
const uint8_t D_NORTH     = 1 << 2;
const uint8_t D_NORTHWEST = 1 << 3;
const uint8_t D_WEST      = 1 << 4;
const uint8_t D_SOUTHWEST = 1 << 5;
const uint8_t D_SOUTH     = 1 << 6;
const uint8_t D_SOUTHEAST = 1 << 7;

typedef struct __attribute__((__packed__)) {
  uint32_t control_number;
  uint16_t button_field;
  uint8_t dpad;
  float_t right_trigger;
  float_t left_trigger;
  float_t right_stick_x;
  float_t right_stick_y;
  float_t left_stick_x;
  float_t left_stick_y;
} GamepadMessage;

bool validateGamepadMessage(GamepadMessage *message);

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
  log_d("Decoded content: '%s'",(char *) decoded_buffer);

  if (decoded_length != sizeof(GamepadMessage)) {
    log_e("Decoded message has invalid size %d.", decoded_length);
    return;
  };

  GamepadMessage gamepad;
  memcpy(&gamepad, decoded_buffer, sizeof(GamepadMessage));

  //log_i("#, Gamepad left trigger: %d, %f", gamepad.control_number, gamepad.left_trigger);

  if (!validateGamepadMessage(&gamepad)) {
    log_e("Gamepad message failed validation.");
    return;
  }

  log_d("Gamepad message passed validation.");

  _leftStickX = gamepad.left_stick_x;
  _leftStickY = gamepad.left_stick_y;
  _rightStickX = gamepad.right_stick_x;
  _rightStickY = gamepad.right_stick_y;
  _triggerLeft = gamepad.left_trigger;
  _triggerRight = gamepad.right_trigger;

  _bumperRight      = (gamepad.button_field & right_bumper_mask) != 0;
  _bumperLeft       = (gamepad.button_field & left_bumper_mask) != 0;
  _buttonStart      = (gamepad.button_field & start_mask) != 0;
  _buttonBack       = (gamepad.button_field & back_mask) != 0;
  _buttonA          = (gamepad.button_field & ba_mask) != 0;
  _buttonB          = (gamepad.button_field & bb_mask) != 0;
  _buttonX          = (gamepad.button_field & bx_mask) != 0;
  _buttonY          = (gamepad.button_field & by_mask) != 0;
  _buttonStickLeft  = (gamepad.button_field & left_stick_mask) != 0;
  _buttonStickRight = (gamepad.button_field & right_stick_mask) != 0;

  log_i("a %d b %d x %d y %d", _buttonA, _buttonB, _buttonX, _buttonY);


  //log_i("lx %f ly %f rx %f ry %f", _leftStickX, _leftStickY, _rightStickX, _rightStickY);

}

bool Receiver::getAlive()
{
  return _alive;
}

bool validateGamepadMessage(GamepadMessage *message)
{
  if (isnan(message->right_trigger) or isinf(message->right_trigger) or message->right_trigger < -1.0f or message->right_trigger > 1.0f)
  {
    log_e("Message right_trigger value invalid: %f", message->right_trigger);
    return false;
  };

  if (isnan(message->left_trigger) or isinf(message->left_trigger) or message->left_trigger < -1.0f or message->left_trigger > 1.0f)
  {
    log_e("Message left_trigger value invalid: %f", message->left_trigger);
    return false;
  };

  if (isnan(message->right_stick_x) or isinf(message->right_stick_x) or message->right_stick_x < -1.0f or message->right_stick_x > 1.0f)
  {
    log_e("Message right_stick_x value invalid: %f", message->right_stick_x);
    return false;
  };

  if (isnan(message->right_stick_y) or isinf(message->right_stick_y) or message->right_stick_y < -1.0f or message->right_stick_y > 1.0f)
  {
    log_e("Message right_stick_y value invalid: %f", message->right_stick_y);
    return false;
  };

  if (isnan(message->left_stick_x) or isinf(message->left_stick_x) or message->left_stick_x < -1.0f or message->left_stick_x > 1.0f)
  {
    log_e("Message left_stick_x value invalid: %f", message->left_stick_x);
    return false;
  };

  if (isnan(message->left_stick_y) or isinf(message->left_stick_y) or message->left_stick_y < -1.0f or message->left_stick_y > 1.0f)
  {
    log_e("Message left_stick_y value invalid: %f", message->left_stick_y);
    return false;
  };

  uint16_t mask = 0b111111 << 9;
  if (mask & message->button_field != 0) {
    log_e("Message button_field bits overlap with reserved bits: %016b", message->button_field);
    return false;
  }

  if (__builtin_popcount(message->dpad) > 1) {
    log_e("Message dpad has more than a single 1 bit: %08b", message->dpad);
    return false;
  };

  return true;
};