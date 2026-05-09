import pickle
from pathlib import Path
from tkinter import font

import customtkinter
from PIL import Image

cur_dir = Path(__file__).resolve().parent

sun_img = cur_dir / "sun.png"
moon_img = cur_dir / "moon.png"
left_arrow_dark_img = cur_dir / "left_arrow_dark.png"
left_arrow_light_img = cur_dir / "left_arrow_light.png"
right_arrow_dark_img = cur_dir / "right_arrow_dark.png"
right_arrow_light_img = cur_dir / "right_arrow_light.png"

change_theme_image = customtkinter.CTkImage(
    light_image=Image.open(sun_img), dark_image=Image.open(moon_img), size=(50, 50)
)
left_arrow_image = customtkinter.CTkImage(
    light_image=Image.open(left_arrow_light_img),
    dark_image=Image.open(left_arrow_dark_img),
)
right_arrow_image = customtkinter.CTkImage(
    light_image=Image.open(right_arrow_light_img),
    dark_image=Image.open(right_arrow_dark_img),
)


customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")


class Salt:
    n_grp_tests = {
        "Lead": 2,
        "Copper": 3,
        "Aluminium": 4,
        "Iron": 4,
        "Zinc": 5,
        "Barium": 6,
        "Calcium": 6,
        "Strontium": 6,
        "Ammonium": 7,
        "Magnesium": 7,
    }

    def __init__(self, acid, base):
        self.acid = acid
        self.base = base
        self.full = base + " " + acid
        self.ngrp = self.n_grp_tests.get(self.base)


class Test:
    def __init__(self, name, section, experiment, result_dict, component=None):
        self.name = name
        self.section = section
        self.experiment = experiment
        self.result_dict = result_dict
        self.component = component

    def __str__(self):
        result = ""
        result += f"Name: {self.name}\n"
        result += f"Section: {self.section}\n"
        result += f"Experiment: {self.experiment}\n"
        result += f"Choices: \n {self.result_dict}\n"
        if self.component:
            result += f"Confirmatory for {self.component}\n"
        return result

    def get_obs_inf(self, salt):
        observation, inference = "", ""
        acid_present = salt.acid in self.result_dict
        base_present = salt.base in self.result_dict
        full_present = salt.full in self.result_dict
        if acid_present:
            observation += self.result_dict.get(salt.acid)[0]
            inference += self.result_dict.get(salt.acid)[1]
        if base_present:
            observation += self.result_dict.get(salt.base)[0]
            inference += self.result_dict.get(salt.base)[1]
        if full_present:
            observation += self.result_dict.get(salt.full)[0]
            inference += self.result_dict.get(salt.full)[1]
        if not (acid_present or base_present or full_present):
            observation += self.result_dict.get("default")[0]
            inference += self.result_dict.get("default")[1]
        return observation, inference


class General:
    def __init__(self, text):
        self.text = text
        self.section = "Other"

    def __str__(self):
        return self.text


class SomeStuff:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class Parsed:
    def __init__(self, title, name, some_txt, experiment, observation, inference):
        self.title = title
        self.name = name
        self.some_txt = some_txt
        self.experiment = experiment
        self.observation = observation
        self.inference = inference

    def __str__(self):
        result = ""
        result += f"Title: {self.title}\n"
        result += f"Name: {self.name}\n"
        result += f"Upper: {self.some_txt}\n"
        result += f"Experiment: {self.experiment}\n"
        result += f"Observation: {self.observation}\n"
        result += f"Inference: {self.inference}\n"
        return result


class UI_Temp(customtkinter.CTk):
    def __init__(self, typ, font_name, font_size):
        super().__init__()

        if typ == "Help":
            self.title("Venkat Chem Record - Help")
        else:
            self.title("Venkat Chem Record - About")
        self.geometry("500x400")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        if typ == "Help":
            txt = "\n".join(
                [
                    "Hello! This is a guide to using this software!",
                    "",
                    "",
                    "You can change the font and the font size of the given text!",
                    "",
                    "",
                    "Use the textbox to change the font style.",
                    "NOTE: The font will only work if it is in your computer",
                    "",
                    "Use the nearby textbox to change the font size",
                    "",
                    "",
                    "",
                    "If bugs are found, please report them at",
                    "venkateshv2k10@gmail.com",
                ]
            )
        else:
            txt = "\n".join(
                [
                    "Hi! I am V.Venkatesh. I am the developer of this project!",
                    "",
                    "This project helps students write their chemistry record.",
                    "",
                    "",
                    "Developement and Coding: V.Venkatesh",
                    "Special thanks: V.Vidula",
                    "",
                    "If you liked this software, or found any bugs, etc.",
                    "Please contact me at venkateshv2k10@gmail.com",
                ]
            )

        self.text_frame = customtkinter.CTkFrame(self)
        self.text_lbl = create_label(
            self.text_frame, text=txt, font=(font_name, font_size)
        )
        self.text_lbl.configure(justify="left")
        self.text_lbl.grid(row=0, column=0, padx=13, pady=10, sticky="nsew")
        self.text_frame.grid(row=0, column=0, sticky="nsew")


class UI_Main(customtkinter.CTk):
    def __init__(self, parsed_list, app_name="Venkat Chem Record"):
        super().__init__()

        self.cur_index = 0
        self.parsed_list = parsed_list
        self.total_no_tests = len(self.parsed_list)
        self.cur_parse = self.parsed_list[0]

        self.title(app_name)
        self.geometry("900x400")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1, uniform="group1")
        self.grid_rowconfigure(1, weight=5, uniform="group1")
        self.grid_rowconfigure(2, weight=1, uniform="group1")

        self.font_name_var = customtkinter.StringVar()
        self.font_size_var = customtkinter.StringVar()

        self.font_name_var.trace_add("write", self.change_font_name)
        self.font_size_var.trace_add("write", self.change_font_size)

        self.fontname = "Calibri"
        self.default_fontsize = 20
        self.fontsize = self.default_fontsize

        self.toolbar = UI_toolbar(self)
        self.centrebar = UI_centre_frame(
            self, self.cur_parse, self.fontname, self.fontsize
        )
        self.taskbar = UI_taskbar(self)

        self.toolbar.grid(row=0, column=0, sticky="nsew")
        self.centrebar.grid(row=1, column=0, sticky="nsew")
        self.taskbar.grid(row=2, column=0, sticky="nsew")

    def change_font_name(self, name, index, mode):
        temp_font_name = self.font_name_var.get()
        try:
            all_fonts = font.families()
            if temp_font_name.lower() in [f.lower() for f in all_fonts]:
                self.fontname = temp_font_name
                self.update_font_everywhere()
        except:
            pass

    def change_font_size(self, name, index, mode):
        temp_font_size = self.font_size_var.get().strip()
        try:
            if temp_font_size:
                temp_font_size = int(temp_font_size)
                self.fontsize = temp_font_size
                self.update_font_everywhere()
        except:
            pass

    def update_font_everywhere(self):
        self.toolbar.font_entry_box.configure(font=(self.fontname, 20))
        self.toolbar.font_size_entry_box.configure(font=(self.fontname, 20))
        self.toolbar.progress_lbl.configure(font=(self.fontname, 30))
        self.toolbar.help_button.configure(font=(self.fontname, 20))
        self.toolbar.about_button.configure(font=(self.fontname, 20))
        self.centrebar.change_font(fontname=self.fontname, fontsize=self.fontsize)

    def move_left(self):
        if self.cur_index == 0:
            return
        self.cur_index -= 1
        self.update_progress_bar()
        self.update_centre_bar()

    def move_right(self):
        if self.cur_index == self.total_no_tests - 1:
            return
        self.cur_index += 1
        self.update_progress_bar()
        self.update_centre_bar()

    def update_progress_bar(self):
        progress_bar_lbl = self.toolbar.progress_lbl
        string = f"{self.cur_index + 1} / {self.total_no_tests}"
        progress_bar_lbl.configure(text=string)

    def update_centre_bar(self):
        self.cur_parse = self.parsed_list[self.cur_index]
        slaves = self.grid_slaves(row=1, column=0)
        for widget in slaves:
            widget.destroy()
        self.centrebar = UI_centre_frame(
            self, self.cur_parse, self.fontname, self.fontsize
        )
        self.centrebar.grid(row=1, column=0, sticky="nsew")


class UI_toolbar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="col")
        self.grid_columnconfigure(1, weight=3, uniform="col")
        self.grid_columnconfigure(2, weight=1, uniform="col")
        self.grid_columnconfigure(3, weight=3, uniform="col")
        self.grid_columnconfigure(4, weight=2, uniform="col")
        self.grid_columnconfigure(5, weight=2, uniform="col")

        self.change_theme_button = customtkinter.CTkButton(
            self,
            image=change_theme_image,
            text="",
            command=self.change_theme,
            width=0,
            height=0,
        )
        self.font_entry_box = customtkinter.CTkEntry(
            self,
            placeholder_text="Enter font name",
            justify="center",
            textvariable=self.master.font_name_var,
            font=(self.master.fontname, self.master.default_fontsize),
        )
        self.font_size_entry_box = customtkinter.CTkEntry(
            self,
            placeholder_text="Size",
            justify="center",
            textvariable=self.master.font_size_var,
            font=(self.master.fontname, self.master.default_fontsize),
        )
        self.total_tests = str(len(self.master.parsed_list))
        self.progress_lbl = create_label(
            self,
            text=f"1 / {self.total_tests}",
            font=(self.master.fontname, 30),
        )
        self.help_button = customtkinter.CTkButton(
            self,
            text="Help",
            command=self.display_help,
            font=(self.master.fontname, self.master.default_fontsize),
        )
        self.about_button = customtkinter.CTkButton(
            self,
            text="About",
            command=self.display_about,
            font=(self.master.fontname, self.master.default_fontsize),
        )

        self.font_entry_box.insert(0, self.master.fontname)
        self.font_size_entry_box.insert(0, str(self.master.default_fontsize))

        self.change_theme_button.grid(row=0, column=0, sticky="nsew")
        self.font_entry_box.grid(row=0, column=1, sticky="nsew")
        self.font_size_entry_box.grid(row=0, column=2, sticky="nsew")
        self.progress_lbl.grid(row=0, column=3, sticky="nsew")
        self.help_button.grid(row=0, column=4, sticky="nsew")
        self.about_button.grid(row=0, column=5, sticky="nsew")

    def change_theme(self):
        if customtkinter.get_appearance_mode() == "Light":
            customtkinter.set_appearance_mode("Dark")
            customtkinter.set_default_color_theme = "dark-blue"
        else:
            customtkinter.set_appearance_mode("Light")
            customtkinter.set_default_color_theme = "blue"

    def display_help(self):
        help_window = UI_Temp("Help", self.master.fontname, self.master.fontsize)
        help_window.mainloop()

    def display_about(self):
        about_window = UI_Temp("About", self.master.fontname, self.master.fontsize)
        about_window.mainloop()


class UI_taskbar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=4, uniform="col")
        self.grid_columnconfigure(1, weight=1, uniform="col")
        self.grid_columnconfigure(2, weight=3, uniform="col")
        self.grid_columnconfigure(3, weight=1, uniform="col")
        self.grid_columnconfigure(4, weight=4, uniform="col")

        left_button = customtkinter.CTkButton(
            self, image=left_arrow_image, text="", command=self.master.move_left
        )
        right_button = customtkinter.CTkButton(
            self, image=right_arrow_image, text="", command=self.master.move_right
        )
        left_button.grid(row=0, column=1)
        right_button.grid(row=0, column=3)


class UI_centre_frame(customtkinter.CTkFrame):
    def __init__(self, master, parsed, fontname, fontsize):
        super().__init__(master)

        self.fontname = fontname
        self.fontsize = fontsize
        self.header_txt = parsed.title
        self.some_txt = parsed.some_txt
        self.main_content = UI_main_content(
            self,
            parsed.name,
            parsed.experiment,
            parsed.observation,
            parsed.inference,
            self.fontname,
            self.fontsize,
        )

        self.grid_columnconfigure(0, weight=1)
        if self.some_txt is None:
            self.grid_rowconfigure(0, weight=1, uniform="rowA")
            self.grid_rowconfigure(1, weight=2, uniform="rowA")

            self.main_content.grid(row=1, column=0, sticky="nsew")
        else:
            self.grid_rowconfigure(0, weight=3, uniform="rowB")
            self.grid_rowconfigure(1, weight=1, uniform="rowB")
            self.grid_rowconfigure(2, weight=6, uniform="rowB")

            self.label_label = create_label(
                self, text=self.some_txt, font=(self.fontname, self.fontsize)
            )
            self.label_label.grid(row=1, column=0, sticky="nsew")
            self.main_content.grid(row=2, column=0, sticky="nsew")

        self.header_label = create_label(
            self, text=self.header_txt, font=(self.fontname, 2 * self.fontsize)
        )
        self.header_label.grid(row=0, column=0, sticky="nsew")

    def change_font(self, fontname, fontsize):
        self.header_label.configure(font=(fontname, 2 * fontsize))
        if self.some_txt:
            self.label_label.configure(font=(fontname, fontsize))
        self.main_content.change_font(fontname, fontsize)


class UI_main_content(customtkinter.CTkFrame):
    def __init__(
        self, master, name, experiment, observation, inference, fontname, fontsize
    ):
        super().__init__(master)

        self.name = name
        self.experiment_txt = experiment
        self.observation_txt = observation
        self.inference_txt = inference
        self.fontname = fontname
        self.fontsize = fontsize

        # Finishing experiment_col
        self.experiment_col = customtkinter.CTkScrollableFrame(self)
        self.experiment_lbl = create_label(
            self.experiment_col,
            text=self.experiment_txt,
            font=(self.fontname, self.fontsize),
        )
        self.experiment_col.grid_columnconfigure(0, weight=1)
        self.experiment_col.grid_rowconfigure(0, weight=1)
        if self.name is None:
            self.experiment_lbl.grid(row=0, column=0, sticky="nsew")
        else:
            self.experiment_col.grid_rowconfigure(1, weight=3)
            self.experiment_lbl.grid(row=1, column=0, sticky="nsew")

            self.name_lbl = create_label(
                self.experiment_col, text=self.name, font=(self.fontname, self.fontsize)
            )
            self.name_lbl.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="column")

        if self.observation_txt is not None:
            self.grid_columnconfigure(1, weight=1, uniform="column")
            self.grid_columnconfigure(2, weight=1, uniform="column")

            self.observation_col = customtkinter.CTkScrollableFrame(self)
            self.observation_col.grid_columnconfigure(0, weight=1)
            self.observation_col.grid_rowconfigure(0, weight=1)

            self.observation_lbl = create_label(
                self.observation_col,
                text=self.observation_txt,
                font=(self.fontname, self.fontsize),
            )
            self.observation_lbl.grid(row=0, column=0, sticky="nsew")

            self.inference_col = customtkinter.CTkScrollableFrame(self)
            self.inference_col.grid_columnconfigure(0, weight=1)
            self.inference_col.grid_rowconfigure(0, weight=1)

            self.inference_lbl = create_label(
                self.inference_col,
                text=self.inference_txt,
                font=(self.fontname, self.fontsize),
            )
            self.inference_lbl.grid(row=0, column=0, sticky="nsew")

            self.observation_col.grid(row=0, column=1, sticky="nsew")
            self.inference_col.grid(row=0, column=2, sticky="nsew")
        self.experiment_col.grid(row=0, column=0, sticky="nsew")

    def change_font(self, fontname, fontsize):
        if self.name:
            self.name_lbl.configure(font=(fontname, fontsize))
        self.experiment_lbl.configure(font=(fontname, fontsize))
        if self.observation_txt:
            self.observation_lbl.configure(font=(fontname, fontsize))
            self.inference_lbl.configure(font=(fontname, fontsize))


def wrap_text(event):
    event.widget.configure(wraplength=event.widget.master.winfo_width())


def create_label(master, text, font=None):
    if font is None:
        lbl = customtkinter.CTkLabel(master, text=text)
    else:
        lbl = customtkinter.CTkLabel(master, text=text, font=font)
    lbl.bind("<Configure>", wrap_text)
    return lbl


def gets_salt(acid_tuple, base_tuple):
    global acid, base

    def show_selection():
        global base, acid
        base = base_select.get()
        acid = acid_select.get()
        if base in base_tuple and acid in acid_tuple:
            getter.destroy()

    getter = customtkinter.CTk()
    getter.title("Venkat Chem Record - Enter Salt")
    getter.geometry("400x250")

    base_select = customtkinter.StringVar()
    acid_select = customtkinter.StringVar()

    customtkinter.CTkLabel(getter, text="Select Basic Radical:").pack(pady=(10, 0))
    base_dd = customtkinter.CTkComboBox(getter, variable=base_select, values=base_tuple)
    base_dd.pack(pady=5)
    base_dd.set(base_tuple[0])

    customtkinter.CTkLabel(getter, text="Select Acid Radical:").pack(pady=(10, 0))
    acid_dd = customtkinter.CTkComboBox(getter, variable=acid_select, values=acid_tuple)
    acid_dd["values"] = acid_tuple
    acid_dd.pack(pady=5)
    acid_dd.set(acid_tuple[0])

    btn = customtkinter.CTkButton(getter, text="Submit", command=show_selection)
    btn.pack(pady=20)

    getter.mainloop()


def parse_tests(salt, all_tests):
    no_of_grps = 0
    parsed_list = []
    for i in range(len(all_tests)):
        test = all_tests[i]
        if type(test) is General:
            parsed_test = Parsed("Prep of OS", None, None, test.text, None, None)
            parsed_list.append(parsed_test)
            continue
        elif type(test) is SomeStuff:
            continue
        else:
            ## TITLE
            if test.section == "Prelim":
                title = "Preliminary Tests"
            elif test.section == "Group":
                title = "Group Seperation"
            elif test.section == "Confirm":
                title = f"Confirmatory Tests: {test.component}"
            else:
                title = "Result"

            ## OBSERVATION AND INFERENCE
            if test.section == "Prelim":
                observation, inference = test.get_obs_inf(salt)
            if test.section == "Group":
                if salt.ngrp > no_of_grps:
                    no_of_grps += 1
                    observation, inference = test.get_obs_inf(salt)
                else:
                    continue
            if test.section == "Confirm":
                if test.component in (salt.acid, salt.base):
                    observation, inference = test.get_obs_inf(salt)
                else:
                    continue

            ## LABEL
            if (i - 1 > -1) and type(all_tests[i - 1]) is SomeStuff:
                lbl = all_tests[i - 1].text
            else:
                lbl = None

            parsed_test = Parsed(
                title, test.name, lbl, test.experiment, observation, inference
            )
        parsed_list.append(parsed_test)
    parsed_result = Parsed(
        "Result",
        None,
        None,
        f"The acid radical present in the given simple salt was found to be {salt.acid} ion. The basic radical present in the given simple salt was found to be {salt.base} ion. Therefore, the given simple salt is {salt.full}",
        None,
        None,
    )
    parsed_list.append(parsed_result)
    return parsed_list


def main():
    global acid, base
    base_tuple = (
        "Ammonium",
        "Lead",
        "Copper",
        "Zinc",
        "Aluminium",
        "Iron",
        "Barium",
        "Calcium",
        "Strontium",
        "Magnesium",
    )
    acid_tuple = (
        "Chloride",
        "Bromide",
        "Sulphate",
        "Nitrate",
        "Acetate",
        "Carbonate",
        "Phosphate",
    )

    with open("tests.pkl", "rb") as fl:
        all_tests = pickle.load(fl)
    gets_salt(acid_tuple, base_tuple)
    salt = Salt(acid, base)
    parsed_list = parse_tests(salt, all_tests)

    app = UI_Main(parsed_list)
    app.mainloop()


acid, base = None, None
main()
