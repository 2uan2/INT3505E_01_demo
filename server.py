from flask import Flask, jsonify, abort

app = Flask(__name__)

students = {
    "22028250": {"name": "Alice Smith", "gpa": 3.85, "major": "Computer Science"},
    "22029101": {"name": "Bob Johnson", "gpa": 3.10, "major": "Mathematics"},
    "22030555": {"name": "Charlie Brown", "gpa": 4.00, "major": "Physics"}
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
