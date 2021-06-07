import signal
import time
from parameter_parser import ParameterParser
from dim_class import DIM
from mongo_db import Mongo

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

#----------------------------------------------------------------------
if __name__ == '__main__':
    #Connecting the single for graceful exit
    signal.signal(signal.SIGINT, signal_handler)
    interrupted = False

    validate = ParameterParser()

    # check user inputs and exit if input is incorrect
    if validate.has_invalid_input():
        print("Parameters missing. \n Exiting...")
        exit(-1)

    args = validate.get_args()
    dim = DIM(args.external_ip, args.live_port, args.apache_port, args.nginx_port ,args.min_wait_sec, args.max_wait_sec, args.iptables_rules)
    is_test_mode = args.test_flag

    if is_test_mode:
        mongo_test_db = Mongo()

    while not interrupted:

        rotation_start_time = time.time() #returns time in seconds
        dim.make_live()
        rotation_end_time = time.time()
        live_web_server_label = dim.get_live_web_server_label()

        wait_time = dim.get_wait_time()
        time.sleep(wait_time)
        end_server_time = time.time()
        server_up_time = end_server_time - rotation_end_time

        if is_test_mode:
            mongo_test_db.insert_mtd_data(live_web_server_label, wait_time, server_up_time, rotation_start_time, rotation_end_time)

        if interrupted:
            print("Exiting...")

    print("\n Done! \n Stopped running DARE rotation script.")