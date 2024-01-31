# Roblox Video to Spritesheet converter
This converts a video to multiple spritesheets, and uploads them all to Roblox.

# Setup
Open `spriter.py` and set <i>id</i> to your user id, and <i>key</i> to your Roblox API key

# How to get an API key
1. Go to [Creator Hub >> Open Cloud >> API keys](https://create.roblox.com/dashboard/credentials?activeTab=ApiKeysTab)
2. Click "Create API Key" and put a name
3. Set Access Permisions to "Assets API", then give it Read and Write operations
4. Put in your IP Address in Accepted IP Addresses, or you can just put `0.0.0.0/0` for no protection.
5. Set your desired expiration, then press Save & Generate Key and copy it

# How to use
Run `convert.sh`<br/>
Args: video (must be in current dir), segment length (in seconds), fps, video width (resolution)<br/>
Outputs: a lua file with a table of all the spritesheets, with columns, rows, and frames