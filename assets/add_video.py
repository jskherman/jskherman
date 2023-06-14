import http.client
import json
import os
import re

# Load Access Token
token = os.environ.get("ACCESS_TOKEN")

# Create an HTTP connection to the host
conn = http.client.HTTPSConnection("botsin.space")

# Prepare the Authentication headers
headers = {"Authorization": f"Bearer {token}"}

# Prepare the query parameters
params = {
    "only_media": "true",
    "exclude_replies": "true",
    "exclude_reblogs": "true",
    "limit": "1",
}

# Build the URL with the query parameters
url = "/api/v1/accounts/109344207892656199/statuses?" + "&".join(
    [f"{key}={value}" for key, value in params.items()]
)

# Send the GET request
conn.request("GET", url, headers=headers)

# Get the response from the server
response = conn.getresponse()

# Print the response status code
print("Response Status:", response.status, ("OK" if (response.status == 200) else ""))

# Get and parse the response body
body = response.read()
data = json.loads(body.decode())

# Save video URL
video_url = data[0]["media_attachments"][0]["url"]

# Close the connection
conn.close()

# Define the file path
script_path = os.path.abspath(__file__)
readme_path = os.path.join(os.path.dirname(script_path), "..", "README.md")

# Read the contents of the file
with open(readme_path, "r") as file:
    content = file.read()

# Find the target string
string = '<!-- THREE-BODY-LIST:START -->\n<video type="mp4" height="100%" src="'
target_string = (
    r'<!-- THREE-BODY-LIST:START -->\n<video type="mp4" height="100%" src=".*'
)

# Define replacement string
replacement = string + video_url + '" autoplay controls loop>'

# Perform the replacement
modified_content = re.sub(target_string, replacement, content)

# Write the modified content back to the file
with open(readme_path, "w") as file:
    file.write(modified_content)

print("Replacement completed.")
