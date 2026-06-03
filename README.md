# IMU-Low-Latency-Tracker
A UIUC ECE major's embedded systems project

## **Project Overview**
This project aims to implement a low-latency IMU-based motion tracking system utilizing Python real-time visualization. The system reads accelerometer and gyroscope data from the IMU, which then sends the data to a PC over USB serial, estimating roll/pitch orientation using a complementary filter.

## **Hardware Components**
- Embedded System Development Board: STM32 NUCLEO-F411RE
- IMU: ICM-20948
- Digilent Breadboard


## **Weekly Progress Log**
### **Week 1**
The main goal of week 1 was to configure SPI and read the WHO_AM_I register successfully. Initial problems encountered were WHO_AM_I returning     incorrect values and the printf feature on the IDE not functioning. The correct value of WHO_AM_I was returned after realizing improper soldering of pins on the IMU, and correcting debug optimization settings on the IDE itself.

### **Week 2**
The goal of week 2 was to actually read the accelerometer/gyroscope data. While ax, ay, az, gx, gy, and gz values could be read, there were initial problems regarding the fact that their updates could not be viewed in live, and instead were only updated whenever I pressed resume in the debug session, even though those variables were added under "live expressions". They were fixed after removing a breakpoint that was present in my debugging session. As I achieved week 2's goal, I moved on early to start streaming data through a UART-to-USB bridge (using UART on the microcontroller but the data travels along a USB cable to a computer). This way, I could gain the advantage of faster processing speed of UART, while ST-Link handles the USB translation without having to do clock configuration and other background coding.
