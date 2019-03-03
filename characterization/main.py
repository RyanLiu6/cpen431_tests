from ping import pingServers
from goodput import genGoodput

def main():
    print("Starting Characterization Process ...")
    print("Pinging servers ...")
    pingServers("servers.txt", "results.txt")
    print("Pinging servers complete.")

    print("Generating Goodput ...")
    genGoodput()
    print("Generating Goodput complete ...")

if __name__ == "__main__":
    main()
