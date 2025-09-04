from ftplib import FTP
from pathlib import Path

def run_ftp_demo():
    server = "ftp.dlptest.com"
    username = "dlpuser"
    password = "rNrKYTX9g7z3RgJRmxWuGHbeu"

    with FTP(server) as conn:
        conn.login(user=username, passwd=password)
        print(f"✅ Connected to {server}")

        print("\n📂 Files on server:")
        conn.dir()

        data_file = Path("ftp_upload.txt")
        data_file.write_text("Greetings from a Python FTP session")

        with data_file.open("rb") as fh:
            conn.storbinary("STOR ftp_upload.txt", fh)
        print("📤 Uploaded ftp_upload.txt")

        with open("ftp_download.txt", "wb") as out_fh:
            conn.retrbinary("RETR ftp_upload.txt", out_fh.write)
        print("📥 Downloaded ftp_download.txt")

if __name__ == "__main__":
    run_ftp_demo()
