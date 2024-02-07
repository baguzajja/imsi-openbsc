import paramiko
import subprocess
import re

def tail_and_grep(log_file, pattern):
    # Membuka proses tail -f dan grep pada file log
    command = ['tail', '-f', log_file]
    tail_process = subprocess.Popen(command, stdout=subprocess.PIPE)

    try:
        # Membaca output dari tail dan mencari pola yang cocok
        for line in iter(tail_process.stdout.readline, b''):
            decoded_line = line.decode('utf-8')
            match = re.search(pattern, decoded_line)
            if match:
                # Mengambil nilai IMSI dari hasil pencarian
                imsi_value = match.group(1)

                # Mengirim nilai IMSI ke server SSH
                send_to_ssh(imsi_value)
                print(imsi_value)

    except KeyboardInterrupt:
        # Menangani penekanan Ctrl+C
        print("Terminating tail process...")
        tail_process.terminate()
        tail_process.wait()

def send_to_ssh(new_imsi):
    # Menghubungkan ke server SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.1.112", 22, "local", "123123")

    try:
        # Mengirim perintah ke server SSH
        command = "echo 'subscriber create imsi %s' | nc localhost 4242" % new_imsi
        ssh.exec_command(command)

        # Mencetak output dan pesan kesalahan
        #print(command)
    finally:
        # Menutup koneksi SSH
        ssh.close()

if __name__ == "__main__":
    log_file_path = "/tmp/epc.log"
    #log_file_path = "/home/gz/docker_open5gs/log/mme.log"
    #grep_pattern = r"INFO: \[(\d+)\]"
    grep_pattern = r"IMSI: (\d+)"

    tail_and_grep(log_file_path, grep_pattern)
