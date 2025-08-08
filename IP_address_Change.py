# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 08:53:42 2023

@author: qhu
"""

import os
import ctypes
import time
import wmi
import psutil
import subprocess



# Step 1: Get the list of the Network Adapter
#cmd /k execute a command then remain
#cmd / c execute a command and then terminate
os.system('cmd /c wmic nic get NetEnabled, NetConnectionID,name, index')

c = wmi.WMI()

time.sleep(3)

#os.system('cmd /c "netsh interface show interface"')

#---------------------------------------------------------------------------------------------------------

def Call_CMD(Index, EnableOrNot):
    cmd = u'/c "'+ 'wmic path win32_networkadapter where index='+Index+ ' call '+EnableOrNot
    ctypes.windll.shell32.ShellExecuteW(None, u"runas",u"cmd.exe",cmd, None, 1)
    time.sleep(2)
#---------------------------------------------------------------------------------------------------------

   
# Step 2: Enable and Disable the adapter
ChooseAdapter_disable_NO =  input ('Choose which Network Adapter you want to Disable (index), press "e" if none: ')
''' Open an elevated command windows '''

if ChooseAdapter_disable_NO != 'e':
    #pass the Command line to the admin window
    Call_CMD(ChooseAdapter_disable_NO,'disable')
else:
    pass

#---------------------------------------------------------------------------------------------------------

# Step 3 Enable the Network Adapter you want
ChooseAdapter_enable_NO =  input ('Choose which Network Adapter you want to Enable (index): ')
''' Open an elevated command windows '''

#pass the Command line to the admin window
Call_CMD(ChooseAdapter_enable_NO,'enable')

NetworkAdapter_NIC1 = c.Win32_NetworkAdapterConfiguration(Index = ChooseAdapter_enable_NO)
nic_selection_all = NetworkAdapter_NIC1[0]

#---------------------------------------------------------------------------------------------------------
# Step 4 Change the IP Address
def FindRightNetworkAdapter_AssignAddress():
    
    addrs = psutil.net_if_addrs()# Only show all the lived network
    ToList = list(addrs.keys())
    print('Here is the list of available network, specify which one you want to change.')
    
    ToList_v2 = [str(i)+'. '+ToList[i]for i in range (0,len(ToList))]
    print(*ToList_v2,sep="\n")
    Select_Network_NO = int(input('Enter the number here: '))
    
    cmd_line = 'cmd /c netsh interface ipv4 set address name="'+ ToList[Select_Network_NO]+ '" static '+IP_Addr+' '+subnet+' '+gateway
    ctypes.windll.shell32.ShellExecuteW(None, u"runas",u"cmd.exe",cmd_line, None, 1)
    
    
User_Input = input('Do you want to change IP Address (Y or N): ')
if User_Input == 'Y':
    IP_Addr = input ('IP Address: ')
    subnet = input('Subnet: ')
    gateway = input ('Gateway:')
    time.sleep(5)
    FindRightNetworkAdapter_AssignAddress()


time.sleep(2)
print('Done for you. Thank you\n')

# Step 5 Show IP config and run a ping test.

try:
    # Execute ipconfig command and capture output
    # decode('utf-8') converts the bytes output to a UTF-8 string
    # check_output raises CalledProcessError if the command returns a non-zero exit code
    output_bytes = subprocess.check_output("ipconfig")
    output_str = output_bytes.decode('utf-8')

    # Print the captured output
    print(output_str)

except subprocess.CalledProcessError as e:
    print(f"Error executing ipconfig: {e}")
    print(f"Stderr: {e.stderr.decode('utf-8') if e.stderr else 'N/A'}")
except FileNotFoundError:
    print("Error: 'ipconfig' command not found. This command is specific to Windows.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

pingTest = input('Want to run a ping test? Y or N: ')

def ping_with_os(host):
    """Pings a host using the os.system() function."""
    # -c 4 for Linux/macOS to send 4 packets, -n 4 for Windows
    command = f"ping -c 4 {host}" if os.name != "nt" else f"ping -n 4 {host}"
    response = os.system(command)
    if response == 0:
        print(f"{host} is reachable.")
    else:
        print(f"{host} is unreachable.")

# Example usage:
if pingTest == 'Y':
    destination_IP = input('Partners IP address:  ')
    ping_with_os(destination_IP)
    
# Wait for user to exit
while True:
    exit_program = input('\nExit the program ?')
    if exit_program =='':
        break




    