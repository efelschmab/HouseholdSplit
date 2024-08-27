from modules import *
import tkinter
import customtkinter as ctk

window = ctk.CTk(fg_color="#181818")
window.geometry("500x900")
window.title("HouseHold Split")
window.resizable(width=False, height=False)


"""Household name"""
house_hold_name_frame = ctk.CTkFrame(master=window, width=480, fg_color=classes.background, height=40, corner_radius=0)
house_hold_name_frame.grid(columnspan=2, padx=10, pady=10, column=0, row=0)

household_obj = classes.HouseHold()
house_hold_widget = household_obj.hh_name_entry_widget(master_frame=house_hold_name_frame)

divider_line_obj = classes.HouseHold()
divider_line_widget = household_obj.divider_line(master_frame=window, row=1)

"""Household members"""
household_member_1_frame = ctk.CTkFrame(master=window, width=200, fg_color="red", height=60)
household_member_1_frame.grid(columnspan=1, padx=10, pady=10, column=0, row=2)

memb_obj_1 = classes.HouseHoldMember()
memb_1_widget = memb_obj_1.memb_name_entry_widget(master_frame=household_member_1_frame)

household_member_2_frame = ctk.CTkFrame(master=window, width=200, fg_color="green", height=60)
household_member_2_frame.grid(columnspan=1, padx=10, pady=10, column=1, row=2)

memb_obj_2 = classes.HouseHoldMember()
memb_2_widget = memb_obj_2.memb_name_entry_widget(master_frame=household_member_2_frame)

divider_line_obj = classes.HouseHold()
divider_line_widget = household_obj.divider_line(master_frame=window, row=3)

""""Combined household net income"""
household_net_GUI_frame = ctk.CTkFrame(master=window, width=200, fg_color=classes.background, height=40, corner_radius=0)
household_net_GUI_frame.grid(columnspan=2, padx=35, pady=10, column=0, row=4, sticky="ew")

household_net_obj = classes.HouseHold()
household_net_widget = household_obj.hh_net_widget(master_frame=household_net_GUI_frame)

window.mainloop()