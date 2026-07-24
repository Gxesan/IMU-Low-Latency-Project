# IMU-Low-Latency-Tracker
A UIUC ECE major's embedded systems project

## **Project Overview**
This project aims to implement a low-latency IMU-based motion tracking system utilizing Python real-time visualization. This project implements a low-latency IMU tracking system using the STM32F411RE MCU and an ICM-20948 IMU. Motion data are sampled over SPI, which is then processed on the MCU to stream it to a PC over UART-to-USB, and then finally visualized in real time using Python and Teleplot. 

## **Definition of Latency**
In this project, the exact “latency” that was measured was MCU execution latency. MCU execution latency can be defined as the total CPU time consumed from fetching the sensor data to sending it to the PC. Execution time was measured by setting a GPIO pin to high immediately before the SPI sensor started reading data, and it was then turned low as soon as the UART transmission function finished.

## **Hardware Components**
- Embedded System Development Board: STM32 NUCLEO-F411RE (configured to an internal 16 MHz HSI clock during latency measurements)
- IMU: ICM-20948
- Digilent Breadboard
- Oscilloscope: Digilent Analog Discovery 3

## **System Architecture & Data Flow**
Below is the pipeline through which the system processes motion data:
1. Physical Motion: Changes in acceleration and rotation are detected by the ICM-20948 IMU's accelerometer and gyroscope
2. SPI Read: The STM32 board reads the raw sensor registers via SPI
3. MCU Processing: The STM32 converts raw data into a 14-byte binary payload (now 10 after sensor fusion moved to main.c)
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

### **Experimental Conditions**
1. System Clock: 16 MHz (HSI)
2. SPI Clock: 4 MHz
3. UART Baud Rate: 115200 Bd or 921600 Bd (depending on the stage of measurement)

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
Starting from week 7, the goal is to record the latency values, comparing them to my old code that utilized ASCII format (using sprintf) and a baud rate of 115200 bd, to the improved code setup that uses a higher baud rate of 921600 bd and pure binary to send data. All measurements were performed with the STM32 configured to run at an internal 16 MHz HSI clock. It was left intentionally unchanged so that the measured latency improvements are attributed to software optimizations rather than increased CPU frequency. However, when using Waveforms to measure the latency, there were a few problems. The PA8 was shown to be floating, and DIO 1, which received data from UART, was completely flat. Furthermore, Waveforms gave me an error message stating, "Reduce the timebase or increase the sample rate". The sample rate was easily fixed by changing the sample settings in Waveforms from "default" to manually setting it to 2 million samples. The floating PA8 issue was solved after realizing that the pin was uninitialized in the MX_GPIO_Init function, and only PA4 was initialized. Below are the results attained:
| Formatting Method  | Baud Rate | Payload Size (Bytes) | Mean Latency (ms) | CPU Time Saved (%) |
| ------------------ | --------- | -------------------- | ----------------- | ------------------ |
| ASCII (sprintf)  | 115200  | 40 - 50 | 3.223 | 0      |
| ASCII (sprintf)  | 921600  | 40 - 50 | 0.883 | 72.8   |
| Binary           | 921600  | 14   | 0.420 | 87.0

As shown in the results above, we can see that as soon as the formatting method was switched to binary, the mean latency was greatly reduced, even though the hardware power did not change (as the baud rate stayed constant). This is because binary transmission removed the slow and costly ASCII formatting method performed by sprintf, and the payload size was also reduced greatly from 40-50 bytes to 14 bytes.

### **Week 8**
The first goal of week 8 was to split the MCU execution latency measurements into the three stages listed above: SPI read, data processing, and UART transmission. To achieve that, I used three different GPIO pins to measure each stage, turning it on and off at the correct position in the infinite while loop. Further hardware connections also had to be made, as two more pins had to be connected to two more channels of the oscilloscope. Below are the results attained:
1. SPI Read → 243.8 μs
2. Data Processing → 9.2 μs
3. UART Transmission → 173.8 μs

The results above show a higher latency compared to the mean latency that was measured when the MCU execution latency was measured as a whole. This is most likely due to the fact that measuring the three different stages individually required additional GPIO writes. That slightly altered the execution path, resulting in the total latency being higher compared to when it was measured as a whole. Furthermore, we can see that compared to SPI reading and UART transmission, data processing took comparatively less time. This is expected since most of the latency is composed of communication in and between devices instead of math. 

### **Week 9**
Week 9's time was spent on moving the complementary filter from the Python visualization script onto main.c. There are several advantages to this. Firstly, the dt calculations in the Python script would not be a fixed value, as it would differ depending on the state of the OS the program is being run from. However, the STM32 hardware timer triggers every 10ms, which makes the dt value a fixed value, making the filter more accurate. Additionally, the payload shrinks from 14 bytes to 10 bytes, as it no longer sends all the accelerometer and gyroscope measurements and instead just sends the final pitch and roll estimations. Even though the size of the payload decreased from 14 bytes to 10 bytes, the total latency increased due to the fact that complex sensor fusion was added into main.c. Now, the total latency is:
- **Total Latency: 454.6 μs**

### **Final Results**
| Optimization | Total Latency (ms) |
| ------------ | ------------------ |
| ASCII @ 115200 Bd | 3.223 |
| ASCII @ 921600 Bd | 0.883 |
| Binary @ 921600 Bd | 0.420 |
| Binary w/ On-board Sensor Fusion | 0.455 |


## **Future Improvements**
### **Replace Blocking Communication wtih DMA**
As of current, blocking HAL functions are implemented for both SPI read and UART transmissions. Using DMA instead would let the CPU to perform sensor fusion and other computations while data transfer occurs in the background, which would reduce system responsiveness.

### **Use ICM-20948 Data Ready Interrupt**
The data ready interrupt pin on the ICM-20948 IMU could be connected to the STM32's external interrupt pin instead of sampling with a periodic timer. This would reduce sampling jitter and unnecessary polling as it would ensure each SPI reading happens immediately after new sensor data becomes available. 

### **Replace the Complementary Filter with a Madgwick Filter**
While a complementary filter is easy to utilize and requires fewer computational resources, a Madgwick filter would improve orientation accuracy while remaining efficient enough for real-time execution. This is because a Madgwick filter combines the accelerometer, gyroscope, and magnetometer measurements using quaternion-based estimation.
