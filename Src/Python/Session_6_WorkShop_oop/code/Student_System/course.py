from student import Student
class Course:
    _id_counter = 1

    def __init__(self, name):
        self.course_id = Course._id_counter
        Course._id_counter +=1
        self.name = name
        self.enrolled_students =[]

    def __str__(self):
        return f"Course ID : {self.course_id}, Name : {self.name}, Enrolled Students : {len(self.enrolled_students)}"

    def __repr__(self):
        return f"Course ID : {self.course_id}, Name : {self.name}, Enrolled Students : {len(self.enrolled_students)}"

    def enroll_student(self, student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
            print(f"student {student.name} enrolled in {self.name}")
        else:
            print(f"student is already enrolled in {self.name}")

    def remove_student(self, student):
        if student in self.enrolled_students:
            self.enrolled_students.remove(student)
            print(f"student {student.name} remove from {self.name}")
        else:
            print(f"student is not enrolled in {self.name}")

