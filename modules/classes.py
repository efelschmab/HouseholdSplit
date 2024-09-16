# To-Do:
# somehow restrict number input entry fields
# better placement for floating expense adding window
# if total spent > total income -> warning
# update_conclusion if statements need to be refined

from turtle import back
import customtkinter as ctk
import re
from PIL import Image, ImageTk

from . import database_logic

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

# def validate_numeric_input(entry_var):
#     value = entry_var.get()
#     if not value.isdigit():
#         entry_var.set(''.join(filter(str.isdigit, value)))


def trace_add(string_var, char_limit):
    string_var.trace_add(
        "write", lambda *args: limit_characters(string_var, char_limit))


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
        formatted_value = f"{value:,.2f}".replace(
            ',', 'X').replace('.', ',').replace('X', '.')
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

        self.household_dict["total_expenses"] = 0
        self.household_dict["household_name"] = ""
        self.household_dict["net_income"] = ""

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
        text_var.trace_add(
            "write", lambda *args: limit_characters(text_var, character_limit))

        def on_name_entry_confirm(hh_name_entry):
            self.HouseHoldName = hh_name_entry.get()
            self.household_dict["household_name"] = self.HouseHoldName
            activate_entry(HouseHoldMember.member_instances[0].memb_name_entry)
            print(self.household_dict)
            print(f"the new household name is {self.HouseHoldName}")
            database_logic.write_to_database(
                entry=self.household_dict["household_name"], table="household", column="household_name")

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
        divider_line_frame_vertical.grid(
            column=column, row=row, columnspan=1, padx=10)

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

    def total_shared_expenses_widget(self, master_frame):
        self.total_shared_expenses_lbl = ctk.CTkLabel(
            master=master_frame, fg_color=background, text="0,00", compound="center", width=40, text_color=red, font=("Roboto", 12))
        self.total_shared_expenses_lbl.grid(columnspan=3, padx=0, pady=0)

    def conclusion(self, master_frame):
        self.conclusion_label = ctk.CTkLabel(master=master_frame, fg_color=background, text=" ",
                                             text_color="white", font=("Roboto", 16), width=430, wraplength=400)
        self.conclusion_label.grid()

    def update_conclusion(self):
        if self.household_instance[0].household_dict["total_expenses"] > 0:
            member_1_name = HouseHoldMember.member_instances[0].member_dict["household_member_name"]
            member_1_share = HouseHoldMember.member_instances[0].member_dict["member_share_total"]
            member_1_share = str(member_1_share).replace(
                ".", "").replace(",", "")

            member_2_name = HouseHoldMember.member_instances[1].member_dict["household_member_name"]
            member_2_share = HouseHoldMember.member_instances[1].member_dict["member_share_total"]
            member_2_share = str(member_2_share).replace(
                ".", "").replace(",", "")

            member_1_total_expenses = HouseHoldMember.member_instances[
                0].member_dict["member_total_expenses"]
            member_2_total_expenses = HouseHoldMember.member_instances[
                1].member_dict["member_total_expenses"]

            member_1_split_calc = int(member_1_share) - member_1_total_expenses
            member_2_split_calc = int(member_2_share) - member_2_total_expenses

            member_1_split_format = format_income_entry(
                str(member_1_split_calc))
            member_2_split_format = format_income_entry(
                str(member_2_split_calc))

            if member_1_share == 0:
                label_string = f"{member_1_name} has no income, {member_2_name} has to pay the expenses of {
                    self.household_instance[0].household_dict["total_expenses"]}"
            elif member_2_share == 0:
                label_string = f"{member_2_name} has no income, {member_1_name} has to pay the expenses of {
                    self.household_instance[0].household_dict["total_expenses"]}"
            elif member_1_total_expenses > member_2_total_expenses:
                label_string = f"{member_2_name} needs to pay {
                    member_1_name} {member_1_split_format} per month"
            elif member_2_total_expenses > member_1_total_expenses:
                label_string = f"{member_1_name} needs to pay {
                    member_2_name} {member_2_split_format} per month"
            else:
                label_string = "Share and expenses are perfectly equal, crazy!"

            self.conclusion_label.configure(text=label_string)
        else:
            self.conclusion_label.configure(text=" ")


class HouseHoldMember():

    member_instances = []

    def __init__(self,
                 MembName=None,
                 MtlyNet=0,
                 NetPercent=None,
                 ExpenseTotal=None,
                 MembShare=None,
                 percent_of_net_widget=None):

        self.MembName = MembName
        self.MtlyNet = MtlyNet
        self.NetPercent = NetPercent
        self.ExpenseTotal = ExpenseTotal
        self.MembShare = MembShare
        self.total_net = 0
        self.percent_of_net_widget = percent_of_net_widget
        self.mtly_net_unformatted = 0
        self.total_net_unformatted = 0
        self.formatted_net = 0

        self.member_dict = {"member_net_income": 0,
                            "member_net_raw": 0,
                            "household_member_name": "",
                            "member_percent_share": 0,
                            "member_share_total": 0,
                            "member_percent_raw": 0,
                            "member_total_expenses": 0, }

        self.income_dict = {}
        self.expense_entry_list = []
        self.expense_row = 1
        self.next_expense_id = 0

        self.expense_widget_list = []

        HouseHoldMember.member_instances.append(self)

    def memb_name_entry_widget(self, master_frame):
        """Name entry for household member"""
        memb_container = ctk.CTkFrame(
            master=master_frame, corner_radius=0, fg_color=background)
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
        self.memb_name_entry.pack(
            pady=member_widget_pady, padx=member_widget_padx)

        name_character_limit = 20
        trace_add(memb_name_var, name_character_limit)

        def on_name_entry_confirm(memb_name_entry):
            self.MembName = memb_name_entry.get()
            activate_entry(self.mtly_net_entry)
            for member in self.member_instances:
                member.member_dict["household_member_name"] = self.MembName
            print("the household member name is " + self.MembName)

            self.calculate_member_percent_amount()
            self.calculate_combined_total_expenses()
            HouseHold.update_conclusion(HouseHold.household_instance[0])

        create_lambda(on_name_entry_confirm, self.memb_name_entry)
        self.memb_name_entry.bind("<Return>", create_lambda(
            on_name_entry_confirm, self.memb_name_entry))

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
        self.mtly_net_entry.pack(
            pady=member_widget_pady, padx=member_widget_padx)

        income_character_limit = 12
        trace_add(mtly_net_var, income_character_limit)

        def on_income_entry_confirm(mtly_net_entry):
            self.MtlyNet = mtly_net_entry.get()
            self.mtly_net_unformatted = self.MtlyNet.replace(
                ".", "").replace(",", "")

            for i, member in enumerate(self.member_instances):
                self.income_dict[f"member_{i}"] = int(
                    member.mtly_net_unformatted)

            """format input, format it and put it back onto the label"""
            self.formatted_net = format_income_entry(self.MtlyNet)
            self.mtly_net_entry.delete(0, 'end')
            self.mtly_net_entry.insert(0, str(self.formatted_net))
            print(str(self.MembName) + " monthly net income is " +
                  str(self.formatted_net))

            """this is for calculating the combined household net"""
            self.total_net = sum(self.income_dict.values())
            self.total_net_unformatted = self.total_net
            self.total_net = format_income_entry(str(self.total_net))

            HouseHold.household_instance[0].household_dict["net_income"] = self.total_net
            HouseHold.household_instance[0].household_net_number.configure(
                text=self.total_net)

            activate_entry(self.member_instances[1].memb_name_entry)
            activate_entry(self.add_expense_btn)

            print(f"the combined total net income is: {self.total_net}")
            for member in self.member_instances:
                percent_number = str(round(self.calculate_member_percent_share(
                    input=member.mtly_net_unformatted), 2)) + "%"
                member.member_dict["member_percent_raw"] = round(
                    self.calculate_member_percent_share(input=member.mtly_net_unformatted), 2)
                member.percent_of_net_widget.configure(text=percent_number)
                member.member_share_percent.configure(text=percent_number)

                """filling the member dictionary"""
                member.member_dict["member_percent_share"] = percent_number
                member.member_dict["member_net_income"] = member.formatted_net
                member.member_dict["member_net_raw"] = member.mtly_net_unformatted
                member.member_dict["household_member_name"] = member.MembName

                print(f"{member.MembName} dictionary:{
                    member.member_dict} ")

            self.calculate_member_percent_amount()
            self.calculate_combined_total_expenses()
            HouseHold.update_conclusion(HouseHold.household_instance[0])

        create_lambda(on_income_entry_confirm, self.mtly_net_entry)
        self.mtly_net_entry.bind("<Return>", create_lambda(
            on_income_entry_confirm, self.mtly_net_entry))

    def member_percent_of_net(self, master_frame, column):
        self.percent_of_net_widget = ctk.CTkLabel(master=master_frame,
                                                  fg_color=background,
                                                  text=" ",
                                                  width=150)
        self.percent_of_net_widget.grid(row=0, column=column, sticky="n")

    def calculate_member_percent_share(self, input):
        if self.total_net_unformatted == 0:
            return 0
        percent_share = (int(input) / self.total_net_unformatted) * 100
        return percent_share

    """Adding expenses"""

    def expenses_widget(self, master_frame):

        expenses_container = ctk.CTkFrame(
            master=master_frame, corner_radius=0, fg_color=background)
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

    def add_expense_widget_frame(self, master_frame):
        self.add_expense_widget_container = ctk.CTkFrame(
            master=master_frame, corner_radius=0, fg_color=background)
        self.add_expense_widget_container.grid(columnspan=1, row=1)

    def add_expenses(self, expense_name, expense_value):
        """This is the actual widget that is beeing created on the GUI"""

        expense_ID = self.next_expense_id

        expense_field_frame = ctk.CTkFrame(master=self.add_expense_widget_container,
                                           fg_color=background,
                                           width=200,
                                           corner_radius=0)
        expense_field_frame.grid(columnspan=3,
                                 row=self.expense_row,
                                 pady=member_widget_pady,
                                 padx=member_widget_padx)

        self.expense_widget_list.append((expense_ID, expense_field_frame))

        def remove_expense_btn(widget_ID=expense_ID):
            for id, frame in self.expense_widget_list:
                if id == widget_ID:
                    frame.destroy()
                    break
            self.expense_widget_list[:] = [
                entry for entry in self.expense_widget_list if entry[0] != widget_ID]

            expense_entry_list_copy = self.expense_entry_list[:]
            for entry in expense_entry_list_copy:
                if entry["ID"] == widget_ID:
                    self.expense_entry_list.remove(entry)
                    break

            self.calculate_total_expenses()
            self.calculate_combined_total_expenses()
            self.calculate_member_percent_amount()
            HouseHold.update_conclusion(HouseHold.household_instance[0])

        remove_expense = ctk.CTkButton(master=expense_field_frame,
                                       corner_radius=100,
                                       width=20,
                                       height=20,
                                       command=lambda: remove_expense_btn(
                                           expense_ID),
                                       text="X")
        remove_expense.grid(pady=member_widget_pady,
                            padx=member_widget_padx,
                            column=0,
                            row=0,
                            sticky="nw")

        name_and_amount_frame = ctk.CTkFrame(master=expense_field_frame,
                                             width=150,
                                             height=20,
                                             fg_color=background,
                                             corner_radius=0)
        name_and_amount_frame.grid(column=1, row=0)

        self.expense_name_field = ctk.CTkLabel(master=name_and_amount_frame,
                                               width=100,
                                               height=20,
                                               fg_color=background,
                                               corner_radius=0,
                                               text=f"{expense_name}",
                                               compound="left",
                                               anchor="w")
        self.expense_name_field.grid(column=0,
                                     row=0,
                                     sticky="e")

        expense_amount_field = ctk.CTkLabel(master=name_and_amount_frame,
                                            width=60,
                                            fg_color=background,
                                            height=20,
                                            corner_radius=0,
                                            compound="right",
                                            anchor="e",
                                            text=expense_value)
        expense_amount_field.grid(column=1,
                                  row=0,
                                  sticky="e")

        self.expense_row += 1

    def floating_expense_entry(self):

        if len(self.expense_entry_list) <= 7:
            expense_entry = ctk.CTkToplevel()
            expense_entry.geometry("310x40+200+200")
            expense_entry.overrideredirect(True)
            expense_entry.attributes("-topmost", True)
            expense_entry.configure(fg_color=background)

            self.expense_entry_dict = {}
            self.expense_entry_dict["expense_name"] = ""
            self.expense_entry_dict["expense_amount_raw"] = ""
            self.expense_entry_dict["expense_amount_formatted"] = ""
            self.expense_entry_dict["ID"] = self.next_expense_id

            def create_expense_widget():
                """Filling the expense entry dict for future use"""
                self.expense_entry_dict["expense_name"] = self.expense_name_entry.get(
                )
                self.expense_entry_dict["expense_amount_raw"] = self.expense_value_entry.get(
                )

                if self.optionmenu_value.get() == "monthly":
                    expense_widget_amount = self.expense_entry_dict["expense_amount_raw"]
                else:
                    expense_widget_amount = self.expense_entry_dict["expense_amount_raw"]
                    expense_widget_amount = expense_widget_amount[:-
                                                                  2] + "." + expense_widget_amount[-2:]
                    expense_widget_amount = float(expense_widget_amount) / 12
                    amount_numbers = len(
                        self.expense_entry_dict["expense_amount_raw"])
                    self.expense_entry_dict["expense_amount_raw"] = str(
                        expense_widget_amount)[:amount_numbers].replace(".", "")
                    expense_widget_amount = round(expense_widget_amount, 2)
                    expense_widget_amount = str(
                        expense_widget_amount).replace(".", "")

                self.expense_entry_dict["expense_amount_formatted"] = format_income_entry(
                    expense_widget_amount)
                self.expense_entry_list.append(self.expense_entry_dict)

                self.add_expenses(expense_name=self.expense_entry_dict["expense_name"],
                                  expense_value=self.expense_entry_dict["expense_amount_formatted"])
                self.calculate_total_expenses()
                self.calculate_combined_total_expenses()
                self.calculate_member_percent_amount()
                HouseHold.update_conclusion(HouseHold.household_instance[0])

                self.next_expense_id += 1

                expense_entry.destroy()

        self.expense_name_entry_var = ctk.StringVar()
        self.expense_name_entry = ctk.CTkEntry(master=expense_entry,
                                               textvariable=self.expense_name_entry_var,
                                               placeholder_text="EnterExpense",
                                               font=("Roboto", 10),
                                               corner_radius=0,
                                               border_width=0,
                                               text_color="white",
                                               width=100,
                                               fg_color=entry_background)
        self.expense_name_entry.grid(
            pady=member_widget_pady, padx=member_widget_padx, column=0, row=0)

        def on_expense_name_entry_confirm(expense_name_entry):
            activate_entry(self.expense_value_entry)

        create_lambda(on_expense_name_entry_confirm, self.expense_name_entry)
        self.expense_name_entry.bind("<Return>", create_lambda(
            on_expense_name_entry_confirm, self.expense_name_entry))

        expense_name_character_limit = 10
        trace_add(self.expense_name_entry_var, expense_name_character_limit)

        self.expense_value_entry_var = ctk.StringVar()
        self.expense_value_entry = ctk.CTkEntry(master=expense_entry,
                                                textvariable=self.expense_value_entry_var,
                                                placeholder_text="0,00",
                                                font=("Roboto", 10),
                                                corner_radius=0,
                                                border_width=0,
                                                width=60,
                                                fg_color=entry_background,
                                                text_color=red,
                                                state="disabled")
        self.expense_value_entry.grid(
            pady=member_widget_pady, padx=member_widget_padx, column=1, row=0)

        def on_expense_value_entry_confirm(expense_value_entry):
            activate_entry(self.optionmenu)

        create_lambda(on_expense_value_entry_confirm, self.expense_value_entry)
        self.expense_value_entry.bind("<Return>", create_lambda(
            on_expense_value_entry_confirm, self.expense_value_entry))

        expense_value_character_limit = 6
        trace_add(self.expense_value_entry_var, expense_value_character_limit)

        def optionmenu_callback(choice):
            self.optionmenu_value.set(choice)
            activate_entry(self.confirm_btn)

        self.optionmenu_value = ctk.StringVar()
        self.optionmenu = ctk.CTkOptionMenu(master=expense_entry,
                                            values=["monthly", "yearly"],
                                            font=("Roboto", 10),
                                            width=60,
                                            command=optionmenu_callback,
                                            state="disabled")
        self.optionmenu.grid(padx=5, pady=5, row=0, column=2)
        self.optionmenu.set("select cycle")

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

    def calculate_total_expenses(self):
        total_expenses = 0
        for entry in self.expense_entry_list:
            total_expenses = int(total_expenses) + \
                int(entry["expense_amount_raw"])
            self.member_dict["member_total_expenses"] = total_expenses

        total_expenses = format_income_entry(str(total_expenses))
        self.total_label_amount.configure(text=total_expenses)

    def total_expenses(self, master_frame, column):
        total_expenses_frame = ctk.CTkFrame(
            master=master_frame, fg_color=background, width=100)
        total_expenses_frame.grid(columnspan=2, column=column, row=0)

        total_label_text = ctk.CTkLabel(
            master=total_expenses_frame, fg_color=background, text="total monthly expenses", anchor="w", width=40)
        total_label_text.grid(row=0, column=0, sticky="w",
                              pady=member_widget_pady, padx=10)

        self.total_label_amount = ctk.CTkLabel(
            master=total_expenses_frame, fg_color=background, text="0,00", anchor="e", width=40, text_color=red)
        self.total_label_amount.grid(
            row=0, column=1, sticky="e", pady=member_widget_pady, padx=10)

    def calculate_combined_total_expenses(self):
        combined_expense_list = []
        for member in HouseHoldMember.member_instances:
            combined_expense_list.extend(member.expense_entry_list)
        total = 0
        for expense in combined_expense_list:
            total = int(total) + int(expense["expense_amount_raw"])
            total_raw = total if total is not None else 0

        if combined_expense_list == []:
            total_raw = 0
            total = 0

        total = format_income_entry(str(total))
        HouseHold.household_instance[0].household_dict["total_expenses"] = total_raw
        HouseHold.household_instance[0].total_shared_expenses_lbl.configure(
            text=total)

    def member_share_of_total(self, master_frame, column):
        member_share_frame = ctk.CTkFrame(
            master=master_frame, fg_color=background)
        member_share_frame.grid(column=column, sticky="n", row=0)

        self.member_share_percent = ctk.CTkLabel(master=member_share_frame, font=(
            "Roboto", 10), text_color="white", text="0.0%", width=200, height=5)
        self.member_share_percent.grid(sticky="n")

        self.member_share_amount = ctk.CTkLabel(master=member_share_frame, font=(
            "Roboto", 14), text_color="white", text="0,00", width=200, height=5)
        self.member_share_amount.grid(sticky="n")

    def calculate_member_percent_amount(self):
        expenses = HouseHold.household_instance[0].household_dict["total_expenses"] / 10
        for member in self.member_instances:
            if member.member_dict["member_percent_raw"] == 0.0:
                member_amount = 0
            else:
                percent = member.member_dict["member_percent_raw"] / 100
                expenses = round(expenses, 2)
                member_amount = expenses * percent
                member_amount = round(member_amount, 1)
                member_amount = format_income_entry(
                    str(member_amount).replace(".", ""))
            member.member_share_amount.configure(text=str(member_amount))
            member.member_dict["member_share_total"] = member_amount
