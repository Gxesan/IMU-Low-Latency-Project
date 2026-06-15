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
The main goal of week 1 was to configure SPI and read the WHO_AM_I register successfully. Initial problems encountered were WHO_AM_I returning incorrect values and the printf feature on the IDE not functioning. The correct value of WHO_AM_I was returned after realizing improper soldering of pins on the IMU, and correcting debug optimization settings on the IDE itself.

### **Week 2**
The goal of week 2 was to actually read the accelerometer/gyroscope data. While ax, ay, az, gx, gy, and gz values could be read, there were initial problems regarding the fact that their updates could not be viewed in live, and instead were only updated whenever I pressed resume in the debug session, even though those variables were added under "live expressions". They were fixed after removing a breakpoint that was present in my debugging session. 

### **Week 3**
In week 3, I moved on early to start streaming data through a UART-to-USB bridge (using UART on the microcontroller but the data travels along a USB cable to a computer). This way, I could gain the advantage of the faster processing speed of UART, while ST-Link handles the USB translation without having to do clock configuration and other background coding. The next step was to calibrate and convert the raw numerical data into Gs and degrees/sec. This was started in a Python script, and while I was able to convert the numerical data, there are problems regarding visualizing the data using Teleplot. While it reads the correct accelerometer and gyroscope values, Teleplot does not seem to convert them into a visual graph. I have added a Python script to test if Teleplot works, and I found out that Teleplot was not plotting data beforehand due to the fact that both Teleplot and my Python script were using COM5, and hence Teleplot has to be connected by UDP.

### **Week 4**
Week 4 was started by fixing the Python script so that it displays the ax, ay, az, gx, gy, and gz values through Teleplot instead of just printing their values out. The problem was, in fact, the fact that COM5 could not be used by both the Python script and Teleplot at the same time. Hence, sending the data to the UDP socket and making Teleplot display graphs from data received from UDP was the solution. Moving on to changing the data collection method from polling to interrupt, and achieving a stable timing through enabling the hardware timer was also done in this week. 
