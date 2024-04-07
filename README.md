# Roblox Video to Spritesheet converter
This converts a video to multiple spritesheets, and uploads them all to Roblox.

# Setup
Install requirements with:
```py
pip3 install -r requirements.txt
```

Open `.env` and set <i>V2S_UID</i> to your user id, and <i>V2S_KEY</i> to your Roblox API key

# Getting an API Key
1. Go to [Creator Hub >> Open Cloud >> API keys](https://create.roblox.com/dashboard/credentials?activeTab=ApiKeysTab)
2. Click "Create API Key" and put a name
3. Set Access Permisions to "Assets API", then give it Read and Write operations
4. Put in your IP Address in Accepted IP Addresses, or you can just put `0.0.0.0/0` for no protection.
5. Set your desired expiration, then press Save & Generate Key and copy it

# How to use
Run `convert.py`<br/>
Outputs: a lua file with a table of all the spritesheets, with columns, rows, and frames
