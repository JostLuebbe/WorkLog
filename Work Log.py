from datetime import datetime as dt
import enum as em
import tkinter as tk
from tkinter import ttk
import pickle as pk
import logging as lg


class Status(em.Enum):
    Incomplete = 0
    Complete = 1


class Priority(em.Enum):
    Low = 0
    Medium = 1
    High = 2


class Task(object):
    name = ''
    status = ''
    start_date = ''
    task_description = ''
    updates = {}
    priority = ''

    def __init__(self):
        self.name = ''
        self.status = ''
        self.start_date = dt.strftime(dt.now(),'%m/%d/%y %I:%M')
        self.task_description = ''
        self.updates = {dt.now(), 'task start date'}
        self.priority = ''


class TaskWindow(tk.Toplevel):
    task_window = ''
    task = Task()
    name_field_var = ''
    status_field_var = ''
    priority_field_var = ''
    updates_field_var = ''
    td_field_var = ''

    def __init__(self, root_window, task_window, task):
        self.task = task
        self.task_window = task_window
        task_window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.name_field_var = tk.StringVar(root_window)
        self.status_field_var = tk.StringVar(root_window)
        self.priority_field_var = tk.StringVar(root_window)
        self.td_field_var = tk.StringVar(root_window)
        self.updates_field_var = tk.StringVar(root_window)
        self.create_task_window(task_window)

    def create_task_window(self, task_window):
        self.task_window.title('Task Creator')

        name_label = tk.Label(
            self.task_window,
            text='Name:'
        )
        name_label.grid(row=0, column=0)

        name_field = tk.Entry(
            self.task_window,
            textvariable=self.name_field_var
        )
        name_field.grid(row=0, column=1)

        status_label = tk.Label(
            self.task_window,
            text='Status:'
        )
        status_label.grid(row=1, column=0)

        status_menu = tk.OptionMenu(self.task_window, self.status_field_var, Status.Incomplete.name, Status.Complete.name)
        status_menu.grid(row=1, column=1)

        priority_label = tk.Label(
            self.task_window,
            text='Priority:'
        )
        priority_label.grid(row=2, column=0)

        priority_menu = tk.OptionMenu(
            self.task_window,
            self.priority_field_var,
            Priority.Low.name,
            Priority.Medium.name,
            Priority.High.name
        )
        priority_menu.grid(row=2, column=1)

        desc_label = tk.Label(
            self.task_window,
            text='Description:',
        )
        desc_label.grid(row=3, column=0)

        desc_field = tk.Entry(
            self.task_window,
            textvariable=self.td_field_var,
        )
        desc_field.grid(row=3, column=1)

        updates_tree = ttk.Treeview(self.task_window)
        updates_tree.grid(row=4, column=0, columnspan=2)

        self.updates_field = tk.Text(self.task_window)
        self.updates_field.grid(row=5, column=0, columnspan=2)
        self.updates_field.bind('<Return>', self.add_text)

        close_button = tk.Button(
            self.task_window,
            text='Add Task',
            command=lambda: self.set_task_object(task_window),
        )
        close_button.grid(row=6, column=0, columnspan=2)

    def set_task_object(self, task_window):
        self.task.task_description = self.td_field_var.get()
        self.task.priority = self.priority_field_var.get()
        self.task.name = self.name_field_var.get()
        self.task.status = self.status_field_var.get()
        task_window.destroy()

    def on_close(self):
        self.task.name = 'None'
        self.task_window.destroy()

    def add_text(self):
        self.updates_field_var = self.updates_field.get(1.0, tk.END)


class WorkLog(tk.Frame):
    taskList = []
    tree = ''

    def __init__(self, master=None):
        super().__init__(master)
        root.title('Work Log')
        root.iconbitmap(r'C:\PyCharm Projects\Work Projects\Task Log\resources\icon.ico')
        root.minsize(300,600)
        root.geometry('1000x800')
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(
            self,
            columns=('Start Date', 'Status', 'Priority', 'Description'),
            height=20,
            selectmode='browse'
        )
        self.tree.heading('#0', text='Task Name', anchor='w')
        self.tree.column('#0', anchor='w', minwidth=120, stretch=True)
        self.tree.heading('#1', text='Start Date')
        self.tree.column('#1', anchor='c', minwidth=90, width=90, stretch=False)
        self.tree.heading('#2', text='Status')
        self.tree.column('#2', anchor='c', minwidth=75, width=75, stretch=False)
        self.tree.heading('#3', text='Priority')
        self.tree.column('#3', anchor='c', minwidth=60, width=60, stretch=False)
        self.tree.heading('#4', text='Description')
        self.tree.column('#4', anchor='w', minwidth=500, stretch=True)

        ysb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        #xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(
            yscroll=ysb.set,
            #xscroll=xsb.set,
        )
        self.tree.grid(row=0, column=0, sticky='nsew')
        ysb.grid(row=0, column=1, sticky='nse')
        #xsb.grid(row=1, column=0, sticky='sew')

        self.populate_list()

        button = tk.Button(
            self,
            height=2,
            width=5,
            text='Add Task',
            command=self.new_task,
            activebackground='royalblue',
            activeforeground='red',
            bg='powderblue',
            fg='black'
        )
        button.bind('<Enter>', lambda event, h=button: h.configure(bg='royalblue', fg='darkblue'))
        button.bind('<Leave>', lambda event, h=button: h.configure(bg='powderblue', fg='black'))
        button.grid(row=2, column=0, columnspan=2, sticky='nsew')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(sticky='nsew')

    def new_task(self):
        task = Task()
        task_window = tk.Toplevel()
        TaskWindow(self, task_window, task)
        root.wait_window(task_window)
        if task.name is not 'None':
            self.taskList.append(task)
            self.tree.insert(
                '',
                'end',
                text=task.name,
                values=(task.start_date, task.status, task.priority, task.task_description)
            )

    def populate_list(self):
        with open(r'C:\PyCharm Projects\Work Projects\Task Log\resources\tasks.pkl', 'rb') as f:
            self.taskList = pk.load(f)

        for task in self.taskList:
            self.tree.insert(
                '',
                'end',
                text=task.name,
                values=(task.start_date, task.status, task.priority, task.task_description)
            )

    def on_close(self):
        with open(r'C:\PyCharm Projects\Work Projects\Task Log\resources\tasks.pkl', 'wb') as f:
            pk.dump(self.taskList, f)
        root.destroy()


root = tk.Tk()
app = WorkLog(master=root)
app.mainloop()