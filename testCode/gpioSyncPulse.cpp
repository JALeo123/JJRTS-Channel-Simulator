#include <lime/LimeSuite.h>
#include <iostream>
#include <chrono>
#include <thread>
#include <stdlib.h>

//Device structure, should be initialize to NULL
lms_device_t* device = NULL;

int error()
{
    if (device != NULL)
        LMS_Close(device);
    exit(-1);
}

void print_gpio(int gpio_val)
{
    for (int i =0; i < 8; i++)
    {
        bool set = gpio_val&(1<<i); 
        std::cout << "GPIO" << i <<": " << (set ? "High" : "Low") << std::endl;
    }
}

int main(int argc, char** argv)
{
    //Find devices
    int n;
    lms_info_str_t list[8]; //should be large enough to hold all detected devices
    if ((n = LMS_GetDeviceList(list)) < 0) //NULL can be passed to only get number of devices
        error();

    std::cout << "Devices found: " << n << std::endl; //print number of devices
    if (n < 1)
        return -1;

    //open the first device
    if (LMS_Open(&device, list[0], NULL))
        error();

    //Read current GPIO pins state using LMS_GPIORead()
    std::cout << "Read current GPIO state:" << std::endl;
    uint8_t gpio_val = 0;
    //while(1){
    	if (LMS_GPIORead(device, &gpio_val, 1)!=0) //1 byte buffer is enough to read 8 GPIO pins on LimeSDR-USB
        	error();
    		print_gpio(gpio_val);
   //	sleep(250);
   
   // }
    return 0;
}
