from tkinter import *
from tkcalendar import DateEntry
from tkinter import ttk,messagebox,filedialog
from datetime import date
import pyodbc
import pandas as pd
import webbrowser
#Kết nối tới SQL Sever
TEN_SERVER = '(local)'
TEN_CSDL = 'QLBH'
MATHELOAI = {}
def lay_ket_noi():
    try:
        conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};'
            f'SERVER={TEN_SERVER};'
            f'DATABASE={TEN_CSDL};'
            f'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", f"Không kết nối được SQL Server!\nLỗi: {e}")
        return None
#Chỉnh màu
MAU_NEN = "#F0F2F5"
MAU_NUT = "#639CD6"
MAU_NUT_XOA = "#FA0429"
MAU_CHU = "Black"     
#Dịch từ thể loại thành mã thể loại
def tai_danh_sach_the_loai():
    global MATHELOAI
    conn = lay_ket_noi()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tentheloai, matheloai FROM THELOAI")
        data = cursor.fetchall()
        MATHELOAI = {row[0]: row[1] for row in data}
        Theloai['values'] = list(MATHELOAI.keys())
        conn.close()
def lay_ma_the_loai(ten_the_loai):
    return MATHELOAI.get(ten_the_loai)
#Hàm canh giữa cửa sổ
def center_window(win, rong, dai):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (rong // 2)
    y = (hs // 2) - (dai // 2)
    win.geometry(f'{rong}x{dai}+{x}+{y}')
#Cửa sổ chính
root = Tk()
root.title("Quản lý bài hát")
center_window(root, 750, 550)
root.resizable(FALSE,FALSE)
root.configure(bg=MAU_NEN)
#Tiêu đề
Label(root,text="QUẢN LÝ BÀI HÁT",font=("Arial", 18, "bold"),bg=MAU_NEN,fg="DarkGreen").pack(pady=10)
#Frame nhập thông tin
thongtin=Frame(root,bg=MAU_NEN)
thongtin.pack(pady=5, padx=10, fill="x")
    #Mã bài hát
Label(thongtin,text="Mã bài hát",font=("Arial",15),bg=MAU_NEN,fg=MAU_CHU).grid(row=0, column=0, padx=5, pady=5,sticky="w")
Maso=Entry(thongtin,width=20)
Maso.grid(row=0, column=1, padx=(5,50), pady=5, sticky="w")
    #Tên ca sĩ
Label(thongtin,text="Tên ca sĩ",font=("Arial",15),bg=MAU_NEN,fg=MAU_CHU).grid(row=0, column=2, padx=2, pady=5,sticky="w")
Tencasi=Entry(thongtin,width=20)
Tencasi.grid(row=0,column=3,padx=5,pady=5,sticky="w")
    #Tên bài hát
Label(thongtin,text="Tên bài hát",font=("Arial",15),bg=MAU_NEN,fg=MAU_CHU).grid(row=1, column=0, padx=5, pady=5,sticky="w")
Tenbaihat=Entry(thongtin,width=20)
Tenbaihat.grid(row=1, column=1, padx=(5,50), pady=5, sticky="w")
    #Ngày ra mắt
Label(thongtin,text="Ngày ra mắt",font=("Arial",15),bg=MAU_NEN,fg=MAU_CHU).grid(row=1,column=2,padx=5,pady=5,sticky="w")
Ngayramat=DateEntry(thongtin,width=12,background="black",foreground="white", date_pattern="yyyy-mm-dd")
Ngayramat.grid(row=1,column=3,padx=5,pady=5,sticky="w")
    #Thể loại
Label(thongtin,text="Thể loại",font=("Arial",15),bg=MAU_NEN,fg=MAU_CHU).grid(row=2,column=0,padx=5,pady=5,sticky="w")
Theloai=ttk.Combobox(thongtin,values=["Rap","Trữ tình","Dân ca","Pop","Rock","Ballad"],width=20)
Theloai.grid(row=2, column=1, padx=(5,50), pady=5, sticky="w")
#Chức năng tìm kiếm (theo mã bài hát) và sắp xếp (theo thể loại)
def tim_kiem():
    ma_can_tim = timkiem.get()
    if ma_can_tim == "":
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã bài hát cần tìm!")
        return
    # Xóa bảng cũ
    for item in bang.get_children(): bang.delete(item)
    conn = lay_ket_noi()
    cursor = conn.cursor()
    sql = """
        SELECT B.maso, B.tenbaihat, B.tencasi, B.ngayramat, T.tentheloai 
        FROM BAIHAT B JOIN THELOAI T ON B.matheloai = T.matheloai
        WHERE B.maso LIKE ?
    """
    cursor.execute(sql, (f"%{ma_can_tim}%",))
    rows = cursor.fetchall()
    if len(rows) == 0:
        messagebox.showinfo("Thông báo", "Không tìm thấy bài hát nào!")
    for row in rows:
        bang.insert("", END, values=list(row))
    conn.close()
def sap_xep():
    for item in bang.get_children(): bang.delete(item)
    conn = lay_ket_noi()
    cursor = conn.cursor()
    sql = """
        SELECT B.maso, B.tenbaihat, B.tencasi, B.ngayramat, T.tentheloai 
        FROM BAIHAT B JOIN THELOAI T ON B.matheloai = T.matheloai
        ORDER BY T.tentheloai ASC
    """
    cursor.execute(sql)
    for row in cursor.fetchall():
        bang.insert("", END, values=list(row))
    conn.close()
#Nút tìm kiếm và sắp xếp
tkvasx=Frame(root,bg=MAU_NEN)
tkvasx.pack(pady=5, fill="x", padx=20)
    #Nút tìm kiếm 
Label(tkvasx,text="Tìm kiếm (Theo mã bài hát)",font=("Arial",10,"bold"),bg=MAU_NEN,fg=MAU_CHU).grid(row=0,column=0,padx=10)
timkiem=Entry(tkvasx,width=30)
timkiem.grid(row=0,column=1)
Button(tkvasx,text="Tìm",bg=MAU_NUT,command=tim_kiem).grid(row=0,column=2,padx=2)
    #Nút sắp xếp
Button(tkvasx,text="Sắp xếp theo thể loại",bg=MAU_NUT,command=sap_xep).grid(row=0,column=3,padx=150)
#Bảng danh sách bài hát
ds_baihat=Label(root,text="Danh sách bài hát",font=("Arial",15,"bold"),bg=MAU_NEN,fg=MAU_CHU).pack(pady=5, anchor="w", padx=10)
cot=("Mã bài hát","Tên bài hát","Tên ca sĩ","Ngày ra mắt","Thể loại")
bang=ttk.Treeview(root, columns=cot,show="headings",height=10)
for col in cot:
    bang.heading(col,text=col.capitalize())
bang.column("Mã bài hát", width=60, anchor="center")
bang.column("Tên bài hát", width=150)
bang.column("Tên ca sĩ", width=100)
bang.column("Ngày ra mắt", width=70, anchor="center")
bang.column("Thể loại", width=100, anchor="center")
bang.pack(padx=10, pady=5, fill="both")
#Hàm chức năng
def tai_du_lieu_len_bang():
    for item in bang.get_children(): bang.delete(item)
    conn = lay_ket_noi()
    if conn:
        cursor = conn.cursor()
        sql = """
            SELECT B.maso, B.tenbaihat, B.tencasi, B.ngayramat, T.tentheloai 
            FROM BAIHAT B 
            JOIN THELOAI T ON B.matheloai = T.matheloai
        """
        cursor.execute(sql)
        for row in cursor.fetchall():
            bang.insert("", END, values=list(row))
        conn.close()
def them_bh():
    ms = Maso.get()
    tbh = Tenbaihat.get()
    tcs = Tencasi.get()
    nrm = Ngayramat.get()
    ten_tl = Theloai.get()
    # Chuyển tên thể loại thành mã
    ma_tl = lay_ma_the_loai(ten_tl)
    if not ms or not ma_tl or not tbh or not tcs:
        messagebox.showwarning("Thiếu dữ liệu")
        return
    try:
        conn = lay_ket_noi()
        cursor = conn.cursor()
        sql = "INSERT INTO BAIHAT (maso, tencasi, tenbaihat, ngayramat, matheloai) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql, (ms, tcs, tbh, nrm, ma_tl))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thêm dữ liệu", "Thêm thành công!")
        tai_du_lieu_len_bang()
        huy_dulieu()
    except Exception as e:
        messagebox.showerror("Lỗi SQL", str(e))
def sua_bh():
    chon_sua = bang.selection()
    if not chon_sua:
        messagebox.showwarning("Chưa chọn", "Chọn dòng cần sửa")
        return
    ma_tl = lay_ma_the_loai(Theloai.get())
    try:
        conn = lay_ket_noi()
        cursor = conn.cursor()
        sql = """
            UPDATE BAIHAT 
            SET tencasi=?, tenbaihat=?, ngayramat=?, matheloai=? 
            WHERE maso=?
        """
        cursor.execute(sql, (Tencasi.get(), Tenbaihat.get(), Ngayramat.get(), ma_tl, Maso.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("OK", "Cập nhật thành công!")
        tai_du_lieu_len_bang()
        huy_dulieu()
    except Exception as e:
        messagebox.showerror("Lỗi SQL", str(e))
def xoa_bh():
    chon_xoa = bang.selection()
    if not chon_xoa: return
    ms_xoa = bang.item(chon_xoa)['values'][0]
    if messagebox.askyesno("Xóa", "Bạn chắc chắn muốn xóa?"):
        try:
            conn = lay_ket_noi()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM BAIHAT WHERE maso = ?", (ms_xoa,))
            conn.commit()
            conn.close()
            tai_du_lieu_len_bang()
            huy_dulieu()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
def huy_dulieu():
    Maso.delete(0, END)
    Tencasi.delete(0, END)
    Tenbaihat.delete(0, END)
    Ngayramat.set_date(date.today())
    Theloai.set("")
    timkiem.delete(0, END)
    for item in bang.get_children():
        bang.delete(item)
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=.;DATABASE=QLBH;Trusted_Connection=yes;')
        cursor = conn.cursor()
        sql = """
            SELECT B.maso, B.tenbaihat, B.tencasi, B.ngayramat, T.tentheloai 
            FROM BAIHAT B 
            JOIN THELOAI T ON B.matheloai = T.matheloai
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            bang.insert("", END, values=list(row))
        conn.close()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi tải lại dữ liệu: {e}")
def do_du_lieu(event):
    selected = bang.selection()
    if selected:
        values = bang.item(selected)['values']
        Maso.delete(0, END); Maso.insert(0, values[0])
        Tenbaihat.delete(0, END); Tenbaihat.insert(0, values[1])
        Tencasi.delete(0, END); Tencasi.insert(0, values[2])
        Ngayramat.set_date(values[3])
        Theloai.set(values[4])
def xuat_excel():
    duong_dan=filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files","*.xlsx"),("All Files","*.*")],
        title="Chọn nơi lưu danh sách bài hát"
    )
    if not duong_dan :
        return 
    try :
        conn = lay_ket_noi()
        sql="""
            SELECT B.maso, B.tenbaihat, B.tencasi, B.ngayramat, T.tentheloai
            FROM BAIHAT B
            JOIN THELOAI T ON B.matheloai = T.matheloai
        """
        df=pd.read_sql(sql,conn)
        df.columns=['Mã Bài Hát','Tên Bài Hát','Tên Ca Sĩ','Ngày Ra Mắt','Thể Loại']
        df.to_excel(duong_dan,index=False)
        conn.close()
        messagebox.showinfo("Thành công",f"Đã xuất ra file excel tại:\n{duong_dan}")
    except Exception as e :
        messagebox.showerror("Lỗi",f"Không xuất file excel thành công\n Lỗi:{e}")
def phat_nhac():
    chon=bang.selection()
    if not chon:
        messagebox.showwarning("Chưa chọn bài hát","Vui lòng chọn bài hát")
        return
    values = bang.item(chon)['values']
    ten_bai_hat=values[1]
    ten_ca_si=values[2]
    tu_khoa=f"{ten_bai_hat} {ten_ca_si}"
    webbrowser.open(f"https://www.youtube.com/results?search_query={tu_khoa}")
bang.bind("<<TreeviewSelect>>", do_du_lieu)
#Frame nút
nut=Frame(root,bg=MAU_NEN)
nut.pack(pady=5)
Button(nut, text="Thêm",bg=MAU_NUT, width=8, command=them_bh).grid(row=0, column=0,padx=5)
Button(nut, text="Sửa",bg=MAU_NUT, width=8, command=sua_bh).grid(row=0, column=1,padx=5)
Button(nut, text="Hủy",bg=MAU_NUT, width=8, command=huy_dulieu).grid(row=0,column=2, padx=5)
Button(nut, text="Xóa",bg=MAU_NUT_XOA, width=8, command=xoa_bh).grid(row=0, column=3,padx=5)
Button(nut, text="Xuất File Excel",bg=MAU_NUT, width=12, command=xuat_excel).grid(row=0, column=4,padx=5)
Button(nut, text="Phát Nhạc",bg=MAU_NUT, width=10, command=phat_nhac).grid(row=0, column=5,padx=5)
Button(nut, text="Thoát",bg=MAU_NUT, width=8, command=root.quit).grid(row=0,column=6, padx=5)
tai_danh_sach_the_loai()
tai_du_lieu_len_bang()
root.mainloop()