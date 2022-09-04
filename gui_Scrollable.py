from math import sqrt
from tkinter import *
from tkinter import ttk
from att_filesystem import att_filesystem
from get_ips import get_ips
from pingMachines import pingMachines
from machine_cls import machine
from WoL import wol
from shut_clients import shut_clients
from get_macs import get_macs

def handle_resize(event):
    canvas = event.widget
    canvas_frame = canvas.nametowidget(canvas.itemcget("canvas_frame", "window"))
    min_width = canvas_frame.winfo_reqwidth()
    min_height = canvas_frame.winfo_reqheight()
    if min_width < event.width:
        canvas.itemconfigure("canvas_frame", width=event.width)
    if min_height < event.height:
        canvas.itemconfigure("canvas_frame", height=event.height)

    canvas.configure(scrollregion=canvas.bbox("all"))

def autoping(lst_machs):
    for machine in lst_machs:
        ip = machine.ip.get()
        if ip != "não disponível":
            status = pingMachines([ip])
            if status[ip]:
                machine.canvas.itemconfigure("circle",fill="green")
                machine.set_status(1)
            else:
                machine.canvas.itemconfigure("circle",fill="red")
                machine.set_status(0)
        else:
            machine.canvas.itemconfigure("circle",fill="black")
    
    for i,mach in enumerate(lst_machs):
        ip = get_ips([mach.mac])
        mach.set_ip(ip[mach.mac])


    root.after(3000, lambda : autoping(lst_machs))

def gui():
    global root
    root = Tk()
    root.title('Gerenciador da Plataforma')
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)
        
    win_width= 840
    win_height=600
    scr_width= root.winfo_screenwidth()
    scr_height= root.winfo_screenheight()
    center_x = int(scr_width/2 - win_width / 2)
    center_y = int(scr_height/2 - win_height / 2)
    root.geometry(f"{win_width}x{win_height}+{center_x}+{center_y}")

    def shut_down(ips):
        frm_pw = Toplevel(root)
        win_width= 200
        win_height=150
        frm_pw.title("Senha")
        center_x = int(scr_width/2 - win_width / 2)
        center_y = int(scr_height/2 - win_height / 2)
        frm_pw.geometry(f"{win_width}x{win_height}+{center_x}+{center_y}")
        frm_pw.grid_rowconfigure(0, weight=1)
        frm_pw.grid_columnconfigure(0, weight=1)
        frm_pw.grid_rowconfigure(1, weight=1)
        frm_pw.grid_columnconfigure(1, weight=1)
        frm_pw.grid_rowconfigure(2, weight=1)
        pwd = StringVar()
        ttk.Label(frm_pw,text="Senha da máquina:").grid(row=0,column=0,columnspan=2)
        senha = ttk.Entry(frm_pw,show="*", textvariable=pwd)
        senha.focus_set()
        senha.grid(row=1,column=0,columnspan=2)
        ttk.Button(frm_pw, text="enviar",command=lambda passw=pwd:[frm_pw.destroy(),shut_clients(ips,passw.get())]).grid(row=2,column=0)
        # ttk.Button(frm_pw, text="enviar",command=lambda:[frm_pw.destroy(),print(ips,senha)]).grid(row=2,column=0)
        # senha.bind("<Return>",lambda passw=pwd:[frm_pw.destroy(),shut_clients(ips,passw.get())])
        ttk.Button(frm_pw, text="cancelar",command=lambda:frm_pw.destroy()).grid(row=2,column=1)
        
        

    # Canvas para poder usar scrollbar
    canvas = Canvas(root,width=win_width,height=win_height)

    scroll_x = ttk.Scrollbar(root, orient="horizontal", command=canvas.xview)
    scroll_x.grid(row=1, column=0, sticky="ew")

    scroll_y = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_y.grid(row=0, column=1, sticky="ns")

    # Frame é o item do canvas acima, que será usado para comportar todos os outros frames do programa
    frame = ttk.Frame(canvas)
    frame.rowconfigure(0,weight=1)
    frame.columnconfigure(0,weight=1)

    # Frame para abrigar botões gerais e o frame para as máquinas
    frm0 = ttk.Labelframe(frame, padding="1 1 1 1")
    frm0.pack()
    frm0.grid(column=0, row=0)

    # Frame para abrigar os frames de cada máquina
    frm1 = ttk.Labelframe(frm0, padding="1 1 1 1")

    frm1.grid(column=0, row=1,pady=10,columnspan=4)

    # Make the window sticky for every case
    frm0.grid_rowconfigure(0, weight=1)
    frm0.grid_columnconfigure(0, weight=1)
    frm0.grid_rowconfigure(1, weight=1)
    frm0.grid_columnconfigure(1, weight=1)
    frm0.grid_rowconfigure(2, weight=1)
    frm0.grid_columnconfigure(2, weight=1)
    frm0.grid_rowconfigure(3, weight=1)
    frm0.grid_columnconfigure(3, weight=1)

    machines = [] # Dicionário para instanciar máquinas, sustituir por classe futuramente.
    lst_mac = get_macs() # lista dos macs para facilitar
    # loop para instanciar as máquinas na classe
    for i,mac in enumerate(lst_mac):
        ip = get_ips([mac])
        machines.append(machine(mac,StringVar(),StringVar(), ttk.Labelframe(frm1, text=f"Máquina {i}: ({mac[0:5]}:XX:XX:XX:XX)", padding="10 5 10 5"), Canvas))
        machines[i].set_ip(ip[mac])

    ## Botões gerais, não específicos para cada máquina ##
    ttk.Button(frm0, text="Ligar todas máquinas",command=lambda : wol(lst_mac)).grid(column=0, row=0, padx=10, pady=10)
    ttk.Button(frm0, text="Desligar todas máquinas",command=lambda : shut_down([machine.ip.get() for machine in machines])).grid(column=1, row=0, padx=10, pady=10)
    ttk.Button(frm0, text="Atualizar filesystem",command=lambda  : att_filesystem()).grid(column=2, row=0, padx=10, pady=10)
    ttk.Button(frm0, text="Atualizar configurações", command=lambda : root.destroy).grid(column=3, row=0, padx=10, pady=10)
    # ttk.Button(frm0, text="", command=root.destroy).grid(column=2, row=1, padx=10, pady=10)


    # Loop para criar frame para cada máquina (e seus widgets)
    for i,mach in enumerate(machines):
        
        i_column = i%3
        i_row = i//3 + 1
        # posicionamento relativo dos fremes, bem como definição do redimencionamento das linha e coluna deste frame
        mach.frame.grid(column=i_column, row=i_row, pady=10,padx=10)
        frm1.grid_rowconfigure(i_row, weight=1)
        frm1.grid_columnconfigure(i_column, weight=1)

        # status das máquinas começam com 0 (offline) até que seja atualizados pelo método a ser definido
        mach.set_status(0) 

        ttk.Label( mach.frame, text="IP : ").grid(column=0, row=0,padx=10, pady=10)
        ttk.Label( mach.frame, textvariable=mach.ip).grid(column=1, row=0,padx=10, pady=10, columnspan=2)
        
        # Frame para circulo de status das máquinas
        ttk.Label( mach.frame, text="Status : ").grid(column=0, row=1,padx=10, pady=10)
        mach.canvas = Canvas(mach.frame, name="status_canvas",width=25,height=25)
        mach.canvas.grid(column=1, row=1,padx=10, pady=10)
        mach.canvas.create_oval(2,2,23,23, fill="black", tags=("circle",), width=0)
        ttk.Button( mach.frame, text="Ligar", command=lambda m=machines[i].mac: wol([m])).grid(column=2, row=1,padx=10, pady=5)
        ttk.Button( mach.frame, text="Desligar", command=lambda ip=mach.ip.get(): shut_down([ip])).grid(column=2, row=2,padx=10, pady=5)

    canvas.create_window(0, 0, anchor='nw', window=frame, tags=("canvas_frame",))
    canvas.bind('<Configure>', handle_resize)
    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox('all'), 
                    yscrollcommand=scroll_y.set, 
                    xscrollcommand=scroll_x.set)

    canvas.grid(row=0, column=0,sticky="WESN")
    canvas.grid_rowconfigure(0, weight=1)
    canvas.grid_columnconfigure(0, weight=1)
    canvas.configure(scrollregion=canvas.bbox("all"))
    autoping(machines) 

    
gui()
root.mainloop()
