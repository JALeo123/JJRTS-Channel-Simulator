#include <lime/LimeSuite.h>
//#include "Logger.h"
#include <iostream>
#include <chrono>
#include <thread>
#include <Si5351C/Si5351C.h>
#include <LMS7_device.h>
//#include <ADF4002.h>

using namespace std;
using namespace lime;
//Device structure, should be initialize to NULL
//lms_device_t* device = NULL;
lime::LMS7_Device* device;
/*
int error()
{
    if (device != NULL)
        LMS_Close(device);
    exit(-1);
}
*/
int main(int argc, char** argv)
{
    /*
    int n;
   
    if ((n = LMS_GetDeviceList(NULL)) < 0)//Pass NULL to only obtain number of devices
        error();
    cout << "Devices found: " << n << endl;
    if (n < 1)
        return -1;

    lms_info_str_t* list = new lms_info_str_t[n];   //allocate device list

    if (LMS_GetDeviceList(list) < 0)                //Populate device list
        error();

    for (int i = 0; i < n; i++)                     //print device list
        cout << i << ": " << list[i] << endl;
    cout << endl;

    //Open the first device
    if (LMS_Open(&device, list[0], NULL))
        error();

    delete [] list;     
    */

    //Clock Setup
    /*
    Generate a 60MHz clock with Si5351C
    */
    // Create a new clock generator
    
    auto port = device->GetConnection();
    std::cout << "Board connected " << std::endl;
    std::shared_ptr<Si5351C> si5351module(new Si5351C());
    std::cout << "Si5351 initialized" << std::endl;
    si5351module->Initialize(0);    
    // Set PLL 0 to phase lock at 60 MHz to CLKIN
    si5351module->SetPLL(0, 60000000, 1);
    si5351module->SetPLL(1, 60000000, 1);
    Si5351C::Status status = si5351module->ConfigureClocks();
    if (status != Si5351C::SUCCESS)
    {
        lime::warning("Failed to configure Si5351C");
        return 0;
    }
    status = si5351module->UploadConfiguration();
    if (status != Si5351C::SUCCESS)
        lime::warning("Failed to upload Si5351C configuration");

    //Set the ADF4002 PLL to 60MHz

    //Find devices
   


    


    //std::cout << "ClockFreq:" << externalClockFreq << std::endl;
    return 0;
}
