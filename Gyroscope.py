class gyroscope:
    def __init__(self, port = '/dev/ttyUSB0', baud = 9600):
        self.baud = baud
        self.port = port
        self.msg = ''

        self.accData = [0.0] * 8
        self.gyroData = [0.0] * 8
        self.angleData = [0.0] * 8
        self.state = 0
        self.byteNum = 0
        self.checkSum = 0

        self.a = [0.0] * 3
        self.w = [0.0] * 3
        self.angle = [0.0] * 3
    
    def get_msg(self):
        pass

    def display(self):
        try:
            import serial
        except:
            print('warning: No "serial" module found.')
            return
        
        ser = serial.Serial(self.port, self.baud, timeout = 0.5)
        if ser.is_open:
            print('The serial port was opened successfully!')
            while True:
                dataHex = ser.read(33) # How many bytes are read from the port
                self.readData(dataHex)
                try:
                    print("a(g):%10.3f %10.3f %10.3f w(deg/s):%10.3f %10.3f %10.3f Angle(deg):%10.3f %10.3f %10.3f" % self.msg)
                except: continue
        else:
            print('Failed to open the serial!')
    
    def clear(self):
        self.checkSum = 0
        self.byteNum = 0
        self.state = 0

    def readData(self, inputData):
        for data in inputData:
            if self.state == 0: # The situation is undecided
                if data == 0x55 and self.byteNum == 0:
                    self.checkSum = data
                    self.byteNum = 1
                    continue
                elif data == 0x51 and self.byteNum == 1:
                    self.checkSum += data
                    self.state = 1
                    self.byteNum = 2
                elif data == 0x52 and self.byteNum == 1:
                    self.checkSum += data
                    self.state = 2
                    self.byteNum = 2
                elif data == 0x53 and self.byteNum == 1:
                    self.checkSum += data
                    self.state = 3
                    self.byteNum = 2
            elif self.state == 1: # acceleration
                if self.byteNum < 10:
                    self.accData[self.byteNum - 2] = data
                    self.checkSum += data
                    self.byteNum += 1
                else:
                    if data  == (self.checkSum & 0xff):
                        self.a = self.get_acc(self.accData)
                    self.clear()
            elif self.state == 2: # angular velocity
                if self.byteNum < 10:
                    self.accData[self.byteNum - 2] = data
                    self.checkSum += data
                    self.byteNum += 1
                else:
                    if data  == (self.checkSum & 0xff):
                        self.w = self.get_w(self.accData)
                    self.clear()
            elif self.state == 3: # angle
                if self.byteNum < 10:
                    self.accData[self.byteNum - 2] = data
                    self.checkSum += data
                    self.byteNum += 1
                else:
                    if data  == (self.checkSum & 0xff):
                        self.angle = self.get_angle(self.accData)
                        try:
                            self.msg = self.a + self.w + self.angle
                        except:
                            continue
                    self.clear()

    def get_acc(self, dataHex):
        axl = dataHex[0]                                        
        axh = dataHex[1]
        ayl = dataHex[2]                                        
        ayh = dataHex[3]
        azl = dataHex[4]                                        
        azh = dataHex[5]
        
        k_acc = 16.0
    
        acc_x = (axh << 8 | axl) / 32768.0 * k_acc
        acc_y = (ayh << 8 | ayl) / 32768.0 * k_acc
        acc_z = (azh << 8 | azl) / 32768.0 * k_acc
        if acc_x >= k_acc:
            acc_x -= 2 * k_acc
        if acc_y >= k_acc:
            acc_y -= 2 * k_acc
        if acc_z >= k_acc:
            acc_z -= 2 * k_acc
        
        return acc_x, acc_y, acc_z

    def get_w(self, dataHex):
        wxl = dataHex[0]                                        
        wxh = dataHex[1]
        wyl = dataHex[2]                                        
        wyh = dataHex[3]
        wzl = dataHex[4]                                        
        wzh = dataHex[5]

        k_w = 2000.0
    
        w_x = (wxh << 8 | wxl) / 32768.0 * k_w
        w_y = (wyh << 8 | wyl) / 32768.0 * k_w
        w_z = (wzh << 8 | wzl) / 32768.0 * k_w
        if w_x >= k_w:
            w_x -= 2 * k_w
        if w_y >= k_w:
            w_y -= 2 * k_w
        if w_z >=k_w:
            w_z-= 2 * k_w
        return w_x, w_y, w_z

    def get_angle(self, dataHex):
        rxl = dataHex[0]                                        
        rxh = dataHex[1]
        ryl = dataHex[2]                                        
        ryh = dataHex[3]
        rzl = dataHex[4]                                        
        rzh = dataHex[5]

        k_angle = 180.0
    
        angle_x = (rxh << 8 | rxl) / 32768.0 * k_angle
        angle_y = (ryh << 8 | ryl) / 32768.0 * k_angle
        angle_z = (rzh << 8 | rzl) / 32768.0 * k_angle
        if angle_x >= k_angle:
            angle_x -= 2 * k_angle
        if angle_y >= k_angle:
            angle_y -= 2 * k_angle
        if angle_z >=k_angle:
            angle_z-= 2 * k_angle
    
        return angle_x, angle_y, angle_z
    
if __name__ == '__main__':
    # use '/dev/ttyAMA0' for USB or '/dev/ttyAMA0' for GPIO
    g = gyroscope('/dev/ttyUSB0', 9600)
    g.display()