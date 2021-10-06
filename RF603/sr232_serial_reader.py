from serial import Serial

ser = Serial('/dev/ttyUSB0')
print(ser.name)
ser.flushInput()

print('start')
while True:
    try:
        print('read: ')
        ser_bytes = ser.readline()
        print('decode: ')
        decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        print('print: ')
        print(decoded_bytes)
    except:
        print("Keyboard Interrupt")
        break