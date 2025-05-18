import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from managers.question_manager import add_question, load_questions, delete_question, save_questions
from . import main_ui

# List of subjects for questions
SUBJECTS = ["Toán", "Lý", "Hóa", "Anh", "Python", "Java", "C/C++"]

def center_window(win, width, height):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws - width) // 2
    y = (hs - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

def show_question_manager(root):
    # Ẩn form chính
    root.withdraw()

    # Tạo cửa sổ con chính Quản lý câu hỏi
    window = tk.Toplevel(root)
    window.title("Quản lý câu hỏi")
    window.configure(bg="#f0f4f8")

    # Căn giữa màn hình
    center_window(window, 900, 650)
    window.resizable(False, False)

    # Fonts & Style
    title_font = ("Segoe UI", 18, "bold")
    label_font = ("Calibri", 12)
    entry_font = ("Arial Rounded MT Bold", 11)
    btn_font = ("Segoe UI", 11, "bold")

    style = ttk.Style(window)
    style.theme_use("clam")
    style.configure("Rounded.TButton",
                    background="#a9cce3",
                    foreground="#08306b",
                    borderwidth=0,
                    padding=8,
                    font=btn_font)
    style.map("Rounded.TButton",
              background=[("active", "#2e86c1")])

    # Tiêu đề
    tk.Label(window, text="Quản lý câu hỏi", font=title_font, fg="#1E90FF", bg="#f0f4f8").pack(pady=(15, 5))

    # Combobox chọn môn học
    combo_frame = tk.Frame(window, bg="#f0f4f8")
    combo_frame.pack(pady=(0, 10))
    tk.Label(combo_frame, text="Môn học:", font=label_font, bg="#f0f4f8").pack(side="left", padx=(0,5))
    subject_var = tk.StringVar(value=SUBJECTS[0])
    subject_combo = ttk.Combobox(combo_frame, textvariable=subject_var, values=SUBJECTS, state="readonly", font=entry_font)
    subject_combo.pack(side="left")

    # Khung tìm kiếm
    sf = tk.Frame(window, bg="#f0f4f8")
    sf.pack(pady=10)
    tk.Label(sf, text="🔍 Tìm kiếm:", font=label_font, bg="#f0f4f8").pack(side="left")
    search_entry = tk.Entry(sf, font=entry_font, width=50, relief="solid", bd=1)
    search_entry.pack(side="left", padx=8)

    # Listbox với scrollbar
    lf = tk.Frame(window, bg="#f0f4f8")
    lf.pack(padx=15, pady=5, fill="both", expand=True)
    sb = tk.Scrollbar(lf)
    sb.pack(side="right", fill="y")
    lb = tk.Listbox(lf, font=("Arial",11), yscrollcommand=sb.set,
                    selectbackground="#1E90FF", activestyle="none")
    lb.pack(side="left", fill="both", expand=True)
    sb.config(command=lb.yview)

    # Load danh sách câu hỏi
    def load(filtered=None):
        lb.delete(0, tk.END)
        qs = filtered if filtered is not None else load_questions()
        for q in qs:
            lb.insert(tk.END, f"[{q['id']}] ({q.get('subject','')}) {q['question']}")

    # Tìm kiếm
    def search():
        key = search_entry.get().strip().lower()
        if not key:
            load()
            return
        filtered = [q for q in load_questions()
                    if key in q['id'].lower() or key in q['question'].lower()]
        load(filtered)

    # Thêm câu hỏi
    def add():
        subj = subject_var.get()
        question = simpledialog.askstring("➕ Thêm câu hỏi", "Nhập nội dung câu hỏi:", parent=window)
        if not question:
            return
        options = []
        for i in range(4):
            opt = simpledialog.askstring("➕ Thêm phương án", f"Phương án {chr(65+i)}:", parent=window)
            if not opt:
                messagebox.showwarning("Lỗi", "Phải nhập đầy đủ phương án.", parent=window)
                return
            options.append(opt)
        answer = simpledialog.askstring("➕ Đáp án đúng", "Nhập đáp án (A/B/C/D):", parent=window)
        if not answer or answer.upper() not in ["A","B","C","D"]:
            messagebox.showwarning("Lỗi", "Đáp án phải là A, B, C hoặc D.", parent=window)
            return
        # Gọi hàm add_question với subject
        add_question(question, options, answer.upper(), subject=subj)
        load()

    # Xóa câu hỏi
    def delete():
        sel = lb.curselection()
        if not sel:
            messagebox.showinfo("Thông báo", "Chọn câu hỏi để xoá.", parent=window)
            return
        qid = lb.get(sel[0]).split("]")[0][1:]
        if messagebox.askyesno("Xác nhận", "Xoá câu hỏi?", parent=window):
            delete_question(qid)
            load()

    # Sửa câu hỏi
    def edit():
        sel = lb.curselection()
        if not sel:
            messagebox.showwarning("Chú ý", "Chọn câu hỏi để sửa.", parent=window)
            return
        qid = lb.get(sel[0]).split("]")[0][1:]
        qs = load_questions()
        q = next((x for x in qs if x['id']==qid), None)
        if not q:
            messagebox.showerror("Lỗi", "Không tìm thấy.", parent=window)
            return
        ew = tk.Toplevel(window)
        ew.title("Chỉnh sửa câu hỏi")
        ew.configure(bg="#f0f4f8")

        # Căn giữa cửa sổ sửa câu hỏi
        center_window(ew, 750, 650)

        ew.grab_set()
        tk.Label(ew, text="Câu hỏi:", font=label_font, bg="#f0f4f8").pack(anchor="w", padx=10,pady=(10,0))
        te = tk.Text(ew, height=4, wrap="word", font=entry_font, relief="solid", bd=1)
        te.insert("1.0", q['question'])
        te.pack(fill="x", padx=10,pady=5)
        oe=[]
        for i,opt in enumerate(q['options']):
            tk.Label(ew, text=f"Phương án {chr(65+i)}:", font=label_font, bg="#f0f4f8").pack(anchor="w", padx=10,pady=(5,0))
            en = tk.Entry(ew, font=entry_font, relief="solid", bd=1)
            en.insert(0,opt)
            en.pack(fill="x", padx=10,pady=2)
            oe.append(en)
        tk.Label(ew, text="Đáp án đúng (A/B/C/D):", font=label_font, bg="#f0f4f8").pack(anchor="w", padx=10,pady=(10,0))
        ae = tk.Entry(ew, font=entry_font, relief="solid", bd=1)
        ae.insert(0,q['answer'])
        ae.pack(padx=10,pady=5)
        def save_edit():
            newq=te.get("1.0","end").strip()
            nopts=[e.get().strip() for e in oe]
            nans=ae.get().strip().upper()
            if not newq or not all(nopts) or nans not in ["A","B","C","D"]:
                messagebox.showwarning("Lỗi","Thông tin không hợp lệ.", parent=ew)
                return
            q['question']=newq
            q['options']=nopts
            q['answer']=nans
            save_questions(qs)
            messagebox.showinfo("Thành công","Cập nhật thành công.", parent=ew)
            ew.destroy()
            load()
        ttk.Button(ew, text="💾 Lưu", style="Rounded.TButton", command=save_edit).pack(pady=15)

    # Button frame
    bf = tk.Frame(window, bg="#f0f4f8")
    bf.pack(pady=10)
    for txt, cmd in [
        ("➕ Thêm câu hỏi", add),
        ("✏️ Sửa câu hỏi", edit),
        ("🗑️ Xoá câu hỏi", delete),
        ("🔎 Tìm kiếm", search),
    ]:
        ttk.Button(bf, text=txt, style="Rounded.TButton", command=cmd).pack(side="left", padx=8)

    def on_close():
        window.destroy()
        root.deiconify()
    ttk.Button(bf, text="❌ Đóng", style="Rounded.TButton", command=on_close).pack(side="left", padx=8)
    window.protocol("WM_DELETE_WINDOW", on_close)

    load()
    window.mainloop()
