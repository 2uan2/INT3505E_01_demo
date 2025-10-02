import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api/students'

def get_student(student_id):
    url = f"{BASE_URL}/{student_id}"
    print(f"\n--- Requesting Student ID: {student_id} ---")
    
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Data Received:")
        print(json.dumps(data, indent=4))
    elif response.status_code == 404:
        print(f"Error: {response.json().get('description')}")
    else:
        print("An unexpected error occurred.")
        print(response.text)

if __name__ == '__main__':
    get_student("22028250")
    
    get_student("22030555")

