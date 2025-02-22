import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

# Database file
DB_FILE = "atm_users.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(DB_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Initialize users if file is empty
users = load_users()
if not users:
    users = {
        "123456": {"pin": "7890", "balance": 5000, "transactions": []},
    }
    save_users(users)

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EliteBank ATM")
        self.root.geometry("900x500")
        self.root.configure(bg="#D8BFD8")  # Light purple theme
        self.current_user = list(users.keys())[0]  # Automatically pick the first user from the database
        self.create_main_menu()
    
    def create_main_menu(self):
        self.clear_screen()
        
        ttk.Label(self.root, text="ELITEBANK ATM", font=("Arial", 24, "bold"), background="#D8BFD8", foreground="black").pack(pady=20)
        ttk.Label(self.root, text="Main Menu", font=("Arial", 14), background="#D8BFD8", foreground="black").pack(pady=10)
        
        buttons = ["Withdraw", "Deposit", "Balance", "Exit"]
        for btn in buttons:
            ttk.Button(self.root, text=btn, command=lambda b=btn: self.menu_action(b), style='TButton').pack(pady=10, ipadx=50, ipady=10)
    
    def menu_action(self, action):
        if action == "Withdraw":
            self.create_withdraw_screen()
        elif action == "Deposit":
            self.deposit_money()
        elif action == "Balance":
            self.check_balance()
        elif action == "Exit":
            self.root.quit()
    
    def create_withdraw_screen(self):
        self.clear_screen()
        
        ttk.Label(self.root, text="ELITEBANK ATM", font=("Arial", 24, "bold"), background="#D8BFD8", foreground="black").pack(pady=20)
        ttk.Label(self.root, text="Choose the amount you want to withdraw", font=("Arial", 14), background="#D8BFD8", foreground="black").pack(pady=10)
        
        amounts = [20, 40, 60, 80, 100, 200, 300]
        frame = tk.Frame(self.root, bg="#D8BFD8")
        frame.pack()
        
        for i in range(0, len(amounts), 2):
            ttk.Button(frame, text=f"{amounts[i]}", command=lambda a=amounts[i]: self.withdraw_money(a), style='TButton').grid(row=i, column=0, padx=20, pady=5, ipadx=20, ipady=10)
            if i+1 < len(amounts):
                ttk.Button(frame, text=f"{amounts[i+1]}", command=lambda a=amounts[i+1]: self.withdraw_money(a), style='TButton').grid(row=i, column=1, padx=20, pady=5, ipadx=20, ipady=10)
        ttk.Button(frame, text="Custom Amount", command=self.custom_withdraw, style='TButton').grid(row=len(amounts), columnspan=2, pady=10)
    
    def check_balance(self):
        messagebox.showinfo("Balance", f"Your current balance: ${users[self.current_user]['balance']}")
    
    def deposit_money(self):
        amount = self.simple_input("Enter deposit amount:")
        if amount and amount > 0:
            users[self.current_user]["balance"] += amount
            users[self.current_user]["transactions"].append(f"Deposited: ${amount}")
            save_users(users)
            messagebox.showinfo("Success", "Deposit successful!")
    
    def withdraw_money(self, amount):
        if 0 < amount <= users[self.current_user]["balance"]:
            users[self.current_user]["balance"] -= amount
            users[self.current_user]["transactions"].append(f"Withdrew: ${amount}")
            save_users(users)
            messagebox.showinfo("Success", "Withdrawal successful!")
        else:
            messagebox.showerror("Error", "Insufficient balance or invalid amount!")
    
    def custom_withdraw(self):
        amount = self.simple_input("Enter withdrawal amount:")
        if amount:
            self.withdraw_money(amount)
    
    def simple_input(self, prompt):
        return simpledialog.askfloat("Input", prompt)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=10, background="#ffffff", foreground="black")
    app = ATMApp(root)
    root.mainloop()
