# AI School Companion Application

# This application serves as a school companion integrating authentication and lesson management features.

class SchoolCompanion:
    def __init__(self):
        self.lessons = []
        self.users = {}

    def add_lesson(self, lesson_name):
        self.lessons.append(lesson_name)
        print(f"Lesson '{lesson_name}' added.")

    def register_user(self, username):
        if username not in self.users:
            self.users[username] = []
            print(f"User '{username}' registered.")
        else:
            print(f"User '{username}' already exists.")

# Sample usage
if __name__ == '__main__':
    app = SchoolCompanion()
    app.register_user('john_doe')
    app.add_lesson('Mathematics 101')
