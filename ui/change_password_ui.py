import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from managers.user_manager import change_password  # Giả sử bạn dùng hàm change_password


class ChangePasswordUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Đổi Mật Khẩu")

        width = 400
        height = 320
        self.root.geometry(f"{width}x{height}")

        # Căn giữa cửa sổ trên màn hình
        self.root.update_idletasks()  # Cập nhật trước để lấy chính xác kích thước
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.root.configure(bg="#cce6ff")  # Xanh dương nhạt

        # Load icon ảnh (bạn có thể thay bằng đường dẫn icon khác)
        try:
            self.icon_img = PhotoImage(file="icon_key.png")
        except Exception:
            self.icon_img = None

        # Tiêu đề có icon
        if self.icon_img:
            label_icon = tk.Label(root, image=self.icon_img, bg="#cce6ff")
            label_icon.pack(pady=(15, 0))

        title = tk.Label(root, text="ĐỔI MẬT KHẨU", font=("Arial", 18, "bold"), bg="#cce6ff", fg="#004080")
        title.pack(pady=(10, 20))

        # Form nhập liệu
        self.frame_form = tk.Frame(root, bg="#cce6ff")
        self.frame_form.pack(pady=5)

        self._add_labeled_entry("Tên đăng nhập:", "username")
        self._add_labeled_entry("Mật khẩu cũ:", "old_password", show="*")
        self._add_labeled_entry("Mật khẩu mới:", "new_password", show="*")
        self._add_labeled_entry("Xác nhận mật khẩu:", "confirm_password", show="*")

        # Button đổi mật khẩu với bo tròn và màu xanh dương
        self.btn_change = tk.Button(
            root,
            text="Đổi Mật Khẩu",
            command=self.change_password,
            font=("Arial", 14),
            bg="#3399ff",
            fg="white",
            activebackground="#2673cc",
            activeforeground="white",
            bd=0,
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.btn_change.pack(pady=20)

        # Bo tròn button (kỹ thuật dùng canvas)
        self._make_rounded_button(self.btn_change, 12)

    def _add_labeled_entry(self, label_text, attr_name, show=None):
        frame = tk.Frame(self.frame_form, bg="#cce6ff")
        frame.pack(pady=5, fill="x", padx=40)

        label = tk.Label(frame, text=label_text, font=("Arial", 12), bg="#cce6ff", fg="#003366", width=15, anchor="w")
        label.pack(side="left")

        entry = tk.Entry(frame, font=("Arial", 12), show=show)
        entry.pack(side="left", fill="x", expand=True)

        setattr(self, attr_name, entry)

    def change_password(self):
        username = self.username.get().strip()
        old_pass = self.old_password.get()
        new_pass = self.new_password.get()
        confirm_pass = self.confirm_password.get()

        if not username or not old_pass or not new_pass or not confirm_pass:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Lỗi", "Mật khẩu mới và xác nhận không khớp.")
            return

        success = change_password(username, old_pass, new_pass)
        if success:
            messagebox.showinfo("Thành công", "Đổi mật khẩu thành công!")
            self._clear_entries()
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu cũ không đúng.")

    def _clear_entries(self):
        self.username.delete(0, tk.END)
        self.old_password.delete(0, tk.END)
        self.new_password.delete(0, tk.END)
        self.confirm_password.delete(0, tk.END)

    def _make_rounded_button(self, button, radius):
        # Tkinter không hỗ trợ bo tròn button sẵn, có thể dùng ttk hoặc thư viện ngoài
        # Ở đây không thực sự bo tròn, nên giữ empty
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ChangePasswordUI(root)
    root.mainloop()
