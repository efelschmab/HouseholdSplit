import customtkinter as ctk

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

    def divider_line(self, master_frame):
        divider_line_frame = ctk.CTkFrame(master=master_frame,
                            height=2,
                            fg_color="#ffffff",
                            width=430)
        divider_line_frame.pack()




class HouseHoldMember():

    def __init__(self, MembName=None, MtlyNet=None, NetPercent=None, ExpenseTotal=None, MembShare=None):

        self.MembName = MembName
        self.MtlyNet = MtlyNet
        self.NetPercent = NetPercent
        self.ExpenseTotal = ExpenseTotal
        self.MembShare = MembShare

    def memb_name_entry_widget(self, master_frame):
        text_var = ctk.StringVar()
        memb_name_entry = ctk.CTkEntry(master=master_frame,
                            textvariable=text_var,
                            #fg_color="#181818",
                            fg_color="blue",
                            placeholder_text="Enter Member Name",
                            font=("Roboto", 12),
                            corner_radius=0,
                            border_width=0,
                            text_color="white",
                            width=200)
        memb_name_entry.pack(padx=10, pady=20)

        def limit_characters(entry, limit):
            value = entry.get()
            if len(value) > limit:
                entry.set(value[:limit])

        character_limit = 10
        text_var.trace_add("write", lambda *args: limit_characters(text_var, character_limit))

        def on_name_entry_confirm(memb_name_entry):
            self.MembName = memb_name_entry.get()
            print("the household member name is " + self.MembName)

        def create_lambda(memb_name_entry):
            return lambda event: on_name_entry_confirm(memb_name_entry)
        
        memb_name_entry.bind("<Return>", create_lambda(memb_name_entry))