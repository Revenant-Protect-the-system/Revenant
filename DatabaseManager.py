import time
from scapy.all import *
from scapy.all import Ether, IP, TCP, UDP, ICMP

class Database_Class:
    def __init__(self):
        self.content = list()                   # Format: self.content = list<{"ip": insert_ip, "time": insert_time)> = [
                                                #   {"ip":"255.255.100.126", "time":1203003.2],
                                                #   ["ip":"100.255.234.200", "time":4343447.12],
                                                #   etc... ]
        self.filename = "Database.txt"
        #self.Open()
    
    ### <summary>
    ### Retrieves all the database's data from a ".txt" file(s)
    ### </summary>
    def Open(self):
        # 1. Opens the file containing the database's data
        file_content = None
        try:
            file = open(self.filename, 'r')
            file_content = file.read()
            file.close()
            print("Database Opened.")
        except FileNotFoundError:
            print("ERROR: file \"{}\" could not be found".format(self.filename))
            print("Open Database Failed.")
            return
        # 2. converts the raw data into a format suitable to store
        if len(file_content) < 10:
            print("the database currently is empty.")
            return
        file_content = file_content.split('\n')
        for item in file_content:
            item = item.split('|')
            self.AddRaw(
                i_ip = item[0],
                i_src = item[1],
                i_size = item[2],
                i_time = item[3] )
        print("Database loaded.")
    
    ### <summary>
    ### Saves the contents of the database in a ".txt" file(s) for later use
    ### </summary>
    def Save(self):
        # 1. Convert self.content into a format suitable for storing on a txt file
        file_content = ""
        for record in self.content:
            file_content += record["ip"]
            file_content += '|'
            file_content += str(record["src"])
            file_content += '|'
            file_content += str(record["size"])
            file_content += '|'
            file_content += str(record["time"])
            file_content += '\n'
        file_content = file_content[0:-1]    # remove the last useless '\n' in "file_content"
        # 2. Save it into the txt file
        try:
            file = open(self.filename, 'w')
            file.write(file_content)
            file.close()
            print("Database saved")
        except FileNotFoundError:
            print("ERROR: Database: Save(): file \"{}\" could not be found".format(self.filename))
            print("Database Save Failed")

    ### <summary>
    ### Iteration 2: A more direct "Add()" function for database
    ### </summary>
    def Add(self, packet):
        add = dict()
        # 1. Get packet IP
        if packet.haslayer(Ether):
            add["ip"] = packet[Ether].src
        elif packet.haslayer(IP):
            add["ip"] = packet[IP].src
        else:
            raise IOError
        # 2. Get packet source location
        if packet.haslayer(Ether):
            add["src"] = packet[Ether].src
        if packet.haslayer(IP):
            add["src"] = packet[IP].src
        if packet.haslayer(TCP):
            add["src"] = packet[TCP].sport
        if packet.haslayer(UDP):
            add["src"] = packet[UDP].sport
        if packet.haslayer(ICMP):               # NOTE: ICMPs are very popular for DDoS!!!
            add["src"] = packet[ICMP].type
        # 3. Get file size of the packet
        add["size"] = len(packet)
        # 4. Get time of the packet's arrival
        add["time"] = float(time.time())
        # INSERT the packet's info into "self.content" CHRONOLOGICALLY
        if len(self.content) == 0:
            self.content.append(add)
            return
        if add["time"] > self.content[-1]["time"]:          # Can we just add it to the end?
            self.content.append(add)
            return
        i = -1                                              # ELSE: look back through the list until you're no longer looking at the future
        while add["time"] > self.content[i]["time"]:
            i -= 1
        self.content.insert(i, add)

    ### <summary>
    ### enables directly adding data
    ### </summary>
    def AddRaw(self, i_ip, i_src, i_size, i_time):
        add = dict()
        add["ip"] = i_ip
        add["src"] = i_src
        add["size"] = i_size
        add["time"] = float(i_time)
        self.content.append(add)

    ### <summary>
    ### Prints out the contents of the database
    ### </summary>
    def Print(self):
        print(" Id  | IP                | source | size(b) | Time(s)")
        i = -1
        for record in self.content:
            i += 1
            print(f"{i:4} | {record["ip"]:16} | {record["src"]:6} | {record["size"]:7} | {record["time"]:19}")
        print("")

    ### <summary>
    ### A private function used to find the index of a particular ip/time inside "self.content".
    ### Used by "self.IndexIp(...)"
    ### </summary>
    ### <returns>
    ### Returns the index of the "input_value" inside "self.contents"
    ### Returns -1 if "input_value" isn't present
    ### </returns>
    def _Index(self, input_value, input_type, start_search=0):
        index = start_search
        while index < len(self.content):
            if self.content[index][input_type] == input_value:
                return index
            index += 1
        return -1
    
    ### <summary>
    ### identical to "self._Index(...)", however instead of returning the first instance of the 
    ### "input_value", it returns all instances of the "input value", in the specified 
    ### "output_type" format.
    ### </summary>
    ### <returns>
    ### returns all instances of "input_value" within the database.
    ### </returns>
    def _IndexAll(self, input_value, input_type, output_type):
        output_indexes = list()
        index = 0
        while index < len(self.content):
            index = self._Index(input_value, input_type, index)
            if index == -1:
                break
            output_indexes.append(index)
            index += 1
        if output_indexes == []:
            return []
        output = list()
        for i in output_indexes:
            add = self.content[i][output_type]
            output.append(add)
        return output
    

    def SelectIp(self, input_ip):
        return self._IndexAll(
            input_value = input_ip, 
            input_type = "ip", 
            output_type = "time")

    def SelectTime(self, input_time_select):
        # 1. Perform and input selection
        return self._IndexAll(
            input_value = input_time_select, 
            input_type = "time", 
            output_type = "ip")
    def SelectTimes(self, input_time_start=None, input_time_end=None):
        if input_time_start == input_time_end == None:
            raise ValueError("ERROR: no data was input")
        if input_time_start == None:
            input_time_start = 0                # If a start time isn't specified: set it to a 
                                                # value so low that every time inside the database 
                                                # should be within the start time.
        if input_time_end == None:
            input_time_end = time.time() * 2    # If an end time isn't specified: set it to a 
                                                # value so high that every time inside the database
                                                # should be within the end time.
        output = list()
        for record in self.content:
            if input_time_start != None:        # IF the time bellow the minimum value: skip
                if record["time"] < input_time_start:
                    continue
            if input_time_end != None:          # IF the time above the maximum value: skip
                if record["time"] > input_time_end:
                    continue
            output.append(record["ip"])
        return output
    ### <summary>
    ### Selects all ips between time "Start" and "end"
    ### </summary>
    def SelectTimes(self, start=None, end=None):
        if end == None:
            raise ValueError("ERROR: no data was input")
        if start == None:
            start = 0                # If a start time isn't specified: set it to a 
                                                # value so low that every time inside the database 
                                                # should be within the start time.
        if end == None:
            end = time.time() * 2    # If an end time isn't specified: set it to a 
                                                # value so high that every time inside the database
                                                # should be within the end time.
        outputEnd = len(self.content) - 1
        while outputEnd > 0 and end < self.content[outputEnd]["time"]:
            outputEnd -= 1
        outputStart = outputEnd
        while outputStart > 0 and start < self.content[outputStart]["time"]:
            outputStart -= 1
        print("Start time = ",start)
        print("end time = ",end)
        print("start[-1] =", self.content[outputStart-1])
        print("start[ 0] =", self.content[outputStart  ])
        try:
            print("start[ 1] =", self.content[outputStart+1])
        except Exception: pass
        print("end[-1] =", self.content[outputEnd-1])
        print("end[ 0] =", self.content[outputEnd  ])
        try:
            print("end[ 1] =", self.content[outputStart+1])
        except Exception: pass
        return self.content[outputStart+1 : outputEnd + 1]








if __name__ == '__main__':
    the_database = Database_Class()

    the_database.Print()

    the_database.Add("100.100.100.100", 10.0)
    the_database.Add("101.101.101.101", 10.1)
    the_database.Add("102.102.102.102")


    a = the_database.SelectIp("255.255.100.126")
    print("\nOBJ = 255.255.100.126")
    print(a)
    a = the_database.SelectIp("102.102.102.102")
    print("\nOBJ = 102.102.102.102")
    print(a)
    a = the_database.SelectIp("102.102.999.999")
    print("\nOBJ = 102.102.999.999")
    print(a)
    a = the_database.SelectTime(1739448892.115104)
    print("\nOBJ: time <i=0>")
    print(a)
    a = the_database.SelectTime(10.1)
    print("\nOBJ: time = 10.1")
    print(a)
    a = the_database.SelectTime(1739959592.7819402)
    print("\nOBJ: time <i=END>")
    print(a)
    a = the_database.SelectTimes(9, 11)
    print("\nOBJ: times: 9 < t < 11")
    print(a)
    a = the_database.SelectTimes(input_time_start = 11)
    print("\nOBJ: times: t > 11")
    print(a)
    a = the_database.SelectTimes(input_time_end = 11)
    print("\nOBJ: times: t < 11")
    print(a)

    the_database.Save()
