import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",
        database="students",
        user="postgres",
        password="Tinny987654321"
    )
    return conn

def test_connection():
    try:
        conn = connect_to_db()
        print("Kết nối thành công!")
        conn.close()
    except Exception as e:
        print("Kết nối thất bại:", e)

test_connection()

class Student:
    def __init__(self, id, name, age, gender, major):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.major = major

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Sinh viên")
        self.frame_input = tk.Frame(self.root, padx=10, pady=10)  # Thêm padding cho frame
        self.frame_input.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Sử dụng grid thay vì pack
        self.frame_buttons = tk.Frame(self.root, padx=10, pady=10)
        self.frame_buttons.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.frame_treeview = tk.Frame(self.root)
        self.frame_treeview.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")  # Khung hiển thị bảng
        self.create_widgets()

    def create_widgets(self):
        # Tạo label và entry với các padding hợp lý
        self.label_name = tk.Label(self.frame_input, text="Tên:", width=15)
        self.label_name.grid(row=0, column=0, sticky="w", padx=5, pady=5)  # Căn trái và thêm padding
        self.entry_name = tk.Entry(self.frame_input, width=30, font=('Arial', 12))
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        self.label_age = tk.Label(self.frame_input, text="Tuổi:", width=15)
        self.label_age.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_age = tk.Entry(self.frame_input, width=30, font=('Arial', 12))
        self.entry_age.grid(row=1, column=1, padx=5, pady=5)

        # Giới tính: Sử dụng Radio Buttons
        self.label_gender = tk.Label(self.frame_input, text="Giới tính:", width=15)
        self.label_gender.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.gender_var = tk.StringVar(value="Nam")
        self.radio_male = tk.Radiobutton(self.frame_input, text="Nam", variable=self.gender_var, value="Nam")
        self.radio_female = tk.Radiobutton(self.frame_input, text="Nữ", variable=self.gender_var, value="Nữ")
        self.radio_male.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.radio_female.grid(row=2, column=2, sticky="w", padx=5, pady=5)

        self.label_major = tk.Label(self.frame_input, text="Ngành:", width=15)
        self.label_major.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_major = tk.Entry(self.frame_input, width=30, font=('Arial', 12))
        self.entry_major.grid(row=3, column=1, padx=5, pady=5)

        # Tạo các nút bấm
        self.button_add = tk.Button(self.frame_buttons, text="Thêm học sinh", command=self.add_student, width=20, bg="lightgreen", font=('Arial', 12))
        self.button_add.grid(row=0, column=0, padx=5, pady=10)

        self.button_update = tk.Button(self.frame_buttons, text="Cập nhật thông tin", command=self.update_student, width=20, bg="lightyellow", font=('Arial', 12))
        self.button_update.grid(row=0, column=1, padx=5, pady=10)

        self.button_delete = tk.Button(self.frame_buttons, text="Xoá sinh viên", command=self.delete_student, width=20, bg="lightcoral", font=('Arial', 12))
        self.button_delete.grid(row=0, column=2, padx=5, pady=10)

        self.button_reload = tk.Button(self.frame_buttons, text="Tải lại danh sách", command=self.reload_treeview, width=20, bg="lightblue", font=('Arial', 12))
        self.button_reload.grid(row=0, column=3, padx=5, pady=10)

        # Tạo treeview để hiển thị danh sách sinh viên
        self.treeview = ttk.Treeview(self.frame_treeview, columns=("id", "name", "age", "gender", "major"), show='headings', height=15)
        self.treeview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.treeview.heading("id", text="ID")
        self.treeview.heading("name", text="Tên")
        self.treeview.heading("age", text="Tuổi")
        self.treeview.heading("gender", text="Giới tính")
        self.treeview.heading("major", text="Ngành")

        self.treeview.column("id", width=50)
        self.treeview.column("name", width=150)
        self.treeview.column("age", width=50)
        self.treeview.column("gender", width=100)
        self.treeview.column("major", width=150)

    def add_student(self):
        # Lấy thông tin từ các trường nhập liệu
        name = self.entry_name.get()
        age = int(self.entry_age.get())
        gender = self.gender_var.get()
        major = self.entry_major.get()

        # Kiểm tra tính hợp lệ của thông tin
        if not name or not age or not gender or not major:
            print("Vui lòng nhập đầy đủ thông tin")
            return

        # Thêm sinh viên vào cơ sở dữ liệu
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)", (name, age, gender, major))
        conn.commit()
        cur.close()
        conn.close()

        # Làm mới bảng treeview
        self.reload_treeview()

    def update_student(self):
        # Lấy thông tin sinh viên được chọn
        selected_student = self.treeview.selection()[0]
        student_id = self.treeview.item(selected_student, "values")[0]

        # Lấy thông tin từ các trường nhập liệu
        name = self.entry_name.get()
        age = int(self.entry_age.get())
        gender = self.gender_var.get()
        major = self.entry_major.get()

        # Kiểm tra tính hợp lệ của thông tin
        if not name or not age or not gender or not major:
            print("Vui lòng nhập đầy đủ thông tin")
            return

        # Cập nhật thông tin sinh viên vào cơ sở dữ liệu
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE students SET name = %s, age = %s, gender = %s, major = %s WHERE id = %s", (name, age, gender, major, student_id))
        conn.commit()
        cur.close()
        conn.close()

        # Làm mới bảng treeview
        self.reload_treeview()

    def delete_student(self):
        # Lấy thông tin sinh viên được chọn
        selected_student = self.treeview.selection()[0]
        student_id = self.treeview.item(selected_student, "values")[0]

        # Xóa sinh viên khỏi cơ sở dữ liệu
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()
        cur.close()
        conn.close()

        # Làm mới bảng treeview
        self.reload_treeview()

    def reload_treeview(self):
        # Xóa hết dữ liệu trong treeview
        self.treeview.delete(*self.treeview.get_children())

        # Tải lại dữ liệu từ cơ sở dữ liệu
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Thêm dữ liệu vào treeview
        for row in rows:
            self.treeview.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()
