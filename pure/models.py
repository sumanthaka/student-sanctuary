from pure import client, bcrypt, login_manager, app
from flask_login import UserMixin
from bson import ObjectId
from itsdangerous import URLSafeTimedSerializer as Serializer
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    for college in client.list_database_names():
        user = client[college]["user"].find_one({'_id': ObjectId(user_id)})
        if user is not None:
            curr_user = None
            if user["user"] == "student":
                curr_user = Student()
                curr_user.set_object(user["email"])
            elif user["user"] == "faculty":
                curr_user = Faculty()
                curr_user.set_object(user["email"])
            elif user["user"] == "admin":
                curr_user = Admin()
                curr_user.set_object(user["email"])
            return curr_user


class User(UserMixin):
    def __init__(self):
        self.id = ""
        self.name = ""
        self.email = ""
        self.college = ""
        self.password = ""
        self.user = ""
        self.role = ""
        self.course = ""
        self.qualification = ""
        self.approved = ""

    def create_user(self, **kwargs):
        kwargs["password"] = bcrypt.generate_password_hash(kwargs["password"]).decode('utf8')
        college = kwargs["college"].replace(' ', '_')
        db = client[college]
        db["user"].insert_one(kwargs)

    def set_object(self, email):
        user = None
        for college in client.list_database_names():
            if user is not None:
                break
            user = client[college]["user"].find_one({'email': email})
        self.id = user["_id"]
        self.name = user["name"]
        self.email = user["email"]
        self.college = user["college"].replace(' ', '_')
        self.password = user["password"]
        self.user = user["user"]
        if self.user == "student":
            self.course = user["course"]
            self.role = user["role"]
        elif self.user == "faculty":
            self.qualification = user["qualification"]
            self.role = user["role"]
            self.approved = user["approved"]

    @staticmethod
    def check_existence(email):
        for college in client.list_database_names():
            if client[college]["user"].find_one({'email': email}):
                return True
        return False

    @staticmethod
    def get_data(email):
        for college in client.list_database_names():
            user = client[college]["user"].find_one({'email': email})
            if user:
                return user
        return None

    def set_password(self, email, college):
        college = college.replace(' ', '_')
        client[college]["user"].update_one({'email': email}, {'$set': {'password': self.password}})

    def check_password(self, email, password):
        hash_password = None
        for college in client.list_database_names():
            hash_password = client[college]["user"].find_one({'email': email})
            if hash_password is not None:
                hash_password = hash_password["password"]
                break
        return bcrypt.check_password_hash(hash_password, password)

    @staticmethod
    def get_reset_token(user):
        serial = Serializer(app.config['SECRET_KEY'])
        return serial.dumps({'user_id': str(user['_id'])})

    @staticmethod
    def verify_reset_token(token, expires_in=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, expires_in)['user_id']
        except:
            return None
        for college in client.list_database_names():
            user = client[college]["user"].find_one({'_id': ObjectId(user_id)})
            if user:
                req_user = User()
                req_user.set_object(user["email"])
                return req_user

    @staticmethod
    def get_courses(college):
        courses = client[college]["info"].find_one({'courses': {'$exists': 'true'}}, {'courses': 1, '_id': 0})["courses"]
        return courses

    @staticmethod
    def get_colleges():
        colleges = client.list_database_names()
        colleges.remove('admin')
        colleges.remove('local')
        colleges.remove('config')
        return [college.replace('_', ' ') for college in colleges]


class Student(User):
    def create_user(self, name, email, college, course, password):
        User.create_user(self, name=name, email=email, college=college, password=password, course=course, user="student", role="regular")


class Faculty(User):
    def create_user(self, name, email, college, qualification, password):
        User.create_user(self, name=name, email=email, college=college, qualification=qualification, password=password, user="faculty", role="regular", approved=False)


class Admin(User):
    def get_courses(self):
        courses = client[self.college]["info"].find_one({'courses': {'$exists': 'true'}}, {'courses': 1, '_id': 0})["courses"]
        return courses

    def add_course(self, course):
        client[self.college]["info"].update_one({'courses': {'$exists': 'true'}}, {'$push': {'courses': course}})

    def delete_course(self, course):
        client[self.college]["info"].update_one({'courses': {'$exists': 'true'}}, {'$pull': {'courses': course}})

    def get_faculty_list(self):
        faculty_list = client[self.college]["user"].find({'user': 'faculty', 'approved': False})
        faculty_list = [faculty for faculty in faculty_list]
        return faculty_list

    def approve_faculty(self, email):
        client[self.college]["user"].update_one({'user': 'faculty', 'email': email}, {'$set': {'approved': True}})

    def reject_faculty(self, email):
        client[self.college]["user"].delete_one({'user': 'faculty', 'email': email})

    def get_roles(self):
        return client[self.college]["info"].find_one({'roles': {'$exists': 'true'}}, {'roles': 1, '_id': 0})["roles"]

    def get_candidates(self):
        candidates = client[self.college]["user"].find(
            {'$and': [{'role': {'$ne': 'regular'}}, {'role': {'$exists': 'true'}}]},
            {'email': 1, 'name': 1, 'role': 1, '_id': 0})
        candidates = [candidate for candidate in candidates]
        return candidates
    
    def create_role(self, role_name, role_perm):
        role_name = role_name.lower()
        check_role = client[self.college]["info"].find_one({f'roles.{role_name}': {'$exists': 'true'}}, {'roles': 1, '_id': 0})
        if check_role is None:
            client[self.college]["info"].update_one({'roles': {'$exists': 'true'}},
                                                    {'$push': {'roles': {role_name: role_perm}}})
            return True
        return False

    def delete_role(self, role_name):
        role_name = role_name.lower()
        client[self.college]["info"].update_one({'roles': {'$exists': 'true'}},
                                                {'$pull': {'roles': {role_name: {'$exists': 'true'}}}})

    def change_role(self, email):
        client[self.college]["user"].update_one({'email': email}, {'$set': {'role': "regular"}})

    def assign_role(self, email, role):
        client[self.college]["user"].update_one({'email': email}, {'$set': {'role': role}})


class Announcement:
    def __init__(self, author, target, title, subject, desc):
        self.author = author
        self.target = target
        self.title = title
        self.subject = subject
        self.desc = desc

    def create_announcement(self, college):
        client[college]["announcements"].insert_one({'author': self.author,
                                                     'date': datetime.now(),
                                                     'target': self.target,
                                                     'title': self.title,
                                                     'subject': self.subject,
                                                     'desc': self.desc})
