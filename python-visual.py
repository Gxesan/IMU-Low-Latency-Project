import serial
import struct
import time

SERIAL_PORT = 'COM5'
BAUD_RATE = 115200

ACCEL_SCALE = 16384.0  # Assuming accelerometer range is ±2g
GYRO_SCALE = 131.0     # Assuming gyroscope range is ±250°/s

def read_sensor_data(ser):
    # Read 14 bytes of data (6 for accelerometer, 6 for gyroscope, 2 for temperature)
    data = ser.read(14)
    
    # Unpack the data (assuming little-endian format)
    accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z = struct.unpack('<hhhbhhh', data)
    
    # Scale the accelerometer and gyroscope values
    accel_x /= ACCEL_SCALE
    accel_y /= ACCEL_SCALE
    accel_z /= ACCEL_SCALE
    
    gyro_x /= GYRO_SCALE
    gyro_y /= GYRO_SCALE
    gyro_z /= GYRO_SCALE
    
    return accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z