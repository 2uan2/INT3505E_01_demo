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
    else:
        print("An unexpected error occurred.")

def create_student(student_id, name, gpa, major):
    url = f"{BASE_URL}"
    print(f"\n--- Creating Student ID: {student_id} ---")
    
    data  = {
        "student_id": student_id,
        "name": name,
        "gpa": gpa,
        "major": major 
    }
    response = requests.post(url, json=data)

    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        print("SUCCESS: Student record created.")
        print(json.dumps(response.json(), indent=4))
    elif response.status_code == 400:
        print("FAILED: Bad Request (Status 400). Missing required fields.")
        print(f"Server response: {response.text}")
    elif response.status_code == 409:
        print("FAILED: Conflict (Status 409). Student ID already exists.")
        print(f"Server response: {response.json().get('description')}")
    else:
        print(f"Unexpected error (Status {response.status_code}).")
        print(f"Response: {response.text}")


if __name__ == '__main__':
    get_student("22028250")

    create_student("10000001", "Nam", "4.0", "CS")
    get_student("10000001")
    
    get_student("22030555")
    get_student("3324239")

