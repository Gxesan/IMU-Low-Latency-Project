# IMU-Low-Latency-Tracker
A UIUC ECE major's embedded systems project

## **Project Overview**
This project aims to implement a low-latency IMU-based motion tracking system utilizing Python real-time visualization. The system reads accelerometer and gyroscope data from the IMU, which then sends the data to a PC over USB serial, estimating roll/pitch orientation using a complementary filter.

## **Definition of Latency**
In this project, the exact “latency” that was measured was MCU execution latency, also commonly known as interrupt latency. MCU execution latency can be defined as the total CPU time consumed from fetching the sensor data to sending it to the PC. Execution time was measured by setting a GPIO pin to high immediately before the SPI sensor started reading data, and it was then turned low as soon as the UART transmission function finished.

## **Hardware Components**
- Embedded System Development Board: STM32 NUCLEO-F411RE
- IMU: ICM-20948
- Digilent Breadboard
- Oscilloscope: Digilent Analog Discovery 3

## **System Architecture & Data Flow**
Below is the pipeline through which the system processes motion data:
1. Physical Motion: Changes in acceleration and rotation are detected by the ICM-20948 IMU's accelerometer and gyroscope
2. SPI Read: The STM32 board reads the raw sensor registers via SPI
3. MCU Processing: The STM32 converts raw data into a 14-byte binary payload
4. UART-to-USB: The binary payload is transmitted to the ST-LINK USB Bridge
5. Python backend: A Python script converts the binary stream and estimates pitch and roll after calibration, and a complementary filter is applied
6. UDP Teleplot: The calculated results are sent to Teleplot for real-time graphing via UDP

## **Repository Structure**
- /Core/Src → Contains main.c that has STM32CubeMX settings and C source code
- /Python-Scripts → Contains a Python script that calibrates the IMU and the visualization script

## **How to Run**
### **Required software:**
1. STM32CubeIDE
2. STM32CubeMX
3. Python 3
4. Teleplot (on web client or VSCode)

### **Setup Instructions**
1. Flash the STM32 board with main.c
2. Install the required Python libaries using: pip install pyserial
3. Open Teleplot and configure it to listen to UDP port 47269
4. Run the Python visualization script
5. Move the IMU to see real-time pitch and roll estimation

## **Weekly Progress Log**
### **Week 1**
The main goal of week 1 was to configure SPI and read the WHO_AM_I register successfully. Initial problems encountered were WHO_AM_I returning incorrect values and the printf feature on the IDE not functioning. The correct value of WHO_AM_I was returned after realizing improper soldering of pins on the IMU and correcting debug optimization settings on the IDE itself.

### **Week 2**
The goal of week 2 was to actually read the accelerometer/gyroscope data. While ax, ay, az, gx, gy, and gz values could be read, there were initial problems regarding the fact that their updates could not be viewed in live, and instead were only updated whenever I pressed resume in the debug session, even though those variables were added under "live expressions". They were fixed after removing a breakpoint that was present in my debugging session. 

### **Week 3**
In week 3, I moved on early to start streaming data through a UART-to-USB bridge (using UART on the microcontroller, but the data travels along a USB cable to a computer). This way, I could gain the advantage of the faster processing speed of UART, while ST-Link handles the USB translation without having to do clock configuration and other background coding. The next step was to calibrate and convert the raw numerical data into Gs and degrees/sec. This was started in a Python script, and while I was able to convert the numerical data, there are problems regarding visualizing the data using Teleplot. While it reads the correct accelerometer and gyroscope values, Teleplot does not seem to convert them into a visual graph. I have added a Python script to test if Teleplot works, and I found out that Teleplot was not plotting data beforehand due to the fact that both Teleplot and my Python script were using COM5, and hence Teleplot has to be connected by UDP.

### **Week 4**
Week 4 started by fixing the Python script so that it displays the ax, ay, az, gx, gy, and gz values through Teleplot instead of just printing their values. The problem was, in fact, the fact that COM5 could not be used by both the Python script and Teleplot at the same time. Hence, sending the data to the UDP socket and making Teleplot display graphs from data received from UDP was the solution. Moving on to changing the data collection method from polling to interrupt, and achieving a stable timing through enabling the hardware timer, was also done this week. 

### **Week 5**
Before moving on to roll and pitch estimation, I decided to filter out the jitter first. The initial bandwidth frequency of 50Hz seems to contain too much noise. Hence, I will have to increase the frequency in the future. However, during the testing of the DLPF, I found out that both the accelerometer and gyroscope were not calibrated correctly. Some values showed non-zero values when they were not supposed to (i.e., sitting still on a table). Hence, I decided to correctly calibrate the accelerometer and gyroscope first. However, due to the length of my jumper cables, it is difficult to calibrate my accelerometer correctly, as it is dangling in mid-air. But, as long as it is not swinging, the gyroscope's values should still be zero. Hence, the Gyroscope calibration was done first using a Python script that initially collected 500 samples of gyroscope data. Then, it used the formula gx_bias = gx_sum / target_samples to determine the bias of the gyroscope. The offset for the value of gz seemed very off, sitting at around 25 when the IMU is still. It turns out that I was using the wrong register and was instead making it read from the temperature sensor. Hence, it was quickly fixed by changing the registers from which the gyroscope values were read. For the sake of this project, while it isn't perfect, the calibration of the accelerometer was done with the IMU plugged into a breadboard while making the chip as parallel to the table breadboard surface as possible. After trial and failure of every possible DLPF frequency, I determined 24Hz was the best bandwidth to achieve a balance between speed and smoothness.

### **Week 6**
Beginning of week 6, I completed the code for roll and pitch estimation. However, with a filter tuning parameter (FTP) of 0.98, I realized that the speed at which the IMU reacts was too sluggish. Hence, after further experimentation with trial and error, the perfect sweet spot FTP I found was 0.94. Moving on to trying to lower the latency as much as possible, I first started with increasing the baud rate to 921600. However, when that was done, I did not realize that regenerating the code through STM32CubeMX actually deleted my while loop code in main.c, as it was not in the user code comments. Hence, I had to rebuild the while loop, and in the process, I changed the format to not use printf and instead send the binary bytes to the Python script. However, the Python script did not seem to be able to pick up data from the IMU after that. The problem was that the Python script had to be updated to search for the sync header instead of raw English text, as I had now removed sprintf from the C code.

### **Week 7**
Starting from week 7, the goal is to record the latency values, comparing them to my old code that utilized ASCII format (using sprintf) and a baud rate of 115200 bd, to the improved code setup that uses a higher baud rate of 921600 bd and pure binary to send data. However, when using Waveforms to measure the latency, there were a few problems. The PA8 was shown to be floating, and DIO 1, which received data from UART, was completely flat. Furthermore, Waveforms gave me an error message stating, "Reduce the timebase or increase the sample rate". The sample rate was easily fixed by changing the sample settings in Waveforms from "default" to manually setting it to 2 million samples. The floating PA8 issue was solved after realizing that the pin was uninitialized in the MX_GPIO_Init function, and only PA4 was initialized. Below are the results attained:
| Formatting Method  | Baud Rate | Payload Size (Bytes) | Mean Latency (ms) | CPU Time Saved (%) |
| ------------------ | --------- | -------------------- | ----------------- | ------------------ |
| ASCII (sprintf)  | 115200  | 40 - 50 | 3.223 | 0      |
| ASCII (sprintf)  | 921600  | 40 - 50 | 0.883 | 72.8   |
| Binary           | 921600  | 14   | 0.420 | 87.0

### **Week 8**
The first goal of week 8 was to split the MCU execution latency measurements into the three stages listed above: SPI read, data processing, and UART transmission. To achieve that, I used three different GPIO pins to measure each stage, turning it on and off at the correct position in the infinite while loop. Further hardware connections also had to be made, as two more pins had to be connected to two more channels of the oscilloscope. Below are the results attained:
1. SPI Read → 243.8 μs
2. Data Processing → 9.2 μs
3. UART Transmission → 173.8 μs

The results above show a higher latency compared to the mean latency that was measured when the MCU execution latency was measured as a whole. This is most likely due to the "Observer Effect", also known as Instrumentation Overhead. When the total latency was measured, the pin's stopwatch only had to be turned on and off once, while measuring separately required the pins' stopwatches to be toggled three times. The act of toggling a pin's stopwatch also involves latency from the CPU (about 1.5 μs), which explains the small increase in latency when measured separately. 
