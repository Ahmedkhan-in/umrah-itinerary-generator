import shutil
import os

# Delete the entire vectorstore directory
vectorstore_path = "vectorstore"
if os.path.exists(vectorstore_path):
    shutil.rmtree(vectorstore_path)
    print(f"Deleted entire vectorstore at {vectorstore_path}")

