# Code API Notes
## Useful Documentation Links
**Overall Documentation**  
https://docs.myriadrf.org/LMS_API/index.html  
http://pothosware.github.io/SoapySDR/doxygen/latest/annotated.html  
**Code Examples**  
LimeSuite  
https://github.com/myriadrf/LimeSuite/tree/master/src/examples  
SoapySDR  
https://github.com/pothosware/SoapySDR/wiki/C_API_Example  
https://github.com/pothosware/SoapySDR/wiki/Cpp_API_Example  
https://github.com/pothosware/SoapySDR/wiki/PythonSupport  


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
### Python - From Example Code  
Import statements
```Python
import SoapySDR
from SoapySDR import *
import numpy
import sys
```
Basic device set up Python commands  
```Python
#enumerate devices
results = SoapySDR.Device.enumerate()
for result in results: 
	print(result)

#create device instance
#args can be user defined or from the enumeration result
args = dict(driver="lime")
sdr = SoapySDR.Device(args)
```
