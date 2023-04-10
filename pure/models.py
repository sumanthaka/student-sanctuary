import pandas

from pure import client, cursor, bcrypt, login_manager, app, sql_client, engine
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
        self.course_faculty = None
        self.approved = ""
        self.verified = ""

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
            self.verified = user["verified"]
        elif self.user == "faculty":
            self.course_faculty = user["course_faculty"]
            self.approved = user["approved"]

    def update_user(self):
        if self.user == 'student':
            update_values = {'name': self.name, 'course': self.course}
        else:
            update_values = {'name': self.name}
        client[self.college]["user"].update_one({'_id': self.id}, {'$set': update_values})

    @staticmethod
    def check_existence(email, specific=False):
        databases = client.list_database_names()
        if specific:
            databases.remove("super_admin")
        for college in databases:
            if client[college]["user"].find_one({'email': email}):
                return True
        return False

    @staticmethod
    def get_data(email):
        databases = client.list_database_names()
        databases.remove('super_admin')
        for college in databases:
            user = client[college]["user"].find_one({'email': email})
            if user is not None:
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
        # courses = client[college]["info"].find_one({'courses': {'$exists': 'true'}}, {'courses': 1, '_id': 0})["courses"]
        courses = client[college]["courses"].find({}, {'course': 1, '_id': 0})
        courses = [course['course'] for course in courses]
        return courses

    def get_subjects(self, requested_semester, requested_course, req_id=False):
        # college_id = str(client[self.college]["info"].find_one({'email': {'$exists': 'true'}}, {'_id': 1})['_id'])
        # cursor.execute(f'SELECT * FROM {college_id}_subjects WHERE COURSE="{requested_course}";')
        # subjects = cursor.fetchall()
        # subjects = [subject[0] for subject in subjects]
        if req_id:
            subjects_query = client[self.college]["subjects"].find({'semester': int(requested_semester), 'course': requested_course}, {'subject': 1, '_id': 1})
            subjects = []
            for subject in subjects_query:
                subject['_id'] = str(subject['_id'])
                subjects.append(subject)
            return subjects
        subjects = client[self.college]["subjects"].find({'semester': int(requested_semester), 'course': requested_course}, {'subject': 1, '_id': 0})
        subjects = [subject["subject"] for subject in subjects]
        return subjects

    def get_duration(self, course):
        course_duration = client[self.college]["courses"].find_one({'course': course}, {'semesters': 1, '_id': 0})['semesters']
        return course_duration

    def get_current_sem(self, requested_course):
        current_sem = client[self.college]["courses"].find_one({'course': requested_course}, {'current_sem': 1, '_id': 0})["current_sem"]
        return current_sem

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
            # courses.extend(
            #     client[college]["info"].find_one({'courses': {'$exists': 'true'}}, {'courses': 1, '_id': 0})["courses"])
            courses_query = client[college]["courses"].find({}, {'course': 1, '_id': 0})
            course = [course['course'] for course in courses_query]
            courses.extend(course)
        return courses

    def get_permissions(self):
        return client[self.college]["info"].find_one({'roles': {'$exists': 'true'}}, {'_id': 0, 'roles': {'$elemMatch': {self.role: {'$exists': 'true'}}}})["roles"][0][self.role]

    def save_message(self, room_id, email, name, message):
        return client[self.college]["chat"].insert_one({'room_id': room_id, 'email': email, 'name': name, 'message': message})

    def get_messages(self, room_id):
        return list(client[self.college]["chat"].find({'room_id': room_id}, {'_id': 0, 'room_id': 0}))

    def get_logo(self):
        return client[self.college]["info"].find_one({'logo': {'$exists': 'true'}}, {'logo': 1, '_id': 0})['logo']


class Student(User):
    def create_user(self, name, email, college, course, password):
        college = college.replace(' ', '_')
        User.create_user(self, name=name, email=email, college=college, password=password, course=course, user="student", role="regular", verified=False)
        student = client[college]["user"].find_one({'email': email})
        return student

    @staticmethod
    def verify_student(user):
        client[user.college]["user"].update_one({'email': user.email}, {'$set': {'verified': True}})
        user.verified = True


class Faculty(User):
    def create_user(self, name, email, college, password):
        college.replace(' ', '_')
        User.create_user(self, name=name, email=email, college=college, password=password, course_faculty=None, subjects=[],user="faculty", approved=False)

    def get_course_student(self):
        student_list = client[self.college]["user"].find({'course': self.course_faculty, 'user': 'student'})
        student_list = [student for student in student_list]
        return student_list

    def upload_exam(self, exam_info, marks_file):
        exam_info.update({'course': self.course_faculty})
        exam_info.update({'date': datetime.now()})
        exam_info.update({'semester': self.get_current_sem(self.course_faculty)})
        exist = client[self.college]["exams"].find_one({'exam_name': exam_info['exam_name'], 'course': exam_info['course'], 'semester': exam_info['semester']})
        if exist:
            return [False, "Exam already exists"]
        marks_dataframe = pandas.read_excel(marks_file)
        headers = list(marks_dataframe.columns)
        if not headers[:2] == ['Name', 'Email']:
            return [False,
                    "Please check format(including CAPITAL LETTERS in headers!!) Please download template for correct format"]
        subjects = list(headers[2:])
        course_subjects = self.get_subjects(self.get_current_sem(self.course_faculty), self.course_faculty)
        subjects.sort()
        course_subjects.sort()
        if not subjects == course_subjects:
            return [False, "Subjects not matching with course, Please check format"]
        check = list(marks_dataframe.columns[2:])
        for col in check:
            if marks_dataframe[col].gt(exam_info["max_marks"][col]).any():
                return [False, "Marks inputted is greater than the given max marks"]
        client[self.college]["exams"].insert_one(exam_info)
        exam_id = str(client[self.college]["exams"].find_one(exam_info, {'_id': 1})['_id'])
        marks_dataframe.to_sql(name=exam_id, con=engine)
        return [True, "Successfully uploaded"]

    def get_exams(self, semester):
        raw_exams = client[self.college]["exams"].find({'semester': int(semester)})
        exam_list = [exam for exam in raw_exams]
        return exam_list

    def exam_sub_avg(self, exam_id):
        df = pandas.read_sql_table(exam_id, engine, index_col="index")
        title = client[self.college]["exams"].find_one({'_id': ObjectId(exam_id)})["exam_name"]
        average = df.mean(numeric_only=True).round()
        x = list(average.index)
        y = list(average.values)
        return x, y, title

    def student_all_marks(self, student_id, sem_val):
        stu_id = ObjectId(student_id)
        student_email = client[self.college]["user"].find_one({'_id': stu_id})["email"]
        exams = self.get_exams(sem_val)
        student_marks = []
        max_marks_list = []
        course_subjects = self.get_subjects(self.get_current_sem(self.course_faculty), self.course_faculty)
        columns = ['exam_id', 'exam_name'] + course_subjects
        for exam in exams:
            exam_id, exam_name, max_marks = exam['_id'], exam['exam_name'], exam['max_marks']
            sql_client.commit()
            cursor = sql_client.cursor()
            cursor.execute(f'SELECT * FROM {exam_id} WHERE EMAIL LIKE "{student_email}"')
            mark = cursor.fetchall()[0][3:]
            data = [exam_id, exam_name]
            for i in mark:
                data.append(i)
            max_marks = [max_marks.get(i) for i in max_marks.keys()]
            max_marks = sum(max_marks) / len(max_marks)
            max_marks_list.append(max_marks)
            student_marks.append(tuple(data))
        df = pandas.DataFrame(student_marks, columns=columns)
        x = list(df.columns[2:])
        y = {}
        df['average'] = df.mean(axis=1, numeric_only=True).round()
        df = df.fillna(0)
        average_list = list(df['average'])
        for i in range(len(average_list)):
            average_list[i] = average_list[i] / max_marks_list[i] * 100
        y.update({'exam_names': list(df['exam_name'])})
        y.update({'avg': average_list})
        y.update({'marks': df.iloc[:, 1:-1].values.tolist()})
        return x, y

    def get_faculty_subjects(self):
        subject_ids = client[self.college]["user"].find_one({'email': self.email}, {'subjects': 1, '_id': 0})['subjects']
        subjects = []
        for subject_id in subject_ids:
            subject = client[self.college]["subjects"].find_one({'_id': ObjectId(subject_id)}, {'subject': 1, '_id': 0})['subject']
            subjects.append([subject, subject_id])
        return subjects

    def get_course_students(self, course):
        students = client[self.college]["user"].find({'course': course, 'user': 'student'})
        students = [student for student in students]
        return students

class Admin(User):
    def get_student(self, email):
        return client[self.college]["user"].find_one({'email': email})

    def get_courses(self, duration=False):
        # courses = client[self.college]["info"].find_one({'courses': {'$exists': 'true'}}, {'courses': 1, '_id': 0})["courses"]
        courses = client[self.college]["courses"].find({}, {'course': 1, '_id': 0})
        courses = [course['course'] for course in courses]
        return courses

    def add_course(self, course_info):
        course = course_info[0] + course_info[1]
        course = course.upper()
        if course in self.get_courses():
            return False
        # client[self.college]["info"].update_one({'courses': {'$exists': 'true'}}, {'$push': {'courses': course}})
        client[self.college]["courses"].insert_one({'course': course, 'year': int(course_info[1]), 'semesters': int(course_info[2])*2, 'current_sem': 1})
        client[self.college]["info"].update_one({'room_ids': {'$exists': 'true'}}, {'$set': {f'room_ids.{course}': ObjectId()}})
        return True

    def delete_course(self, semester, course):
        # client[self.college]["info"].update_one({'courses': {'$exists': 'true'}}, {'$pull': {'courses': course}})
        client[self.college]["courses"].delete_one({'semester': semester, 'course': course})
        client[self.college]["info"].update_one({'room_ids': {'$exists': 'true'}},
                                                {'$unset': {f'room_ids.{course}': {'$exists': 'true'}}})

    def add_subject(self, subject, semester, course):
        subject = subject.upper()
        # college_id = str(client[self.college]["info"].find_one({'email': {'$exists': 'true'}}, {'_id': 1})['_id'])
        if subject in self.get_subjects(semester, course):
            return False
        # cursor.execute(f'INSERT INTO {college_id}_subjects VALUES("{subject}", "{course}");')
        # sql_client.commit()
        client[self.college]["subjects"].insert_one({'subject': subject, 'semester': int(semester), 'course': course})
        return True

    def delete_subject(self, semester, course, subject):
        # college_id = str(client[self.college]["info"].find_one({'email': {'$exists': 'true'}}, {'_id': 1})['_id'])
        # cursor.execute(f'DELETE FROM {college_id}_subjects WHERE SUBJECT="{subject}" AND COURSE="{course}";')
        # sql_client.commit()
        value = client[self.college]["subjects"].delete_one({'semester': int(semester), 'course': course, 'subject': subject})

    def get_unapproved_faculty_list(self):
        faculty_list = client[self.college]["user"].find({'user': 'faculty', 'approved': False})
        faculty_list = [faculty for faculty in faculty_list]
        return faculty_list

    def get_faculty_list(self):
        faculty_list = client[self.college]["user"].find({'user': 'faculty', 'approved': True})
        faculty_list = [faculty for faculty in faculty_list]
        return faculty_list

    def get_faculty_details(self, faculty_id):
        faculty = client[self.college]["user"].find_one({'_id': ObjectId(faculty_id)}, {'course_faculty': 1, 'subjects': 1, '_id': 0})
        subjects = []
        for subject_id in faculty['subjects']:
            subject = client[self.college]["subjects"].find_one({'_id': subject_id}, {'subject': 1, 'course': 1, '_id': 0})
            subjects.append([subject['subject'], subject['course'], str(subject_id)])
        faculty['subjects'] = subjects
        return faculty

    def get_all_subjects(self):
        subjects = client[self.college]["subjects"].find({})
        subjects = [subject for subject in subjects]
        return subjects

    def update_teacher(self, faculty_id, course, subjects):
        print(subjects)
        subjects = [ObjectId(subject) for subject in subjects]
        client[self.college]["user"].update_one({'_id': ObjectId(faculty_id)}, {'$set': {'course_faculty': course, 'subjects': subjects}})
        return True

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
    def create_college(college, email, name, mobile, password, path):
        college = college.lower().replace(' ', '_')
        if User.check_existence(email):
            return False
        if college in client.list_database_names():
            return False
        else:
            db = client[college]
            collection = db["info"]
            collection.insert_one({'email': email, 'name': name, 'mobile': mobile, 'logo': path})
            college_id = collection.find_one({'email': email})['_id']
            collection.insert_one({'roles': [{'cr': ['announcement_maker']}, {'regular': []}]})
            collection.insert_one({'courses': []})
            collection.insert_one({'room_ids': {}, 'faculty_room': ObjectId(), 'student_council_room': ObjectId()})
            collection = db["user"]
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            collection.insert_one({"name": name, "email": email, "college": college,
                                   "password": password,
                                   "user": "admin"})
            cursor.execute(f'CREATE TABLE {college_id}_subjects(SUBJECT VARCHAR(80), COURSE VARCHAR(80))')
            sql_client.commit()
            admin = collection.find_one({'email': email})
            return admin

    @staticmethod
    def remove_college(college):
        exam_ids = client[college]["exams"].find({}, {'_id': 1})
        for exam in exam_ids:
            exam_table = exam['_id']
            cursor.execute(f'DROP TABLE {exam_table}')
            sql_client.commit()
        college_id = client[college]["info"].find_one({'email': {'$exists': 'true'}}, {'_id': 1})['_id']
        cursor.execute(f'DROP TABLE {college_id}_subjects')
        sql_client.commit()
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
    def get_room_id_course_faculty(college, email):
        course = client[college]["user"].find_one({'email': email})['course_faculty']
        room_id = client[college]["info"].find_one({f'room_ids.{course}': {'$exists': 'true'}}, {'room_ids': 1, '_id': 0})['room_ids'][course]
        return str(room_id)

    @staticmethod
    def get_room_id_college(college):
        room_id = client[college]["info"].find_one({'room_ids': {'$exists': 'true'}})['_id']
        return str(room_id)

    @staticmethod
    def get_room_id_faculty(college):
        room_id = client[college]["info"].find_one({'faculty_room': {'$exists': 'true'}}, {'_id': 0, 'faculty_room': 1})['faculty_room']
        return str(room_id)

    @staticmethod
    def get_room_id_council(college):
        room_id = client[college]["info"].find_one({'student_council_room': {'$exists': 'true'}}, {'_id': 0, 'student_council_room': 1})['student_council_room']
        return str(room_id)


class Study_material:
    @staticmethod
    def upload_notes(college, file_info):
        file_info['subject_id'] = ObjectId(file_info['subject_id'])
        file_info.update({'date': datetime.now()})
        client[college]["notes"].insert_one(file_info)

    @staticmethod
    def get_notes(college, subject):
        notes = client[college]["notes"].find({'subject_id': ObjectId(subject)})
        new_notes = []
        for note in notes:
            note['_id'] = str(note['_id'])
            del note['subject_id']
            new_notes.append(note)
        return new_notes

    @staticmethod
    def get_notes_path(college, note_id):
        path = client[college]["notes"].find_one({'_id': ObjectId(note_id)}, {'path': 1, '_id': 0})['path']
        return path

    @staticmethod
    def delete_notes(college, note_id):
        path = client[college]["notes"].find_one({'_id': ObjectId(note_id)}, {'path': 1, '_id': 0})['path']
        client[college]["notes"].delete_one({'_id': ObjectId(note_id)})
        return path


class Event:
    def __init__(self, title, desc, date, participants, paths, author):
        self.title = title
        self.desc = desc
        self.date = datetime.combine(date, datetime.min.time())
        self.participants = participants
        self.paths = paths
        self.author = author

    def create_event(self, college):
        client[college]["events"].insert_one({'title': self.title,
                                              'desc': self.desc,
                                              'date': self.date,
                                              'participants': self.participants,
                                              'paths': self.paths,
                                              'author': self.author})

    @staticmethod
    def get_events(college, author):
        events = client[college]["events"].find({'author': author}).sort("date", -1)
        events_temp = []
        for event in events:
            event['date'] = datetime.date(event['date'])
            events_temp.append(event)
        return events_temp

    @staticmethod
    def get_event(college, event_id):
        event = client[college]["events"].find_one({'_id': ObjectId(event_id)})
        event['date'] = datetime.date(event['date'])
        return event

    @staticmethod
    def delete_event(college, event_id):
        print(event_id)
        images = client[college]["events"].find_one({'_id': ObjectId(event_id)}, {'paths': 1, '_id': 0})['paths']
        print(images)
        client[college]["events"].delete_one({'_id': ObjectId(event_id)})
        return images


class Feedback:
    pass