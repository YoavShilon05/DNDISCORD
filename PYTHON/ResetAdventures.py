import dill

with open("Adventures.dat", "wb") as f:
    dill.dump([], f)