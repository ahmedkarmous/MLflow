with open("/home/getalp/karmouah/Bureau/TutoMLflow/tracking/mlruns/889925657107515489/1cd62bbb7a7a4e7a8ab6c72f5e447b2e/metrics/rmse") as file:
    first_line = file.readline()
    words = first_line.split()

    print(words[1])