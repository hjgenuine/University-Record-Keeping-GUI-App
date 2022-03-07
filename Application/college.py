from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
import json
from PIL import ImageTk, Image


# Writing Data into JSON File
def write_data(data, filename='student.json'):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


# Clearing main form
def clear_form():
    variables_list = [namevar, phonenovar, addressvar, batchvar, rollnovar]
    for var in variables_list:
        var.set('')
    gendervar.set('Male')
    hostelvar.set(True)


# Submitting the main form
def submit_form():
    tmsg.showinfo('Save', 'Your record has been saved')
    record_dict = dict()
    record_dict['RollNo'] = rollnovar.get()
    record_dict['Name'] = namevar.get()
    record_dict['Gender'] = gendervar.get()
    record_dict['Address'] = addressvar.get()
    record_dict['PhoneNo'] = phonenovar.get()
    record_dict['Batch'] = batchvar.get()
    record_dict['Hostel'] = hostelvar.get()
    with open('student.json', 'r') as file:
        data = json.load(file)
        temp = data['Students']
        temp.append(record_dict)
    write_data(data)
    clear_form()


# Loading the students JSON
def load():
    for child in table.get_children():
        table.delete(child)
    with open("student.json", 'r') as file:
        students = json.load(file)
        temp_list = []
        for student in students['Students']:
            temp_list.append(tuple(student.values()))
        for item in temp_list:
            table.insert(parent='', index='end', value=item)


# Loading the Courses JSON
def load_c():
    for child in course_v.get_children():
        course_v.delete(child)
    with open('course.json', 'r') as file:
        data = json.load(file)
        temp_list = []
        for course in data['Courses']:
            temp_list.append(tuple(course.values()))
        for item in temp_list:
            course_v.insert(parent='', index=END, value=item)


# Saving the created Courses into JSON file
def c_save():
    record_dict = dict()
    record_dict['CourseID'] = course_id.get()
    record_dict['CourseName'] = course_name.get()
    with open('course.json', 'r') as file:
        data = json.load(file)
        temp = data['Courses']
        for item in temp:
            if item['CourseID'] == record_dict['CourseID']:
                tmsg.showwarning('Duplicate', 'Course with the same Id already present')
                return
        temp.append(record_dict)
    write_data(data, filename='course.json')
    tmsg.showinfo('Save', 'Your record has been saved')
    c_clear()


# Clearing the Created Course
def c_clear():
    course_id.set('')
    course_name.set('')


# Clearing the Allocated Course
def clear_a():
    s_rollno.set('')
    s_course.set('')


# Checking the Allocated Course's RollNo in Students JSON
def check_roll(roll_no):
    with open('student.json', 'r') as test_file:
        students = json.load(test_file)
        for obj in students['Students']:
            if obj['RollNo'] == roll_no:
                return True
    return False


# Checking and Saving Allocated Course to allocation JSON
def save_a():
    course_a = dict()
    course_a["RollNo"] = s_rollno.get()
    course_a["CourseID"] = s_course.get()
    # Check Roll No.
    if not check_roll(course_a['RollNo']):
        tmsg.showwarning('Invalid', 'Roll Number not found...')
        return

    with open('allocation.json', 'r') as file:
        data = json.load(file)
        temp = data["Stu_Course"]
        temp.append(course_a)
    write_data(data, filename='allocation.json')
    tmsg.showinfo('Save', 'Your record has been saved')
    clear_a()


# Loading the Updated Courses in the ComboBox
def load_courses(event):
    new_list = []
    with open('course.json', 'r') as f:
        new_data = json.load(f)
        for c in new_data['Courses']:
            new_list.append(c['CourseName'])
    new_box = ttk.Combobox(tab5, font=('Trebuchet MS', 14), width=38, textvariable=s_course)
    new_box['values'] = tuple(new_list)
    new_box.grid(row=1, column=3)


# Main Programme
root = Tk()
root.geometry('1200x700')
root.resizable(0, 0)
root.configure(bg='black')
root.title('Chitkara University - Form')

image_right = Image.open('2.png')
photo_right = ImageTk.PhotoImage(image_right)
Label(image=photo_right, borderwidth=0).pack(side=RIGHT, anchor=N)

image_left = Image.open('1.jpg')
photo_left = ImageTk.PhotoImage(image_left)
Label(root, image=photo_left, borderwidth=0).pack(side=LEFT, anchor=N)

Label(root, text='Chitkara University', fg='white', font=('Trebuchet MS', 20), bg='black').pack(anchor=CENTER)
Label(root, text='STUDENT DATABASE', fg='white', font=('Trebuchet MS', 20), bg='black').pack(anchor=CENTER, pady=30)

tabControl = ttk.Notebook(root)

tab1 = Frame(tabControl)
tab2 = Frame(tabControl)
tab3 = Frame(tabControl)
tab4 = Frame(tabControl)
tab5 = Frame(tabControl)

tabControl.add(tab1, text='New Student')
tabControl.add(tab2, text='Display')
tabControl.add(tab3, text='Course Creation')
tabControl.add(tab4, text='Display Courses')
tabControl.add(tab5, text='Course Allocation')

tabControl.pack(anchor=CENTER)

# Tab 1
Label(tab1, text='Enter Your Name', font=('Trebuchet MS', 18)).grid(row=0, column=0, pady=5, padx=3)
Label(tab1, text='Enter Your RollNo', font=('Trebuchet MS', 18)).grid(row=1, column=0, pady=5, padx=3)
Label(tab1, text='Choose Your Gender', font=('Trebuchet MS', 18)).grid(row=2, column=0, pady=5, padx=3)
Label(tab1, text='Address For Correspondence', font=('Trebuchet MS', 18)).grid(row=3, column=0, pady=5, padx=3)
Label(tab1, text='Phone No', font=('Trebuchet MS', 18)).grid(row=4, column=0, pady=5, padx=3)
Label(tab1, text='Your Batch', font=('Trebuchet MS', 18)).grid(row=5, column=0, pady=5, padx=3)
Label(tab1, text='Hostel[Y/N]', font=('Trebuchet MS', 18)).grid(row=6, column=0, pady=5, padx=3)

namevar = StringVar()
rollnovar = StringVar()
gendervar = StringVar()
gendervar.set('Male')
addressvar = StringVar()
phonenovar = StringVar()
batchvar = StringVar()
hostelvar = BooleanVar()
hostelvar.set(True)

Entry(tab1, textvariable=namevar, font=('Trebuchet MS', 14), width=38).grid(row=0, column=3, columnspan=3)
Entry(tab1, textvariable=rollnovar, font=('Trebuchet MS', 14), width=38).grid(row=1, column=3, columnspan=3)
Radiobutton(tab1, text='Male', variable=gendervar, value='Male', font=('Trebuchet MS', 11)).grid(row=2, column=3)
Radiobutton(tab1, text='Female', variable=gendervar, value='Female', font=('Trebuchet MS', 11)).grid(row=2, column=5)
Entry(tab1, textvariable=addressvar, font=('Trebuchet MS', 14), width=38).grid(row=3, column=3, columnspan=3)
Entry(tab1, textvariable=phonenovar, font=('Trebuchet MS', 14), width=38).grid(row=4, column=3, columnspan=3)
combobox = ttk.Combobox(tab1, textvariable=batchvar, font=('Trebuchet MS', 11), width=30)
combobox['values'] = ('2018', '2019', '2020')
combobox.grid(row=5, column=5)
Checkbutton(tab1, text='Click if you need Hostel Facility', variable=hostelvar, font=('Trebuchet MS', 11)).grid(row=6, column=5)

Button(tab1, text='Save', font=('Trebuchet MS', 14), padx=25, command=submit_form).grid(row=7, column=1)
Button(tab1, text='Clear', font=('Trebuchet MS', 14), padx=15, command=clear_form).grid(row=7, column=2)

# Tab2
table = ttk.Treeview(tab2)

table['columns'] = ('RollNo', 'Name', 'Gender', 'Address', 'PhoneNo', 'Batch', 'Hostel')
table['show'] = 'headings'
style = ttk.Style()
style.configure('Treeview.Heading', font=('Trebuchet MS', 13, 'bold'))
style.configure('Treeview', font=('Trebuchet MS', 12))
table.column('RollNo',  width=130, minwidth=100)
table.column('Name',  width=130, minwidth=100, anchor=E)
table.column('Gender',  width=130, minwidth=100)
table.column('Address',  width=130, minwidth=100)
table.column('PhoneNo',  width=130, minwidth=100)
table.column('Batch',  width=130, minwidth=100)
table.column('Hostel',  width=130, minwidth=100)

table.heading('RollNo', text='RollNo')
table.heading('Name', text='Name')
table.heading('Gender', text='Gender')
table.heading('Address', text='Address')
table.heading('PhoneNo', text='PhoneNo')
table.heading('Batch', text='Batch')
table.heading('Hostel', text='Hostel')

table.pack()

Button(tab2, text='Show Students', fg='white', bg='black', font=('Trebuchet MS', 15), command=load).pack(side=BOTTOM)

# Tab3
for i in range(4):
    tab3.columnconfigure(i, weight=1)
for i in range(4):
    tab3.rowconfigure(i, weight=1)
Label(tab3, text='Course ID', font=('Trebuchet MS', 18)).grid(row=0, column=0, columnspan=2)
Label(tab3, text='Course Name', font=('Trebuchet MS', 18)).grid(row=1, column=0, columnspan=2)
course_id = StringVar()
course_name = StringVar()
Entry(tab3, textvariable=course_id, font=('Trebuchet MS', 14), width=40).grid(row=0, column=3)
Entry(tab3, textvariable=course_name, font=('Trebuchet MS', 14), width=40).grid(row=1, column=3)

Button(tab3, text='Save', font=('Trebuchet MS', 14), padx=25, command=c_save).grid(row=3, column=2)
Button(tab3, text='Clear', font=('Trebuchet MS', 14), padx=15, command=c_clear).grid(row=3, column=3)

# Tab4
course_v = ttk.Treeview(tab4)
course_v['columns'] = ('CourseID', 'CourseName')
course_v['show'] = 'headings'

course_v.column('CourseID', width=300)
course_v.column('CourseName', width=300, anchor=E)

course_v.heading('CourseID', text='CourseID')
course_v.heading('CourseName', text='CourseName')
course_v.pack()

Button(tab4, text='Show Courses', fg='white', bg='black', font=('Trebuchet MS', 15), command=load_c).pack(side=BOTTOM)

# Tab5
course_list = []
with open('course.json', 'r') as f:
    course_data = json.load(f)
    for course in course_data['Courses']:
        course_list.append(course['CourseName'])
for i in range(4):
    tab5.columnconfigure(i, weight=1)
for i in range(4):
    tab5.rowconfigure(i, weight=1)
Label(tab5, text='Student RollNo', font=('Trebuchet MS', 18)).grid(row=0, column=0, columnspan=2)
Label(tab5, text='Course Name', font=('Trebuchet MS', 18)).grid(row=1, column=0, columnspan=2)

s_rollno = StringVar()
s_course = StringVar()

Entry(tab5, textvariable=s_rollno, font=('Trebuchet MS', 14), width=40).grid(row=0, column=3)
course_box = ttk.Combobox(tab5, font=('Trebuchet MS', 14), width=38, textvariable=s_course)
course_box['values'] = tuple(course_list)
course_box.grid(row=1, column=3)

Button(tab5, text='Allocate', font=('Trebuchet MS', 14), padx=25, command=save_a).grid(row=3, column=2)
Button(tab5, text='Clear', font=('Trebuchet MS', 14), padx=15, command=clear_a).grid(row=3, column=3)

Label(root, text='Department of Computer Science & Engineering', fg='white', font=('Trebuchet MS', 20), bg='black').pack(anchor=CENTER, pady=50)

tabControl.bind('<Button-1>', load_courses)
root.mainloop()