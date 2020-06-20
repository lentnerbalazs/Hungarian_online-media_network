import pickle
import os
import requests
import subprocess
import pandas as pd
import numpy as np

print("generate dataframe")
df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD"))

print("Writing out df")
df.to_pickle("random_test.pkl")

print("getting secret")
key = os.environ["RAJK_KEY"]

key_file_path = "temp_key"

print("writing secret")
with open(key_file_path, "w") as fp:
    fp.write(key)

print("first subprocess")
subprocess.call(["chmod", "600", key_file_path])


data_file_path = "random_test.pkl"
print("second subprocess")
subprocess.call(
    [
        "scp",
        "-P",
        "2222",
        "-i",
        key_file_path,
        data_file_path,
        "rajk@146.110.60.20:/var/www/rajk/cikkek",
    ]
)
