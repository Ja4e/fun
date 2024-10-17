import bluetooth
from bleak import BleakScanner

def discover_classic_devices():
    print("Discovering classic Bluetooth devices...")
    
    try:
        nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=8, flush_cache=True)

        if not nearby_devices:
            print("No classic Bluetooth devices found.")
            return
        
        print("Found classic Bluetooth devices:")
        for addr, name in nearby_devices:
            print(f"  Address: {addr}, Name: {name}")
    
    except bluetooth.BluetoothError as e:
        print(f"Bluetooth error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def discover_ble_devices():
    print("Discovering BLE devices...")
    
    try:
        devices = await BleakScanner.discover()

        if not devices:
            print("No BLE devices found.")
            return
        
        print("Found BLE devices:")
        for device in devices:
            print(f"  Address: {device.address}, Name: {device.name}")
    
    except Exception as e:
        print(f"An unexpected error occurred while discovering BLE devices: {e}")

if __name__ == "__main__":
    discover_classic_devices()
    import asyncio
    asyncio.run(discover_ble_devices())
