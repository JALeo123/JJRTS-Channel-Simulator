# Code API Notes
## Lime Suite API - LMS API
Basic include statements needed
```C++
#include "lime/LimeSuite.h"
#include <iostream>
#include <chrono>
#ifdef USE_GNU_PLOT
#include "gnuPlotPipe.h"
#endif

using namespace std;
```
Initilize data structure for the Lime SDR Device
```C++
//Device structure, should be initialize to NULL
lms_device_t* device = NULL;
```
## SoapySDR API 
