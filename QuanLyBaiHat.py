from tkinter import *
from tkcalendar import DateEntry
from tkinter import ttk,messagebox
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
#Tiêu đề
Label(root,text="QUẢN LÝ BÀI HÁT",fg="DarkGreen",font=("Arial", 18, "bold")).pack(pady=10)
#Frame nhập thông tin
thongtin=Frame(root)
thongtin.pack(pady=5, padx=10, fill="x")
    #Mã bài hát
Label(thongtin,text="Mã bài hát",font=("Arial",15)).grid(row=0, column=0, padx=5, pady=5,sticky="w")
Maso=Entry(thongtin,width=20)
Maso.grid(row=0, column=1, padx=(5,50), pady=5, sticky="w")
    #Tên ca sĩ
Label(thongtin,text="Tên ca sĩ",font=("Arial",15)).grid(row=0, column=2, padx=2, pady=5,sticky="w")
Tencasi=Entry(thongtin,width=20)
Tencasi.grid(row=0,column=3,padx=5,pady=5,sticky="w")
    #Tên bài hát
Label(thongtin,text="Tên bài hát",font=("Arial",15)).grid(row=1, column=0, padx=5, pady=5,sticky="w")
Tenbaihat=Entry(thongtin,width=20)
Tenbaihat.grid(row=1, column=1, padx=(5,50), pady=5, sticky="w")
    #Ngày ra mắt
Label(thongtin,text="Ngày ra mắt",font=("Arial",15)).grid(row=1,column=2,padx=5,pady=5,sticky="w")
Ngayramat=DateEntry(thongtin,width=12,background="black",foreground="white", date_pattern="yyyy-mm-dd")
Ngayramat.grid(row=1,column=3,padx=5,pady=5,sticky="w")
    #Thể loại
Label(thongtin,text="Thể loại",font=("Arial",15)).grid(row=2,column=0,padx=5,pady=5,sticky="w")
Theloai=ttk.Combobox(thongtin,values=["Rap","Trữ tình","Dân ca","Pop","Rock","Ballad"],width=20)
Theloai.grid(row=2, column=1, padx=(5,50), pady=5, sticky="w")
#Nút tìm kiếm và sắp xếp
tkvasx=Frame(root)
tkvasx.pack(pady=5, fill="x", padx=20)
Label(tkvasx,text="Tìm kiếm(Theo mã bài hát)",font=("Arial",10,"bold")).grid(row=0,column=0,padx=10)
timkiem=Entry(tkvasx,width=30).grid(row=0,column=1)
Button(tkvasx,text="Tìm").grid(row=0,column=2)
Button(tkvasx,text="Sắp xếp theo thể loại").grid(row=0,column=3,padx=150)
#Bảng danh sách bài hát
ds_baihat=Label(root,text="Danh sách bài hát",font=("Arial",15,"bold")).pack(pady=5, anchor="w", padx=10)
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
def them_bh():
    maso = Maso.get()
    tencasi = Tencasi.get()
    tenbaihat = Tenbaihat.get()
    ngayramat = Ngayramat.get()
    theloai = Theloai.get()
    if maso == "" or tencasi == "" or tenbaihat == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
        return
def luu_bh():
    maso = Maso.get()
    tencasi = Tencasi.get()
    tenbaihat = Tenbaihat.get()
    ngayramat = Ngayramat.get()
    theloai = Theloai.get()
def sua_bh():
    chon = bang.selection()
    if not chon:
        messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để sửa")
        return
    values = bang.item(chon)["values"]
    Maso.delete(0, END)
    Maso.insert(0, values[0])
    Tencasi.delete(0, END)
    Tencasi.insert(0, values[1])
    Tenbaihat.delete(0, END)
    Tenbaihat.insert(0, values[2])
    Ngayramat.set_date(values[3])
    Theloai.set(values[4])
def huy_dulieu():
    Maso.delete(0, END)
    Tencasi.delete(0, END)
    Tenbaihat.delete(0, END)
    Ngayramat.set_date("2000-01-01")
    Theloai.set("")
def xoa_bh():
    selected = bang.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để xóa")
        return
    maso = bang.item(selected)["values"][0]
#Frame nút
nut=Frame(root)
nut.pack(pady=5)
Button(nut, text="Thêm", width=8, command=them_bh).grid(row=0, column=0,padx=5)
Button(nut, text="Lưu", width=8, command=luu_bh).grid(row=0, column=1,padx=5)
Button(nut, text="Sửa", width=8, command=sua_bh).grid(row=0, column=2,padx=5)
Button(nut, text="Hủy", width=8, command=huy_dulieu).grid(row=0,column=3, padx=5)
Button(nut, text="Xóa", width=8, command=xoa_bh).grid(row=0, column=4,padx=5)
Button(nut, text="Thoát", width=8, command=root.quit).grid(row=0,column=5, padx=5)

root.mainloop() 