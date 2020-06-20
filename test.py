import pickle
import os
import requests
import subprocess
import pandas as pd
import numpy as np
import dropbox

if __name__ == "__main__":
    df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD"))

    computer_path = "random_test.pkl"
    df.to_pickle(computer_path)

    print("getting secret")
    dropbox_access_token = os.environ["DROPBOX_TOKEN"]
    dropbox_path= "/random_test.pkl"

    client = dropbox.Dropbox(dropbox_access_token)
    print("[SUCCESS] dropbox account linked")

    client.files_upload(open(computer_path, "rb").read(), dropbox_path)
    print("[UPLOADED] {}".format(computer_path))
