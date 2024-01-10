# 11/01/2024

import piexif
import os
import math
from tkinter import font , Tk , Widget , Button , Frame , Label , Text , OptionMenu , LabelFrame , StringVar , Canvas , Scrollbar
from PIL import ImageTk, Image
from datetime import datetime

global dosya_yolu, resim_yolu, resim_listesi, etiket_listesi

dosya_yolu = os.path.dirname(os.path.realpath(__file__))
resim_yolu = dosya_yolu + "\JPGLER"
resim_listesi = os.listdir(resim_yolu)
etiket_yolu = dosya_yolu + "\Etiketler"
etiket_listesi = ["SEÇ"] + os.listdir(etiket_yolu)

def all_children(wid, finList=None, indent=0):
    finList = finList or []
    children = wid.winfo_children()

    for item in children:
        finList.append(item)
        all_children(item, finList, indent + 1)
    return finList

def resim_geç(taraf:str):
    if taraf == "sağ":
        girilen = int(resim_index_sol.get("0.0","end").strip())
        max_resim_sayı = int(resim_index_sağ.cget("text"))

        if girilen < 1:
            resim_index_sol.delete("0.0","end")
            resim_index_sol.insert("0.0",chars="    2")
        elif girilen < max_resim_sayı :
            resim_index_sol.delete("0.0","end")
            resim_index_sol.insert("0.0",chars="    "+str(girilen+1))
        elif girilen > max_resim_sayı :
            resim_index_sol.delete("0.0","end")
            resim_index_sol.insert("0.0",chars="    "+str(max_resim_sayı))
        
    elif taraf == "sol":            
        girilen = int(resim_index_sol.get("0.0","end").strip())
        max_resim_sayı = int(resim_index_sağ.cget("text"))

        if girilen > max_resim_sayı:
            resim_index_sol.delete("0.0","end")
            resim_index_sol.insert("0.0",chars="    "+str(max_resim_sayı-1))
        elif girilen > 1 :
            resim_index_sol.delete("0.0","end")
            resim_index_sol.insert("0.0",chars="    "+str(girilen-1))
        elif girilen < 1 :
            resim_index_sol.delete("0.0","end")
            resim_index_sol.insert("0.0",chars="    1")

    elif taraf == "git":
        girilen = int(resim_index_sol.get("0.0","end").strip())
        max_resim_sayı = int(resim_index_sağ.cget("text"))

        if girilen > max_resim_sayı:
            resim_index_sol.delete("0.0","end")
            resim_index_sol.insert("0.0",chars="    "+str(max_resim_sayı))
        elif girilen > 1 and girilen <= max_resim_sayı:
            resim_index_sol.delete("0.0","end")
            resim_index_sol.insert("0.0",chars="    "+str(girilen))
        elif girilen < 1 :
            resim_index_sol.delete("0.0","end")
            resim_index_sol.insert("0.0",chars="    1")
              
    x_width = resim_label.winfo_width()
    y_height = resim_label.winfo_height()
    global image
    image = ImageTk.PhotoImage(Image.open((resim_yolu)+"\\"+resim_listesi[int(resim_index_sol.get("0.0","end"))-1]).resize((x_width,y_height)))
    resim_label.configure(image=image)
    resim_adı_label.configure(text=resim_listesi[int(resim_index_sol.get("0.0","end"))-1][:-4])

    tag_varmı()

def get_wh(widget:Widget):
    """
    width + height
    """
    ana_ekran.update_idletasks()
    width = widget.winfo_width()
    height = widget.winfo_height()
    return width , height

def etiket_kaydet():

    now = datetime.now()
    ŞU_ANKİ_TARİH = now.strftime( "%d-%m-%Y" )
    ŞU_ANKİ_SAAT = now.strftime( "%H-%M-%S" )
    dosya_yolu = os.path.dirname(os.path.realpath(__file__))
    açılacak_text = dosya_yolu + "\\Etiketler\\TARIH~"+str(ŞU_ANKİ_TARİH)+" ⨝  SAAT~"+str(ŞU_ANKİ_SAAT)+".txt"
    
    kaydedilen_etiket = []
    for framelabels in all_children(sağ_ekran_orta_ana_FRAME):
        if isinstance(framelabels, LabelFrame) and framelabels.cget("text") != "":
            etiket = ""
            etiket += framelabels.cget("text") + ":"
            for f2_labels in all_children(framelabels):
                if isinstance(f2_labels, LabelFrame):
                    for buttons in all_children(f2_labels):
                        if isinstance(buttons, Button):
                            etiket += str(buttons.cget("text")) + "-"
                    kaydedilen_etiket.append(etiket[:-1])
    
    dosya = open(açılacak_text, "w")

    for kaydet in kaydedilen_etiket:
        dosya.write(kaydet+"\n")

    dosya.close()

    global option_list_variable, etiket_listesi_option
    etiket_listesi_option.destroy()
    etiket_yolu = dosya_yolu + "\Etiketler"
    etiket_listesi = ["SEÇ"] + os.listdir(etiket_yolu)
    option_list_variable = StringVar(ana_ekran)
    option_list_variable.set(etiket_listesi[0])
    etiket_listesi_option = OptionMenu(sağ_ekran_üst, option_list_variable, *etiket_listesi)
    etiket_listesi_option.pack(fill="y", expand=False, side="left")
    
def etiket_yükle():

    for widgets in all_children(sağ_ekran_orta_ana_FRAME):
        widgets.destroy() 
    
    text_dosyası = []
    text_dosya_adı = option_list_variable.get()
    txt_dosyası = open(str(dosya_yolu)+"\\Etiketler\\"+str(text_dosya_adı))
    for satır in txt_dosyası:
        satır = satır.rstrip('\n')
        text_dosyası.append(str(satır))
    txt_dosyası.close()

    for satır in text_dosyası :

        buton_varmı = False
        if ":" in satır:
            satır = satır.split(":")
            satır_konu = satır[0]
            if "-" in satır[1] or len(satır[1][0])>0 :
                satır_etiket = satır[1].split("-")
                buton_varmı = True
        else:
            satır_konu = satır
            buton_varmı = False

        etiket_frame = LabelFrame(sağ_ekran_orta_ana_FRAME, text=satır_konu, width=140, height=200, labelanchor="n")
        etiket_frame.pack(fill="y", expand=False, side="left")

        eklenen_text = Text(etiket_frame, height=1, width=16)
        eklenen_text.pack(fill="x", expand=False, side="top")
        eklenen_text.propagate(0)

        eklenen_buton = Button(etiket_frame, text=str(etiket_frame.cget("text"))+" EKLE", height=1, width=16)
        eklenen_buton.pack(fill="x", expand=False, side="top")
        eklenen_buton.propagate(0)

        Label(etiket_frame, text="▬▬▬▬▬▬▬▬▬▬▬").pack(fill="x", expand=False, side="top")

        labelframe = LabelFrame(etiket_frame)
        labelframe.pack(fill="y", expand=False,side="top")
        labelframe.grid_propagate(0)

        eklenen_buton.configure(command=lambda text=eklenen_text , labelframe=labelframe : etiket_konu_2(text,labelframe))

        if buton_varmı == True:
            for etiket_adı in satır_etiket:
                if labelframe.winfo_id() not in button_pressed: 
                    button_pressed[labelframe.winfo_id()] = {}

                yeni_buton = Button(labelframe, text=etiket_adı, height=1, width=16)
                yeni_buton.pack(fill="x", expand=False)
                yeni_buton.configure(command=lambda master=yeni_buton , labelframe=labelframe : etiket_etiket(master,labelframe))
                button_pressed[labelframe.winfo_id()][yeni_buton.winfo_id()] = 0

    sağ_ekran_orta_ana_CANVAS.update()
    sağ_ekran_orta_ana_CANVAS.configure(scrollregion=sağ_ekran_orta_ana_CANVAS.bbox("all"))

def etiketi_resme_ekle():

    kaydedilen_etiket = []
    for framelabels in all_children(sağ_ekran_orta_ana_FRAME):
        if isinstance(framelabels, LabelFrame):
            etiket = ""
            if framelabels.cget("text") != "":
                etiket += framelabels.cget("text") + ":"
                for buttons in all_children(framelabels):
                    if isinstance(buttons, Button):
                        if buttons.cget("background") == "#84e084":
                            etiket += str(buttons.cget("text")) + "-"
                kaydedilen_etiket.append(etiket[:-1])

    etiketlenen = ""
    for e in kaydedilen_etiket:
        e = e.split(":")
        e_e = e[1].split("-")
        for et in e_e:
            etiketlenen += str(e[0])+":"+str(et)+";"
    etiketlenen = etiketlenen[:-1]

    for wd in all_children(sağ_ekran_orta_ana_FRAME):
        if isinstance(wd,Button):
            wd.configure(background="white")

    Image.open(str(resim_yolu + "\\" + resim_listesi[int(resim_index_sol.get("0.0","end"))-1]))
    etikett = bytes(etiketlenen, 'utf-16le')
    zeroth_ifd = { 40094 : etikett }
    exif_bytes = piexif.dump( { "0th" : zeroth_ifd } )
    piexif.insert(exif_bytes, str(resim_yolu + "\\" + resim_listesi[int(resim_index_sol.get("0.0","end"))-1]))
    piexif.ExifIFD

    tag_varmı()

# 18246 : rating : 0-5 yıldız
# 34665 : Exiftag
# 40091 : XPTitle : Başlık
# 40092 : XPComment : Açıklamalar
# 40093 ve 315 : Yazarlar
# 40094 : etiketler [ her bir etiket "" içinde ; ile ayırarak yazılmalı ]
# 40095 : Konu

#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩
#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩

def etiket_konu(frame:Frame):

    konu = str(etiket_konu_text.get("1.0", "end-1c"))
    konular = []

    etiket_konu_text.delete("1.0", "end")

    for k in all_children(sağ_ekran_orta_ana_FRAME):
        if isinstance(k, LabelFrame):
            if k.cget("text") != "":
                konular.append(k.cget("text"))

    if konu != "" and konu not in konular:

        etiket_frame = LabelFrame(frame, text=konu, width=140, height=200, labelanchor="n")
        etiket_frame.pack(fill="y", expand=False, side="left")
        etiket_frame.grid_propagate(0)

        eklenen_text = Text(etiket_frame, height=1, width=16)
        eklenen_text.pack(fill="x", expand=False, side="top")
        eklenen_text.propagate(0)
        
        eklenen_buton = Button(etiket_frame, text=str(etiket_frame.cget("text"))+" EKLE", height=1, width=16)
        eklenen_buton.pack(fill="x", expand=False, side="top")
        eklenen_buton.propagate(0)
        
        Label(etiket_frame, text="▬▬▬▬▬▬▬▬▬▬▬").pack(fill="x", expand=False, side="top")

        labelframe = LabelFrame(etiket_frame)
        labelframe.pack(fill="y", expand=False,side="top")
        labelframe.grid_propagate(0)

        eklenen_buton.configure(command=lambda text=eklenen_text , labelframe=labelframe : etiket_konu_2(text,labelframe))

        sağ_ekran_orta_ana_CANVAS.update_idletasks()
        sağ_ekran_orta_ana_CANVAS.configure(scrollregion=sağ_ekran_orta_ana_CANVAS.bbox("all"))

def etiket_konu_2(text:Text, labelframe:LabelFrame):

    global button_pressed
    text_text = text.get("1.0", "end")
    text.delete("1.0", "end")
    text_list = []

    for buttons in all_children(labelframe):
        text_list.append(buttons.cget("text"))

    if text_text != "" and text_text not in text_list:
        
        for buttons in all_children(labelframe):
            buttons.destroy()

        if text_list != []:
            button_pressed.pop(labelframe.winfo_id())

        text_list.append(text_text)
        text_list = sorted(text_list)
        
        button_pressed[labelframe.winfo_id()] = {}
        for texts in text_list:
            yeni_buton = Button(labelframe, text=texts, height=1, width=16)
            yeni_buton.pack(fill="x", expand=False)
            yeni_buton.configure(command=lambda master=yeni_buton , labelframe=labelframe : etiket_etiket(master,labelframe))
            button_pressed[labelframe.winfo_id()][yeni_buton.winfo_id()] = 0

        sağ_ekran_orta_ana_CANVAS.update_idletasks()
        sağ_ekran_orta_ana_CANVAS.configure(scrollregion=sağ_ekran_orta_ana_CANVAS.bbox("all"))

def etiket_etiket(master:Button, labelframe:LabelFrame):

    global button_pressed
    if button_pressed[labelframe.winfo_id()][master.winfo_id()] == 0:
        button_pressed[labelframe.winfo_id()][master.winfo_id()] = 1
        master.configure(background="#84e084")

    elif button_pressed[labelframe.winfo_id()][master.winfo_id()] == 1:
        button_pressed[labelframe.winfo_id()][master.winfo_id()] = 0
        master.configure(background="white")

#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩
#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩

def tag_varmı():
    image_tag = Image.open((resim_yolu)+"\\"+resim_listesi[int(resim_index_sol.get("0.0","end"))-1])
    
    if image_tag._getexif() == None:
        resim_label_varmı.configure(background="red")
    else:
        if 40094 in image_tag._getexif().keys():
            resim_label_varmı.configure(background="green")
        else:
            resim_label_varmı.configure(background="red")

def herşeyi_sıfırla():
    for k in all_children(sağ_ekran_orta_ana_FRAME):
        k.destroy()

def kapat(widget:Widget,buton):
    widget.destroy()

    if isinstance(buton,Button):
        buton.configure(background="white", state="active")

def ekran() :

    global ana_ekran
    
    ana_ekran = Tk()

    ana_ekran.configure(background = "#B3B3B3")
    ana_ekran.title("Etiketleyici")
    ana_ekran.attributes("-fullscreen", True)
    
    global button_pressed, resim_adı_FONT, sağ_sol_FONT
    
    küçük_buton_FONT = font.Font(family="Segoe UI Black", weight="bold")
    resim_adı_FONT = font.Font(family="Segoe UI Black", size=15, weight="bold")
    sağ_sol_FONT = font.Font(size=20, weight="bold")
    button_pressed = dict()

#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩
#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩ SOL EKRAN ▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩
#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩

    width , height = get_wh(ana_ekran)
    sol_ekran_width = math.floor(width*35/100)-5
    sol_ekran_height = math.floor(height*1/5)-5
    sol_ekran = Frame( ana_ekran, background="#c8c8c8", width=sol_ekran_width, height=math.floor(height), name="sol_ekran")
    sol_ekran.grid(row=1, column=0)
    width , _ = get_wh(sol_ekran)
    sol_ekran_width = width

    Button(ana_ekran, width=15, height=2, text="KAPAT",\
            command=lambda:kapat(ana_ekran,1), background="red").grid(row=0, column=0)

    sol_ekran_üst = Frame( sol_ekran, width=sol_ekran_width, height=math.floor(get_wh(ana_ekran)[0]*1/25), name="sol_ekran_üst")
    sol_ekran_üst.grid(row=0, column=0)
    sol_ekran_üst.propagate(0)

    sol_ekran_orta = Frame( sol_ekran, width=sol_ekran_width, height=math.floor(height*8/11), name="sol_ekran_orta")
    sol_ekran_orta.grid(row=1, column=0)
    sol_ekran_orta.propagate(0)

    sol_ekran_alt = Frame( sol_ekran, width=sol_ekran_width, height=math.floor(height*15/100), name="sol_ekran_alt")
    sol_ekran_alt.grid(row=2, column=0)
    sol_ekran_alt.propagate(0)

#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩
#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩ SAĞ EKRAN ▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩
#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩

    width , height = get_wh(ana_ekran)
    sağ_ekran_width = math.floor(width*65/100)-5
    sağ_ekran = Frame(ana_ekran, width=sağ_ekran_width, height=math.floor(height), name="sağ_ekran")
    sağ_ekran.grid(row=1, column=1)
    width , _ = get_wh(sağ_ekran)
    sağ_ekran_width = width
    
    global sağ_ekran_üst
    sağ_ekran_üst = Frame(sağ_ekran, width=get_wh(sağ_ekran)[0], height=math.floor(get_wh(sağ_ekran)[1]*5/100), name="sağ_ekran_üst")
    sağ_ekran_üst.grid(row=0, column=0)
    sağ_ekran_üst.propagate(0)

    global sağ_ekran_orta
    sağ_ekran_orta = Frame(sağ_ekran, width=get_wh(sağ_ekran)[0], height=math.floor(height*8/11), name="sağ_ekran_orta")
    sağ_ekran_orta.grid(row=1, column=0)
    sağ_ekran_orta.propagate(0)

    global sağ_ekran_orta_ana
    sağ_ekran_orta_ana = Frame(sağ_ekran_orta, width=sağ_ekran_width-30, height=math.floor(height*8/11)-50, name="sağ_ekran_orta_ana")
    sağ_ekran_orta_ana.grid(row=0, column=0)
    sağ_ekran_orta_ana.propagate(0)

    global sağ_ekran_orta_scroll_y
    sağ_ekran_orta_scroll_y = Frame(sağ_ekran_orta, width=30, height=get_wh(sağ_ekran_orta_ana)[1], name="sağ_ekran_orta_scroll_y")
    sağ_ekran_orta_scroll_y.grid(row=0, column=1)
    sağ_ekran_orta_scroll_y.propagate(0)

    global sağ_ekran_orta_scroll_x
    sağ_ekran_orta_scroll_x = Frame(sağ_ekran_orta, width=get_wh(sağ_ekran_orta_ana)[0], height=30, name="sağ_ekran_orta_scroll_x")
    sağ_ekran_orta_scroll_x.grid(row=1, column=0)
    sağ_ekran_orta_scroll_x.propagate(0)

    global sağ_ekran_orta_ana_CANVAS
    sağ_ekran_orta_ana_CANVAS = Canvas(sağ_ekran_orta_ana, width=get_wh(sağ_ekran_orta_ana)[0], height=get_wh(sağ_ekran_orta_ana)[1])
    sağ_ekran_orta_ana_CANVAS.pack()

    global sağ_ekran_orta_ana_FRAME, canvas_create_window
    sağ_ekran_orta_ana_FRAME = Frame(sağ_ekran_orta_ana_CANVAS, width=get_wh(sağ_ekran_orta)[0]-30, height=get_wh(sağ_ekran_orta)[1])
    sağ_ekran_orta_ana_CANVAS.create_window((0,0), window=sağ_ekran_orta_ana_FRAME, anchor="nw")

    scrollbar_y = Scrollbar(sağ_ekran_orta_scroll_y, orient="vertical", command=sağ_ekran_orta_ana_CANVAS.yview)
    scrollbar_y.pack(fill="y", expand=True)

    scrollbar_x = Scrollbar(sağ_ekran_orta_scroll_x, orient="horizontal", command=sağ_ekran_orta_ana_CANVAS.xview)
    scrollbar_x.pack(fill="x", expand=True)

    sağ_ekran_orta_ana_CANVAS.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    sağ_ekran_alt = Frame(sağ_ekran, width=sağ_ekran_width, height=math.floor(height*15/100), name="sağ_ekran_alt")
    sağ_ekran_alt.grid(row=2, column=0)
    sağ_ekran_alt.propagate(0)

#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩
#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩ WİDGETLERİN YERLEŞTİRİLMESİ ▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩
#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩    

#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩ SOL + ÜST ▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩

    global resim_adı_label, resim_label_varmı
    resim_adı_label = Label(sol_ekran_üst, text="RESİM ADI", font=resim_adı_FONT, background="yellow", name="resim_adı_label")
    resim_adı_label.pack(fill="both", expand=True, side="bottom")

    resim_label_varmı = Label(sol_ekran_üst, background="red", height=1)
    resim_label_varmı.pack(fill="x", expand=False)

#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩ SOL + ORTA ▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩

    global resim_label
    resim_label = Label(sol_ekran_orta, name="resim_label")
    resim_label.pack(fill="both", expand=False)
    x_width = sol_ekran_orta.winfo_width()
    y_height = sol_ekran_orta.winfo_height()
    resim_label.configure(width=x_width, height=y_height)
    resim_label.propagate(0)

    image = ImageTk.PhotoImage(Image.open((resim_yolu)+"\\"+resim_listesi[0]).resize((x_width,y_height)))
    resim_label.configure(image=image)
    resim_adı_label.configure(text=resim_listesi[0][:-4])

#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩ SOL + ALT ▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩

    git_butonu = Button(sol_ekran_alt, text="GİT", width=15, height=3)
    git_butonu.pack(side="bottom")

    resim_sol_geç = Button(sol_ekran_alt, text="<<", width=10, height=2, font=sağ_sol_FONT, name="resim_sol_geç")
    resim_sol_geç.configure(command=lambda:resim_geç("sol"), background="#c8c8c8")
    resim_sol_geç.pack(side="left", expand=False)
    
    global resim_index_sol, resim_index_sağ

    resim_index_sol = Text(sol_ekran_alt, width=5, height=1, background="#c8c8c8", name="resim_index_sol", font=sağ_sol_FONT)
    resim_index_sol.pack(side="left", expand=False)
    resim_index_sol.insert("0.0","    1")

    resim_index_orta = Label(sol_ekran_alt, text="|\n|", width=1, height=2, font=sağ_sol_FONT, name="resim_index_orta")
    resim_index_orta.pack(side="left", expand=False)

    resim_index_sağ = Label(sol_ekran_alt, text=str(len(resim_listesi)), width=5, height=2, name="resim_index_sağ", font=sağ_sol_FONT)
    resim_index_sağ.pack(side="left", expand=False)

    resim_sağ_geç = Button(sol_ekran_alt, text=">>", width=10, height=2, font=sağ_sol_FONT, name="resim_sağ_geç")
    resim_sağ_geç.configure(command=lambda:resim_geç("sağ"), background="#c8c8c8")
    resim_sağ_geç.pack(side="left", expand=False)

    git_butonu.configure(command=lambda : resim_geç(taraf="git"), background="#c8c8c8", font=küçük_buton_FONT)

    tag_varmı()

#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩ SAĞ + ÜST ▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩

    global etiket_konu_text
    etiket_konu_text = Text(sağ_ekran_üst, width=15, height=1, background="#c8c8c8", font=font.Font(size=20,weight="bold"), name="etiket_konu_text")
    etiket_konu_text.pack(fill="y", side="left", anchor="w")

    etiket_konu_buton = Button(sağ_ekran_üst, width=10, text="ETİKET EKLE", background="#c8c8c8", command= lambda widget = sağ_ekran_orta_ana_FRAME : etiket_konu(widget) , name="etiket_konu_buton", font=küçük_buton_FONT)
    etiket_konu_buton.pack(fill="y", side="left")

    etiket_listesi_boş_label = Label(sağ_ekran_üst, width=5, name="etiket_listesi_boş_label")
    etiket_listesi_boş_label.pack(fill="y", expand=False, side="left")

    global option_list_variable, etiket_listesi_option
    option_list_variable = StringVar(ana_ekran)
    option_list_variable.set(etiket_listesi[0])
    etiket_listesi_option = OptionMenu(sağ_ekran_üst, option_list_variable, *etiket_listesi)
    etiket_listesi_option.pack(fill="y", expand=False, side="right")

    etiket_listesi_buton = Button(sağ_ekran_üst, width=10, text="İTHAL ET", background="#c8c8c8", command=etiket_yükle, name="etiket_listesi_buton", font=küçük_buton_FONT)
    etiket_listesi_buton.pack(fill="y", expand=False, side="left", padx=2)
    
    etiket_listesi_kaydet_buton = Button(sağ_ekran_üst, width=10, text="KAYDET", background="#c8c8c8", command=etiket_kaydet, name="etiket_listesi_kaydet_buton", font=küçük_buton_FONT)
    etiket_listesi_kaydet_buton.pack(fill="y", expand=False, side="left", padx=2)

    sıfırla = Button(sağ_ekran_üst, width=10, height=2, text="SIFIRLA", background="#c8c8c8", command=herşeyi_sıfırla, name="sıfırla", font=küçük_buton_FONT)
    sıfırla.pack(fill="y", side="left", padx=2)

#▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩ SAĞ + ALT ▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩

    etiket_ekle = Button(sağ_ekran_alt, text="ETİKET EKLE", font=sağ_sol_FONT, command=etiketi_resme_ekle, background="#c8c8c8")
    etiket_ekle.pack(expand=True, fill="both")

    ana_ekran.mainloop()

ekran()
