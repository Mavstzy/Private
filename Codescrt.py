import os
import sys
from tkinter import Tk, Label, Entry, Button, Text, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter

# --- SETTINGS ---
APP_PASSWORD = "diary123"
PDF_PASSWORD = "Zero"
PDF_HINT_TEXT = "Hint: Empty"  # Used both inside the PDF and in filename

# ---- GUI Diary Window ----
def open_diary():
    diary = Tk()
    diary.title("🔒 My Personal Diary")
    diary.geometry("700x650")
    diary.config(bg="#d41515")

    Label(diary, text="📔 Write your diary entry below:", font=("Helvetica", 16, "bold"), bg="#d41515").pack(pady=15)

    text_box = Text(diary, wrap="word", font=("Helvetica", 12), padx=10, pady=10, relief="solid", bd=1)
    text_box.pack(padx=20, pady=(0, 10), expand=True, fill="both")

    Label(diary, text="💾 PDF File Name (optional):", font=("Helvetica", 12), bg="#d41515").pack()
    filename_entry = Entry(diary, font=("Helvetica", 12), width=40)
    filename_entry.pack(pady=5)

    def save_to_pdf():
        entry = text_box.get("1.0", "end").strip()
        file_name = filename_entry.get().strip()

        if not entry:
            messagebox.showwarning("Empty Entry", "Please write something in your diary.")
            return

        if not file_name:
            file_name = datetime.now().strftime("%Y-%m-%d_%H%M")

        # Clean filename and add hint
        file_name = file_name.replace(" ", "_")
        hint_tag = PDF_HINT_TEXT.replace("Hint:", "").strip().replace(" ", "")
        file_name_with_hint = f"{file_name}_hint-{hint_tag}"

        folder = "Punz___"
        os.makedirs(folder, exist_ok=True)
        temp_pdf = os.path.join(folder, f"{file_name_with_hint}_TEMP.pdf")
        final_pdf = os.path.join(folder, f"{file_name_with_hint}.pdf")

        # Step 1: Create unprotected PDF
        c = canvas.Canvas(temp_pdf, pagesize=A4)
        width, height = A4

        c.setFillColor(colors.darkblue)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, "📔 Personal Diary")

        now = datetime.now().strftime("%A, %B %d, %Y – %I:%M %p")
        c.setFillColor(colors.grey)
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"🗓️ {now}")
        c.setStrokeColor(colors.lightgrey)
        c.line(50, height - 90, width - 50, height - 90)

        c.setFillColor(colors.black)
        text = c.beginText(50, height - 120)
        text.setFont("Helvetica", 12)
        for line in entry.split('\n'):
            text.textLine(f" {line}" if line.strip() else "")
        c.drawText(text)

        # Hint in PDF (at bottom)
        c.setFillColor(colors.red)
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, 30, PDF_HINT_TEXT)

        c.showPage()
        c.save()

        # Step 2: Encrypt PDF
        reader = PdfReader(temp_pdf)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(user_password=PDF_PASSWORD)

        with open(final_pdf, "wb") as f:
            writer.write(f)

        os.remove(temp_pdf)

        messagebox.showinfo(
            "Saved",
            f"Diary saved to:\n{final_pdf}\n\nPassword Hint:\n{PDF_HINT_TEXT}"
        )
        text_box.delete("1.0", "end")
        filename_entry.delete(0, "end")

    Button(
        diary,
        text="💾 Save as Password-Protected PDF",
        font=("Helvetica", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        relief="flat",
        padx=10,
        pady=5,
        command=save_to_pdf
    ).pack(pady=15)

    diary.mainloop()

# ---- Login Prompt ----
def login():
    def check_password():
        if password_entry.get() == APP_PASSWORD:
            login_win.destroy()
            open_diary()
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")
            login_win.destroy()
            sys.exit()

    login_win = Tk()
    login_win.title("🔐 Diary Login")
    login_win.geometry("300x150")
    login_win.resizable(False, False)

    Label(login_win, text="🔐 Enter App Password:", font=("Helvetica", 12)).pack(pady=10)
    password_entry = Entry(login_win, show="*", font=("Helvetica", 12), width=25)
    password_entry.pack(pady=5)
    password_entry.focus()

    Button(
        login_win,
        text="Unlock Diary",
        font=("Helvetica", 11, "bold"),
        bg="#2196F3",
        fg="white",
        relief="flat",
        command=check_password
    ).pack(pady=10)

    login_win.mainloop()

# ---- Run the App ----
login()
