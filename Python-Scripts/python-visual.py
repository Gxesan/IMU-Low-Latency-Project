import serial
import time
import socket
import math
import struct

SERIAL_PORT = 'COM5'
BAUD_RATE = 921600

ACCEL_SCALE = 16384.0  # Assuming accelerometer range is ±2g
GYRO_SCALE = 131.0     # Assuming gyroscope range is ±250°/s

# Accelerometer and Gyroscope bias offsets (calibrated using IMU-calibrate.py)
AX_BIAS = -0.0401
AY_BIAS = -0.0671
AZ_BIAS = -0.1047
GX_BIAS = -1.2682
GY_BIAS = -1.3128
GZ_BIAS = -0.0054

UDP_IP = "127.0.0.1"
UDP_PORT = 47269
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_to_teleplot(name, value):
    msg = f"{name}:{value}\n"
    sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))
    
def read_IMU(ser):
    try: # Looks for 0xAA and 0xBB (Sync Header)
        while True:
            if ser.in_waiting > 0:
                byte1 = ser.read(1)
                if byte1 == b'\xAA':
                    byte2 = ser.read(1)
                    if byte2 == b'\xBB':
                        break

        payload = ser.read(12) # Grabs 12-Byte payload following the sync header
        if len(payload) != 12:
            return None
    
        ax_raw, ay_raw, az_raw, gx_raw, gy_raw, gz_raw = struct.unpack('>hhhhhh', payload)
        # Accelerometer value calculations
        ax = (ax_raw / ACCEL_SCALE) - AX_BIAS 
        ay = (ay_raw / ACCEL_SCALE) - AY_BIAS 
        az = (az_raw / ACCEL_SCALE) - AZ_BIAS 

        gx = (gx_raw / GYRO_SCALE) - GX_BIAS 
        gy = (gy_raw / GYRO_SCALE) - GY_BIAS 
        gz = (gz_raw / GYRO_SCALE) - GZ_BIAS 

        return ax, ay, az, gx, gy, gz
    except Exception as e:
        print(f"Parsing Error: {e}")
        return None

if __name__ == '__main__':
    try:
        # Open serial port
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")


        pitch_est = 0.0
        roll_est = 0.0

        last_time = time.time()

        FTP = 0.94 # FTP = Filter Tuning Parameter

        while True:
            # Read a full line of text until it hits '\n'

            parsed_data = read_IMU(ser)

            if parsed_data:
                ax, ay, az, gx, gy, gz = parsed_data

                # Delta time calculation
                current_time = time.time()
                dt = current_time - last_time
                last_time = current_time

                # Pure accelerometer angle calculations
                accel_pitch = math.degrees(math.atan2(-ax, math.sqrt(ay**2 + az**2)))
                accel_roll = math.degrees(math.atan2(ay, az))


                pitch_est = FTP * (pitch_est + (gy * dt)) + (1.0 - FTP) * accel_pitch
                roll_est = FTP * (roll_est + (gx * dt)) + (1.0 - FTP) *accel_roll

                # Send pitch and roll estimation values to teleplot
                send_to_teleplot("Pitch", pitch_est)
                send_to_teleplot("Roll", roll_est)


    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")

    except KeyboardInterrupt:
        print("\nExiting program...")
    
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()