import yaml
from checkers import getout
from sshcheckers import ssh_checkout, upload_files, ssh_getout


with open('config.yaml') as f:
   data = yaml.safe_load(f)

class TestPositive:
    def save_log(self, starttime, name):
        with open(name, 'w') as f:
            f.write(getout(f"journalctl --since '{starttime}'"))

    
    def test_step1(self, start_time):
        res = []
        upload_files(data["ip"], data["user"], data["passwdssh"], f"{data['pkgname']}.deb",
                f"/home/{data['user']}/{data['pkgname']}.deb")
        res.append(ssh_checkout(data["ip"], data["user"], data["passwdssh"], 
                            f"echo '{data['passwdssh']}' | sudo -S dpkg -i /home/{data['user']}/{data['pkgname']}.deb",
                            "Настраивается пакет"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwdssh"], 
                            f"echo '{data['passwdssh']}' | sudo -S dpkg -s {data['pkgname']}",
                            "Status: install ok installed"))
        self.save_log(start_time, "log1.txt")
        assert all(res), "test1 FAIL"

    
    def test_step2(self, make_folders, clear_folders, make_files, start_time):
        res1 = ssh_checkout(data["ip"], data["user"], data["passwdssh"], f"cd {data['folder_in']};" 
                        f" 7z a {data['folder_out']}/arx2", "Everything is Ok")
        res2 = ssh_checkout(data["ip"], data["user"], data["passwdssh"], f"ls {data['folder_out']}", "arx2.7z")
        self.save_log(start_time, "log2.txt")
        assert res1 and res2, "test2 FAIL"


    def test_step3(self):
        res = []
        res.append(self.ssh_checkout(f"cd {data['folder_out']}; 7z e арх2.7z -o{data['folder_ext']}", "Everithing is ok"))
        res.append(self.ssh_checkout(f"ls {data['folder_out']};", "тестовый_файл.txt"))
        assert all(res), "test 3 FAIL"

    
    def test_step4(self, start_time):
        self.save_log(start_time, "log4.txt")
        assert ssh_checkout(data["ip"], data["user"], data["passwdssh"], f"cd {data['folder_out']}; "
                        f"7z t arx2.7z", "Everything is Ok"), "test4 FAIL"

    
    def test_step5(self, start_time):
        self.save_log(start_time, "log5.txt")
        assert ssh_checkout(data["ip"], data["user"], data["passwdssh"], f"cd {data['folder_in']}; "
                        f"7z u arx2.7z", "Everything is Ok"), "test5 FAIL"

    
    def test_step6(self, clear_folders, make_files, start_time):
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwdssh"], f"cd {data['folder_in']}; "
                            f"7z a {data['folder_out']}/arx2", "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwdssh"], f"cd {data['folder_out']}; "
                                f"7z l arx2.7z", item))
        self.save_log(start_time, "log6.txt")
        assert all(res), "test6 FAIL"

  
