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

void print_gpio(int gpio_val)
{
    for (int i = 0; i < 1; i++)
    {
        bool set = gpio_val&(1<<i); 
        std::cout <<set << std::endl;
    }
}

int main(int argc, char** argv)
{
    //Find devices
    int n;
    lms_info_str_t list[8]; //should be large enough to hold all detected device

    if ((n = LMS_GetDeviceList(list)) < 0) 
        error();

    std::cout << "Devices found: " << n << std::endl; //print number of devices
    if (n < 1)
        return -1;

    //open the first device
    if (LMS_Open(&device, list[0], NULL))
        error();

    //change GPIO pins direction using LMS_GPIODirWrite()
    std::cout << std::endl << "Set GPIO Pins to Input..."<< std::endl;
    uint8_t gpio_dir = 0x00; 
    if (LMS_GPIODirWrite(device, &gpio_dir, 1)!=0) 
        error();
    std::cout << std::endl << "DONE"<< std::endl;

    uint8_t gpio_val = 0;
    while(1){
        if(LMS_GPIORead(device, &gpio_val, 1)!=0)
            error();
        print_gpio(gpio_val);
    }   
    return 0;
}

