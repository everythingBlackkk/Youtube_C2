# YouTube C2 Server
![ph1](https://github.com/everythingBlackkk/Youtube_C2/blob/main/Media/C4.png?raw=true)


![ph2](https://github.com/everythingBlackkk/Youtube_C2/blob/main/Media/End.png?raw=true)


# Full Writeups : [C2 Server Via YouTube](https://medium.com/@snpxblack2006/c2-server-via-youtube-0564f023bc3e)
## Overview

YouTube Command Executor is an advanced security tool that allows for remote command execution through YouTube comments. This tool is designed for security research and testing purposes.

## Features

- Monitor YouTube video comments for encoded commands
- Execute system commands received through comments
- RSA encryption for secure output transmission
- OAuth authentication with YouTube API

## Dependencies

```
pip install google-api-python-client google-auth-oauthlib google-auth rsa
```

## Configuration

Before using the tool, you need to:

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Download the `client_secrets.json` file
5. Set your YouTube API key and video ID in the script
6. Generate an RSA key pair and update the public key in the script

## Usage

1. Set up the required configuration files
2. Run the script:

```bash
python NoTube.py
```

![ph3](https://github.com/everythingBlackkk/Youtube_C2/blob/main/Media/C1.png?raw=true)



3. The tool will monitor comments on the specified YouTube video
4. To execute a command, post a comment on the video with the format:
   ```
   run:base64_encoded_command
   ```
5. The tool will decode the command, execute it, and post the encrypted output as a new comment

##  Disclaimer

This tool is intended for educational and security research purposes only. Unauthorized use to gain access to systems without permission is illegal and unethical. The author and contributors take no responsibility for misuse of this software.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
