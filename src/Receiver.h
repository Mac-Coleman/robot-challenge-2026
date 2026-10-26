#ifndef Receiver_h
#define Receiver_h

#include "Arduino.h"
#include "WiFi.h"

class Receiver
{
  public:
    Receiver(const char* robot_name, const char* robot_password);
    bool begin();
    void receive();
    float leftStickX();
    float leftStickY();
    float rightStickX();
    float rightStickY();
    bool buttonY();
    bool buttonB();
    bool buttonA();
    bool buttonX();
    bool triggerLeft();
    bool triggerRight();
    bool bumperLeft();
    bool bumperRight();
    const char* getName();
    const char* getPassword();
    IPAddress getIpAddress();
    String getSSID();
    bool getAlive();
  private:
    void _acknowledge(int message);
    const char* _robot_name;
    const char* _robot_password;
    WiFiServer _server;
    float _leftStickX;
    float _leftStickY;
    float _rightStickX;
    float _rightStickY;
    bool _buttonY;
    bool _buttonB;
    bool _buttonA;
    bool _buttonX;
    bool _triggerLeft;
    bool _triggerRight;
    bool _bumperLeft;
    bool _bumperRight;
    bool _alive;
    unsigned long _lastReceive;
};

#endif
