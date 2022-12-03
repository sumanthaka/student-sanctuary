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
            if college != "super_admin":
                if user["user"] == "student":
                    curr_user = Student()
                    curr_user.set_object(user["email"])
                elif user["user"] == "faculty":
                    curr_user = Faculty()
                    curr_user.set_object(user["email"])
                elif user["user"] == "admin":
                    curr_user = Admin()
                    curr_user.set_object(user["email"])
            else:
                curr_user = Super_Admin(user["email"])
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
            self.approved = user["approved"]

    def update_user(self):
        if self.user == 'student':
            update_values = {'name': self.name, 'course': self.course}
        else:
            update_values = {'name': self.name}
        client[self.college]["user"].update_one({'_id': self.id}, {'$set': update_values})

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
        college = college.replace(' ', '_')
        courses = client[college]["info"].find_one({'courses': {'$exists': 'true'}}, {'courses': 1, '_id': 0})["courses"]
        return courses

    @staticmethod
    def get_colleges():
        colleges = client.list_database_names()
        colleges.remove('admin')
        colleges.remove('local')
        colleges.remove('config')
        colleges.remove('super_admin')
        return [college.replace('_', ' ') for college in colleges]

    @staticmethod
    def get_all_courses():
        colleges = client.list_database_names()
        colleges.remove('admin')
        colleges.remove('local')
        colleges.remove('config')
        colleges.remove('super_admin')
        courses = []
        for college in colleges:
            courses.extend(
                client[college]["info"].find_one({'courses': {'$exists': 'true'}}, {'courses': 1, '_id': 0})["courses"])
        return courses

    def get_permissions(self):
        return client[self.college]["info"].find_one({'roles': {'$exists': 'true'}}, {'_id': 0, 'roles': {'$elemMatch': {self.role: {'$exists': 'true'}}}})["roles"][0][self.role]

    def save_message(self, room_id, email, name, message):
        return client[self.college]["chat"].insert_one({'room_id': room_id, 'email': email, 'name': name, 'message': message})

    def get_messages(self, room_id):
        return list(client[self.college]["chat"].find({'room_id': room_id}, {'_id': 0, 'room_id': 0}))


class Student(User):
    def create_user(self, name, email, college, course, password):
        User.create_user(self, name=name, email=email, college=college, password=password, course=course, user="student", role="regular")


class Faculty(User):
    def create_user(self, name, email, college, qualification, password):
        User.create_user(self, name=name, email=email, college=college, qualification=qualification, password=password, user="faculty", approved=False)


class Admin(User):
    def get_student(self, email):
        return client[self.college]["user"].find_one({'email': email})

    def get_courses(self):
        courses = client[self.college]["info"].find_one({'courses': {'$exists': 'true'}}, {'courses': 1, '_id': 0})["courses"]
        return courses

    def add_course(self, course):
        client[self.college]["info"].update_one({'courses': {'$exists': 'true'}}, {'$push': {'courses': course}})
        client[self.college]["info"].update_one({'room_ids': {'$exists': 'true'}}, {'$set': {f'room_ids.{course}': ObjectId()}})

    def delete_course(self, course):
        client[self.college]["info"].update_one({'courses': {'$exists': 'true'}}, {'$pull': {'courses': course}})
        client[self.college]["info"].update_one({'room_ids': {'$exists': 'true'}},
                                                {'$unset': {f'room_ids.{course}': {'$exists': 'true'}}})

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
            {'$and': [{'role': {'$ne': 'cr'}}, {'role': {'$ne': 'regular'}}, {'role': {'$exists': 'true'}}]},
            {'email': 1, 'name': 1, 'role': 1, 'course': 1, '_id': 0})
        candidates = [candidate for candidate in candidates]
        return candidates

    def get_crs(self, course):
        crs = client[self.college]["user"].find_one(
            {'$and': [{'role': {'$exists': 'true'}}, {'role': 'cr'}, {'course': course}]},
            {'email': 1, 'name': 1, '_id': 0}
        )
        if crs is None:
            return {'name': None, 'email': None}
        else:
            return crs
    
    def create_role(self, role_name, role_perm):
        print(role_perm)
        role_name = role_name.lower().replace(' ', '_')
        check_role = client[self.college]["info"].find_one({f'roles.{role_name}': {'$exists': 'true'}}, {'roles': 1, '_id': 0})
        if check_role is None:
            client[self.college]["info"].update_one({'roles': {'$exists': 'true'}},
                                                    {'$push': {'roles': {role_name: role_perm}}})
            return True
        return False

    def delete_role(self, role_name):
        role_name = role_name.lower().replace(' ', '_')
        client[self.college]["info"].update_one({'roles': {'$exists': 'true'}},
                                                {'$pull': {'roles': {role_name: {'$exists': 'true'}}}})

    def change_role(self, email):
        client[self.college]["user"].update_one({'email': email}, {'$set': {'role': "regular"}})

    def assign_role(self, email, role):
        candidate = client[self.college]["user"].find_one({'email': email})
        if candidate["user"] != "student":
            return False
        else:
            client[self.college]["user"].update_one({'email': email}, {'$set': {'role': role}})


class Super_Admin(UserMixin):
    def __init__(self, email):
        user = client["super_admin"]["user"].find_one({'email': email})
        if user is not None:
            self.id = user["_id"]
            self.name = user["name"]
            self.email = email
        else:
            self.id = ""

    def check_password(self, password):
        hash_password = client["super_admin"]["user"].find_one({'email': self.email})
        if hash_password is not None:
            hash_password = hash_password["password"]
        return bcrypt.check_password_hash(hash_password, password)

    @staticmethod
    def create_college(college, email, name, mobile, password):
        college = college.lower().replace(' ', '_')
        if User.check_existence(email):
            return False
        if college in client.list_database_names():
            return False
        else:
            db = client[college]
            collection = db["info"]
            collection.insert_one({'email': email, 'name': name, 'mobile': mobile})
            collection.insert_one({'roles': [{'cr': ['announcement_maker']}, {'regular': []}]})
            collection.insert_one({'courses': []})
            collection.insert_one({'room_ids': {}, 'faculty_room': ObjectId(), 'student_council_room': ObjectId()})
            collection = db["user"]
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            collection.insert_one({"name": name, "email": email, "college": college,
                                   "password": password,
                                   "user": "admin"})
            admin = collection.find_one({'email': email})
            return admin

    @staticmethod
    def remove_college(college):
        client.drop_database(college)

    @staticmethod
    def get_colleges():
        colleges = client.list_database_names()
        colleges_info = []
        for college in colleges:
            college_info = client[college]["info"].find_one({"email": {'$exists': 'true'}}, {"_id": 0})
            if college_info is None:
                continue
            colleges_info.append({college: college_info})
        return colleges_info


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

    @staticmethod
    def get_announcements(college, user, course):
        if user == 'admin':
            announcements = client[college]["announcements"].find().sort("date", -1)
        elif user == 'student':
            announcements = client[college]["announcements"].find({'$or': [{'target': ['Everyone']}, {'target': {'$in': [course]}}]}).sort("date", -1)
        elif user == 'faculty':
            announcements = client[college]["announcements"].find({'$or': [{'target': ['Everyone']}, {'target': ['All Faculty']}]}).sort("date", -1)
        announcements = [announcement for announcement in announcements]
        return announcements

    @staticmethod
    def get_user_announcements(college, email=None):
        if email is None:
            return client[college]["announcements"].find().sort("date", -1)
        else:
            return client[college]["announcements"].find({'author.0': email}).sort("date", -1)

    @staticmethod
    def delete_announcement(college, data):
        client[college]["announcements"].delete_one({'_id': ObjectId(str(data)[2:-1])})


class Chat:
    @staticmethod
    def get_room_id_course(college, email):
        course = client[college]["user"].find_one({'email': email})['course']
        room_id = client[college]["info"].find_one({f'room_ids.{course}': {'$exists': 'true'}}, {'room_ids': 1, '_id': 0})['room_ids'][course]
        return str(room_id)

    @staticmethod
    def get_room_id_college(college):
        room_id = client[college]["info"].find_one({'room_ids': {'$exists': 'true'}})['_id']
        return str(room_id)

    @staticmethod
    def get_room_id_faculty(college):
        room_id = client[college]["info"].find_one({'faculty_room': {'$exists': 'true'}}, {'_id': 0, 'faculty_room': 1})
        return str(room_id)

    @staticmethod
    def get_room_id_council(college):
        room_id = client[college]["info"].find_one({'student_council_room': {'$exists': 'true'}}, {'_id': 0, 'student_council_room': 1})
        return str(room_id)