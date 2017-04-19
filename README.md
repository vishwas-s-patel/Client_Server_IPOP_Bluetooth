# Client_Server_IPOP_Bluetooth

Bluetooth Socket Programming using PyBluez on RaspberryPi and Laptop PC to build a table of devices on server side of the IPOP
VPN Network. The clients can access this server via IPOP VPN network as if it is on the same LAN network. 

It offers three different services:
1. LIST     -> lists all the bluetooth devices in the server side.
2. SCAN     -> The client asks the server to scan for bluetooth devices again and update it's table.
3. READ(ID) -> Reads from the bluetooth device using the given ID.
