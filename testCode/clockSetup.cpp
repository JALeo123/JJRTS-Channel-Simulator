#include <lime/LimeSuite.h>
#include <iostream>
#include <chrono>
#include <thread>
#include <Si5351C/Si5351C.h>
//#include <ADF4002.h>

using namespace std;
using namespace lime;
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
    //Clock Setup
    /*
    Generate a 60MHz clock with Si5351C
    */
    // Create a new clock generator
    auto port = device->GetConnection();
    std::shared_ptr<Si5351C> si5351module(new Si5351C());
    si5351module->Initialize(port);
    // Set PLL 0 to phase lock at 60 MHz to CLKIN
    si5351module->SetPLL(0, 60000000, 1);

    Si5351C::Status status = si5351module->ConfigureClocks();
    if (status != Si5351C::SUCCESS)
    {
        lime::warning("Failed to configure Si5351C");
        return;
    }
    status = si5351module->UploadConfiguration();
    if (status != Si5351C::SUCCESS)
        lime::warning("Failed to upload Si5351C configuration");

    //Set the ADF4002 PLL to 60MHz

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

    


    std::cout << "ClockFreq:" << externalClockFreq << std::endl;
    return 0;
}
