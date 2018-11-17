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

class AppFrame(tk.Frame):

    def __init__(self, parent):
        self.list_a = list()
        self.list_b = list()
        self.output_file = ""
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Compare lists v1.0")

        label_frame_browse = ttk.LabelFrame(self.parent, text = "Browse")
        label_frame_browse.pack(fill = tk.BOTH, expand = tk.YES)

        label_frame_find = ttk.LabelFrame(self.parent, text = "Find")
        label_frame_find.pack(fill = tk.BOTH, expand = tk.YES)

        button_list_a = ttk.Button(label_frame_browse, text = "List A", command = self.browse_list_a)
        button_list_a.pack(fill = tk.BOTH, expand = tk.YES)

        button_list_b = ttk.Button(label_frame_browse, text = "List B", command = self.browse_list_b)
        button_list_b.pack(fill = tk.BOTH, expand = tk.YES)

        button_save_to = ttk.Button(label_frame_browse, text = "Save output to", command = self.browse_output)
        button_save_to.pack(fill = tk.BOTH, expand = tk.YES)

        button_difference = ttk.Button(label_frame_find, text = "Difference", command = self.difference)
        button_difference.pack(fill = tk.BOTH, expand = tk.YES)

        button_symmetric_difference = ttk.Button(label_frame_find, text = "Symmetric difference", command = self.symmetric_difference)
        button_symmetric_difference.pack(fill = tk.BOTH, expand = tk.YES)

        button_intersection = ttk.Button(label_frame_find, text = "Intersection", command = self.intersection)
        button_intersection.pack(fill = tk.BOTH, expand = tk.YES)

        label_info = ttk.Label(self.parent, text = "Copyright 2013 Zoran Petrović\nLicence: GNU General Public License\nEmail: zoran@zoran-software.com")
        label_info.pack(fill = tk.BOTH, expand = tk.YES)

    def browse_list_a(self):
        file = tk.filedialog.askopenfilename(filetypes = (("Text files", "*.txt;*.dat"), ("All files", "*.*")))
        try:
            f = open(file, 'r')
            self.list_a = f.readlines()
            f.close()
        except IOError:
            tk.messagebox.showerror("Error", "Error reading from file!")

    def browse_list_b(self):
        file = tk.filedialog.askopenfilename(filetypes = (("Text files", "*.txt;*.dat"), ("All files", "*.*")))
        try:
            f = open(file, 'r')
            self.list_b = f.readlines()
            f.close()
        except IOError:
            tk.messagebox.showerror("Error", "Error reading from file!")

    def browse_output(self):
        self.output_file = tk.filedialog.asksaveasfilename()
        self.list_a = [item.replace("\r\n", "").replace("\n", "") for item in self.list_a]
        self.list_b = [item.replace("\r\n", "").replace("\n", "") for item in self.list_b]

    def check_data(self):
        ok = True
        if len(self.list_a) < 1:
            tk.messagebox.showerror("Error", "Please select list A")
            ok = False
        if len(self.list_b) < 1:
            tk.messagebox.showerror("Error", "Please select list B")
            ok = False
        if len(self.output_file) < 1:
            tk.messagebox.showerror("Error", "Please select output file")
            ok = False
        return ok

    def difference(self):
        if self.check_data():
            try:
                f = open(self.output_file, 'w')
                items = set(self.list_a).difference(self.list_b)
                for item in items:
                    f.write("%s\n" % item)
                f.close()
                tk.messagebox.showinfo("Done", "Output saved to:\n" + self.output_file)
            except:
                tk.messagebox.showerror("Error", "Unexpected error")

    def symmetric_difference(self):
        if self.check_data():
            try:
                f = open(self.output_file, 'w')
                items = set(self.list_a).symmetric_difference(self.list_b)
                for item in items:
                    f.write("%s\n" % item)
                f.close()
                tk.messagebox.showinfo("Done", "Output saved to:\n" + self.output_file)
            except:
                tk.messagebox.showerror("Error", "Unexpected error")

    def intersection(self):
        if self.check_data():
            try:
                f = open(self.output_file, 'w')
                items = set(self.list_a).intersection(self.list_b)
                for item in items:
                    f.write("%s\n" % item)
                f.close()
                tk.messagebox.showinfo("Done", "Output saved to:\n" + self.output_file)
            except:
                tk.messagebox.showerror("Error", "Unexpected error")

if __name__ ==  '__main__':
    root = tk.Tk()
    app = AppFrame(root)
    root.mainloop()
