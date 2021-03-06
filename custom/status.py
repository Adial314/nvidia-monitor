import os

class Status(object):
    __name__ = "Status"
    
    def __init__(self, txt_logfile, csv_logfile, debug=False):
        __func__ = "__init__"
        self.txt_logfile = txt_logfile
        self.csv_logfile = csv_logfile
        self.debug = debug
        self.hostname = self._get_hostname()
        self.day = self._parse_day_term(self._get_raw_status_data().split())
        self.month = self._parse_month_term(self._get_raw_status_data().split())
        self.year = self._parse_year_term(self._get_raw_status_data().split())
        self.temperature = self._parse_temperature_term(self._get_raw_status_data().split())
        self.time = self._parse_time_term(self._get_raw_status_data().split())
        self.fan = self._parse_fan_term(self._get_raw_status_data().split())
        self.utilization = self._parse_utilization_term(self._get_raw_status_data().split())
        self.memory_used = self._parse_memory_term(self._get_raw_status_data().split())[0]
        self.memory_max = self._parse_memory_term(self._get_raw_status_data().split())[1]
        self.power_used = self._parse_power_term(self._get_raw_status_data().split())[0]
        self.power_max = self._parse_power_term(self._get_raw_status_data().split())[1]
#         self._parse_raw_status_data(self._get_raw_status_data())
        
    def write_status_to_logfiles(self):
        self._write_status_to_csv_logfile()
        self._write_status_to_txt_logfile()
        return "Done."
        
    def display(self):
        print(f"----------- META -----------\n" \
              f"Hostname: {self.hostname}\n" \
              f"TXT Logfile: {self.txt_logfile}\n" \
              f"CSV Logfile: {self.csv_logfile}\n" \
              f"Debug: {self.debug}\n" \
              f"---------- STATUS ----------\n" \
              f"{self.year}-{self.month}-{self.day} @ {self.time}\n" \
              f"Temperature: {self.temperature} C\n" \
              f"Utilization: {self.utilization}%\n" \
              f"Fan: {self.fan}%\n" \
              f"Memory: {self.memory_used} / {self.memory_max} MiB\n" \
              f"Power {self.power_used} / {self.power_max} W\n"
             )
        
    def _get_hostname(self):
        __func__ = "_get_hostname"
        return os.popen("echo $HOSTNAME").read().replace("\n", "")
        
    def _get_raw_status_data(self):
        __func__ = "_get_raw_status_data"
        if not self.debug:
            return os.popen("nvidia-smi").read()
        else:
            # TEST SYSTEM DOES NOT HAVE NVIDIA GRAPHICS
            # RETURN THIS EXAMPLE STRING FOR TESTING
            # REMOVE THESE LINES FOR PRODUCTION
            # @seaborn
            return """
Thu Mar  4 13:32:39 2021       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 430.64       Driver Version: 430.64       CUDA Version: 10.1     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce RTX 208...  Off  | 00000000:09:00.0 Off |                  N/A |
|  0%   58C    P0     1W / 250W |      0MiB / 11019MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
"""
    
    def _parse_day_term(self, status_terms):
        __func__ = "_parse_day_term"
        day = status_terms[2]
        if len(day) == 1:
            day = "0" + day
        return day
    
    def _parse_month_term(self, status_terms):
        __func__ = "_parse_month_term"
        months_str = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",\
                      "Aug", "Sep", "Oct", "Nov", "Dec"]
        months_num = ["01", "02", "03", "04", "05", "06", "07", "08", \
                      "09", "10", "11", "12"]
        months_map = dict(zip(months_str, months_num))
        return months_map[status_terms[1]]
    
    def _parse_year_term(self, status_terms):
        __func__ = "_parse_year_term"
        return status_terms[4]
    
    def _parse_time_term(self, status_terms):
        __func__ = "_parse_time_term"
        return status_terms[3]
    
    def _string_int(self, string):
        try:
            _ = int(string)
            return True
        except:
            return False

    def _parse_temperature_term(self, status_terms):
        __func__ = "_parse_temperature_term"
        for status_term in status_terms:
            if status_term[-1] == "C" and self._string_int(status_term[:-1]):
                return status_term[:-1]
        return 1
    
    def _parse_memory_term(self, status_terms):
        __func__ = "_parse_memory_term"
        memory = list()
        for status_term in status_terms:
            if status_term[-3:] == "MiB":
                memory.append(status_term.split('MiB')[0])
        return memory
    
    def _parse_power_term(self, status_terms):
        __func__ = "_parse_power_term"
        power = list()
        for status_term in status_terms:
            if status_term[-1] == "W":
                power.append(status_term.split('W')[0])
        return power
    
    def _parse_fan_term(self, status_terms):
        __func__ = "_parse_fan_term"
        for i in range(len(status_terms)):
            status_term = status_terms[i]
            if status_term[-1] == "%":
                # If the last two terms are equal, then they must
                # be "||" characters defining the wall of the raw
                # status data. Ergo, we found the utilization %.
                if status_terms[i-1] == status_terms[i-2]:
                    fan = status_term.split("%")[0]
        return fan
    
    def _parse_utilization_term(self, status_terms):
        __func__ = "_parse_utilization_term"
        for term_i in range(len(status_terms)):
            status_term = status_terms[term_i]
            if status_term[-1] == "%":
                # If the last two terms are not equal, then we found
                # the utilization % in the middle of the raw status
                # data since it's not up against a "||" wall.
                if status_terms[term_i-1] != status_terms[term_i-2]:
                    utilization = status_term.split("%")[0]
        return utilization
    
#     def _parse_raw_status_data(self, raw_status_data):
#         __func__ = "_parse_raw_status_data"
#         status_terms = raw_status_data.split()
#         self.day = self._parse_day_term(status_terms)
#         self.month = self._parse_month_term(status_terms)
#         self.year = self._parse_year_term(status_terms)
#         self.temperature = self._parse_temperature_term(status_terms)
#         self.time = self._parse_time_term(status_terms)
#         self.fan = self._parse_fan_term(status_terms)
#         self.utilization = self._parse_utilization_term(status_terms)
#         self.memory_used = self._parse_memory_term(status_terms)[0]
#         self.memory_max = self._parse_memory_term(status_terms)[1]
#         self.power_used = self._parse_power_term(status_terms)[0]
#         self.power_max = self._parse_power_term(status_terms)[1]
        
    def _format_txt_log_entry(self):
        __func__ = "_format_txt_log_entry"
        return f"[{self.day}-{self.month}" \
               f"-{self.year} @ {self.time}] >" \
               f"  Temp: {self.temperature}C" \
               f"  Power: {self.power_used}/{self.power_max} W" \
               f"  Fan: {self.fan}%" \
               f"  Utilization: {self.utilization}%" \
               f"  Memory: {self.memory_used}/{self.memory_max} MiB\n"
    
    def _write_status_to_txt_logfile(self):
        __func__ = "_write_status_to_txt_logfile"
        try:
            with open(self.txt_logfile, mode="a") as file:
                entry = self._format_txt_log_entry()
                file.write(entry)
                file.close()
            return 0
        except FileNotFoundError:
            print(f"Error in {__name__}.{__func__}: {self.txt_logfile} not found.")
            return 1
        except KeyError:
            print(f"Error in {__name__}.{__func__}: KeyError when parsing data: {self.display()}")
            return 1
        
    def _format_csv_log_entry(self):
        __func__ = "_format_csv_log_entry"
        return f"{self.day}-{self.month}" \
               f"-{self.year},{self.time}," \
               f"{self.temperature},{self.power_used}," \
               f"{self.power_max},{self.fan}," \
               f"{self.utilization},{self.memory_used}," \
               f"{self.memory_max}\n"
        
    def _write_status_to_csv_logfile(self):
        __func__ = "_write_status_to_csv_logfile"
        file_empty = os.stat(self.csv_logfile).st_size == 0
        try:
            with open(self.csv_logfile, mode="a") as file:
                if file_empty:
                    file.write("Date,Time,Temperature,Power Used, Power Max,Fan," \
                               "Utilization,Memory Used,Memory Max\n")
                entry = self._format_csv_log_entry()
                file.write(entry)
                file.close()
            return 0
        except FileNotFoundError:
            print(f"Error in {__name__}.{__func__}: {self.csv_logfile} not found.")
            return 1
        except KeyError:
            print(f"Error in {__name__}.{__func__}: KeyError when parsing data: {self.display()}")
            return 1
