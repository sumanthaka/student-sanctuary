email: contactus.studentsanctuary@gmail.com
password: SS*CUcontactsanctuary


 db.announcements.find({'$or': [{'target': ['Everyone']}, {'target': {$in: ["BCom"]}}]}).sort({"created_at": 1})
