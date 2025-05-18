import tkinter as tk
from tkinter import messagebox
from managers.auth_manager import authenticate
from ui.main_ui import show_main_ui

def show_login():
    def login():
        username = username_var.get().strip()
        password = password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        user = authenticate(username, password)
        if user:
            messagebox.showinfo("Thành công", f"Chào {user['full_name']}!")
            root.destroy()
            show_main_ui()
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu.")

    root = tk.Tk()
    root.title("Đăng nhập  ")
    root.configure(bg="#f0f0f0")

    # Căn giữa
    w, h = 400, 360
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    root.resizable(False, False)

    frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=300)

    # Tiêu đề ngắn gọn, in hoa, font khác, màu xanh đậm
    tk.Label(
        frame,
        text="PHẦN MỀM QUẢN LÝ ĐỀ THI",
        font=("Helvetica", 12, "bold"),
        fg="#003366",
        bg="white",
        justify="center"
    ).pack(pady=(15, 10))

    # Username
    tk.Label(frame, text="Username", bg="white", anchor="w").pack(fill="x", padx=20)
    username_var = tk.StringVar()
    username_entry = tk.Entry(
        frame, textvariable=username_var,
        relief="flat", bg="#f2f2f2", highlightthickness=1, highlightcolor="#ccc",
        font=("Arial", 10)
    )
    username_entry.pack(ipady=5, ipadx=5, padx=20, pady=(0,10), fill="x")

    # Password
    tk.Label(frame, text="Password", bg="white", anchor="w").pack(fill="x", padx=20)
    password_var = tk.StringVar()
    password_entry = tk.Entry(
        frame, textvariable=password_var, show="*",
        relief="flat", bg="#f2f2f2", highlightthickness=1, highlightcolor="#ccc",
        font=("Arial", 10)
    )
    password_entry.pack(ipady=5, ipadx=5, padx=20, pady=(0,20), fill="x")

    # Nút đăng nhập
    login_btn = tk.Button(
        frame, text="Đăng nhập", command=login,
        bg="#4CAF50", fg="white", activebackground="#45a049",
        relief="flat", font=("Arial", 10, "bold"), cursor="hand2"
    )
    login_btn.pack(pady=(0,15), ipadx=10, ipady=5)

    root.mainloop()


if __name__ == "__main__":
    show_login()
