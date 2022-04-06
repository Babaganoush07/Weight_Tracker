#-*-coding:utf8;-*-
#qpy:console

import pickle, datetime, re, os
from colorama import Fore, Style, init
from colorama import init
init(autoreset=True)

class c:
    r = Fore.RED
    g = Fore.GREEN
    y = Fore.YELLOW
    b = Fore.BLUE
    m = Fore.MAGENTA
    c = Fore.CYAN
    w = Fore.WHITE

def write_pickle(filename, data):
    outfile = open(filename,'wb')
    pickle.dump(data, outfile)
    outfile.close()
    
def read_pickle(filename):
    try:
        infile = open(filename,'rb')
        weights_lst = pickle.load(infile)
        infile.close()
    except:
        weights_lst = []
    return weights_lst
    
def add_date():
    while True:
        date_regex = re.compile(r'^\d{4}\-\d{2}\-\d{2}$')
        today = str(datetime.date.today())
        date = input('Default Date: '  + today + '\nOr enter new Date: ')
        date = date or today
        if date_regex.search(date):
            break
        else:
            print(c.r + '\nDate format is yyyy-mm-dd\n')
            continue
    return date

def add_weight():
    while True:
        weight_reg = re.compile(r'^\d+\.\d+$')
        my_weight = input("Today's weight: ")
        if weight_reg.search(my_weight):
            break
        else:
            print(c.r + '\nWeight format is ##.##\n')
            continue
    return my_weight

def add_new():
    weights_lst = read_pickle('weights')
    date = add_date()
    my_weight = add_weight()
    
    new_entry = (date, my_weight)
    weights_lst.append(new_entry)

    write_pickle('weights', weights_lst)
    print(c.g + '\nSaved\n')
    print_data()

def print_data():
    clear_console()
    weights_lst = read_pickle('weights')
    try:
        starting_weight = weights_lst[0][1]
        current_weight = weights_lst[-1][1]
    except:
        starting_weight = 0
        current_weight = 0
        
    total = 0   
    try:
        for weight in weights_lst:
            total += float(weight[1])       
        average = round((total / len(weights_lst)),2)
    except:
        average = 0

    try:
        previous_weight = float(weights_lst[0][1])
        current_weight = float(weights_lst[-1][1])
        change_weight = round(current_weight - previous_weight,2)
        if change_weight > 0:
            change_weight = Fore.RED + '+' + str(change_weight)
        else:
            change_weight = Fore.GREEN + str(change_weight)
    except:
        previous_weight = 0
        current_weight = 0
        change_weight = 0
    
    print(c.c + 'Starting Weight:  ' + str(starting_weight))
    print(c.c + 'Current Weight:   ' + str(current_weight))
    print(c.c + 'Change in Weight: ' + str(change_weight))
    print(c.c + 'Average Weight:   ' + str(average))

def view_all():
    clear_console()
    weights_lst = read_pickle('weights')
    weight_only = []
    for weight in weights_lst:
        weight_only.append(float(weight[1]))
    maximum_weight = max(weight_only)
    minimum_weight = min(weight_only)
    print(' +------------+---------+')
    print(' |    DATE    |  WEIGHT |')
    print(' +------------+---------+')
    previous = float(weights_lst[0][1])
    for item in weights_lst:
        if float(item[1]) == previous:
            change = c.c + '='+Fore.WHITE
        elif float(item[1]) >= previous:
            change = c.r + '↑'+Fore.WHITE
        elif float(item[1]) <= previous:
            change = c.g + '↓' +Fore.WHITE
        previous = float(item[1])
        
        if float(item[1]) == float(maximum_weight):
            print(' | '+ item[0] +' | '+c.r+ item[1] +' '+change+' |')       
        elif float(item[1]) == float(minimum_weight):
            print(' | '+ item[0] +' | '+c.g+ item[1] +' '+change+' |')
        else:
            print(' | '+ item[0] +' | '+ item[1] +' '+change+' |')
    
    print(' +------------+---------+')
 
def select_record():
    clear_console()
    print('SELECT A RECORD')
    weights_lst = read_pickle('weights')
    row_id = 0
    for item in weights_lst:
        row_id += 1
        print(row_id,item[0],item[1])
    print('Select a record or X to exit.')
    
    while True:
        selected_record = input('Enter item number: ')
        if selected_record.lower() == 'x':
            home_menu()
        try:
            selected_record = int(selected_record) -1
            if selected_record in range(len(weights_lst)):
                break
            else:
                print('Record not found.')
        except ValueError:
            print('Enter a Number.')
    clear_console()
    print('\nYour selection:')
    print(selected_record+1,weights_lst[selected_record][0],weights_lst[selected_record][1])                
    while True:
        print(
        	c.c + '''
+==EDIT/DELETE MENU==+
|'''+c.w+''' 1. Edit Selection   '''+c.c+'''|
|'''+c.w+''' 2. Delete Selection '''+c.c+'''|
|'''+c.w+''' 3. Change Selection '''+c.c+'''|
|'''+c.w+''' 4. Cancel           '''+c.c+'''|
+=====================+''')
        action = input('Enter Selection: ')
        if action == '':
            continue
        elif action.lower().startswith('edit') or action == '1':
            edit_record(selected_record)
            break
        elif action.lower().startswith('delete')or action == '2':
            delete_record(selected_record)
            break
        elif action.lower().startswith('change')or action == '3':
            select_record()
        elif action.lower().startswith('cancel') or action == '4':
            home_menu()
        else:
            print(Fore.RED + '\nSelection Not Found.')

def delete_record(selected_record):
    clear_console()
    print('DELETE RECORD\n')
    weights_lst = read_pickle('weights')
    print(selected_record+1,weights_lst[selected_record][0],weights_lst[selected_record][1])
    print('\nThis is a permanent action.')
    while True:
        confirm = input('Do you want to continue? (Y/N): ')
        if confirm.lower()=='n':
            break
        elif confirm.lower()=='y':
            del weights_lst[selected_record]
            write_pickle('weights', weights_lst)
            clear_console()
            print('Deleted')
            break
        else:
            print(c.r + '\nSelection Not Found.')

def edit_record(selected_record):
    clear_console()
    print('EDIT RECORD\n')
    weights_lst = read_pickle('weights')
    print(selected_record+1,weights_lst[selected_record][0],weights_lst[selected_record][1])
    while True:
        print(
        	c.c + '''
+==EDIT MENU=====+
|'''+c.w+''' 1. Edit Date   '''+c.c+'''|
|'''+c.w+''' 2. Edit Weight '''+c.c+'''|
|'''+c.w+''' 3. Cancel.     '''+c.c+'''|
+================+''')
        action = input('Enter Selection: ')
        if action == '':
            continue
        elif action.lower().endswith('date') or action == '1':
            date = add_date()
            edit_entry = (date, weights_lst[selected_record][1])
            weights_lst[selected_record] = edit_entry
            write_pickle('weights', weights_lst)
            clear_console()
            print('Edit saved')
            break
        elif action.lower().endswith('weight') or action == '2':
            my_weight = add_weight()
            edit_entry = (weights_lst[selected_record][0], my_weight)
            weights_lst[selected_record] = edit_entry
            write_pickle('weights', weights_lst)
            clear_console()
            print('Edit saved')
            break
        elif action.lower().startswith('cancel')or action == '3':
            home_menu()
        else:
            print(Fore.RED + '\nSelection Not Found.')

def clear_console():
    os.system('clear')

def home_menu():
    clear_console()                     
    while True:
        print(
        	c.c + '''
+==HOME MENU=====+
|'''+c.w+''' 1. Add Weight  '''+c.c+'''|
|'''+c.w+''' 2. Get Totals  '''+c.c+'''|
|'''+c.w+''' 3. View All    '''+c.c+'''|
|'''+c.w+''' 4. Edit/Delete '''+c.c+'''|
|'''+c.w+''' 5. Exit        '''+c.c+'''|
+================+''')
        action = input('Enter Selection: ')
        if action == '':
            continue
        elif action.lower().startswith('add') or action == '1':
            clear_console()
            add_new()
        elif action.lower().startswith('get')or action == '2':
            print_data()
        elif action.lower().startswith('view')or action == '3':
            view_all()
        elif action.lower().startswith('edit') or action.lower().startswith('delete') or action == '4':
            select_record()
        elif action.lower().startswith('exit')or action == '5':
            exit()
        else:
            clear_console()
            print(c.r + '\nSelection Not Found.')

if __name__ =='__main__':
    home_menu()