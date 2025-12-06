import tkinter as tk
from tkinter import messagebox

# ===================== GAUSSIAN ELIMINATION =====================

def gaussian_elimination(matrix):
    n = len(matrix)
    steps = []

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

    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = matrix[i][n]
        for j in range(i+1, n):
            x[i] -= matrix[i][j] * x[j]

    steps.append(f"Final solution: {x}")
    return steps, x


# ===================== MATRIX TRANSPOSE =====================

def transpose_matrix(A):
    return list(map(list, zip(*A)))  


# ===================== MATRIX INVERSE (Gauss-Jordan) =====================

def inverse_matrix(A):
    n = len(A)

    # إنشاء مصفوفة الهوية Identity
    I = [[float(i == j) for j in range(n)] for i in range(n)]

    # دمج A مع I
    aug = [A[i] + I[i] for i in range(n)]

    # تطبيق Gauss–Jordan
    for i in range(n):

        pivot = aug[i][i]
        if pivot == 0:
            return None  # غير قابلة للعكس

        for j in range(2*n):
            aug[i][j] /= pivot

        for r in range(n):
            if r != i:
                factor = aug[r][i]
                for j in range(2*n):
                    aug[r][j] -= factor * aug[i][j]

    # استخراج المصفوفة العكسية
    inverse = [row[n:] for row in aug]
    return inverse


# ===================== DISPLAY RESULT =====================

def display_matrix(title, M):
    text.delete("1.0", tk.END)
    text.insert(tk.END, title + "\n\n")

    for row in M:
        text.insert(tk.END, "   " + "   ".join(f"{v:.4f}" for v in row) + "\n")


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


# ===================== READ MATRIX FROM UI =====================

def read_square_matrix():
    try:
        n = int(row_entry.get())
    except:
        messagebox.showerror("Error", "Enter a valid number")
        return None

    M = []
    for i in range(n):
        row = []
        for j in range(n):
            try:
                val = float(entries[i][j].get())
            except:
                messagebox.showerror("Error", "Only numbers allowed")
                return None
            row.append(val)
        M.append(row)
    return M


# ===================== BUTTON FUNCTIONS =====================

def solve_matrix():
    rows = int(row_entry.get())
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


def calc_transpose():
    A = read_square_matrix()
    if A is None:
        return
    T = transpose_matrix(A)
    display_matrix("Transpose Matrix:", T)


def calc_inverse():
    A = read_square_matrix()
    if A is None:
        return

    inv = inverse_matrix(A)
    if inv is None:
        messagebox.showerror("Error", "Matrix is NOT invertible.")
        return

    display_matrix("Inverse Matrix:", inv)


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
            entry = tk.Entry(matrix_frame, width=8, font=("Arial", 12),
                             bg="#FFFFFF", fg="#2F3542")
            entry.grid(row=i, column=j, padx=5, pady=6)
            row_entries.append(entry)
        entries.append(row_entries)


# ===================== GUI SETUP =====================

window = tk.Tk()
window.title("Gaussian Elimination Solver")
window.geometry("900x700")
window.configure(bg="#F5F7FA")

frame_top = tk.Frame(window, bg="#F5F7FA")
frame_top.pack(pady=8)

tk.Label(frame_top, text="Number of Equations:",
         font=("Arial", 12), bg="#F5F7FA", fg="#2F3542").grid(row=0, column=0, padx=5)

row_entry = tk.Entry(frame_top, width=5, font=("Arial", 12),
                     bg="#FFFFFF", fg="#2F3542")
row_entry.grid(row=0, column=1, padx=5)

tk.Button(frame_top, text="Generate Matrix", command=generate_matrix,
          bg="#DAA04C", fg="white", font=("Arial", 11, "bold")).grid(row=0, column=2, padx=10)

matrix_frame = tk.Frame(window, bg="#F5F7FA")
matrix_frame.pack(pady=8)

# Buttons
button_frame = tk.Frame(window, bg="#F5F7FA")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Solve", command=solve_matrix,
          width=12, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10)

tk.Button(button_frame, text="Transpose", command=calc_transpose,
          width=12, bg="#3498DB", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10)

tk.Button(button_frame, text="Inverse", command=calc_inverse,
          width=12, bg="#9B59B6", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10)

text = tk.Text(window, height=20, width=100, font=("Consolas", 11),
               bg="#E3E8F1", fg="#2F3542", insertbackground="black")
text.pack(pady=8)

window.mainloop()
