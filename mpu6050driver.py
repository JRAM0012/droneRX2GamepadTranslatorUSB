from busio import I2C
import board
import time

class MPU6050:
    def __init__(self, i2c, address=0x68):

        self.PWR_MGMT_1 = 0x6B
        self.SMPLRT_DIV = 0x19
        self.CONFIG = 0x1A
        self.GYRO_CONFIG = 0x1B
        self.ACCEL_CONFIG = 0x1C
        self.TEMP_OUT_H = 0x41
        self.ACCEL_XOUT_H = 0x3B
        self.GYRO_XOUT_H = 0x43

        self.i2c = i2c
        self.address = address
        
        print("lock try")
        self.i2c.try_lock()
        
        self.i2c.writeto(self.address, bytes([self.PWR_MGMT_1,   0x00]))
        time.sleep(0.1)
        self.i2c.writeto(self.address, bytes([self.SMPLRT_DIV,   0x07]))
        self.i2c.writeto(self.address, bytes([self.CONFIG,       0x00]))
        self.i2c.writeto(self.address, bytes([self.GYRO_CONFIG,  0x00]))
        self.i2c.writeto(self.address, bytes([self.ACCEL_CONFIG, 0x00]))
    
    def read_raw_data(self, reg):
        self.i2c.writeto(self.address, bytes([reg]))
        buf = bytearray(2)
        self.i2c.readfrom_into(self.address, buf)

        value = (buf[0] << 8) | buf[1]
        if value >= 0x8000:
            value -= 65536

        return value

    def get_data(self):
        temp    = self.read_raw_data(self.TEMP_OUT_H)       / 340.0 + 36.53
        accel_x = self.read_raw_data(self.ACCEL_XOUT_H + 0) / 16384.0
        accel_y = self.read_raw_data(self.ACCEL_XOUT_H + 2) / 16384.0
        accel_z = self.read_raw_data(self.ACCEL_XOUT_H + 4) / 16384.0
        gyro_x  = self.read_raw_data(self.GYRO_XOUT_H  + 0) / 131.0
        gyro_y  = self.read_raw_data(self.GYRO_XOUT_H  + 2) / 131.0
        gyro_z  = self.read_raw_data(self.GYRO_XOUT_H  + 4) / 131.0

        return [ 0x3, temp, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z ]

if __name__ == "__main__":
    scl = board.GP9
    sda = board.GP8
    i2c = I2C(scl, sda)
    mpu = MPU6050(i2c)
    for i in range(1000):
        print(mpu.get_data())
        time.sleep(0.1)
    i2c.deinit()
    