from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import face_recognition
import pickle
import cv2
import numpy as np
import mysql.connector

#setting up database
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="Lab7",
  database="SA_L7"
)
mycursor = mydb.cursor()

#main window
global main
global top
main= Tk()
main.geometry("1280x720")
main.title("MahaTech")
s = ttk.Style()
s.theme_use('classic')
s.configure("Treeview.Heading", font=(None, 20))
s.configure("Treeview", font=(None, 20),rowheight= 60)
main.withdraw()

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
with open('face_enc', "rb") as read:
    data=pickle.load(read)
with open('password', "rb") as read2:
    pw=pickle.load(read2)
video_capture = cv2.VideoCapture(0)

def pass_window():
    global top
    top= Toplevel()
    top.geometry("512x288")
    top.title("Password")
    global pass_entry
    pass_label= Label(top,text="Enter Password",font=("Arial", 25))
    pass_label.pack()
    pass_entry= Entry(top,show="*", width= 15,font=("Arial", 20))
    pass_entry.pack()
    pass_button= Button(top,text="Enter",command= Password)
    pass_button.pack()

def Password():
    string= pass_entry.get()
    if string==pw["password"]:
        top.destroy()
        top0.destroy()
        main.deiconify()
    else:
        pass_label2= Label(top,text="Password is incorrect",fg="Red",font=("Arial", 20))
        pass_label2.pack()

def change_pass():
    old=oldpass_entry.get()
    new=newpass_entry.get()
    if old==pw["password"]:
        pass_data={"password":new}
        with open('password','wb') as write2:
            write2.write(pickle.dumps(pass_data))
        messagebox.showinfo('Success', 'Password changed successfully!')
    else:
        pass_label2= Label(tab4,text="Old Password is incorrect",fg="Red",font=("Arial", 20))
        pass_label2.pack()

def select_file():
    filetypes = (
        ('PNG files', '*.png'),
        ('JPG files', '*.jpg'),
        ('JPEG files', '*.jpeg'),
        ('All files', '*.*')
    )
    global filename
    filename = fd.askopenfilename(title='Choose a photo',initialdir='/',filetypes=filetypes)


def Add():
    global top1
    top1= Toplevel()
    top1.geometry("512x288")
    top1.title("Add")
    #name
    global name_entry
    name_label= Label(top1,text="Name",font=("Arial", 15))
    name_label.grid(row=0,column=0)
    name_entry= Entry(top1,font=("Arial", 15))
    name_entry.grid(row=0,column=1)
    #age
    global age_entry
    age_label= Label(top1,text="Age",font=("Arial", 15))
    age_label.grid(row=1,column=0)
    age_entry= Entry(top1,font=("Arial", 15))
    age_entry.grid(row=1,column=1)
    #addphoto
    photo_button= Button(top1,image=camera,command= select_file)
    photo_button.grid(pady=190,column=1)
    #cancel button
    cancel_button= Button(top1,text="Cancel")
    cancel_button.grid(row=2,column=2)
    #add button
    add_button= Button(top1,text="Add",command= ok)
    add_button.grid(row=2,column=3)

def ok():
    emp_name= name_entry.get()
    age= age_entry.get()
    sql = "INSERT INTO soquor (Name, Age) VALUES (%s, %s)"
    val = (emp_name,age)
    mycursor.execute(sql, val)
    mydb.commit()
    emp_image= face_recognition.load_image_file(filename)
    new_face_encoding = face_recognition.face_encodings(emp_image)[0]
    old_enc= data["encodings"]
    old_names= data["names"]
    old_enc.append(new_face_encoding)
    old_names.append(emp_name)
    data2={"encodings":old_enc,"names":old_names}
    with open('face_enc','wb') as write:
        #pickle.dump(data2, write)
        write.write(pickle.dumps(data2))
    top1.destroy()
    tv.after(1,tv_data)
    messagebox.showinfo('Success', 'Employee added successfully!')


def sorting():
    first= clicked1.get()
    second= clicked2.get()
    #sort by ID:
    for i in tv.get_children():
        tv.delete(i)
    if first=="ID":
        if second=="Ascending":
            command="SELECT * FROM soquor ORDER BY ID"
            mycursor.execute(command)
        if second=="Descending":
            command="SELECT * FROM soquor ORDER BY ID DESC"
            mycursor.execute(command)
    #sort by Name:
    if first=="Name":
        if second=="Ascending":
            command="SELECT * FROM soquor ORDER BY Name"
            mycursor.execute(command)
        if second=="Descending":
            command="SELECT * FROM soquor ORDER BY Name DESC"
            mycursor.execute(command)
    #sort by Age:
    if first=="Age":
        if second=="Ascending":
            command="SELECT * FROM soquor ORDER BY Age"
            mycursor.execute(command)
        if second=="Descending":
            command="SELECT * FROM soquor ORDER BY Age DESC"
            mycursor.execute(command)
    result_set = mycursor.fetchall()
    for data in result_set:
        tv.insert("", 'end',iid=data[0], text=data[0], values =(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
    mydb.commit()

def search_engine():
    for i in tv2.get_children():
        tv2.delete(i)
    global search_entry
    index= search_entry.get()
    sql="SELECT * FROM soquor WHERE Name=%s"
    val=(index,)
    mycursor.execute(sql,val)
    result_set = mycursor.fetchall()
    for data in result_set:
        tv2.insert("", 'end',iid=data[0], text=data[0], values =(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
    mydb.commit()

def change_absent():
    ans= messagebox.askokcancel("Confirmation","Are you sure you want to REMOVE 1 absence day from this employee?")
    if ans==True:
        sql="SELECT Absence FROM soquor WHERE Name=%s"
        index=search_entry.get()
        val=(index,)
        mycursor.execute(sql,val)
        result_set = mycursor.fetchall()
        num= int(result_set[0][0])
        if num>0:
            num=num-1
            sql2="UPDATE soquor SET Absence=%s WHERE Name=%s"
            val=(num,index)
            mycursor.execute(sql2,val)
            mydb.commit()

def change_perm():
    ans= messagebox.askokcancel("Confirmation","Are you sure you want to REMOVE 1 permission day from this employee?")
    if ans==True:
        sql="SELECT Permissions FROM soquor WHERE Name=%s"
        index=search_entry.get()
        val=(index,)
        mycursor.execute(sql,val)
        result_set = mycursor.fetchall()
        num= int(result_set[0][0])
        if num>0:
            num=num-1
            sql2="UPDATE soquor SET Permissions=%s WHERE Name=%s"
            val=(num,index)
            mycursor.execute(sql2,val)
            mydb.commit()

def Remove():
    answer= messagebox.askokcancel("Confirmation","Are you sure you want to REMOVE this employee?")
    if answer==True:
        for i in tv2.get_children():
            tv2.delete(i)
        index= search_entry.get()
        sql="DELETE FROM soquor WHERE Name=%s"
        val=(index,)
        mycursor.execute(sql,val)
        mydb.commit()
        tv.after(1,tv_data)

def show_frames():
    # Get the latest frame and convert into Image
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(60, 60),flags=cv2.CASCADE_SCALE_IMAGE)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb)
    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"],encoding,tolerance=0.5)
        global name
        name = "Unknown"
        face_distance=face_recognition.face_distance(data["encodings"],encoding)
        best_match= np.argmin(face_distance)

        if matches[best_match]:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        names.append(name)
        for ((x, y, w, h), name) in zip(faces, names):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,0.75, (255, 255, 0), 2)
    cv2image= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    face_label.imgtk = imgtk
    face_label.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    face_label.after(1, show_frames)

def free_log():
    global free_top
    global cam_label
    free_top=Toplevel()
    free_top.geometry("512x288")
    free_top.title("Free login")
    cam_label= Label(free_top,text=name)
    cam_label.pack()
    cam_label.after(1,mod_text)
    check_in2= Button(free_top,text="Check in",command= checkin)
    check_in2.pack()
    check_out2= Button(free_top,text="Check out",command= checkout)
    check_out2.pack()

def mod_text():
    cam_label.configure(text=name)
    cam_label.after(1,mod_text)

def rec_log():
    print (name)
    if name=="Yousuf Safwat":
        print("logged in")
        top0.destroy()
        main.deiconify()

top0= Toplevel()
top0.geometry("512x288")
top0.title("Login")
login_label= Label(top0,text="Login Options",font=("Arial", 25))
login_label.pack()
pass_opt= Button(top0,text="Password",command= pass_window)
pass_opt.pack()
rec_opt= Button(top0,text="Recognition",command= rec_log)
rec_opt.pack()
free_opt= Button(top0,text="Free login",command= free_log)
free_opt.pack()

def checkin():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    sql = "UPDATE soquor SET Checkin=%s WHERE Name=%s"
    val=(current_time,name)
    mycursor.execute(sql,val)
    mydb.commit()
    tv.after(1,tv_data)

def checkout():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    sql = "UPDATE soquor SET Checkout=%s WHERE Name=%s"
    val=(current_time,name)
    mycursor.execute(sql,val)
    mydb.commit()
    tv.after(1,tv_data)




#main images
#images must be 400x128
employee = PhotoImage(file=r'C:\Users\Yousuf Gabr\Desktop\MahaTech\Icons\Employee.png')
search = PhotoImage(file=r'C:\Users\Yousuf Gabr\Desktop\MahaTech\Icons\Search.png')
search2 = PhotoImage(file=r'C:\Users\Yousuf Gabr\Desktop\MahaTech\Icons\Search mini.png')
add= PhotoImage(file=r'C:\Users\Yousuf Gabr\Desktop\MahaTech\Icons\Add.png')
remove= PhotoImage(file=r'C:\Users\Yousuf Gabr\Desktop\MahaTech\Icons\Remove.png')
permission= PhotoImage(file=r'C:\Users\Yousuf Gabr\Desktop\MahaTech\Icons\permission.png')
absent=  PhotoImage(file=r'C:\Users\Yousuf Gabr\Desktop\MahaTech\Icons\absent.png')
camera= PhotoImage(file=r'C:\Users\Yousuf Gabr\Desktop\MahaTech\Icons\Camera.png')
settings= PhotoImage(file=r'C:\Users\Yousuf Gabr\Desktop\MahaTech\Icons\Settings.png')
face_rec= PhotoImage(file=r'C:\Users\Yousuf Gabr\Desktop\MahaTech\Icons\Scan.png')

#Main Window:
#Creating tabs:
tabControl = ttk.Notebook(main)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tabControl.add(tab1,image=employee)
tabControl.add(tab2,image=search)
tabControl.add(tab3,image=face_rec)
tabControl.add(tab4,image=settings)
tabControl.pack(expand = 1, fill ="both")

#Employee Status:
add_Employee= Button(tab1,image=add,command= Add).pack(anchor=E)

options1=["ID","Name","Age"]
options2=["Ascending","Descending"]

clicked1= StringVar()
clicked1.set(options1[0])

clicked2= StringVar()
clicked2.set(options2[0])

menu1= OptionMenu(tab1,clicked1,*options1)
menu1.pack()

menu2= OptionMenu(tab1,clicked2,*options2)
menu2.pack()

sort_button= Button(tab1,text="Sort",command= sorting)
sort_button.pack()
global tv
tv = ttk.Treeview(tab1, columns=(1, 2, 3, 4, 5, 6, 7), show='headings',selectmode='browse', height=20)
tv.pack(anchor=NW,fill= X)
tv.column(1, anchor=CENTER,width=130,stretch= False)
tv.column(2, anchor=CENTER,width=305,stretch= False)
tv.column(3, anchor=CENTER,width=120,stretch= False)
tv.column(4, anchor=CENTER,width=180,stretch= False)
tv.column(5, anchor=CENTER,width=180,stretch= False)
tv.column(6, anchor=CENTER,width=180,stretch= False)
tv.column(7, anchor=CENTER,width=180,stretch= False)

tv.heading(1, text="Id")
tv.heading(2, text="Name")
tv.heading(3, text="Age")
tv.heading(4, text="Ckeck in")
tv.heading(5, text="Ckeck out")
tv.heading(6, text="Permissions")
tv.heading(7, text="Absence")

#Search Employee:
add_Employee= Button(tab2,image=add,command= Add).pack(anchor=E)
search_entry= Entry(tab2, width= 15,font=("Arial", 20))
search_entry.pack()
search_button= Button(tab2,image=search2,command= search_engine)
search_button.pack()

global tv2
tv2 = ttk.Treeview(tab2, columns=(1, 2, 3, 4, 5, 6, 7), show='headings',selectmode='browse', height=1)
tv2.pack(anchor=NW,fill= X)
tv2.column(1, anchor=CENTER,width=130,stretch= False)
tv2.column(2, anchor=CENTER,width=305,stretch= False)
tv2.column(3, anchor=CENTER,width=120,stretch= False)
tv2.column(4, anchor=CENTER,width=180,stretch= False)
tv2.column(5, anchor=CENTER,width=180,stretch= False)
tv2.column(6, anchor=CENTER,width=180,stretch= False)
tv2.column(7, anchor=CENTER,width=180,stretch= False)

tv2.heading(1, text="Id")
tv2.heading(2, text="Name")
tv2.heading(3, text="Age")
tv2.heading(4, text="Ckeck in")
tv2.heading(5, text="Ckeck out")
tv2.heading(6, text="Permissions")
tv2.heading(7, text="Absence")

edit_absent= Button(tab2,image=absent,command= change_absent)
edit_absent.pack()
edit_permission= Button(tab2,image=permission,command= change_perm)
edit_permission.pack()
remove_employee= Button(tab2,image=remove,command= Remove)
remove_employee.pack()

#Face Recognition:
add_Employee= Button(tab3,image=add,command= Add).pack(anchor=E)
face_label= Label(tab3)
face_label.pack()
face_label.after(1, show_frames)
check_in= Button(tab3,text="Check in",command= checkin)
check_in.pack()
check_out= Button(tab3,text="Check out",command= checkout)
check_out.pack()
#Settings:
add_Employee= Button(tab4,image=add,command= Add).pack(anchor=E)
changepass_label= Label(tab4,text="Change Password",font=("Arial", 25))
changepass_label.pack()

oldpass_label= Label(tab4,text="Old Password:",font=("Arial", 15))
oldpass_label.pack()
oldpass_entry= Entry(tab4, width= 15,font=("Arial", 20))
oldpass_entry.pack()

newpass_label= Label(tab4,text="New Password:",font=("Arial", 15))
newpass_label.pack()
newpass_entry= Entry(tab4, width= 15,font=("Arial", 20))
newpass_entry.pack()

change_button= Button(tab4,text="Change",command= change_pass)
change_button.pack()

def tv_data():
    for i in tv.get_children():
        tv.delete(i)
    r_set=mycursor.execute("SELECT * FROM soquor;")
    r_set=mycursor.fetchall()
    for data in r_set:
        tv.insert("", 'end',iid=data[0], text=data[0], values =(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
    mydb.commit()
tv.after(1,tv_data)




main.mainloop()
top0.mainloop()
top.mainloop()