import socket
import subprocess

# Set the path to the USB image file
image_path = './imageFESB.001'

# Call bitlocker2john to extract the recovery key
bitlocker2john_cmd = f'bitlocker2john -i {image_path}'
process = subprocess.Popen(bitlocker2john_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
output, error = process.communicate()

# Print the extracted recovery key
keys = output.decode().strip().split('\n')
recovery_key = [s for s in keys if "$bitlocker$1$" in s]
print(f'BitLocker recovery key: {recovery_key[0]}')

hashcat_cmd = f'hashcat -m 22100 -a 3 hash.txt "218?d?d?d?d?d"'
print(f"Running command: {hashcat_cmd}")
process = subprocess.call(hashcat_cmd, shell=True)
# output, error = process.communicate()

cracked_password = subprocess.check_output([hashcat_cmd + " --show"], shell=True).decode()
cracked_password = cracked_password.split(':')[-1]
print(f"Password : {cracked_password}")
