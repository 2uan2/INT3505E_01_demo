from flask import Flask, jsonify, abort, request

app = Flask(__name__)

students = {
    "22028250": {"name": "Quan", "gpa": 3.85, "major": "Physics"},
    "22029101": {"name": "Vu", "gpa": 3.10, "major": "Mathematics"},
    "10000000": {"name": "Le Khanh Trinh", "gpa": 4.00, "major": "Computer Science"}
}

@app.route('/api/students/<string:student_id>', methods=['GET'])
def get_student_info(student_id):
    student = students.get(student_id)
    
    if student is None:
        abort(404, description="Student ID not found")
    
    return jsonify({
        "student_id": student_id,
        "name": student["name"],
        "gpa": student["gpa"],
        "major": student["major"]
    })

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.json
    required_fields = ['student_id', 'name', 'gpa', 'major']
    
    if not data or any(f not in data for f in required_fields):
        abort(400)
    
    new_id = data['student_id']
    if new_id in students:
        abort(409, description="Student ID already exists")

    new_student_data = {
        'name': data['name'],
        'gpa': data['gpa'],
        'major': data['major']
    }
    
    students[new_id] = new_student_data
    return jsonify({"student_id": new_id, **new_student_data}), 201

@app.route('/api/students/<string:student_id>', methods=['PUT'])
def update_student_full(student_id):
    if student_id not in students:
        abort(404)
    
    data = request.json
    required_fields = ['name', 'gpa', 'major']
    
    if not data or any(f not in data for f in required_fields):
        abort(400)
        
    students[student_id] = {
        'name': data['name'],
        'gpa': data['gpa'],
        'major': data['major']
    }
    
    return jsonify({"student_id": student_id, **students[student_id]}), 200

@app.route('/api/students/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    if student_id not in students:
        abort(404)
        
    del students[student_id]
    
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
