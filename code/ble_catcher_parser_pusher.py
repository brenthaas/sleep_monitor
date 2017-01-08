# BLE Catcher Modified by : Mikey Sklar
#
# Original Code Credit : Tony DiCola @ Adafruit
# BLE Catcher Modified by : Mikey Sklar @ Adafruit
#
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

from Adafruit_IO import Client
aio = Client('34e50d0ccb65f955ce54837f19df7ea9fe5e1c7b')


# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    # Scan for UART devices.
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        # Search for the first UART device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.

    print('Discovering services...')
    UART.discover(device)

    while True:
        uart = UART(device)
        receive  = uart.read(timeout_sec=300) # 5min timeout

        if receive:
                sd = receive.split(",");
                print("T: " + sd[0] + " H: " + sd[1] + " Li: " + sd[2] + " Lux: " + sd[3] + " N: " + sd[4] + " HR: " + sd[5])
        else:
                continue


        if len(sd) == 6:
                aio.send('Temperature', sd[0])
                aio.send('Humidity', sd[1])
                aio.send('Light', sd[2])
                aio.send('Lux', sd[3])
                aio.send('Noise', sd[4])
                aio.send('Heart Rate', sd[5])
        else:
                continue

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
