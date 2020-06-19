import dill

with open("Players.dat", "wb") as f:
    dill.dump({}, f)