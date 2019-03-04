from ping import pingServers
from setupServers import setupServers
from goodput import genGoodput
from goodput import runTests
from compileResults import compileResults

def main():
    print("Starting Characterization Process ...")
    print("Setting up servers ...")
    setupServers("servers.txt", '5000')
    print("Setting up servers complete.")
    
    print("Pinging servers ...")
    pingServers("servers.txt", "pings.txt")
    print("Pinging servers complete.")
    
    print("Generating Goodput ...")
    runTests("servers.txt", "goodput.txt", '5000')
    print("Generating Goodput complete ...")
    
    print("Compiling Results ...")
    compileResults("pings.txt", "goodput.txt", "results.txt")
    print("Compiling Results complete ...")

if __name__ == "__main__":
    main()
