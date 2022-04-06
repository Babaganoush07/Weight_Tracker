from tkinter import *
from tkinter import messagebox
import datetime, re, pickle

def read_pickle(filename):
    try:
        infile = open(filename,'rb')
        weights_lst = pickle.load(infile)
        infile.close()
    except:
        weights_lst = []
    return weights_lst

def write_pickle(filename, data):
    outfile = open(filename,'wb')
    pickle.dump(data, outfile)
    outfile.close()

def refresh_all_data():
    date.delete(0, END)
    weight.delete(0, END)
    date.insert(0, str(datetime.date.today()))
    cancel_button.pack_forget()
    delete_button.pack_forget()
    save_button.config(text='SAVE')
    weights_lst = read_pickle('weights')
    try:
        current = weights_lst[-1][1]
    except IndexError:
         current = str(0.00) 
    try:
        last_weight = weights_lst[-2][1]
    except IndexError:
        last_weight = 0.00
    try:
        change = round(float(weights_lst[-1][1]) - float(weights_lst[-2][1]),2)
        if change > 0.00:
            change = ' (+'+str(change)+')'
        else:
            change = ' ('+str(change)+')'
    except IndexError:
        change = ''
        
    current_weight.set('Current Weight\n' + current + change)

    # POPULATE VIEW ALL
    weights_lb.delete(0, END)
    try:
        previous = float(weights_lst[0][1])
    except IndexError:
        previous = 0.00
    for item in weights_lst:
        if float(item[1]) == previous:
            weights_lb.insert(END,' '+str(item[0])+' '+str(item[1])+'  =')
        elif float(item[1]) >= previous:
            weights_lb.insert(END,' '+str(item[0])+' '+str(item[1])+'  ↑')
        elif float(item[1]) <= previous:
            weights_lb.insert(END,' '+str(item[0])+' '+str(item[1])+'  ↓')
        previous = float(item[1])

    #POPULATE MONTHLY DATA
    month_txt.configure(state=NORMAL)
    month_txt.delete(0.0, END)
    averages = {}
    for item in weights_lst:
        if item[0][5:7] not in averages:
            averages.update({item[0][5:7]:{'max':0.0, 'min':0.0, 'avg':[]}})
    
    for item in weights_lst:
        averages[item[0][5:7]]['avg'].append(float(item[1]))
        
    for months in averages:
        averages[months]['max'] = max(averages[months]['avg'])
        averages[months]['min'] = min(averages[months]['avg'])
        averages[months]['avg'] = round(sum(averages[months]['avg']) / len(averages[months]['avg']),1)  

    for month in averages:
        month_txt.insert(END,' '+ datetime.datetime.strptime(month,'%m').strftime('%b').upper() +' '+ str(averages[month]['max'])+' '+ str(averages[month]['min'])+' '+ str(averages[month]['avg'])+'\n')
    month_txt.configure(state=DISABLED)
    return weights_lst

def list_box_selection(event):
    date.delete(0, END)
    weight.delete(0, END)
    index = weights_lb.curselection()[0]
    date.insert(0, weights_lst[index][0])
    weight.insert(0, weights_lst[index][1])
    delete_button.pack(side=LEFT,padx=0, pady=5)
    cancel_button.pack(side=LEFT,padx=5, pady=5)
    save_button.config(text='SAVE')

def save_record():
    check_counter=0
    date_regex = re.compile(r'^\d{4}\-\d{2}\-\d{2}$')
    weight_regex = re.compile(r'^\d+\.\d+$')
    if weight_regex.search(weight.get()):
        check_counter += 1
    else:
        warn = 'Weight Error'

    if date_regex.search(date.get()):
        check_counter += 1
    else:
        warn = 'Date Error'

    if check_counter == 2:
        record = (date.get(), weight.get())
        try:
            # EDIT A RECORD
            index = weights_lb.curselection()[0]
            weights_lst[index]= record
        except IndexError:
            # ADD A RECORD
            weights_lst.append(record)
        write_pickle('weights', weights_lst)
        refresh_all_data()
        messagebox.showinfo('Saved', 'SAVED:\n'+str(record[0])+'\n'+str(record[1]))
    else:
        messagebox.showerror('Error', warn)

def cancel_edit():
    refresh_all_data()
      
def delete_record():
    index = weights_lb.curselection()[0]
    response = messagebox.askyesno('Delete Entry', weights_lst[index][0]+'\n'+weights_lst[index][1]+'\nDELETE?')
    if response ==1:
        del weights_lst[index]
        write_pickle('weights', weights_lst)
        refresh_all_data()

main = Tk()
main.title('My Weight')
main.config(bg='#119DA4')#0485F5

title_frame = Frame(main, bg='#040404')
title_frame.pack(fill=X, padx=10, pady=(10,5))
title = Label(title_frame, text='WEIGHT TRACKER', font=('courier',14,'bold'), bg='#13505B', fg='white')#00458B
title.pack(fill=X, padx=5, pady=(5, 0))
current_weight = StringVar()
current = Label(title_frame, textvariable=current_weight, font=('courier',10), bg='#13505B', fg='white')
current.pack(fill=X, padx=5, pady=(0, 5))

entry_frame = Frame(main, bg='#040404')
entry_frame.pack(padx=10)
date_label = Label(entry_frame, text='DATE', font=('courier', 10), anchor=W, bg='#13505B', fg='white')
date_label.pack(fill=X, padx=5, pady=(5, 0))
date = Entry(entry_frame,justify=CENTER, font=('courier',12))
date.pack(padx=5, pady=(0, 5))
weight_label = Label(entry_frame, text='WEIGHT', font=('courier',10), anchor=W, bg='#13505B', fg='white')
weight_label.pack(fill=X, padx=5, pady=(0,0))
weight = Entry(entry_frame,justify=CENTER, font=('courier',12))
weight.pack(padx=5, pady=(0,5))

button_frame = Frame(main, bg='#040404')
button_frame.pack(padx=5, pady=(5, 0))
save_button = Button(button_frame, text='SAVE', font=('courier',9), bg='#0C7489', fg='white',activebackground='#13505B', command=save_record)
save_button.pack(side=LEFT,padx=5, pady=5)
cancel_button = Button(button_frame, text='CANCEL', font=('courier',9), bg='#0C7489', fg='white', activebackground='#13505B', command=cancel_edit)
delete_button = Button(button_frame, text='DELETE', font=('courier',9), bg='#0C7489', fg='white', activebackground='#13505B',command=delete_record)

view_all = Frame(main, bg='#040404')
view_all.pack(padx=5, pady=5)
view_label = Label(view_all, text='VIEW ALL', font=('courier', 10), anchor=W, bg='#13505B', fg='white')
view_label.pack(fill=X, padx=5, pady=(5, 0))
weights_scroll = Scrollbar(view_all)
weights_scroll.pack(side=RIGHT, fill=Y, padx=(0,5), pady=(0,5))
weights_lb = Listbox(view_all, yscrollcommand=weights_scroll.set, selectmode=SINGLE,font=('courier',10), bg='#D7D9CE', selectbackground='#13505B',  width=23)
weights_lb.pack(side=LEFT, padx=(5,0), pady=(0,5))
weights_lb.bind('<<ListboxSelect>>',list_box_selection)
weights_scroll.config(command=weights_lb.yview)

month_avg= Frame(main, bg='#040404')
month_avg.pack(padx=5, pady=(5, 10))
month_label = Label(month_avg, text='MONTH DATA', font=('courier', 10), anchor=W, bg='#13505B', fg='white')
month_label.pack(fill=X, padx=5, pady=(5, 1))
header_label = Label(month_avg, text='        MAX     MIN    AVG', font=('courier', 8), anchor=W, bg='#13505B', fg='white') 
header_label.pack(fill=X, padx=5)
month_scroll = Scrollbar(month_avg)
month_scroll.pack(side=RIGHT, fill=Y, padx=(0,5), pady=(0,5))
month_txt = Text(month_avg, yscrollcommand=month_scroll.set, font=('courier',10),bg='#D7D9CE', selectbackground='#D7D9CE',  width=23)
month_txt.pack(side=LEFT, padx=(5,0), pady=(0,5))
month_scroll.config(command=month_txt.yview)

weights_lst = refresh_all_data()
main.mainloop()
