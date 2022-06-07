import tkinter as tk
import tkinter.messagebox
from winreg import CreateKey
import customtkinter
from tkinter import *
from PIL import ImageTk, Image
import os
from tkinter import filedialog
import rsa
from tkinter import messagebox


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"




class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("RSA")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

                # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Alice",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Send message",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.saveFile)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Generate keys",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.createKeys)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Hashing",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.hashSignature)
        self.button_4.grid(row=4, column=0, pady=10, padx=20)

        self.label_2 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Bob",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_2.grid(row=5, column=0, pady=10, padx=30)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Check",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.checkMessage)
        self.button_3.grid(row=6, column=0, pady=10, padx=10)



        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_1.grid(row=9, column=0, pady=10, padx=20, sticky="w")

       

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")
       # T = Text(root, height = 5, width = 52)
        


        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="This is application where \n" +
                                                        "we check private and public keys,\n" +
                                                        "and hash message from A to B" ,
                                                   height=100,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)

        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Entry message")
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")
        #text = Text(root)
        #text.pack()
       
        # ============ frame_right ============

        #set default values
        self.switch_1.select()



    def change_mode(self):

        if self.switch_1.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def saveFile(self):
        file = filedialog.asksaveasfile(initialdir=r"C:\Users\julia\Desktop\RSA", #change directory
                                        defaultextension='.txt',
                                        filetypes=[
                                            ("Text file",".txt"),
                                            ("All files", ".*"),
                                        ])
        if file is None:
            return
        filetext = str(self.entry.get())
        file.write(filetext)
        file.close()

    def createKeys(self):
        (pubkey, privkey) = rsa.newkeys(2048)

# write the public key to a file
        with open('publickey.key', 'wb') as key_file:
            key_file.write(pubkey.save_pkcs1('PEM'))

# write the private key to a file
        with open('privatekey.key', 'wb') as key_file:
            key_file.write(privkey.save_pkcs1('PEM'))

    def hashSignature(self):
        def file_open(file):
            key_file = open(file, 'rb')
            key_data = key_file.read()
            key_file.close()
            return key_data



        privkey = rsa.PrivateKey.load_pkcs1(file_open('privatekey.key'))


        message = file_open('message.txt')
        hash_value = rsa.compute_hash(message, 'SHA3-512')  # optional



# Sign the message with the owners private key
        signature = rsa.sign(message, privkey, 'SHA3-512')

        s = open('signature_file','wb')
        s.write(signature)


        print(signature)

    def checkMessage(self):
        def file_open(file):
            key_file = open(file, 'rb')
            key_data = key_file.read()
            key_file.close()
            return key_data


# Open public key file and load in key
        pubkey = rsa.PublicKey.load_pkcs1(file_open('publickey.key'))

        message = file_open('message.txt')
        signature = file_open('signature_file')

# Verify the signature to show if successful or failed
        try:
            rsa.verify(message,signature,pubkey)
            messagebox.showinfo('Attention', 'Signature successfully verified')
            #print("Signature successfully verified")

        except:
            messagebox.showinfo('Attention', 'Warning!!!! Signature could not be verified')
           # print("Warning!!!! Signature could not be verified")

if __name__ == "__main__":
    app = App()
    app.mainloop()