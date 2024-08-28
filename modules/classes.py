import customtkinter as ctk
import re

green = "#15ce27"
red = "#ff0000"
background = "#181818"

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
                                    fg_color=background,
                                    placeholder_text="Enter Household Name",
                                    font=("Roboto", 18),
                                    corner_radius=0,
                                    border_width=0,
                                    text_color="white",
                                    width=460)
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
            print(self.household_dict)
            print("the new household name is " + self.HouseHoldName)

        def create_lambda(hh_name_entry):
            return lambda event: on_name_entry_confirm(hh_name_entry)
        
        hh_name_entry.bind("<Return>", create_lambda(hh_name_entry))



    def divider_line(self, master_frame, row):
        divider_line_frame = ctk.CTkFrame(master=master_frame,
                            height=2,
                            fg_color="#ffffff",
                            width=430)
        divider_line_frame.grid(column=0, row=row, columnspan=2)



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

        self.income_dict = {}

        HouseHoldMember.member_instances.append(self)

    def memb_name_entry_widget(self, master_frame):

        """General functions for this class"""
        def activate_entry(widget):
            widget.configure(state="standard")
        
        def limit_characters(entry, limit):
            value = entry.get()
            if len(value) > limit:
                entry.set(value[:limit])

        def trace_add(string_var, char_limit):
            string_var.trace_add("write", lambda *args: limit_characters(string_var, char_limit))

        def create_lambda(on_entry_confirm, keybind):
            return lambda event: on_entry_confirm(keybind)

        def format_income_entry(value):
            """Function for formatting the numbers input"""
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

        """Name entry for household member"""
        memb_container = ctk.CTkFrame(master=master_frame, corner_radius=0, fg_color=background)
        memb_container.pack()

        memb_name_var = ctk.StringVar()
        memb_name_entry = ctk.CTkEntry(master=memb_container,
                            textvariable=memb_name_var,
                            fg_color=background,
                            placeholder_text="Enter Member Name",
                            font=("Roboto", 12),
                            corner_radius=0,
                            border_width=0,
                            text_color="white",
                            width=200,
                            #state="disabled"
                            )
        memb_name_entry.pack(padx=10)

        name_character_limit = 10
        trace_add(memb_name_var, name_character_limit)

        def on_name_entry_confirm(memb_name_entry):
            self.MembName = memb_name_entry.get()
            self.member_dict["Household member name"] = self.MembName
            print("the household member name is " + self.MembName)

        create_lambda(on_name_entry_confirm, memb_name_entry)
        memb_name_entry.bind("<Return>", create_lambda(on_name_entry_confirm, memb_name_entry))

        """Monthly net entry widget for household member"""
        mtly_net_var = ctk.StringVar()
        mtly_net_entry = ctk.CTkEntry(master=memb_container,
                            textvariable=mtly_net_var,
                            fg_color="black",
                            placeholder_text="Enter Mtly net income",
                            font=("Roboto", 10),
                            corner_radius=0,
                            border_width=0,
                            text_color=green,
                            width=150,
                            #state="disabled"
                            )
        mtly_net_entry.pack(padx=10)

        income_character_limit = 10
        trace_add(mtly_net_var, income_character_limit)

        def on_income_entry_confirm(mtly_net_entry):
            self.MtlyNet = mtly_net_entry.get()
            self.mtly_net_unformatted = self.MtlyNet.replace(".", "").replace(",", "")

            for i, member in enumerate(self.member_instances):
                self.income_dict[f"member_{i}"] = int(member.mtly_net_unformatted)
                print("the income dictionary is:")
                print(self.income_dict)

            """format input, format it and put it back onto the label"""
            formatted_net = format_income_entry(self.MtlyNet)
            self.member_dict["Member net income"] = formatted_net
            mtly_net_entry.delete(0, 'end')
            mtly_net_entry.insert(0, str(formatted_net))
            print(str(self.MembName) + " monthly net income is " + str(formatted_net))

            """this is for calculating the combined household net"""
            self.total_net = sum(self.income_dict.values())
            self.total_net_unformatted = self.total_net
            self.total_net = format_income_entry(str(self.total_net))

            HouseHold.household_instance[0].household_dict["Net income"] = self.total_net
            HouseHold.household_instance[0].household_net_number.configure(text=self.total_net)

            print("the combined total net income is: " + self.total_net)
            if all(value != 0 for value in self.income_dict.values()):
                for member in self.member_instances:
                    percent_number = str(round(self.calculate_member_percent_share(input=member.mtly_net_unformatted), 2)) + "%"
                    member.percent_of_net_widget.configure(text=percent_number)
                    self.member_dict["Member percent share"] = percent_number

        create_lambda(on_income_entry_confirm, mtly_net_entry)
        mtly_net_entry.bind("<Return>", create_lambda(on_income_entry_confirm, mtly_net_entry))

    def member_percent_of_net(self, master_frame, column_in):
        self.percent_of_net_widget = ctk.CTkLabel(master=master_frame,
                                                fg_color=background,
                                                text=" ",
                                                width=150)
        self.percent_of_net_widget.grid(row=0, column=column_in, sticky="n")

    def calculate_member_percent_share(self, input):
        percent_share = (int(input) / self.total_net_unformatted) * 100
        print("input for the % share calculation: " + str(input) + " and " + str(self.total_net_unformatted))
        print("calculated % share = " + str(percent_share))
        return percent_share