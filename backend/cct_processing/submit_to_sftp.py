
import pysftp

# change to prod
# set environment variables
password = "Pec7Vbnp7sBg"
username = "testVectorAiCCT"
hostname = "sftp-test.de.rhenus.com"
port = 22
path = "/in"

remote_file_path = f"{path}/VECTORAI_LUXURY_GOODSa66c2e3f-96df-4823-9bbc-41447cdffda8.json"

def upload_to_sftp(local_file, remote_file, hostname, port, username, password):
    # Connection options
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disable host key checking. Be careful with this in a production environment!

    try:
        # Connect and upload
        with pysftp.Connection(hostname, username=username, password=password, port=port, cnopts=cnopts) as sftp:
            sftp.put(local_file, remote_file)
        print("File uploaded successfully!")
    except Exception as e:
        import traceback
        print(traceback.format_exc())

# Example usage
upload_to_sftp('../tmp/VECTORAI_LUXURY_GOODSa66c2e3f-96df-4823-9bbc-41447cdffda8.json', remote_file_path, hostname, 22, username, password)
