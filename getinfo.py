import psutil
import time
import sys

def get_cpu(vname,vnum):
    #print psutil.__version__
    with open('cpu_info'+vnum+'_'+vname, 'ab') as c:
        with open('mem_info'+vnum+'_'+vname,'ab') as m:
            with open ('io_info'+vnum+'_'+vname, 'ab') as i:
                t_end = time.time() + 5
                while time.time() < t_end:
                    c.writelines(str(psutil.cpu_times())+ '\n')
                    m.writelines(str(psutil.virtual_memory()) + '\n')
                    i.writelines(str(psutil.net_io_counters(pernic=True)) + '\n')
            
              


##============================================================================##
##--------------------------------- MAIN--------------------------------------##
##============================================================================##
if __name__ == "__main__":
    vname = sys.argv[1]
    vm_num = sys.argv[2]
    get_cpu(vname, vm_num)
