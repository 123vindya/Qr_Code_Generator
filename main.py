from tkinter import *
import qrcode
from resizeimage import resizeimage
from PIL import Image, ImageTk
import os
import csv
import time
import subprocess 

class QRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x500+200+50")
        self.root.title("QR Code Generator")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(False, False)

        self.var_emp_code = StringVar()
        self.var_name = StringVar()
        self.var_department = StringVar()
        self.var_designation = StringVar()

        title = Label(self.root, text="QR Code Generator", font=("times new roman", 36, "bold"), bg="#2c3e50", fg="white")
        title.place(x=0, y=0, relwidth=1, relheight=0.15)

        # Employee Details Frame
        emp_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        emp_Frame.place(x=50, y=120, width=500, height=360)

        emp_title = Label(emp_Frame, text="Employee Details", font=("goudy old style", 20), bg="#3498db", fg="white")
        emp_title.place(x=0, y=0, relwidth=1)

        Label(emp_Frame, text="Employee ID", font=("goudy old style", 15), bg="white").place(x=20, y=60)
        Label(emp_Frame, text="Name", font=("goudy old style", 15), bg="white").place(x=20, y=100)
        Label(emp_Frame, text="Department", font=("goudy old style", 15), bg="white").place(x=20, y=140)
        Label(emp_Frame, text="Designation", font=("goudy old style", 15), bg="white").place(x=20, y=180)

        self.entry_emp_code = Entry(emp_Frame, font=("times new roman", 13), bg="lightyellow", textvariable=self.var_emp_code)
        self.entry_emp_code.place(x=150, y=60)
        self.entry_name = Entry(emp_Frame, font=("times new roman", 13), bg="lightyellow", textvariable=self.var_name)
        self.entry_name.place(x=150, y=100)
        self.entry_department = Entry(emp_Frame, font=("times new roman", 13), bg="lightyellow", textvariable=self.var_department)
        self.entry_department.place(x=150, y=140)
        self.entry_designation = Entry(emp_Frame, font=("times new roman", 13), bg="lightyellow", textvariable=self.var_designation)
        self.entry_designation.place(x=150, y=180)

        btn_generate = Button(emp_Frame, text="Generate QR Code", font=("times new roman", 13), bg="pink", command=self.generate)
        btn_generate.place(x=40, y=250, width=180, height=30)

        btn_clear = Button(emp_Frame, text="Clear", font=("times new roman", 13), bg="pink", command=self.clear)
        btn_clear.place(x=250, y=250, width=120, height=30)

        btn_preview = Button(emp_Frame, text="Preview Folder", font=("times new roman", 12), command=self.preview_folder)
        btn_preview.place(x=160, y=290, width=140)

        self.msg_label = Label(emp_Frame, text='', font=("times new roman", 12), fg="green", bg="white")
        self.msg_label.place(x=0, y=330, relwidth=1)

        # QR Display
        qr_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        qr_Frame.place(x=600, y=120, width=250, height=360)

        qr_title = Label(qr_Frame, text="Employee QR Code", font=("goudy old style", 20), bg="#3498db", fg="white")
        qr_title.place(x=0, y=0, relwidth=1)

        self.qr_code = Label(qr_Frame, text='No QR available', bg="white")
        self.qr_code.place(x=35, y=100, width=180, height=180)

    def clear(self):
        self.var_emp_code.set('')
        self.var_name.set('')
        self.var_department.set('')
        self.var_designation.set('')
        self.qr_code.config(image='', text='No QR available')
        self.msg_label.config(text='', fg="green")
        self.entry_emp_code.config(state='normal')
        self.entry_name.config(state='normal')
        self.entry_department.config(state='normal')
        self.entry_designation.config(state='normal')

    def generate(self):
        if (self.var_emp_code.get() == "" or
            self.var_name.get() == "" or
            self.var_department.get() == "" or
            self.var_designation.get() == ""):
            
            self.msg_label.config(text="All fields are required!", fg="red")
            return

        try:
            
            qr_data = (
                f"Employee ID: {self.var_emp_code.get()}\n"
                f"Employee Name: {self.var_name.get()}\n"
                f"Department: {self.var_department.get()}\n"
                f"Designation: {self.var_designation.get()}"
            )

            qr_code = qrcode.make(qr_data)
            qr_code = resizeimage.resize_cover(qr_code, [180, 180])

            if not os.path.exists("employee qr"):
                os.makedirs("employee qr")

            timestamp = time.strftime("%Y%m%d%H%M%S")
            file_path = f"employee qr/Emp_{self.var_emp_code.get()}_{timestamp}.png"
            qr_code.save(file_path)

            # Log to CSV
            with open("employee_data.csv", 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    self.var_emp_code.get(),
                    self.var_name.get(),
                    self.var_department.get(),
                    self.var_designation.get()
                ])

            image = Image.open(file_path)
            self.im = ImageTk.PhotoImage(image)
            self.qr_code.config(image=self.im, text='')
            self.msg_label.config(text="QR Code generated and saved successfully!", fg="green")

         
            self.entry_emp_code.config(state='disabled')
            self.entry_name.config(state='disabled')
            self.entry_department.config(state='disabled')
            self.entry_designation.config(state='disabled')

        except Exception as e:
            self.msg_label.config(text=f"Error: {str(e)}", fg="red")

    def preview_folder(self):
        folder_path = os.path.abspath("employee qr")
        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer "{folder_path}"')  # For Windows
        else:
            self.msg_label.config(text="No QR folder found yet.", fg="red")


root = Tk()
obj = QRGenerator(root)
root.mainloop()
