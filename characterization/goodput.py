import subprocess

def genGoodput():
    testCommand = "java -jar a3_basic_tests_2019_v1.jar basic.txt"

    subprocess.run(testCommand, stdout=subprocess.PIPE, shell=True)

    logFile = open("A3.log", "r")

    for line in logFile:
        print(line)
