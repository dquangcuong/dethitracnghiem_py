import tkinter as tk
from ui.question_form import show_question_manager
from ui.exam_form import show_exam_manager
from ui.change_password_ui import ChangePasswordUI  # Import ChangePasswordUI


def show_main_ui():
    root = tk.Tk()
    root.title("Quản lý đề thi")
    root.configure(bg="#f0f4f8")

    # Căn giữa màn hình
    window_width = 800
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)

    # Sidebar bên trái (menu bar) màu xanh nhạt
    sidebar_bg = "#89bde0"  # xanh nhạt dễ chịu
    sidebar = tk.Frame(root, bg=sidebar_bg, width=200)
    sidebar.pack(side="left", fill="y")

    btn_font = ("Arial", 11, "bold")
    btn_opts = {
        "master": sidebar,
        "font": btn_font,
        "fg": "#08306b",           # xanh đậm dễ nhìn
        "bg": "#a9cce3",           # xanh nhạt hơn chút cho nút
        "activebackground": "#2e86c1",  # khi hover xanh đậm hơn
        "activeforeground": "#ffffff",
        "relief": "flat",
        "width": 18,
        "anchor": "w",
        "padx": 10,
        "pady": 8,
        "cursor": "hand2"
    }

    def open_change_password():
        change_pw_window = tk.Toplevel()
        change_pw_window.grab_set()  # Khóa focus vào cửa sổ đổi mật khẩu
        ChangePasswordUI(change_pw_window)

    tk.Label(sidebar, text="  MENU", font=("Arial", 12, "bold"), fg="#08306b", bg=sidebar_bg).pack(pady=(20,10), anchor="w")
    tk.Button(command=lambda: show_question_manager(root), text="  Quản lý câu hỏi", **btn_opts).pack(pady=5)
    tk.Button(command=lambda: show_exam_manager(root),     text="  Quản lý đề thi",   **btn_opts).pack(pady=5)
    tk.Button(command=open_change_password,                 text="  Đổi mật khẩu",      **btn_opts).pack(pady=5)
    tk.Button(command=root.quit,                            text="  Thoát",            **btn_opts).pack(side="bottom", pady=20)

    # Vùng nội dung chính bên phải
    content = tk.Frame(root, bg="#f0f4f8")
    content.pack(side="right", expand=True, fill="both")
    content.pack_propagate(False)  # Giữ kích thước content

    # Frame chứa icon và text hướng dẫn
    guide_frame = tk.Frame(content, bg="#f0f4f8")
    guide_frame.place(relx=0.5, rely=0.4, anchor="center")

    # Canvas vẽ icon dấu chấm than trong vòng tròn
    canvas = tk.Canvas(guide_frame, width=60, height=60, bg="#f0f4f8", highlightthickness=0)
    canvas.pack(side="left", padx=10)

    # Vẽ vòng tròn xanh dương tươi
    canvas.create_oval(5, 5, 55, 55, fill="#1E90FF", outline="")

    # Vẽ dấu chấm than trắng
    canvas.create_line(30, 15, 30, 40, fill="white", width=5)
    canvas.create_oval(27, 45, 33, 51, fill="white", outline="")

    # Label hướng dẫn
    guide_text = tk.Label(
        guide_frame, 
        text="Hướng dẫn:\n\n"
             "- Sử dụng menu bên trái để chọn chức năng quản lý.\n"
             "- Quản lý câu hỏi: Thêm, sửa, xóa câu hỏi.\n"
             "- Quản lý đề thi: Tạo đề thi từ ngân hàng, chỉnh sửa đề thi.\n"
             "- Nhấn 'Thoát' để đóng chương trình.",
        justify="left",
        font=("Arial", 13, "bold"),
        fg="#1E90FF",
        bg="#f0f4f8",
        width=50,
    )
    guide_text.pack(side="left")

    root.mainloop()


if __name__ == "__main__":
    show_main_ui()
