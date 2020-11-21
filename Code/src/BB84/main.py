import subprocess as sp
from communication import run_simul

tmp = sp.call('clear', shell=True)

if __name__ == "__main__":
    print("Alice wants to confirm that her communication channel with Bob is secure.\n")
    choice = input("Do you want Eve to eavesdrop? (y/n): ") or "n"
    if choice.lower() == "y":
        run_simul(True)
    else:
        run_simul(False)