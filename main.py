import customtkinter as ctk
from modules.create_file_top_level import create_config
from modules.app_opener import run_file
import os 


# destroys and wipes task
def destroy_single(name): #removes task
    instances[name].destroy()
    tasks.remove(task_instance_pairing[name])
    # removes config file
    if "." in name:
        os.remove(f'configs/{name}')
    else:
        os.remove(f'configs/{name}.txt')
        

# destroys an instance
def destroy_instance(name): #keeps task
    instances[name].destroy()


# places destroy button in individual task frames
def place_destroy_button(name):
    destroy_button = ctk.CTkButton(master=instances[name], height=30, width=30, text="x", font=("roboto", 20), fg_color=("#ffffff", "#424242"), hover_color='red', command=lambda:destroy_single(name))
    destroy_button.pack_configure(side="right", padx=1, pady=1)


# pass in 'config_name' because name is used within create_config function
def Create_file(Config_name):
    create_config(Config_name, Root)
    
    
def run_config(name):
    run_file(file=name)
    

# places tasks from task list
def task_packer():
    # formats name, pairs instance name with task name, assigns frame to intances[name]
    # sets that frame to not propogate so it dosnt shrink or expand, packs it, packs the checkbox and desctruction button
    for task in tasks:
        name = f'{task.replace(" ", "_")}'
        
        # pairs name of task to name of instance in pairing dict
        task_instance_pairing[name] = task
        
        # NOTE remeber instances[name] is always equal to the last task in the list]
        instances[name] = ctk.CTkFrame(master=main_frame, height=100, width=110, fg_color=("#ffffff", "#363636"))
        instances[name].pack_propagate(False)
        # NOTE pack propegate stops children from controlling parent frame
        instances[name].pack_configure(side='right', padx=1)
        
        # creates big button which runs a config file
        run_config_button = ctk.CTkButton(master=instances[name],width=80, height=80, command=lambda: run_config(name), text=name)
        run_config_button.pack(side="left")
        # places delete button
        place_destroy_button(name)


# destroys then repacks everything with the updated task list
def pack_from_entry():
    # destroy everything for repack
    destroy_instances()
    # repack
    task_packer()


# destroys instances and wipes instances for repacking
def destroy_instances():
    global instances
    for instance in instances:
        destroy_instance(instance)
    # ensures instances is clear
    instances = {}


# destroys everything
def destroy_all():
    global instances
    for instance in instances:
        destroy_single(instance)


# add tasks to task list and calls repack function
def add_task_to_tasks(task_name):
    def check_for_blanks(task_name):
        return all(char == ' ' for char in task_name)
    if  check_for_blanks(task_name):
        print("string is emty")
    elif task_name in tasks: 
        print("task already in task")
    else: #should only pass this check if it isnt already in tasks and isnt blank.
        tasks.append(task_name)
        Create_file(Config_name=task_name)
        pack_from_entry()


# creates and packs container to add new tasks
def new_task_container():
    # task entry frame
    new_task_frame = ctk.CTkFrame(master=Root, height=30, width=250, fg_color=("#ffffff", "#363636"))
    new_task_frame.pack_propagate(False)
    new_task_frame.pack_configure(side="top",pady=5)
    
    # task entry
    task_input = ctk.CTkEntry(master=new_task_frame, placeholder_text="Add configuration", border_color='#363636')
    task_input.pack_configure(side='left', pady=1, fill='both', expand=True)

    # submit button
    submit_button = ctk.CTkButton(master=new_task_frame, height=30, width=30, text="▲", font=("roboto", 20), command=lambda: add_task_to_tasks(task_input.get())) #send to the list packer
    submit_button.pack_configure(side='right', padx=1, pady= 1)




# root setup
Root = ctk.CTk()

# general config
ctk.set_default_color_theme('dark-blue')
ctk.set_appearance_mode('dark')
Root.geometry("700x300")
Root.title("workstation modes")

tasks = []
for file in os.listdir("configs"):
    tasks.append(file)

# instances dict
instances = {}

# dict with pairs of task names as keys and corresponding instance names
task_instance_pairing = {} 

# main frame
title = ctk.CTkLabel(master=Root, text="workstation modes", font=("roboto", 20))
title.pack_configure(side="top", pady= 10)
title.tkraise()
main_frame =  ctk.CTkScrollableFrame(master=Root, width=300, height = 110, corner_radius=0, fg_color="transparent", orientation = 'horizontal')
main_frame.pack(fill='x')
# main_frame.pack_propagate(True)

task_packer()

# button to destroy all tasks
new_task_container()
delete_all_button = ctk.CTkButton(master=Root, text='Delete All configs', font=("roboto", 20), fg_color=("#ffffff", "#424242"), hover_color='red',command=lambda:destroy_all())
delete_all_button.pack_configure(side='top', pady=5)






Root.mainloop()
"""
# TODO fix edge case of user putting in a task with an undescore, with the same name as one with a space
#    EX: task_3, task 3
#    this tries to force the instances dict, to create two identical keys, which is not allowed in python
 
# TODO add error reporting to app, so the user knows what is going wrong

"""
