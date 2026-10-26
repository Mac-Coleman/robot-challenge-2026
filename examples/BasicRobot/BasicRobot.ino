
#if __has_include(<Cdrv8833.h>)

#include <Receiver.h>
#include <Cdrv8833.h>

Receiver receiver(Serial, "My Robot", "12345678");

void setup()
{
    receiver.begin();
}

void loop()
{
    //This will make sure that the gamepad values are as up-to-date as possible.
    //You should call this at the beginning of your loop()!
    receiver.receive();
}

#else
  #error "You need to install the Cdrv8833 library to make this code compile! Please install it with the library manager."
#endif