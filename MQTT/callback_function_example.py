def myfunction(client, userdata, flags, rc):
     logging.info("Connected flags"+str(flags)+"result code "\
     +str(rc)+"client1_id ")
     client.connected_flag=True
     
client.on_connect = myfunction
