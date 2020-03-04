# Code API Notes
## Useful Documentation Links
**Overall Documentation**  
https://docs.myriadrf.org/LMS_API/index.html  
http://pothosware.github.io/SoapySDR/doxygen/latest/annotated.html
LimeSuite  
https://github.com/myriadrf/LimeSuite/tree/master/src/examples  
SoapySDR  
https://github.com/pothosware/SoapySDR/wiki/C_API_Example  
https://github.com/pothosware/SoapySDR/wiki/Cpp_API_Example  
https://github.com/pothosware/SoapySDR/wiki/PythonSupport  

---

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
---
## Async and Await  
Data structure to use instead of a list. Allows us to break up the work, we can wait until it has something. 
```Python
data = asyncio.Queue()
```
*put is an async method to add an element to an asyncio.Queue.* This might have to wait before it can perform its operation, when it is ready work will resume from here.  
```Python
await data.put(work) 
```
What to do instead of the standard sleep command? Use this instead:
```Python
await asyncio.sleep(.5)
```
Get an item from an async queue
```Python
item = await data.get()
```
Grouping Tasks with asyncio.gather
```Python
loop: AbstractEventLoop = asyncio.get_event_loop()

task = asyncio.gather(
	generate_data(10, data),
	generate_data(10, data),
	process_data(20, data)
)

loop.run_until_complete(task)
```
### anatomy of an async method
```Python
async def process_data(num: int, data: asyncio.Queue):
	processed = 0

	while processed < num
		item = await data.get()
		#work with item
```

**uvloop** - uvloop is an ultra fast implementation of the asyncio event loop on top of libuv
