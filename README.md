# IMU-Low-Latency-Tracker
A UIUC ECE major's embedded systems project

**Project Overview**
This project aims to implement a low-latency IMU-based motion tracking system utilizing Python real-time visualization. The system reads accelerometer and gyroscope data from the IMU, which then sends the data to a PC over USB serial, estimating roll/pitch orientation using a complementary filter.

**Hardware Components**
- Embedded System Development Board: STM32 NUCLEO-F411RE
- IMU: ICM-20948
- Digilent Breadboard


**Weekly Progress Log**
  **Week 1**
  The main goal of week 1 was to configure SPI and read the WHO_AM_I register successfully. Initial problems encountered were WHO_AM_I returning     incorrect values and the printf feature on the IDE not functioning. The correct value of WHO_AM_I was returned after realizing improper soldering of pins on the IMU, and correcting debug optimization settings on the IDE itself.

  **Week 2**
  The goal of week 2 was to actually read the accelerometer/gyroscope data. While ax, ay, az, gx, gy, gz values could be read, there were initial problems regarding the fact that their updates could not be viewed in live, even though those variables were added under "live expressions".
