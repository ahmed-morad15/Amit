import tkinter as tk
import numpy as np

# ======================================
# 1️⃣ Helper Functions
# ======================================
def sigmoid(x):
    """Sigmoid activation function"""
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(output):
    """Derivative of sigmoid function with respect to its output"""
    return output * (1 - output)

# ======================================
# 2️⃣ Define Inputs and Weights
# ======================================
x = np.array([0.5, 0.1, -0.2])
target = 0.03
learnrate = 0.01

weights_input_hidden = np.array([
    [0.5, -0.6],
    [0.1, -0.2],
    [0.1, 0.7]
])

weights_hidden_output = np.array([0.1, -0.3])

# Save initial weights for comparison after update
wih_before = weights_input_hidden.copy()
who_before = weights_hidden_output.copy()

# ======================================
# 3️⃣ Function to perform a Backpropagation step and display results
# ======================================
def run_backprop():
    text_widget.delete("1.0", tk.END)  # Clear previous text
    
    # ---- Forward Pass ----
    hidden_input = np.dot(x, weights_input_hidden)
    hidden_output = sigmoid(hidden_input)
    output_input = np.dot(hidden_output, weights_hidden_output)
    output = sigmoid(output_input)
    
    text_widget.insert(tk.END, "🔹 FORWARD PASS\n")
    text_widget.insert(tk.END, f"Hidden layer input: {hidden_input}\n")
    text_widget.insert(tk.END, f"Hidden layer output: {hidden_output}\n")
    text_widget.insert(tk.END, f"Network output: {output:.5f}\n\n")
    
    # ---- Backward Pass ----
    error = target - output
    output_error_term = error * sigmoid_derivative(output)
    hidden_error = output_error_term * weights_hidden_output
    hidden_error_term = hidden_error * sigmoid_derivative(hidden_output)
    
    delta_w_hidden_output = learnrate * output_error_term * hidden_output
    delta_w_input_hidden = learnrate * np.outer(x, hidden_error_term)
    
    weights_hidden_output[:] += delta_w_hidden_output
    weights_input_hidden[:] += delta_w_input_hidden
    
    text_widget.insert(tk.END, "🔹 BACKWARD PASS RESULTS\n")
    text_widget.insert(tk.END, f"Target: {target}\n")
    text_widget.insert(tk.END, f"Output error: {error:.5f}\n")
    text_widget.insert(tk.END, f"Output error term (δ_output): {output_error_term}\n")
    text_widget.insert(tk.END, f"Hidden error term (δ_hidden): {hidden_error_term}\n\n")
    
    text_widget.insert(tk.END, "🔹 WEIGHT UPDATES\n")
    text_widget.insert(tk.END, "Change in Hidden→Output weights:\n")
    text_widget.insert(tk.END, f"{delta_w_hidden_output}\n\n")
    text_widget.insert(tk.END, "Change in Input→Hidden weights:\n")
    text_widget.insert(tk.END, f"{delta_w_input_hidden}\n\n")
    
    diff_input_hidden = weights_input_hidden - wih_before
    diff_hidden_output = weights_hidden_output - who_before
    
    text_widget.insert(tk.END, "🔹 COMPARISON BEFORE & AFTER\n")
    text_widget.insert(tk.END, "Input→Hidden Weights:\n")
    text_widget.insert(tk.END, f"Before:\n{wih_before}\nAfter:\n{weights_input_hidden}\nDifference:\n{diff_input_hidden}\n\n")
    text_widget.insert(tk.END, "Hidden→Output Weights:\n")
    text_widget.insert(tk.END, f"Before: {who_before}\nAfter: {weights_hidden_output}\nDifference: {diff_hidden_output}\n\n")
    
    text_widget.insert(tk.END, "🔹 RELATIVE CHANGE (percentage %):\n")
    text_widget.insert(tk.END, "Input→Hidden:\n")
    text_widget.insert(tk.END, f"{np.round((diff_input_hidden / wih_before) * 100, 4)}\n")
    text_widget.insert(tk.END, "Hidden→Output:\n")
    text_widget.insert(tk.END, f"{np.round((diff_hidden_output / who_before) * 100, 4)}\n\n")
    
    text_widget.insert(tk.END, "✅ Backpropagation step completed successfully.")

# ======================================
# 4️⃣ Setup Tkinter GUI
# ======================================
root = tk.Tk()
root.title("Backpropagation Step Visualization")

# Button to run backpropagation step
run_button = tk.Button(root, text="Run Backpropagation Step", command=run_backprop)
run_button.pack(pady=10)

# Text widget to display results
text_widget = tk.Text(root, width=80, height=30)
text_widget.pack(padx=10, pady=10)

root.mainloop()
