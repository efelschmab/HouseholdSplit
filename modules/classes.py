import customtkinter as ctk

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
                            #fg_color="#181818",
                            fg_color="red",
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

        household_net_number = ctk.CTkLabel(master=household_net_frame, fg_color="white", text="12345", text_color=green)
        household_net_number.grid(sticky="e", row=0, column=1)




class HouseHoldMember():

    def __init__(self, MembName=None, MtlyNet=None, NetPercent=None, ExpenseTotal=None, MembShare=None):

        self.MembName = MembName
        self.MtlyNet = MtlyNet
        self.NetPercent = NetPercent
        self.ExpenseTotal = ExpenseTotal
        self.MembShare = MembShare

    # general functions for this class
    def limit_characters(entry, limit):
        value = entry.get()
        if len(value) > limit:
            entry.set(value[:limit])

    def memb_name_entry_widget(self, master_frame):

        memb_container = ctk.CTkFrame(master=master_frame, corner_radius=0, fg_color=background)
        memb_container.pack()

        # Name entry for household member

        memb_name_var = ctk.StringVar()
        memb_name_entry = ctk.CTkEntry(master=memb_container,
                            textvariable=memb_name_var,
                            fg_color=background,
                            placeholder_text="Enter Member Name",
                            font=("Roboto", 12),
                            corner_radius=0,
                            border_width=0,
                            text_color="white",
                            width=200)
        memb_name_entry.pack(padx=10)

        character_limit = 10
        memb_name_var.trace_add("write", lambda *args: self.limit_characters(memb_name_var, character_limit))

        def on_name_entry_confirm(memb_name_entry):
            self.MembName = memb_name_entry.get()
            print("the household member name is " + self.MembName)

        def create_lambda(memb_name_entry):
            return lambda event: on_name_entry_confirm(memb_name_entry)
        
        memb_name_entry.bind("<Return>", create_lambda(memb_name_entry))

        # Monthly net entry for household member

        mtly_net_var = ctk.StringVar()
        mtly_net_entry = ctk.CTkEntry(master=memb_container,
                            textvariable=mtly_net_var,
                            fg_color="black",
                            placeholder_text="Enter Mtly net income",
                            font=("Roboto", 10),
                            corner_radius=0,
                            border_width=0,
                            text_color=green,
                            width=150)
        mtly_net_entry.pack(padx=10)

        income_character_limit = 10
        mtly_net_var.trace_add("write", lambda *args: self.limit_characters(mtly_net_var, income_character_limit))

        def on_income_entry_confirm(mtly_net_entry):
            self.MtlyNet = mtly_net_entry.get()
            print(str(self.MembName) + " monthly net income is " + str(self.MtlyNet))

        def create_lambda(mtly_net_entry):
            return lambda event: on_income_entry_confirm(mtly_net_entry)
        
        mtly_net_entry.bind("<Return>", create_lambda(mtly_net_entry))