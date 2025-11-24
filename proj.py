import tkinter as tk
from tkinter import messagebox

# ===================== Gaussian Elimination =====================

def gaussian_elimination(matrix):
    n = len(matrix)
    steps = []

    # Forward elimination
    for i in range(n):

        if matrix[i][i] == 0:
            steps.append(f"Pivot at row {i+1} is zero — searching for swap...")
            for k in range(i+1, n):
                if matrix[k][i] != 0:
                    matrix[i], matrix[k] = matrix[k], matrix[i]
                    steps.append(f"Swapped row {i+1} with row {k+1}")
                    break

        pivot = matrix[i][i]
        if pivot == 0:
            steps.append("No unique solution — pivot = 0.")
            return steps, None

        steps.append(f"Divide row {i+1} by pivot = {pivot}")
        for j in range(i, n+1):
            matrix[i][j] /= pivot

        for k in range(i+1, n):
            factor = matrix[k][i]
            steps.append(f"R{k+1} = R{k+1} - ({factor}) * R{i+1}")
            for j in range(i, n+1):
                matrix[k][j] -= factor * matrix[i][j]

    # Back-substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = matrix[i][n]
        for j in range(i+1, n):
            x[i] -= matrix[i][j] * x[j]

    steps.append(f"Final solution: {x}")
    return steps, x


# ===================== DISPLAY RESULT =====================

def display_result(steps, solution):
    text.delete("1.0", tk.END)

    for s in steps:
        text.insert(tk.END, s + "\n")

    text.insert(tk.END, "\n====================\n")

    if solution:
        text.insert(tk.END, "Solution:\n")
        for i, val in enumerate(solution):
            text.insert(tk.END, f"x{i+1} = {val}\n")
    else:
        text.insert(tk.END, "No unique solution.\n")


# ===================== SOLVE MATRIX =====================

def solve_matrix():
    try:
        rows = int(row_entry.get())
    except:
        messagebox.showerror("Error", "Enter a valid number")
        return

    matrix = []

    for i in range(rows):
        row_vals = []
        for j in range(rows + 1):
            try:
                val = float(entries[i][j].get())
            except:
                messagebox.showerror("Error", "Only numbers allowed")
                return
            row_vals.append(val)
        matrix.append(row_vals)

    steps, solution = gaussian_elimination(matrix)
    display_result(steps, solution)


# ===================== GENERATE MATRIX INPUT FIELDS =====================

def generate_matrix():
    try:
        rows = int(row_entry.get())
    except:
        messagebox.showerror("Error", "Enter a valid number")
        return

    global entries
    entries = []

    for widget in matrix_frame.winfo_children():
        widget.destroy()

    for i in range(rows):
        row_entries = []
        for j in range(rows + 1):
            entry = tk.Entry(
                matrix_frame,
                width=8,
                font=("Arial", 12),
                bg="#FFFFFF",
                fg="#2F3542"
            )
            entry.grid(row=i, column=j, padx=5, pady=6)
            row_entries.append(entry)

        entries.append(row_entries)


# ===================== GUI SETUP =====================

window = tk.Tk()
window.title("Gaussian Elimination Solver")
window.geometry("840x630")
window.configure(bg="#F5F7FA")

frame_top = tk.Frame(window, bg="#F5F7FA")
frame_top.pack(pady=8)

tk.Label(
    frame_top,
    text="Number of Equations:",
    font=("Arial", 12),
    bg="#F5F7FA",
    fg="#2F3542"
).grid(row=0, column=0, padx=5)

row_entry = tk.Entry(
    frame_top,
    width=5,
    font=("Arial", 12),
    bg="#FFFFFF",
    fg="#2F3542"
)
row_entry.grid(row=0, column=1, padx=5)

tk.Button(
    frame_top,
    text="Generate Matrix",
    command=generate_matrix,
    bg="#DAA04C",
    fg="white",
    font=("Arial", 11, "bold")
).grid(row=0, column=2, padx=10)

matrix_frame = tk.Frame(window, bg="#F5F7FA")
matrix_frame.pack(pady=8)

tk.Button(
    window,
    text="Solve",
    command=solve_matrix,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 13, "bold")
).pack(pady=12)

text = tk.Text(
    window,
    height=18,
    width=90,
    font=("Consolas", 11),
    bg="#E3E8F1",
    fg="#2F3542",
    insertbackground="black"
)
text.pack(pady=8)

window.mainloop()
