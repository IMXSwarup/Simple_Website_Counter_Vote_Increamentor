import requests
import json
import time

def get_last_used_suffix(file_path):
    try:
        with open(file_path, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_last_used_suffix(file_path, suffix):
    with open(file_path, 'w') as file:
        file.write(str(suffix))

url = "https://axisbanksplash.in/api/entry/interested"
headers = {
    "Host": "axisbanksplash.in",
    "Cookie": "_ga=GA1.1.1422886774.1702222348; _gcl_au=1.1.1004163373.1702222350; _fbp=fb.1.1702222353301.950081536; _ga_0D426PLY29=GS1.1.1702222347.1.1.1702223542.0.0.0",
    "Sec-Ch-Ua": '"Not:A-Brand";v="99", "Chromium";v="112"',
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Origin": "https://axisbanksplash.in",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://axisbanksplash.in/submission/Kumar-Shirsh/art",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}

# File path to store and retrieve the last used suffix
name_suffix_file = "name_suffix.txt"
email_suffix_file = "email_suffix.txt"

# Initial values 
base_mobile = 8340159312
base_ip = "152.58.190.49"
base_name = "Swarup Saw"
base_email = "bittu28swarup"

# Number of iterations
num_iterations = 10000

# Retrieve the last used suffixes
last_name_suffix = get_last_used_suffix(name_suffix_file)
last_email_suffix = get_last_used_suffix(email_suffix_file)

for i in range(num_iterations):
    # Increment values
    mobile = base_mobile + i

    # Increment and reset the IP address segments
    ip_parts = base_ip.split('.')
    last_segment = int(ip_parts[-1]) + i

    # Initialize the overflow variable
    last_segment_overflow = 0

    # Handle overflow for each segment from right to left
    for j in range(len(ip_parts) - 1, 0, -1):
        if last_segment >= 256:
            last_segment_overflow = last_segment // 256
            last_segment %= 256
            ip_parts[j] = str(int(ip_parts[j]) + last_segment_overflow)
        else:
            break

    # Reset the last segment to the base value when it reaches 255
    ip_parts[-1] = str(last_segment % 256)

    # Increment the just left part if the last segment wrapped around
    if last_segment_overflow > 0:
        ip_parts[-2] = str(int(ip_parts[-2]) + last_segment_overflow)

    new_ip = '.'.join(ip_parts)

    # Increment numerical value for name and email
    name_suffix = last_name_suffix + i + 1
    email_suffix = last_email_suffix + i + 1

    # Prepare payload
    payload = {
        "name": f"{base_name}{name_suffix}",
        "email": f"{base_email}{email_suffix}@gmail.com",
        "verifiedMobile": str(mobile),
        "ip": new_ip,
        "location": "No Location Found",
        "entryId": "6575cb0405880f41d400244e",
    }

    # Send request
    response = requests.post(url, headers=headers, json=payload)

    # Display result and log
    print(f"Iteration {i+1}: Status Code {response.status_code}")
    print(f"Used mobile: {mobile}, Used IP: {new_ip}, Name: {base_name}{name_suffix}, Email: {base_email}{email_suffix}@gmail.com")

    # Sleep for a few seconds to avoid rate limiting or being blocked
    time.sleep(4)

# Save the last used suffixes for the next run
save_last_used_suffix(name_suffix_file, name_suffix)
save_last_used_suffix(email_suffix_file, email_suffix)
