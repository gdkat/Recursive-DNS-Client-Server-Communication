#TS server
import socket as mysoc
import pickle
import sys

file_name = sys.argv[1]

def ts():
    try:
        tscomsd = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)

    except mysoc.error as err:
        print('[TS]: {}\n'.format("socket open error ", err))

    #load table from server
    try:
        #fname = input("Enter file to read (Ex: foo.txt): ")
        # fname = "PROJ2-DNSCOM.txt"
        fr = open(file_name, "r")
    except IOError as err:
        print('{} \n'.format("File Open Error ",err))
        print("Please ensure desired file to reverse exists in source folder")
        exit()

    TS_table = {}
    for line in fr:
        entry = line.split(' ')
        formatted_entry = []
        for item in entry:
            if item != ' ' and item != '':
                if item.endswith('\n'):
                    item = item[:-1]
                formatted_entry.append(item)

        if formatted_entry[0] not in TS_table:
            TS_table[formatted_entry[0]] = {}
        TS_table[formatted_entry[0]]['ip'] = formatted_entry[1]
        TS_table[formatted_entry[0]]['flag'] = formatted_entry[2]

    #determine local hostname, IP
    #address , select a port number
    server_binding=('',5678)
    tscomsd.bind(server_binding)
    tscomsd.listen(1)
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Attempting to connect to client.\n[S]: Server IP address is  ",localhost_ip)
    ctsd,addr=tscomsd.accept()
    print ("[S]: Got a connection request from a client at", addr)

    while True:
        hnstring=ctsd.recv(100).decode('utf-8')
        if not hnstring: break
        entry = ''
        if hnstring in TS_table:
            entry = hnstring + ' ' + TS_table[hnstring]['ip'] + ' ' + TS_table[hnstring]['flag']
        else:
            entry = hnstring + " - Error:HOST NOT FOUND"
        ctsd.send(entry.encode('utf-8'))

    # close everything
    fr.close()
    tscomsd.close()

ts()