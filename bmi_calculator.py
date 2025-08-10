import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Step 1: Connect to SQLite database
conn = sqlite3.connect("bmi_data.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    date TEXT,
    weight REAL,
    height REAL,
    bmi REAL
)''')
conn.commit()

# Step 2: BMI calculation function
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Step 3: Submit and store data
def submit_data():
    username = entry_user.get()
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")
        return

    bmi = calculate_bmi(weight, height)
    category = get_bmi_category(bmi)
    label_result.config(text=f"BMI: {bmi} ({category})")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO bmi_records (username, date, weight, height, bmi) VALUES (?, ?, ?, ?, ?)",
              (username, now, weight, height, bmi))
    conn.commit()

# Step 4: View BMI history in graph
def view_history():
    username = entry_user.get()
    c.execute("SELECT date, bmi FROM bmi_records WHERE username = ? ORDER BY date", (username,))
    data = c.fetchall()

    if not data:
        messagebox.showinfo("No Data", "No records found.")
        return

    dates = [row[0] for row in data]
    bmis = [row[1] for row in data]

    # Plot the BMI trend
    plt.figure(figsize=(10, 5))
    plt.plot(dates, bmis, marker='o', linestyle='-', color='blue')
    plt.xticks(rotation=45, ha='right')
    plt.title(f"BMI Trend for {username}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# Step 5: GUI setup with Tkinter
root = tk.Tk()
root.title("BMI Calculator with Trend Analysis")
root.geometry("400x400")

tk.Label(root, text="Username:").pack()
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Weight (kg):").pack()
entry_weight = tk.Entry(root)
entry_weight.pack()

tk.Label(root, text="Height (cm):").pack()
entry_height = tk.Entry(root)
entry_height.pack()

tk.Button(root, text="Calculate & Save BMI", command=submit_data).pack(pady=10)
label_result = tk.Label(root, text="BMI: --")
label_result.pack()

tk.Button(root, text="View BMI History Graph", command=view_history).pack(pady=20)

root.mainloop()