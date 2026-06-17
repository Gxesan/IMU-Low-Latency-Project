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

### **Week 5**
Before moving on to roll and pitch estimation, I decided to filter out the jitter first. The initial bandwidth frequency of 50Hz seems to contain too much noise. Hence, I will have to increase the frequency in the future. However, during the testing of the DLPF, I found out that both the accelerometer and gyroscope were not calibrated correctly. Some values showed non-zero values when they were not supposed to (i.e., sitting still on a table). Hence, I decided to correctly calibrate the accelerometer and gyroscope first. However, due to the length of my jumper cables, it is difficult to calibrate my accelerometer correctly as it is dangling mid-air. But, as long as it is not swinging, the gyroscope's values should still be zero. Hence, the Gyroscope calibration was done first using a Python script that initially collected 500 samples of gyroscope data. Then, it used the formula gx_bias = gx_sum / target_samples to determine the bias of the gyroscope. The offset for the value of gz seemed very off, sitting at around 25 when the IMU is still. It turns out that I was using the wrong register and was instead making it read from the temperature sensor. Hence, it was quickly fixed by changing the registers from which the gyroscope values were read. For the sake of this project, while it isn't perfect, the calibration of the accelerometer was done with the IMU plugged into a breadboard while making the chip as parallel to the table breadboard surface as possible. After trial and failure of every possible DLPF frequencies, I determined 24Hz was the best bandwidth to achieve a balance between speed and smoothness.
