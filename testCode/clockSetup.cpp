#include <lime/LimeSuite.h>
#include <iostream>
#include <chrono>
#include <thread>

//Device structure, should be initialize to NULL
lms_device_t* device = NULL;

int error()
{
    if (device != NULL)
        LMS_Close(device);
    exit(-1);
}

int main(int argc, char** argv)
{
    //Find devices
    int n;
    double externalClockFreq = 0;
    lms_info_str_t list[8]; //should be large enough to hold all detected devices
    if ((n = LMS_GetDeviceList(list)) < 0) //NULL can be passed to only get number of devices
        error();

    std::cout << "Devices found: " << n << std::endl; //print number of devices
    if (n < 1)
        return -1;

    //open the first device
    if (LMS_Open(&device, list[0], NULL))
        error();
    /*
    if (LMS_SetClockFreq(device,LMS_CLOCK_EXTREF,60000000)<0)
        error(); 
    */

    if (LMS_GetClockFreq(device,LMS_CLOCK_REF,&externalClockFreq))
         error();

    std::cout << "ClockFreq:" << externalClockFreq << std::endl;
    return 0;
}
