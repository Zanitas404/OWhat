import requests
import base64
from impacket.ntlm import NTLMAuthChallenge
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Replace these values with your own

host = "https://example.com"

endpoints = ['/aspnet_client',
      '/Autodiscover',
      '/ecp',
      '/EWS',
      '/Microsoft-Server-ActiveSync',
      '/OAB',
      '/PowerShell',
      '/Rpc']


headers = {"Authorization" : "NTLM TlRMTVNTUAABAAAAB4IIogAAAAAAAAAAAAAAAAAAAAAGAbEdAAAADw=="}

try:
    for endpoint in endpoints:
        url = host + endpoint
        response = requests.get(url, headers=headers, verify=False)

        if 'WWW-Authenticate' not in response.headers:
            continue

        if 'NTLM' not in response.headers["WWW-Authenticate"]:
            continue

        ntlm_header = response.headers.get('WWW-Authenticate', '')
        ntlm_base64 = ntlm_header.split(" ")[1]
        ntlm_bytes = base64.b64decode(ntlm_base64)


        challenge_message = NTLMAuthChallenge()
        challenge_message.fromString(ntlm_bytes)
        domain = challenge_message.fields['domain_name'].decode('utf-16-le')
        print(f"[*] Windows Domain: {domain}")
        break

except Exception as e:
    print(f"An error occurred: {e}")
