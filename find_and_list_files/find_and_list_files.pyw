'''
Tested with Python v3.3.2

Copyright 2013 Zoran Petrović (zoran@zoran-software.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
'''

from tkinter import ttk as ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import re

class AppFrame(tk.Frame):

    def __init__(self, parent):
        self.folder = ""
        self.output_file = ""
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Find and list files v1.0")

        label_frame_browse = ttk.LabelFrame(self.parent, text = "Browse")
        label_frame_browse.pack(fill = tk.BOTH, expand = tk.YES)

        label_frame_find = ttk.LabelFrame(self.parent, text = "Find")
        label_frame_find.pack(fill = tk.BOTH, expand = tk.YES)

        label_frame_options = ttk.LabelFrame(self.parent, text = "Options")
        label_frame_options.pack(fill = tk.BOTH, expand = tk.YES)

        button_folder = ttk.Button(label_frame_browse, text = "Folder", command = self.browse_folder)
        button_folder.pack(fill = tk.BOTH, expand = tk.YES)

        button_output = ttk.Button(label_frame_browse, text = "Save output to", command = self.browse_output)
        button_output.pack(fill = tk.BOTH, expand = tk.YES)

        self.find_type_var = tk.StringVar()
        self.find_type_var.set("Contains")
        self.option_menu_find_type = ttk.OptionMenu(label_frame_find, self.find_type_var, "Contains", *["Starts with", "Ends with", "Contains", "Regular expression (regex)"])
        self.option_menu_find_type.pack(fill = tk.BOTH, expand = tk.YES)

        self.find_input_var = tk.StringVar()
        entry_find_input = ttk.Entry(label_frame_find, textvariable = self.find_input_var)
        entry_find_input.pack(fill = tk.BOTH, expand = tk.YES)

        button_find = ttk.Button(label_frame_find, text = "Find", command = self.find)
        button_find.pack(fill = tk.BOTH, expand = tk.YES)

        self.subfolders_var = tk.IntVar()
        checkbutton_subfolders = ttk.Checkbutton(label_frame_options, text = "Search in subfolders", variable = self.subfolders_var, onvalue = 1, offvalue = 0)
        checkbutton_subfolders.pack(side = tk.TOP, anchor = tk.NW)
        self.subfolders_var.set(checkbutton_subfolders['onvalue'])

        self.include_extension_var = tk.IntVar()
        checkbutton_include_extension = ttk.Checkbutton(label_frame_options, text = "Include file extension", variable = self.include_extension_var, onvalue = 1, offvalue = 0)
        checkbutton_include_extension.pack(side = tk.TOP, anchor = tk.NW)

        self.ignore_case_var = tk.IntVar()
        checkbutton_ignore_case = ttk.Checkbutton(label_frame_options, text = "Ignore case (slower)", variable = self.ignore_case_var, onvalue = 1, offvalue = 0)
        checkbutton_ignore_case.pack(side = tk.TOP, anchor = tk.NW)

        self.split_path_var = tk.IntVar()
        checkbutton_split_path = ttk.Checkbutton(label_frame_options, text = "Split path (Folder File Extension)", variable = self.split_path_var, onvalue = 1, offvalue = 0)
        checkbutton_split_path.pack(side = tk.TOP, anchor = tk.NW)

        ttk.Separator(label_frame_options, orient = tk.HORIZONTAL).pack(side = tk.TOP, fill = tk.X)

        self.remove_suffix_var = tk.IntVar()
        checkbutton_remove_suffix = ttk.Checkbutton(label_frame_options, text = "Remove suffix", variable = self.remove_suffix_var, onvalue = 1, offvalue = 0)
        checkbutton_remove_suffix.pack(side = tk.TOP, anchor = tk.NW)

        self.suffix_type_var = tk.StringVar()
        self.suffix_type_var.set("Suffix length")
        self.option_menu_suffix_type = ttk.OptionMenu(label_frame_options, self.suffix_type_var, "Suffix length", *["Suffix length", "Suffix starts with"])
        self.option_menu_suffix_type.pack(side = tk.LEFT, anchor = tk.NW)

        self.suffix_text_var = tk.StringVar()
        entry_suffix_text = ttk.Entry(label_frame_options, textvariable = self.suffix_text_var)
        entry_suffix_text.pack(fill = tk.X, side = tk.TOP, anchor = tk.NW)

        label_info = ttk.Label(self.parent, text = "Copyright 2013 Zoran Petrović\nLicence: GNU General Public License\nEmail: zoran@zoran-software.com")
        label_info.pack(fill = tk.BOTH, expand = tk.YES)

    def browse_folder(self):
        self.folder = tk.filedialog.askdirectory()

    def browse_output(self):
        self.output_file = tk.filedialog.asksaveasfilename()

    def match(self, find_in, find_what):
        if self.find_type_var.get() == "Starts with" and find_in.startswith(find_what):
            return True
        elif self.find_type_var.get() == "Ends with" and find_in.endswith(find_what):
            return True
        elif self.find_type_var.get() == "Contains" and find_what in find_in:
            return True
        elif self.find_type_var.get() == "Regular expression (regex)" and re.search(find_what, find_in):
            return True
        return False

    def find(self):
        if self.check_data():
            output_no, output_yes, output_yes_remove_suffix = range(3)
            files_all = list()
            if self.subfolders_var.get() == 0:
                files_all = [os.path.join(self.folder, f) for f in os.listdir(self.folder) if os.path.isfile(f)]
            else:
                for root, subfolders, files in os.walk(self.folder):
                    for file in files:
                        files_all.append(os.path.join(root, file))
            files = list()
            for item in files_all:
                file_name, file_extension = os.path.splitext(os.path.basename(item))
                if self.include_extension_var.get():
                    find_in = file_name + file_extension
                else:
                    find_in = file_name
                find_what = self.find_input_var.get()
                if (self.ignore_case_var.get() == 0 and self.match(find_in, find_what)) or (self.ignore_case_var.get() == 1 and self.match(find_in.lower(), find_what.lower())):
                    item = os.path.normpath(item)
                    files.append({'dirname': os.path.dirname(item), 'filename': file_name, 'extension': file_extension, 'output': output_yes})

            suffix_text = self.suffix_text_var.get()
            suffix_text_length = len(suffix_text)
            if self.remove_suffix_var.get() == 1 and suffix_text_length > 0:
                files_count = len(files)
                if self.suffix_type_var.get() == "Suffix length":
                    try:
                        suffix_length = int(suffix_text)
                        for i in range(files_count):
                            if files[i]['output'] != output_no:
                                temp_item_1 = files[i]['filename'][:suffix_length * -1]
                                for j in range(i + 1, files_count):
                                    temp_item_2 = files[j]['filename'][:suffix_length * -1]
                                    if files[i]['dirname'] == files[j]['dirname'] and temp_item_1 == temp_item_2 and len(temp_item_1) > 0:
                                        files[i]['filename'] = temp_item_1
                                        files[i]['output'] = output_yes_remove_suffix
                                        files[j]['output'] = output_no
                    except:
                        tk.messagebox.showerror("Error", "Remove suffix - Unexpected error")
                elif self.suffix_type_var.get() == "Suffix starts with":
                    try:
                        for i in range(files_count):
                            if files[i]['output'] != output_no:
                                temp_item_1 = files[i]['filename']
                                suffix_index = temp_item_1.rfind(suffix_text)
                                if suffix_index > 0:
                                    temp_item_1 = temp_item_1[0:suffix_index]
                                    for j in range(i + 1, files_count):
                                        temp_item_2 = files[j]['filename']
                                        suffix_index = temp_item_2.rfind(suffix_text)
                                        if suffix_index > 0:
                                            temp_item_2 = temp_item_2[0:suffix_index]
                                            if files[i]['dirname'] == files[j]['dirname'] and temp_item_1 == temp_item_2 and len(temp_item_1) > 0:
                                                files[i]['filename'] = temp_item_1
                                                files[i]['output'] = output_yes_remove_suffix
                                                files[j]['output'] = output_no
                    except:
                        tk.messagebox.showerror("Error", "Remove suffix - Unexpected error")
            try:
                f = open(self.output_file, 'w')
                for item in files:
                    if self.split_path_var.get() == 0 and item['output'] != output_no:
                        f.write("%s\n" % os.path.join(item['dirname'], item['filename'] + item['extension']))
                    elif self.split_path_var.get() == 1 and item['output'] != output_no:
                        f.write(item['dirname'] + "\t" + item['filename'] + "\t" + item['extension'] + '\n')
                f.close()
                messagebox.showinfo("Done", "Output saved to:\n" + self.output_file)
            except IOError:
                tk.messagebox.showerror("Error", "Error writing to file!")

    def check_data(self):
        ok = True
        if len(self.folder) < 1:
             messagebox.showerror("Error", "Please select folder")
             ok = False
        if len(self.output_file) < 1:
            messagebox.showerror("Error", "Please select output file")
            ok = False
        return ok

if __name__ ==  '__main__':
    root = tk.Tk()
    app = AppFrame(root)
    root.mainloop()
