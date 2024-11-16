import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('student_info.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                grade TEXT,
                email TEXT)''')

conn.commit()
conn.close()
import streamlit as st
import sqlite3

# Database connection
def get_db_connection():
    conn = sqlite3.connect('student_info.db')
    conn.row_factory = sqlite3.Row
    return conn

# User authentication
def login(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    return user

# Add user
def add_user(username, password):
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# Add student
def add_student(name, age, grade, email):
    conn = get_db_connection()
    conn.execute('INSERT INTO students (name, age, grade, email) VALUES (?, ?, ?, ?)', (name, age, grade, email))
    conn.commit()
    conn.close()

# Get all students
def get_all_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return students

# Update student
def update_student(student_id, name, age, grade, email):
    conn = get_db_connection()
    conn.execute('UPDATE students SET name = ?, age = ?, grade = ?, email = ? WHERE id = ?', (name, age, grade, email, student_id))
    conn.commit()
    conn.close()

# Delete student
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()

# Main app
def main():
    st.title('Online Student Information Management System')

    menu = ['Login', 'Sign Up', 'Add Student', 'View Students', 'Update Student', 'Delete Student']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Login':
        st.subheader('Login')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            user = login(username, password)
            if user:
                st.success(f'Welcome {username}')
                st.session_state['user'] = user
            else:
                st.error('Invalid username or password')

    elif choice == 'Sign Up':
        st.subheader('Create New Account')
        new_user = st.text_input('Username')
        new_password = st.text_input('Password', type='password')
        if st.button('Sign Up'):
            add_user(new_user, new_password)
            st.success('Account created successfully')

    elif choice == 'Add Student':
        st.subheader('Add Student')
        if 'user' in st.session_state:
            name = st.text_input('Name')
            age = st.number_input('Age', min_value=1)
            grade = st.text_input('Grade')
            email = st.text_input('Email')
            if st.button('Add Student'):
                add_student(name, age, grade, email)
                st.success('Student added successfully')
        else:
            st.write('Please login to add students')

    elif choice == 'View Students':
        st.subheader('View Students')
        if 'user' in st.session_state:
            students = get_all_students()
            if students:
                for student in students:
                    st.write(f"ID: {student['id']}, Name: {student['name']}, Age: {student['age']}, Grade: {student['grade']}, Email: {student['email']}")
            else:
                st.write('No students found')
        else:
            st.write('Please login to view students')

    elif choice == 'Update Student':
        st.subheader('Update Student')
        if 'user' in st.session_state:
            student_id = st.number_input('Student ID', min_value=1)
            name = st.text_input('Name')
            age = st.number_input('Age', min_value=1)
            grade = st.text_input('Grade')
            email = st.text_input('Email')
            if st.button('Update Student'):
                update_student(student_id, name, age, grade, email)
                st.success('Student updated successfully')
        else:
            st.write('Please login to update students')

    elif choice == 'Delete Student':
        st.subheader('Delete Student')
        if 'user' in st.session_state:
            student_id = st.number_input('Student ID', min_value=1)
            if st.button('Delete Student'):
                delete_student(student_id)
                st.success('Student deleted successfully')
        else:
            st.write('Please login to delete students')

if __name__ == '__main__':
    main()