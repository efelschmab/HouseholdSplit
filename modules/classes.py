import customtkinter as ctk
import re

green = "#15ce27"
red = "#ff0000"
background = "#181818"

class HouseHold():

    def __init__(self, HouseHoldName=None, HouseHoldNet=None, HouseHoldShared=None):

        self.HouseHoldName = HouseHoldName
        self.HouseHoldNet = HouseHoldNet
        self.HouseHoldShared = HouseHoldShared

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
            HouseHoldMember.memb_name_entry_widget.mem
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
        household_net_frame = ctk.CTkFrame(master=master_frame, fg_color=background, corner_radius=0)
        household_net_frame.grid(columnspan=2, sticky="ew", row=0, column=1)
        household_net_frame.grid_columnconfigure(1, weight=1)
        
        household_net_label = ctk.CTkLabel(master=household_net_frame, fg_color=red, text="Household net / month")
        household_net_label.grid(sticky="w", row=0, column=0)

        self.household_net_number = ctk.CTkLabel(master=household_net_frame, fg_color="white", text="test", text_color=green)
        self.household_net_number.grid(sticky="e", row=0, column=1)

class HouseHoldMember():

    def __init__(self, MembName=None, MtlyNet=0, NetPercent=None, ExpenseTotal=None, MembShare=None):

        self.MembName = MembName
        self.MtlyNet = MtlyNet
        self.NetPercent = NetPercent
        self.ExpenseTotal = ExpenseTotal
        self.MembShare = MembShare
        self.total_net = 0

        self.income_list = []

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
            self.income_list.append(int(self.MtlyNet))
            format_income_entry(self.MtlyNet)
            print(str(self.MembName) + " monthly net income is " + str(self.MtlyNet))
            if len(self.income_list) > 1:
                self.total_net = self.income_list[0] + self.income_list[1]
                self.total_net = str(self.total_net)
                format_income_entry(self.total_net) # das funktioniert noch nicht so ganz, bei der format_income_entry funktion wird das entry field angepasst!
                print("the combined total income is: " + self.total_net)
            print(self.income_list)
            print(self.total_net)
        
        create_lambda(on_income_entry_confirm, mtly_net_entry)
        mtly_net_entry.bind("<Return>", create_lambda(on_income_entry_confirm, mtly_net_entry))

        def format_income_entry(value):
            value = re.sub(r'[^\d]', '', value)
            print(value)
            try:
                if len(value) > 2:
                    value = value[:-2] + '.' + value[-2:]
                    value = float(value)
                else:
                    value = '0.' + value.zfill(2)
                    value = float(value)
                    print(f"Float value: {value}")
                formatted_value = f"{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                self.MtlyNet = formatted_value
                formatted_value_str = str(formatted_value)
                mtly_net_entry.delete(0, 'end')
                mtly_net_entry.insert(0, formatted_value_str)
                return self.MtlyNet
            except ValueError as e:
                print(f"Error: {e}")
                return ""
