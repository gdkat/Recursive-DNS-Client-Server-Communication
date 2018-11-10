#Client
import socket as mysoc
import pickle
import sys

file_name = sys.argv[1]

def client():
    #[ rs socket]
    try:
        ctors=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)

    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))

    #load file with hostname information to be resolved
    try:
        #fname = input("Enter file to read (Ex: foo.txt): ")
        # fname = "PROJ2-HNS.txt"
        fr = open(file_name, "r")
    except IOError as err:
        print('{} \n'.format("File Open Error ",err))
        print("Please ensure desired file to reverse exists in source folder and is named PROJI-HNS.txt")
        exit()

    #[determine hostname of RS server and port ]
    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
    # sa_sameas_myaddr = 'grep.cs.rutgers.edu'
    # Define the port on which you want to connect to the server
    port = 50008
    #[bind ctors socket to RS address, RS port]
    try:
        server_binding=(sa_sameas_myaddr,port)
        ctors.connect(server_binding)
    except mysoc.error as err:
        print('{} \n'.format("connect error "), err)
        exit()

    #check rs-server.py for information on how data
    #is being transferred and stored
    #write all resolved IP information to RESOLVED.txt
    with open("RESOLVED.txt", "w") as fw:
        for hostname in fr:
            ctors.send(hostname.strip().encode('utf-8'))
            dataFromRS=ctors.recv(100).decode('utf-8')
            if not dataFromRS: break
            fw.write(dataFromRS+'\n')
                
    # close everything
    fr.close()
    fw.close()
    ctors.close()
    exit()
client()