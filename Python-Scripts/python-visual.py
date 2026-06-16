import serial
import struct
import time
import socket

SERIAL_PORT = 'COM5'
BAUD_RATE = 115200

ACCEL_SCALE = 16384.0  # Assuming accelerometer range is ±2g
GYRO_SCALE = 131.0     # Assuming gyroscope range is ±250°/s

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def parse_sensor_data(line):

    try:
        parts = line.strip().split() # Clean the string and seperate by spaces

        # Ensure exactly 6 pieces of data were received
        if len(parts) != 6:
            return None
        
        # Extract the numbers (Split by = and grab second part)
        ax_raw = int(parts[0].split('=')[1])
        ay_raw = int(parts[1].split('=')[1])
        az_raw = int(parts[2].split('=')[1])
        gx_raw = int(parts[3].split('=')[1])
        gy_raw = int(parts[4].split('=')[1])
        gz_raw = int(parts[5].split('=')[1])

        accel_x = ax_raw / ACCEL_SCALE
        accel_y = ay_raw / ACCEL_SCALE
        accel_z = az_raw / ACCEL_SCALE

        gyro_x = gx_raw / GYRO_SCALE
        gyro_y = gy_raw / GYRO_SCALE
        gyro_z = gz_raw / GYRO_SCALE
        return accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z
    
    except Exception as e:
        # Don't crash if corrupted line goes through
        return None
    
if __name__ == '__main__':
    try:
        # Open serial port
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        # Flush garbage data in buffer during startup
        ser.reset_input_buffer()

        # Accelerometer and Gyroscope bias offsets (calibrated using IMU-calibrate.py)
        AX_BIAS = -0.0401
        AY_BIAS = -0.0671
        AZ_BIAS = -2.1047
        GX_BIAS = -1.2682
        GY_BIAS = -1.3128
        GZ_BIAS = -0.0054

        while True:
            # Read a full line of text until it hits '\n'
            if ser.in_waiting > 0:
                raw_line = ser.readline().decode('utf-8', errors = 'ignore')

                # Parse data
                parsed_data = parse_sensor_data(raw_line)

                if parsed_data:
                    ax, ay, az, gx, gy, gz = parsed_data

                    ax_calibrated = ax - AX_BIAS
                    ay_calibrated = ay - AY_BIAS
                    az_calibrated = az - AZ_BIAS
                    gx_calibrated = gx - GX_BIAS
                    gy_calibrated = gy - GY_BIAS
                    gz_calibrated = gz - GZ_BIAS

                    sock.sendto(f"Accel_X:{ax_calibrated:.2f}".encode(), ("127.0.0.1", 47269))
                    sock.sendto(f"Accel_Y:{ay_calibrated:.2f}".encode(), ("127.0.0.1", 47269))
                    sock.sendto(f"Accel_Z:{az_calibrated:.2f}".encode(), ("127.0.0.1", 47269))

                    sock.sendto(f"Gyro_X:{gx_calibrated:.2f}".encode(), ("127.0.0.1", 47269))
                    sock.sendto(f"Gyro_Y:{gy_calibrated:.2f}".encode(), ("127.0.0.1", 47269))
                    sock.sendto(f"Gyro_Z:{gz_calibrated:.2f}".encode(), ("127.0.0.1", 47269))

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")

    except KeyboardInterrupt:
        print("\nExiting program...")
    
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
