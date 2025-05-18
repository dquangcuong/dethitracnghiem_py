import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from managers.exam_manager import create_exam, load_exams, delete_exam
from managers.question_manager import load_questions
import random

def show_exam_manager(root):
    # Ẩn form main
    root.withdraw()

    # Tạo cửa sổ con
    window = tk.Toplevel(root)
    window.title("Quản lý đề thi")

    # Căn giữa màn hình
    w, h = 800, 600
    ws, hs = window.winfo_screenwidth(), window.winfo_screenheight()
    x, y = (ws - w) // 2, (hs - h) // 2
    window.geometry(f"{w}x{h}+{x}+{y}")
    window.configure(bg="#cce6ff")
    window.resizable(False, False)

    # Style cho nút bo tròn
    style = ttk.Style(window)
    style.theme_use("clam")
    style.configure("Rounded.TButton",
                    background="#99ccff",
                    foreground="#003366",
                    borderwidth=0,
                    padding=8,
                    font=("Segoe UI", 10, "bold"))
    style.map("Rounded.TButton",
              background=[("active", "#7abaff")])

    # Icon unicode đơn giản
    icon_add = "\u2795"
    icon_del = "\u274C"
    icon_view = "\U0001F441"
    icon_close = "\u2716"

    # Listbox
    listbox = tk.Listbox(window, font=("Segoe UI", 11), selectbackground="#99ccff")
    listbox.pack(fill="both", expand=True, padx=20, pady=(20, 10))

    # Khung chứa các nút chức năng xếp hàng ngang
    button_frame = tk.Frame(window, bg="#cce6ff")
    button_frame.pack(pady=10)

    def load():
        listbox.delete(0, tk.END)
        for ex in load_exams():
            listbox.insert(tk.END, f"[{ex['id']}] {ex['name']} - {len(ex['questions'])} câu hỏi")

    def add():
        name = simpledialog.askstring("Tên đề thi", "Nhập tên đề thi:", parent=window)
        if not name:
            return
        subjects = ["Python", "Java", "C#", "C/C++", "Toán", "Lý", "Hóa", "Sử", "Địa", "GDCD", "Anh"]
        # Chọn môn
        sw = tk.Toplevel(window)
        sw.title("Chọn môn học")
        sw.geometry("300x120")
        sw.configure(bg="#cce6ff")
        sw.grab_set()
        tk.Label(sw, text="Chọn môn học:", bg="#cce6ff", font=("Segoe UI", 11)).pack(pady=5)
        var = tk.StringVar(value=subjects[0])
        combo = ttk.Combobox(sw, values=subjects, textvariable=var, state="readonly", font=("Segoe UI", 11))
        combo.pack(pady=5)
        def ok(): sw.destroy()
        ttk.Button(sw, text="✔ Xác nhận", style="Rounded.TButton", command=ok).pack(pady=5)
        sw.wait_window()

        sub = var.get()
        try:
            num = simpledialog.askinteger("Số câu hỏi", "Nhập số câu hỏi cần tạo:", parent=window, minvalue=1)
            if num is None: return
        except:
            messagebox.showerror("Lỗi", "Số không hợp lệ.", parent=window)
            return

        qs = [q for q in load_questions() if q.get("subject") == sub]
        if len(qs) < num:
            messagebox.showerror("Lỗi", f"Chỉ có {len(qs)} câu cho {sub}.", parent=window)
            return
        ids = random.sample([q["id"] for q in qs], num)
        try:
            create_exam(name, ids, subject=sub)
            messagebox.showinfo("Thành công", "Tạo đề thi thành công.", parent=window)
            load()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e), parent=window)

    def delete():
        sel = listbox.curselection()
        if not sel: return
        eid = listbox.get(sel[0]).split("]")[0][1:]
        if messagebox.askyesno("Xác nhận", "Xoá đề thi?", parent=window):
            delete_exam(eid)
            load()

    def view():
        sel = listbox.curselection()
        if not sel:
            messagebox.showwarning("Chú ý", "Chọn đề thi để xem.", parent=window)
            return
        eid = listbox.get(sel[0]).split("]")[0][1:]
        ex = next((e for e in load_exams() if e["id"] == eid), None)
        if not ex:
            messagebox.showerror("Lỗi", "Không tìm thấy.", parent=window)
            return

        qmap = {q["id"]: q for q in load_questions()}
        vw = tk.Toplevel(window)
        vw.title(f"Chi tiết: {ex['name']}")
        vw.geometry("700x500")
        vw.configure(bg="#cce6ff")
        cv = tk.Canvas(vw, bg="#cce6ff")
        sb = tk.Scrollbar(vw, command=cv.yview)
        fr = tk.Frame(cv, bg="#cce6ff")
        fr.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.create_window((0, 0), window=fr, anchor="nw")
        cv.configure(yscrollcommand=sb.set)
        cv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def save_q(qid, txt, ans, opts):
            qq = qmap[qid]
            qq["question"] = txt
            qq["answer"] = ans
            qq["options"] = opts
            from managers.question_manager import save_questions
            save_questions(list(qmap.values()))
            messagebox.showinfo("Thành công", "Lưu thành công.", parent=vw)

        for i, qid in enumerate(ex["questions"], 1):
            q = qmap.get(qid)
            if not q: continue
            f = tk.Frame(fr, bg="white", bd=1, relief="solid", padx=5, pady=5)
            f.pack(fill="x", pady=5)
            tk.Label(f, text=f"Câu {i}:", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w")
            txt = tk.Text(f, height=3, wrap="word", font=("Segoe UI", 11))
            txt.insert("1.0", q["question"])
            txt.pack(fill="x")
            tk.Label(f, text="Đáp án đúng:", font=("Segoe UI", 10), bg="white").pack(anchor="w")
            ae = tk.Entry(f, font=("Segoe UI", 11))
            ae.insert(0, q["answer"])
            ae.pack(anchor="w")
            tk.Label(f, text="Các lựa chọn:", font=("Segoe UI", 10, "italic"), bg="white").pack(anchor="w")
            opts = []
            for idx, opt in enumerate(q.get("options", [])):
                tk.Label(f, text=f"Phương án {chr(65 + idx)}:", bg="white").pack(anchor="w")
                e = tk.Entry(f, font=("Segoe UI", 11), width=100)
                e.insert(0, opt)
                e.pack(anchor="w", pady=2)
                opts.append(e)
            btn = ttk.Button(f, text="💾 Lưu", style="Rounded.TButton",
                             command=lambda qid=qid, t=txt, a=ae, os=opts:
                             save_q(qid, t.get("1.0", "end").strip(), a.get().strip(), [o.get().strip() for o in os]))
            btn.pack(pady=5)

    # Các nút chức năng
    ttk.Button(button_frame, text=f"{icon_add} Tạo đề thi", style="Rounded.TButton", command=add).pack(side="left", padx=10)
    ttk.Button(button_frame, text=f"{icon_del} Xoá đề thi", style="Rounded.TButton", command=delete).pack(side="left", padx=10)
    ttk.Button(button_frame, text=f"{icon_view} Xem đề thi", style="Rounded.TButton", command=view).pack(side="left", padx=10)

    def on_close():
        window.destroy()
        root.deiconify()

    # Nút đóng bên dưới
    ttk.Button(window, text=f"{icon_close} Đóng", style="Rounded.TButton", command=on_close).pack(pady=10)

    load()
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()
