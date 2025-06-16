import subprocess


def test_help():
    # Run the command and capture the output
    result = subprocess.run(["marimushka", "--help"], capture_output=True, text=True, check=True)
    print("Command succeeded:")
    print(result.stdout)

def test_compile():
    # Run the command and capture the output
    result = subprocess.run(["marimushka", "compile", "--help"], capture_output=True, text=True, check=True)
    print("Command succeeded:")
    print(result.stdout)
