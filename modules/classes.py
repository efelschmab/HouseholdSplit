import customtkinter as ctk
import re
from PIL import Image, ImageTk

"""Some variables for general use"""
green = "#15ce27"
red = "#ff0000"
background = "#181818"
entry_background = "#141414"

member_widget_width = 180
member_widget_padx = 5
member_widget_pady = 5
entry_round_corners = 8

def activate_entry(widget):
    """Widgets only get activated if needed"""
    widget.configure(state="normal")

def limit_characters(entry, limit):
    value = entry.get()
    if len(value) > limit:
        entry.set(value[:limit])

def trace_add(string_var, char_limit):
    string_var.trace_add("write", lambda *args: limit_characters(string_var, char_limit))

def create_lambda(on_entry_confirm, keybind):
    return lambda event: on_entry_confirm(keybind)

def format_income_entry(value):
    """Function for formatting the numbers input to look like currency"""
    value = re.sub(r'[^\d]', '', value)
    try:
        if len(value) > 2:
            value = value[:-2] + '.' + value[-2:]
            value = float(value)
        else:
            value = '0.' + value.zfill(2)
            value = float(value)
            print(f"Float value: {value}")
        formatted_value = f"{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return formatted_value
    except ValueError as e:
        print(f"Error: {e}")
        return ""
    
class HouseHold():

    household_instance = []

    def __init__(self,
                 HouseHoldName=None,
                 HouseHoldNet=None,
                 HouseHoldShared=None,
                 household_net_number=None,
                 household_dict={}):

        self.HouseHoldName = HouseHoldName
        self.HouseHoldNet = HouseHoldNet
        self.HouseHoldShared = HouseHoldShared
        self.household_net_number = household_net_number

        self.household_dict = household_dict

        HouseHold.household_instance.append(self)

    def hh_name_entry_widget(self, master_frame):
        text_var = ctk.StringVar()
        hh_name_entry = ctk.CTkEntry(master=master_frame,
                                    textvariable=text_var,
                                    fg_color=entry_background,
                                    placeholder_text="Enter Household Name",
                                    font=("Roboto", 18),
                                    corner_radius=entry_round_corners,
                                    border_width=0,
                                    text_color="white",
                                    width=400)
        hh_name_entry.pack(padx=10, pady=20)

        def limit_characters(entry, limit):
            value = entry.get()
            if len(value) > limit:
                entry.set(value[:limit])

        character_limit = 30
        text_var.trace_add("write", lambda *args: limit_characters(text_var, character_limit))

        def on_name_entry_confirm(hh_name_entry):
            self.HouseHoldName = hh_name_entry.get()
            self.household_dict["Household name"] = self.HouseHoldName
            activate_entry(HouseHoldMember.member_instances[0].memb_name_entry)
            print(self.household_dict)
            print("the new household name is " + self.HouseHoldName)

        def create_lambda(hh_name_entry):
            return lambda event: on_name_entry_confirm(hh_name_entry)
        
        hh_name_entry.bind("<Return>", create_lambda(hh_name_entry))

    def divider_line_horizontal(self, master_frame, row):
        divider_line_frame_horizontal = ctk.CTkFrame(master=master_frame,
                            height=2,
                            fg_color="#ffffff",
                            width=430)
        divider_line_frame_horizontal.grid(column=0, row=row, columnspan=2)

    def divider_line_vertical(self, master_frame, row, column, height):
        divider_line_frame_vertical = ctk.CTkFrame(master=master_frame,
                            height=height,
                            fg_color="#ffffff",
                            width=2)
        divider_line_frame_vertical.grid(column=column, row=row, columnspan=1, padx=10)

    def hh_net_widget(self, master_frame):
        household_net_frame = ctk.CTkFrame(master=master_frame,
                                           fg_color=background,
                                           corner_radius=0)
        household_net_frame.grid(columnspan=2, sticky="ew", row=0, column=1)
        household_net_frame.grid_columnconfigure(1, weight=1)
        
        household_net_label = ctk.CTkLabel(master=household_net_frame,
                                           fg_color=background,
                                           text="Household net / month",
                                           width=200,
                                           anchor="w")
        household_net_label.grid(sticky="w", row=0, column=0)

        self.household_net_number = ctk.CTkLabel(master=household_net_frame,
                                                 fg_color=background,
                                                 text="0",
                                                 text_color=green,
                                                 width=230,
                                                 anchor="e")
        self.household_net_number.grid(sticky="e", row=0, column=1)

class HouseHoldMember():

    member_instances = []

    def __init__(self,
                 MembName=None,
                 MtlyNet=0,
                 NetPercent=None,
                 ExpenseTotal=None,
                 MembShare=None,
                 percent_of_net_widget=None,
                 member_dict={}):

        self.MembName = MembName
        self.MtlyNet = MtlyNet
        self.NetPercent = NetPercent
        self.ExpenseTotal = ExpenseTotal
        self.MembShare = MembShare
        self.total_net = 0
        self.percent_of_net_widget = percent_of_net_widget
        self.mtly_net_unformatted = 0
        self.total_net_unformatted = 0

        self.member_dict = member_dict

        self.member_dict["member_net_income"] = 0
        self.member_dict["member_net_raw"] = 0
        self.member_dict["household_member_name"] = ""
        self.member_dict["member_percent_share"] = 0

        self.income_dict = {}

        HouseHoldMember.member_instances.append(self)

    def memb_name_entry_widget(self, master_frame):

        """Name entry for household member"""
        memb_container = ctk.CTkFrame(master=master_frame, corner_radius=0, fg_color=background)
        memb_container.pack()

        memb_name_var = ctk.StringVar()
        self.memb_name_entry = ctk.CTkEntry(master=memb_container,
                            textvariable=memb_name_var,
                            fg_color=entry_background,
                            placeholder_text="Enter Member Name",
                            font=("Roboto", 12),
                            corner_radius=entry_round_corners,
                            border_width=0,
                            text_color="white",
                            width=member_widget_width,
                            state="disabled"
                            )
        self.memb_name_entry.pack(pady=member_widget_pady, padx=member_widget_padx)

        name_character_limit = 20
        trace_add(memb_name_var, name_character_limit)

        def on_name_entry_confirm(memb_name_entry):
            self.MembName = memb_name_entry.get()
            activate_entry(self.mtly_net_entry)
            print("the household member name is " + self.MembName)

        create_lambda(on_name_entry_confirm, self.memb_name_entry)
        self.memb_name_entry.bind("<Return>", create_lambda(on_name_entry_confirm, self.memb_name_entry))

        """Monthly net entry widget for household member"""
        mtly_net_var = ctk.StringVar()
        self.mtly_net_entry = ctk.CTkEntry(master=memb_container,
                            textvariable=mtly_net_var,
                            fg_color=entry_background,
                            placeholder_text="Enter Mtly net income",
                            font=("Roboto", 10),
                            corner_radius=entry_round_corners,
                            border_width=0,
                            text_color=green,
                            width=member_widget_width,
                            state="disabled"
                            )
        self.mtly_net_entry.pack(pady=member_widget_pady, padx=member_widget_padx)

        income_character_limit = 12
        trace_add(mtly_net_var, income_character_limit)

        def on_income_entry_confirm(mtly_net_entry):
            self.MtlyNet = mtly_net_entry.get()
            self.mtly_net_unformatted = self.MtlyNet.replace(".", "").replace(",", "")

            for i, member in enumerate(self.member_instances):
                self.income_dict[f"member_{i}"] = int(member.mtly_net_unformatted)
                print("the income dictionary is:")
                print(self.income_dict)

            """format input, format it and put it back onto the label"""
            self.formatted_net = format_income_entry(self.MtlyNet)
            self.mtly_net_entry.delete(0, 'end')
            self.mtly_net_entry.insert(0, str(self.formatted_net))
            print(str(self.MembName) + " monthly net income is " + str(self.formatted_net))

            """this is for calculating the combined household net"""
            self.total_net = sum(self.income_dict.values())
            self.total_net_unformatted = self.total_net
            self.total_net = format_income_entry(str(self.total_net))

            HouseHold.household_instance[0].household_dict["Net income"] = self.total_net
            HouseHold.household_instance[0].household_net_number.configure(text=self.total_net)

            activate_entry(self.member_instances[1].memb_name_entry)
            activate_entry(self.add_expense_btn)

            print("the combined total net income is: " + self.total_net)
            if all(value != 0 for value in self.income_dict.values()):
                for member in self.member_instances:
                    percent_number = str(round(self.calculate_member_percent_share(input=member.mtly_net_unformatted), 2)) + "%"
                    member.percent_of_net_widget.configure(text=percent_number)
                    """filling the member dictionary"""
                    self.member_dict["member_percent_share"] = percent_number
                    self.member_dict["member_net_income"] = member.formatted_net
                    self.member_dict["member_net_raw"] = member.mtly_net_unformatted
                    self.member_dict["household_member_name"] = member.MembName

                    print(member.MembName + " dictionary: ")
                    print(member.member_dict)

        create_lambda(on_income_entry_confirm, self.mtly_net_entry)
        self.mtly_net_entry.bind("<Return>", create_lambda(on_income_entry_confirm, self.mtly_net_entry))

    def member_percent_of_net(self, master_frame, column):
        self.percent_of_net_widget = ctk.CTkLabel(master=master_frame,
                                                fg_color=background,
                                                text=" ",
                                                width=150)
        self.percent_of_net_widget.grid(row=0, column=column, sticky="n")

    def calculate_member_percent_share(self, input):
        percent_share = (int(input) / self.total_net_unformatted) * 100
        print("input for the % share calculation: " + str(input) + " and " + str(self.total_net_unformatted))
        print("calculated % share = " + str(percent_share))
        return percent_share

    """Adding expenses"""
    def expenses_widget(self, master_frame):

        expenses_container = ctk.CTkFrame(master=master_frame, corner_radius=0, fg_color=background)
        expenses_container.grid(columnspan=3)

        self.add_expense_btn = ctk.CTkButton(master=expenses_container,
                                    height=25,
                                    width=25,
                                    corner_radius=100,
                                    border_width=0,
                                    text="+",
                                    state="disabled",
                                    command=self.floating_expense_entry)
        self.add_expense_btn.grid(sticky="n", column=1, row=0)

    def add_expenses(self, master_frame, expense_name, expense_value):

        expense_field_frame = ctk.CTkFrame(master=master_frame,
                                           fg_color=entry_background,
                                           width=200,
                                           corner_radius=entry_round_corners)
        expense_field_frame.grid(columnspan=3,
                                 row=1,
                                 pady=member_widget_pady,
                                 padx=member_widget_padx)
        
        remove_expense = ctk.CTkButton(master=expense_field_frame,
                                       corner_radius=100,
                                       width=20,
                                       height=20,
                                       text="X")
        remove_expense.grid(pady=member_widget_pady,
                            padx=member_widget_padx,
                            column=0,
                            row=0,
                            sticky="nw")
        
        name_and_amount_frame = ctk.CTkFrame(master=expense_field_frame,
                                  width=150,
                                  height=20,
                                  fg_color=entry_background,
                                  corner_radius=entry_round_corners)
        name_and_amount_frame.grid(column=1, row=0)

        expense_name_field = ctk.CTkLabel(master=name_and_amount_frame,
                                          width=100,
                                          height=20,
                                          fg_color=entry_background,
                                          corner_radius=entry_round_corners,
                                          text=expense_name)
        expense_name_field.grid(column=0,
                                row=0,
                                sticky="e")

        expense_amount_field = ctk.CTkLabel(master=name_and_amount_frame,
                                            width=60,
                                            fg_color=entry_background,
                                            corner_radius=entry_round_corners,
                                            text=expense_value)
        expense_amount_field.grid(column=1,
                                  row=0)
        
    def floating_expense_entry(self):

        expense_entry = ctk.CTkToplevel()
        expense_entry.geometry("310x40+200+200")
        expense_entry.overrideredirect(True)
        expense_entry.attributes("-topmost", True)
        expense_entry.configure(fg_color=background)

        self.expense_entry_dict = {}
        self.expense_entry_dict["expense_name"] = ""
        self.expense_entry_dict["expense_amount_raw"] = ""
        self.expense_entry_dict["expense_amount_formatted"] = ""

        self.expense_entry_list = []
        self.expense_entry_list.append(self.expense_entry_dict)

        def create_expense_widget():
            """Filling the expense entry dict for future use"""
            self.expense_entry_dict["expense_name"] = expense_name_entry.get()
            self.expense_entry_dict["expense_amount_raw"] = expense_value_entry.get()
            
            if self.optionmenu_value.get() == "monthly":
                expense_widget_amount = self.expense_entry_dict["expense_amount_raw"]
            else:
                expense_widget_amount = self.expense_entry_dict["expense_amount_raw"]
                expense_widget_amount = expense_widget_amount[:-2] + "." + expense_widget_amount[-2:]
                expense_widget_amount = float(expense_widget_amount) / 12
                self.expense_entry_dict["expense_amount_raw"] = str(expense_widget_amount).replace(".", "")
                expense_widget_amount = round(expense_widget_amount, 2)
                expense_widget_amount = str(expense_widget_amount).replace(".", "")
                            
            self.expense_entry_dict["expense_amount_formatted"] = format_income_entry(expense_widget_amount)

            # from ..HouseHoldSplit import spawn_expense
            # spawn_expense()

            expense_entry.destroy()

        expense_name_entry_var = ctk.StringVar()
        expense_name_entry = ctk.CTkEntry(master=expense_entry,
                            textvariable=expense_name_entry_var,
                            placeholder_text="EnterExpense",
                            font=("Roboto", 10),
                            corner_radius=0,
                            border_width=0,
                            text_color="white",
                            width=100,
                            fg_color=entry_background)
        expense_name_entry.grid(pady=member_widget_pady, padx=member_widget_padx, column=0, row=0)

        expense_name_character_limit = 12
        trace_add(expense_name_entry_var, expense_name_character_limit)
        
        expense_value_entry_var = ctk.StringVar()
        expense_value_entry = ctk.CTkEntry(master=expense_entry,
                            textvariable=expense_value_entry_var,
                            placeholder_text="0000.00",
                            font=("Roboto", 10),
                            corner_radius=0,
                            border_width=0,
                            text_color="white",
                            width=60,
                            fg_color=entry_background)
        expense_value_entry.grid(pady=member_widget_pady, padx=member_widget_padx, column=1, row=0)

        expense_value_character_limit = 7
        trace_add(expense_value_entry_var, expense_value_character_limit)

        def optionmenu_callback(choice):
            self.optionmenu_value.set(choice)
            activate_entry(self.confirm_btn)
            print("Selected choice:", choice)

        self.optionmenu_value = ctk.StringVar()
        optionmenu = ctk.CTkOptionMenu(master=expense_entry,
                                       values=["monthly", "yearly"],
                                       font=("Roboto", 10),
                                       width=60,
                                       command=optionmenu_callback)
        optionmenu.grid(padx=5, pady=5, row=0, column=2)
        optionmenu.set("select cycle")

        image_path = "./check.png"
        image = Image.open(image_path)
        scaled_image = image.resize((20, 20))
        check_icon = ImageTk.PhotoImage(scaled_image)

        self.confirm_btn = ctk.CTkButton(master=expense_entry,
                                    width=10,
                                    height=10,
                                    corner_radius=50,
                                    image=check_icon,
                                    fg_color=background,
                                    hover_color=green,
                                    text="",
                                    state="disabled",
                                    command=create_expense_widget)
        self.confirm_btn.grid(column=3, row=0)