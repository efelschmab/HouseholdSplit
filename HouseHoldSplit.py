from modules import *
import tkinter
import customtkinter as ctk

window = ctk.CTk(fg_color="#181818")
window.geometry("500x900")
window.title("HouseHold Split")
window.resizable(width=False, height=False)


"""Household name"""
house_hold_name_frame = ctk.CTkFrame(master=window, width=40,
                                     fg_color=classes.background,
                                     height=40,
                                     corner_radius=0)
house_hold_name_frame.grid(columnspan=2,
                           padx=0,
                           pady=0,
                           column=0,
                           row=0)

household_obj = classes.HouseHold()
house_hold_widget = household_obj.hh_name_entry_widget(master_frame=house_hold_name_frame)

divider_line_obj = classes.HouseHold()
divider_line_horizontal_widget = household_obj.divider_line_horizontal(master_frame=window, row=1)

"""Household members"""
household_members_basic_frame = ctk.CTkFrame(master=window,
                                             fg_color=classes.background)
household_members_basic_frame.grid(columnspan=3)

household_member_1_frame = ctk.CTkFrame(master=household_members_basic_frame,
                                        width=150,
                                        fg_color=classes.background,
                                        height=60)
household_member_1_frame.grid(columnspan=1, padx=10, pady=10, column=0, row=2)

memb_obj_1 = classes.HouseHoldMember()
memb_1_widget = memb_obj_1.memb_name_entry_widget(master_frame=household_member_1_frame)

divider_line_vertical_widget = household_obj.divider_line_vertical(master_frame=household_members_basic_frame,
                                                                   column=1,
                                                                   row=2,
                                                                   height=50)

household_member_2_frame = ctk.CTkFrame(master=household_members_basic_frame,
                                        width=150,
                                        fg_color=classes.background,
                                        height=60)
household_member_2_frame.grid(columnspan=1,
                              padx=10,
                              pady=10,
                              column=2,
                              row=2)

memb_obj_2 = classes.HouseHoldMember()
memb_2_widget = memb_obj_2.memb_name_entry_widget(master_frame=household_member_2_frame)

divider_line_horizontal_widget = household_obj.divider_line_horizontal(master_frame=window, row=3)

""""Combined household net income"""
household_net_GUI_frame = ctk.CTkFrame(master=window,
                                       width=200,
                                       fg_color=classes.background,
                                       height=40,
                                       corner_radius=0)
household_net_GUI_frame.grid(columnspan=2,
                             padx=35,
                             pady=10,
                             column=0,
                             row=4,
                             sticky="ew")

household_net_obj = classes.HouseHold()
household_net_widget = household_obj.hh_net_widget(master_frame=household_net_GUI_frame)

divider_line_horizontal_widget = household_obj.divider_line_horizontal(master_frame=window, row=5)

""""Member% of hosehold net"""
percent_net_container = ctk.CTkFrame(master=window,
                                     width=430,
                                     corner_radius=0,
                                     fg_color=classes.background)
percent_net_container.grid(columnspan=3, padx=10, pady=10)

memb1_percent_widget = memb_obj_1.member_percent_of_net(master_frame=percent_net_container, column=0)

percent_label = ctk.CTkLabel(master=percent_net_container,
                             fg_color=classes.background,
                             corner_radius=0,
                             width=20,
                             text="% of household net")
percent_label.grid(row=0,
                   column=1,
                   padx=10,
                   sticky="n")

memb2_percent_widget = memb_obj_2.member_percent_of_net(master_frame=percent_net_container, column=2)

"""Expenses"""
expenses_base_frame = ctk.CTkFrame(master=window,
                                   fg_color=classes.background,
                                   corner_radius=0)
expenses_base_frame.grid(columnspan=3,
                         row=7)

member_1_expenses_frame = ctk.CTkFrame(master=expenses_base_frame,
                                       width=200,
                                       fg_color=classes.background,
                                       height=60,
                                       corner_radius=0)
member_1_expenses_frame.grid(columnspan=1,
                             pady=classes.member_widget_pady,
                             padx=classes.member_widget_padx,
                             column=0,
                             row=0,
                             sticky="n")

memb_1_expenses = memb_obj_1.expenses_widget(master_frame=member_1_expenses_frame)

# def spawn_expense():
#     memb_1_add_expenses_widget = memb_obj_1.add_expenses(master_frame=member_1_expenses_frame, expense_name=classes.HouseHoldMember.expense_entry_dict["expense_name"], expense_value=classes.HouseHoldMember.expense_entry_dict["expense_amount_formatted"])

divider_line_vertical_widget = household_obj.divider_line_vertical(master_frame=expenses_base_frame,
                                                                   column=1,
                                                                   row=0,
                                                                   height=400)

member_2_expenses_frame = ctk.CTkFrame(master=expenses_base_frame,
                                       width=200,
                                       fg_color=classes.background,
                                       height=60,
                                       corner_radius=0)
member_2_expenses_frame.grid(columnspan=1,
                             pady=classes.member_widget_pady,
                             padx=classes.member_widget_padx,
                             column=2,
                             row=0,
                             sticky="n")

memb_2_expenses = memb_obj_2.expenses_widget(master_frame=member_2_expenses_frame)
#memb_2_add_expenses_widget = memb_obj_2.add_expenses(master_frame=member_2_expenses_frame)

window.mainloop()