import csv
import random
import string

# Example name lists
first_names = [
    "Aahana","Kabir","Mira","Vivaan","Sahana","Ishaan","Tania","Reyansh","Esha",
    "Neil","Anvi","Dev","Diya","Raghav","Tanvi","Aarush","Kiara","Pranav","Myra","Arin"
]

last_names = [
    "Choudhary","Bhattacharya","Deshmukh","Ganguly","Joshi","Malik","Rao","Nayak",
    "Shukla","Menon","Trivedi","Mehra","Kapadia","Saxena","Bhardwaj","Chopra",
    "D'Souza","Iyer","Pandey","Chatterjee"
]

filename = "students_rolls_10char.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["roll_no", "name", "year", "course", "branch"])

    letters = list(string.ascii_uppercase[:10])  # A-J
    alphas = list(string.ascii_uppercase[:10])   # A-J for alphanumeric part

    for letter in letters:
        # Numeric series 01-99
        for i in range(1, 100):
            roll_no = f"25H71{letter}05{i:02}"
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            writer.writerow([roll_no, name, 1, "B.Tech", "AIDS"])

        # Alphanumeric series A0-A9, B0-B9, ..., J0
        for alpha in alphas:
            for digit in range(0, 10):
                roll_no = f"25H71{letter}05{alpha}{digit}"
                name = f"{random.choice(first_names)} {random.choice(last_names)}"
                writer.writerow([roll_no, name,1, "B.Tech", "AIDS"])

print(f"CSV generated: {filename}")
