import sqlite3
import os

DB_FILE = 'faq_database.db'

def get_db_connection():
    """Establish and return a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # Returns dictionary-like rows
    return conn

def init_db():
    """Create the FAQs table and insert sample data if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            keywords TEXT NOT NULL,
            policy_section TEXT NOT NULL
        )
    ''')
    
    # Check if we need to seed the database
    cursor.execute('SELECT COUNT(*) FROM faqs')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # 20 Sample University FAQs
        sample_faqs = [
            ("Leave of Absence", "How do I apply for LOA?", "Students must submit a Leave of Absence form through the Registrar's Office signed by their department head.", "apply loa leave absence break", "Section 4.2"),
            ("Enrollment", "What are the enrollment requirements?", "You need your clearance, previous semester grades, and advising slip.", "enrollment requirements enroll register", "Section 1.1"),
            ("Tuition Payment", "Where can I pay my tuition?", "Tuition can be paid at the Cashier's Office or via partnered online banking apps.", "tuition pay payment cashier money fee", "Section 3.4"),
            ("Scholarships", "How do I apply for a scholarship?", "Submit the Financial Aid application form along with your latest Income Tax Return to the OSAS.", "scholarship financial aid discount apply", "Section 5.1"),
            ("Student ID", "How do I replace a lost student ID?", "Provide an Affidavit of Loss and pay the replacement fee at the accounting office.", "id student identification lost replace card", "Section 7.3"),
            ("Transcript Requests", "How do I request my Transcript of Records (TOR)?", "Fill out the TOR request form at the Registrar. Processing takes 5-7 working days.", "transcript records tor request grades", "Section 2.5"),
            ("Graduation", "What are the requirements for graduation?", "Completion of all academic units, NSTP, PE, and a cleared university account.", "graduation graduate requirements march toga", "Section 8.0"),
            ("Clearance", "How do I get my clearance?", "Clearance is processed online via the Student Portal at the end of each semester.", "clearance clear account semester end", "Section 1.5"),
            ("Library", "How do I borrow a book from the library?", "Present your validated student ID to the librarian. You can borrow up to 3 books for one week.", "library borrow book read study", "Section 9.2"),
            ("Student Portal", "I forgot my student portal password, what do I do?", "Click 'Forgot Password' on the login page or visit the IT Helpdesk for a manual reset.", "portal password account login reset it", "Section 10.1"),
            ("Internship", "When can I start my internship or OJT?", "Internships are typically taken during the summer semester before your senior year.", "internship ojt practicum work training", "Section 6.4"),
            ("Shifting Courses", "How do I shift to another degree program?", "Secure a shifting form, get approval from both your current and target Deans, and meet the GPA requirement.", "shift shifting course program change degree", "Section 4.5"),
            ("Dropping Subjects", "What is the deadline for dropping subjects?", "Subjects must be dropped before the midterm examination week to avoid a failing grade.", "drop dropping subjects withdraw remove", "Section 4.7"),
            ("Adding Subjects", "Can I still add subjects?", "Adding of subjects is only allowed during the first two weeks of regular classes.", "add adding subjects extra load", "Section 4.6"),
            ("Academic Probation", "What happens if I fail my classes?", "Students failing more than 30% of their total units will be placed on academic probation.", "fail failing academic probation warning grades", "Section 5.5"),
            ("Class Schedule", "Where can I view my class schedule?", "Your official schedule is available on the Student Portal under the 'My Schedule' tab.", "class schedule time room room assignment", "Section 1.2"),
            ("Student Organizations", "How do I join a student organization?", "Attend the Org Recruitment Week usually held during the second week of the first semester.", "organization org club join extracurricular", "Section 11.0"),
            ("Dormitory", "Does the university provide dormitories?", "Yes, on-campus housing is available. Applications open a month before the semester starts.", "dormitory dorm housing sleep live campus", "Section 12.3"),
            ("Registrar Services", "What are the registrar office hours?", "The Registrar's Office is open Monday to Friday, 8:00 AM to 5:00 PM.", "registrar office hours open close time", "Section 2.1"),
            ("Grading System", "What is the university grading system?", "The university uses a 1.0 (Excellent) to 5.0 (Fail) grading system.", "grade grading system pass fail score", "Section 5.0")
        ]
        
        cursor.executemany('''
            INSERT INTO faqs (title, question, answer, keywords, policy_section)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_faqs)
        conn.commit()
    
    conn.close()

def get_all_faqs():
    conn = get_db_connection()
    faqs = conn.execute('SELECT * FROM faqs').fetchall()
    conn.close()
    return [dict(ix) for ix in faqs]

def get_faq_by_id(faq_id):
    conn = get_db_connection()
    faq = conn.execute('SELECT * FROM faqs WHERE id = ?', (faq_id,)).fetchone()
    conn.close()
    return dict(faq) if faq else None

def add_faq(title, question, answer, keywords, policy_section):
    conn = get_db_connection()
    conn.execute('INSERT INTO faqs (title, question, answer, keywords, policy_section) VALUES (?, ?, ?, ?, ?)',
                 (title, question, answer, keywords, policy_section))
    conn.commit()
    conn.close()

def update_faq(faq_id, title, question, answer, keywords, policy_section):
    conn = get_db_connection()
    conn.execute('''UPDATE faqs SET title = ?, question = ?, answer = ?, keywords = ?, policy_section = ? WHERE id = ?''',
                 (title, question, answer, keywords, policy_section, faq_id))
    conn.commit()
    conn.close()

def delete_faq(faq_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM faqs WHERE id = ?', (faq_id,))
    conn.commit()
    conn.close()
    