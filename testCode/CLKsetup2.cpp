#include <cstdlib>
#include "lime/lms7_device.h"
#include "lime/LimeSuite.h"
#include "lime/ADF4002.h"
#include <iostream>
#include "math.h"
#include <thread>
#include <memory.h>
using namespace std;
using namespace lime;

#define N_RADIOS 1

static lime::ADF4002 *adf4002;
static float_type fref, fvco;
static lms_device_t* m_lms_device;
static int m_n_devices;

static int error()
{
    //print last error message
    cout << "ERROR:" << LMS_GetLastErrorMessage();
    if (m_lms_device != NULL)
        LMS_Close(m_lms_device);
    exit(-1);
}

int main( void )
{
    fref = 10.0;
    fvco = 30.72;
    unsigned char adf4002_spi[12];

    int rCount, nCounter;
    int result;

    lms_info_str_t list[N_RADIOS]; //should be large enough to hold all detected devices

    memset(&adf4002_spi, 0, 12);

    try {
      adf4002 = nullptr;
      adf4002 = new lime::ADF4002();
    } catch (...) {
      adf4002 = nullptr;
    }

    if ( adf4002 == nullptr ) {
      cerr << "Unable to set up ADF4002 data structs." << endl;
      return -1;
    }

    cout << "Setting ADF4002 defaults" << endl;
    adf4002->SetDefaults();
    adf4002->GetConfig(adf4002_spi);

    m_lms_device = NULL;

    if ((m_n_devices = LMS_GetDeviceList(list)) < 0) error();//NULL can be passed to only get number of devices

    cout << "Devices found: " << m_n_devices << endl; //print number of devices

    if (m_n_devices < 1) {
      cout << "No device found" << endl;
      return -1;
    }

    //open the first device
    if (LMS_Open(&m_lms_device, list[0], NULL)) {
      if ( m_lms_device != NULL )
        LMS_Close(m_lms_device);
      cout << "Unable to open zeroth device" << endl;
      return -1;
    }

    cout << "Device opened. Initializing..." << endl;

    //Initialize device with default configuration
    if (LMS_Init(m_lms_device) != 0) {
      LMS_Close(m_lms_device);;
      cout << "Unable to initialize device" << endl;
      return -2;
    }

    if (1 == LMS_IsOpen(m_lms_device,0)) {

      adf4002->SetFrefFvco(fref, fvco, rCount, nCounter);
      adf4002->GetConfig(adf4002_spi);

      vector<uint32_t> bytearray;

      for ( int n = 0; n < 12 ; n+= 3 )
        bytearray.push_back((uint32_t)adf4002_spi[n] << 16 |
            (uint32_t)adf4002_spi[n+1] << 8 |
            adf4002_spi[n+2]);

      cout << "Setting ( Fref, Fvco ) to ( " << fref << ", " << fvco << " )" << endl;

      auto conn = ((LMS7_Device *)m_lms_device)->GetConnection();

      result = conn->TransactSPI(conn->GetDeviceInfo().addrADF4002,
          bytearray.data(),
          nullptr,
          4 );

      if ( result != 0 )
        cout << "Unable to set external clock frequency" << endl;
      else
        cout << "Fref set" << endl;
    }

    LMS_Close(m_lms_device);

    if ( !(adf4002 == nullptr) ) {
      delete adf4002;
      adf4002 = nullptr;
    }

    return 0;
}