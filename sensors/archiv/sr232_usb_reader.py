import usb.core

dev=usb.core.find(idVendor=0x0403, idProduct=0x6001)
ep=dev[0].interfaces()[0].endpoints()[0]
i=dev[0].interfaces()[0].bInterfaceNumber
dev.reset()

if dev.is_kernel_driver_active(i):
  dev.detach_kernel_driver(i)

dev.set_configuration()
eaddr=ep.bEndpointAddress

for byte in range(100):
  r=dev.read(eaddr,1024)
  print(r)