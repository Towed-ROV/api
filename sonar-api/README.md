# Sonar API

Various approaches could be used to install the ZMQ depenceny.
In this guide, we will build and static link ZeroMQ on a Windows PC.

As the Sonar API uses x86 architecture, we need to install the ZMQ library in the same format.

## Requirements
- Git
- Visual Studio 2019

## Installation

##### 1. Build Vcpkg ( https://github.com/Microsoft/vcpkg )
##### 2. Use vcpkg to build ZeroMQ ( vcpkg install zeromq:x86-windows-static )
##### 3. Build an executable that statically links ZeroMQ
.   
.   
.
### 1. Download [Vcpkg]()

Find a suitable folder on your PC for storing Vcpkg (the Vcpkg stores C++ libraries), then
```bash
cd <folder>
git clone https://github.com/Microsoft/vcpkg
cd vcpkg
bootstrap-vcpkg.bat
```
now ... <folder>\vcpkg\vcpkg.exe should exist.


### 2. Use vcpkg to build ZeroMQ

```bash
.\vcpkg install zeromq:x86-windows-static
```

### 3. Build an executable that statically links ZeroMQ
Inside a empty C++ project, create a .cpp file paste
```cpp
#include <zmq.h>
#include <iostream>
 
int main()
{
	int major = 0;
	int minor = 0;
	int patch = 0;
	zmq_version( &major, &minor, &patch );
	std::wcout << "Current 0MQ version is " << major << '.' << minor << '.' << patch << '\n';
}
```
This won't run yet, so lets configure a few settings first. 

1. Change the Solution Platform to x86:
2. In project properties \ Configuration Properties \ Advanced change the Character Set to "Use Multi-Byte Character Set".
2. Inside project properties, change the Configuration to “All Configurations“, then configuration properties / C/C++ / General, and then add the following include folder to “Additional Include Directories“:
...\folder>\vcpkg\packages\zeromq_x86-windows-static\include
3. Next, for “All Configurations“, select configuration properties / C/C++ / Preprocessor, and then add the following preprocessor definition to “Preprocessor Definitions“:
ZMQ_STATIC
4. Change the configuration to “Debug“, select configuration properties / C/C++ / Code Generation, and then change the “Runtime Library” to “Multi-threaded Debug (/MTd)“:
5. Change the configuration to “Release“, select configuration properties / C/C++ / Code Generation, and then change the “Runtime Library” to “Multi-threaded (/MT)“:
6. Switch the configuration back to “Debug“, select configuration properties / Linker / Input, and then add the following entries to “Additional Dependencies“:
...\<folder>\vcpkg\packages\zeromq_x86-windows-static\debug\lib\libzmq-mt-sgd-4_3_3.lib
Ws2_32.lib
Iphlpapi.lib
7. Switch the configuration back to “Release“, select ponfiguration properties / Linker / Input, and then add the following entries to “Additional Dependencies“:
...\<repos>\vcpkg\packages\zeromq_x86-windows-static\lib\libzmq-mt-s-4_3_3.lib, 
Ws2_32.lib and 
Iphlpapi.lib
8. Go back to project, rebuild solution
9. Finally, run the example code provided earlier

Should print out into console:
```bash
Current 0MQ version is 4.3.X
```

This install guide is similar to the one provided by Joshua Burkholder [[GUIDE]](https://joshuaburkholder.com/wordpress/2018/05/25/build-and-static-link-zeromq-on-windows/#step_2)

## Usage
Open the src-files in your created directory and run main.cpp
