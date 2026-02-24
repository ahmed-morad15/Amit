import tkinter as tk
from tkinter import ttk
import pandas as pd
import pickle

# ------------------- Load Model & Scaler -------------------
model = pickle.load(open("C:/DEPI/Amit/Src/ML/Boston-Housing-App/models/Boston_Housing_Best_model.pkl", "rb"))
scaler = pickle.load(open("C:/DEPI/Amit/Src/ML/Boston-Housing-App/models/scaler.pkl", "rb"))

# ------------------- Main Window -------------------
root = tk.Tk()
root.title("Boston Housing Price Prediction")
root.geometry("750x600")
root.configure(bg="#eef1f5")
root.resizable(False, False)

# ------------------- Style Configuration -------------------
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#ffffff", font=("Segoe UI", 10))
style.configure("TEntry", padding=5)
style.configure("TButton",
                font=("Segoe UI", 11, "bold"),
                padding=6)

# ------------------- Card Frame (Professional Look) -------------------
card = tk.Frame(root, bg="white", bd=0)
card.place(relx=0.5, rely=0.5, anchor="center", width=700, height=550)

# ------------------- Title -------------------
title = tk.Label(card,
                 text="🏠 Boston Housing Price Prediction",
                 font=("Segoe UI", 16, "bold"),
                 bg="white",
                 fg="#2E8B57")
title.pack(pady=15)

# ------------------- Input Frame -------------------
input_frame = tk.Frame(card, bg="white")
input_frame.pack(pady=10)

def create_input(label_text, default, row, col):
    label = ttk.Label(input_frame, text=label_text)
    label.grid(row=row, column=col*2, sticky="w", padx=10, pady=6)

    entry = ttk.Entry(input_frame, width=12)
    entry.insert(0, str(default))
    entry.grid(row=row, column=col*2+1, padx=5, pady=6)

    return entry

# ------------------- Inputs -------------------
crim = create_input("Crime Rate", 0.1, 0, 0)
zn = create_input("Residential Zone", 0.0, 1, 0)
indus = create_input("Industrial Area", 5.0, 2, 0)
nox = create_input("Nitric Oxide", 0.5, 3, 0)
rm = create_input("Average Rooms", 6.0, 4, 0)
age = create_input("Old Houses %", 50.0, 5, 0)

dis = create_input("Distance to Employment", 4.0, 0, 1)
rad = create_input("Accessibility Index", 5.0, 1, 1)
tax = create_input("Property Tax", 300.0, 2, 1)
ptratio = create_input("Pupil-Teacher Ratio", 18.0, 3, 1)
b = create_input("B Feature", 300.0, 4, 1)
lstat = create_input("Lower Status %", 12.0, 5, 1)

# Charles River Dropdown
ttk.Label(input_frame, text="Charles River").grid(row=6, column=0, sticky="w", padx=10, pady=6)
chas_var = tk.StringVar(value="0")
chas_menu = ttk.Combobox(input_frame, textvariable=chas_var, values=["0", "1"], width=10, state="readonly")
chas_menu.grid(row=6, column=1, pady=6)

# ------------------- Prediction Function -------------------
result_label = tk.Label(card, text="", font=("Segoe UI", 12, "bold"), bg="white")
result_label.pack(pady=10)

def predict_price():
    try:
        input_data = pd.DataFrame([{
            "crim": float(crim.get()),
            "zn": float(zn.get()),
            "indus": float(indus.get()),
            "chas": int(chas_var.get()),
            "nox": float(nox.get()),
            "rm": float(rm.get()),
            "age": float(age.get()),
            "dis": float(dis.get()),
            "rad": float(rad.get()),
            "tax": float(tax.get()),
            "ptratio": float(ptratio.get()),
            "b": float(b.get()),
            "lstat": float(lstat.get())
        }])

        scaled = scaler.transform(input_data)
        prediction = model.predict(scaled)[0] * 1000

        result_label.config(
            text=f"Predicted Price: ${prediction:,.2f}",
            fg="#2E8B57"
        )

    except Exception:
        result_label.config(
            text="⚠ Please enter valid numeric values.",
            fg="red"
        )

# ------------------- Predict Button -------------------
predict_btn = ttk.Button(card, text="Predict Price", command=predict_price)
predict_btn.pack(pady=15)

root.mainloop()