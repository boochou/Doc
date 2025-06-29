import tkinter as tk
from tkinter import messagebox, filedialog
import random
# Giao diện đăng nhập
class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Log in")
        self.geometry("350x200")
        self.resizable(False, False)

        tk.Label(self, text="Username:").pack(pady=(20, 5))
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="RACF Password:").pack(pady=(10, 5))
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Log in", command=self.check_login).pack(pady=15)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            self.destroy()
            MainAppScreen(username)
        else:
            messagebox.showerror("Error", "Please enter username and password")

# Giao diện chính
class MainAppScreen(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.active_button_label = None
        self.sidebar_buttons = []

        self.title("Application")
        self.geometry("900x600")
        self.configure(bg="#e0e0e0")

        self.create_header()
        self.create_sidebar()
        self.create_main_content()
        self.mainloop()

    def create_header(self):
        self.header = tk.Frame(self, height=50, bg="#b30000")  # đỏ đậm
        self.header.pack(side="top", fill="x")

        tk.Label(
            self.header,
            text="🛡️ Small Tool",
            fg="white",
            bg="#b30000",
            font=("Arial", 16, "bold"),
            anchor="w",
            padx=20
        ).pack(side="left", fill="y")

        tk.Label(
            self.header,
            text=f"Hi, {self.username}",
            fg="white",
            bg="#b30000",
            font=("Arial", 12),
            anchor="e",
            padx=10
        ).pack(side="right")

    def create_sidebar(self):
        self.sidebar = tk.Frame(self, width=200, bg="#f9f9f9")
        self.sidebar.pack(side="left", fill="y")

        options = [
            ("Generate Cert Command", self.load_cert),
            ("Generate Map Command", self.load_map),
            ("Update Report", self.load_report),
            ("Transfer File", self.load_transfer),
        ]

        for label, command in options:
            btn = tk.Button(
                self.sidebar,
                text=label,
                anchor="w",
                bg="#f9f9f9",
                relief="flat",
                padx=20,
                command=lambda c=command, l=label: self.on_sidebar_click(c, l)
            )
            btn.pack(fill="x", pady=2)

            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#ffe6e6"))  # hover: đỏ sáng
            btn.bind("<Leave>", lambda e, b=btn, lbl=label: b.configure(
                bg="#ffcccc" if lbl == self.active_button_label else "#f9f9f9"))

            self.sidebar_buttons.append((label, btn))

    def on_sidebar_click(self, command_function, selected_label):
        self.active_button_label = selected_label
        for label, btn in self.sidebar_buttons:
            if label == selected_label:
                btn.configure(bg="#ffcccc", fg="black")  # đỏ nhạt
            else:
                btn.configure(bg="#f9f9f9", fg="black")
        command_function()

    def create_main_content(self):
        self.content_frame = tk.Frame(self, bg="#ffffff")
        self.content_frame.pack(side="right", expand=True, fill="both")
        self.on_sidebar_click(self.load_cert, "Generate Cert Command")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_cert(self):
        self.clear_content()
        CertFlow(self.content_frame)


    def load_map(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Map Generator", font=("Arial", 16)).pack(pady=20)

    def load_report(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Report Updater", font=("Arial", 16)).pack(pady=20)

    def load_transfer(self):
        self.clear_content()
        tk.Label(self.content_frame, text="File Transfer", font=("Arial", 16)).pack(pady=20)

class CertFlow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # Cấu hình màu sắc & font
        self.bg = "#ffffff"
        self.fg = "#333333"
        self.accent = "#b30000"
        self.highlight = "#ffe6e6"
        self.font_main = ("Segoe UI", 11)
        self.font_title = ("Segoe UI", 14, "bold")

        self.configure(bg=self.bg)

        # Biến dữ liệu
        self.text_data = ""
        self.folder_path = ""
        self.file_path = ""
        self.file_names = []
        self.selected_system = tk.StringVar()
        self.input_mode = tk.StringVar(value="text")

        self.step_index = 0
        self.step_frame = None

        self.build_step_0()

    def switch_step(self, index):
        self.step_index = index
        if self.step_frame:
            self.step_frame.destroy()
        steps = [self.build_step_0, self.build_step_1, self.build_step_2]
        steps[index]()

    # ===== STEP 0: Nhập thông tin =====
    def build_step_0(self):
        self.step_frame = tk.Frame(self, bg=self.bg)
        self.step_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(self.step_frame, text="Bước 1: Nhập thông tin", font=self.font_title, fg=self.accent, bg=self.bg).pack(anchor="w")

        # Chọn loại input
        option_frame = tk.Frame(self.step_frame, bg=self.bg)
        option_frame.pack(anchor="w", pady=(10, 5))
        tk.Radiobutton(option_frame, text="Nhập Text", variable=self.input_mode, value="text",
                       font=self.font_main, bg=self.bg, command=self.render_input_mode).pack(side="left", padx=10)
        tk.Radiobutton(option_frame, text="Chọn File", variable=self.input_mode, value="file",
                       font=self.font_main, bg=self.bg, command=self.render_input_mode).pack(side="left", padx=10)

        # Khung nhập liệu
        self.input_area = tk.Frame(self.step_frame, bg=self.bg)
        self.input_area.pack(anchor="w", fill="x", pady=10)
        self.render_input_mode()

    def render_input_mode(self):
        for widget in self.input_area.winfo_children():
            widget.destroy()

        if self.input_mode.get() == "text":
            tk.Label(self.input_area, text="Nội dung file:", font=self.font_main, bg=self.bg).pack(anchor="w")
            self.text_entry = tk.Text(self.input_area, height=6, width=70, font=self.font_main)
            self.text_entry.pack(pady=5)

            folder_frame = tk.Frame(self.input_area, bg=self.bg)
            folder_frame.pack(anchor="w", pady=(10, 5))
            tk.Label(folder_frame, text="Thư mục lưu:", font=self.font_main, bg=self.bg).pack(side="left")
            self.folder_entry = tk.Entry(folder_frame, width=50, font=self.font_main)
            self.folder_entry.pack(side="left", padx=5)
            tk.Button(folder_frame, text="Browse", command=self.pick_folder,
                      bg=self.accent, fg="white", relief="flat", font=("Segoe UI", 10)).pack(side="left")

            tk.Button(self.input_area, text="Xác nhận", command=self.confirm_text,
                      bg=self.accent, fg="white", relief="flat", padx=10, pady=5).pack(pady=10)

        else:
            file_frame = tk.Frame(self.input_area, bg=self.bg)
            file_frame.pack(anchor="w", pady=10)
            self.file_label = tk.Label(file_frame, text="Chưa chọn file", fg="gray", font=self.font_main, bg=self.bg)
            self.file_label.pack(side="left", padx=5)
            tk.Button(file_frame, text="Chọn File", command=self.pick_file,
                      bg=self.accent, fg="white", relief="flat").pack(side="left")

            tk.Button(self.input_area, text="Xác nhận & Tiếp tục", command=self.confirm_file,
                      bg=self.accent, fg="white", relief="flat", padx=10, pady=5).pack(pady=15)

    def pick_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, path)

    def pick_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            self.file_path = path
            self.file_label.config(text=path)

    def confirm_text(self):
        text = self.text_entry.get("1.0", "end").strip()
        folder = self.folder_entry.get().strip()
        if not text or not folder:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập nội dung và chọn thư mục.")
            return
        self.text_data = text
        self.folder_path = folder

        # Popup xem trước
        popup = tk.Toplevel(self)
        popup.title("Xác nhận nội dung")
        popup.geometry("460x350")
        popup.config(bg="white")

        tk.Label(popup, text="Xem lại nội dung:", font=self.font_main, bg="white").pack(pady=(10, 0))
        preview = tk.Text(popup, height=8, wrap="word")
        preview.pack(padx=10, pady=5, fill="both")
        preview.insert("1.0", text)
        preview.configure(state="disabled")

        tk.Label(popup, text=f"Lưu vào: {folder}", bg="white", fg="gray").pack()

        btns = tk.Frame(popup, bg="white")
        btns.pack(pady=10)
        tk.Button(btns, text="Chỉnh sửa", command=popup.destroy, bg="#888", fg="white", relief="flat").pack(side="left", padx=10)
        tk.Button(btns, text="Xác nhận", command=lambda: [popup.destroy(), self.switch_step(1)],
                  bg=self.accent, fg="white", relief="flat").pack(side="left")

    def confirm_file(self):
        if not self.file_path:
            messagebox.showwarning("Chưa chọn file", "Vui lòng chọn file đầu vào.")
            return
        self.switch_step(1)

    # ===== STEP 1: Sinh mã =====
    def build_step_1(self):
        self.step_frame = tk.Frame(self, bg=self.bg)
        self.step_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(self.step_frame, text="Bước 2: Sinh mã", font=self.font_title, fg=self.accent, bg=self.bg).pack(anchor="w", pady=(0, 10))

        info = self.text_data if self.input_mode.get() == "text" else f"Dữ liệu từ file: {self.file_path}"
        tk.Label(self.step_frame, text="Thông tin đầu vào:", font=self.font_main, bg=self.bg).pack(anchor="w")
        txt = tk.Text(self.step_frame, height=6, width=70, font=self.font_main)
        txt.pack()
        txt.insert("1.0", info)
        txt.configure(state="disabled")

        tk.Button(self.step_frame, text="Tạo mã", command=self.generate_files,
                  bg=self.accent, fg="white", relief="flat", padx=10, pady=5).pack(pady=10)

        self.file_listbox = tk.Listbox(self.step_frame, height=8, width=70, font=("Consolas", 10))
        self.file_listbox.pack()
        self.file_listbox.bind("<<ListboxSelect>>", self.show_file_detail)

        tk.Button(self.step_frame, text="Tiếp tục", command=lambda: self.switch_step(2),
                  bg=self.accent, fg="white", relief="flat", padx=10, pady=5).pack(pady=15)

    def generate_files(self):
        self.file_listbox.delete(0, "end")
        self.file_names = [f"file_{i}.py" for i in range(1, random.randint(7, 10) + 1)]
        for f in self.file_names:
            self.file_listbox.insert("end", f)

    def show_file_detail(self, event):
        idx = self.file_listbox.curselection()
        if not idx:
            return
        filename = self.file_listbox.get(idx)
        messagebox.showinfo("Chi tiết", f"Bạn đã chọn: {filename}\n(Nội dung file mẫu giả lập)")

    # Bước 3 – Gửi lên hệ thống
    def build_step_2(self):
        self.step_frame = tk.Frame(self, bg=self.bg)
        self.step_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tiêu đề bước
        tk.Label(
            self.step_frame,
            text="Bước 3: Gửi mã lên hệ thống",
            font=self.font_title,
            fg=self.accent,
            bg=self.bg
        ).pack(anchor="w", pady=(0, 15))

        # Danh sách hệ thống
        systems = ["System Alpha", "System Beta", "System Gamma", "Hệ thống nội bộ"]
        tk.Label(
            self.step_frame,
            text="Chọn hệ thống:",
            font=self.font_main,
            bg=self.bg
        ).pack(anchor="w")

        self.selected_system.set(systems[0])
        dropdown = tk.OptionMenu(self.step_frame, self.selected_system, *systems)
        dropdown.config(font=self.font_main)
        dropdown.pack(anchor="w", pady=(5, 15))

        # Nút gửi
        tk.Button(
            self.step_frame,
            text="Gửi mã",
            command=self.send_code,
            bg=self.accent,
            fg="white",
            relief="flat",
            padx=10,
            pady=5
        ).pack()

    def send_code(self):
        system = self.selected_system.get()
        messagebox.showinfo("Thành công", f"Mã đã được gửi lên hệ thống: {system}")
        self.switch_step(0)

if __name__ == "__main__":
    LoginScreen().mainloop()
