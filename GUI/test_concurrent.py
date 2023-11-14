import subprocess
#run both main and watertrackerapp concurrently

def run_concurrently():
    # Start main code
    proc1 = subprocess.Popen(["python", "main.py"])

    # Start watertrackerapp 2
    proc2 = subprocess.Popen(["python", "kivy_trial.py"])


    proc1.wait()
    proc2.wait()


if __name__ == "__main__":
    # Run both codes concurrently when this script is executed
    run_concurrently()
