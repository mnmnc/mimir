import psutil
import platform
import socket
import datetime
import json

def main():
	data = {
		'system_info': get_dict_system_info(),
		'cpu_usage': get_dict_cpu_usage(0.1,True),
		'cpu_count': get_dict_cpu_count(),
		'mem_usage': get_dict_mem_usage(),
		'swap_usage': get_dict_smem_usage(),
		'disks': get_dict_disks(),
		'io_counters': get_dict_io_counters(True),
		'net_counters': get_dict_net_counters(True),
		'net_connections': get_dict_net_connections(),
		'current_users': get_dict_current_users(),
		'boot_time': get_dict_boot_time(),
		'processes': get_dict_processes()
	}
	#print(json.dumps(data, sort_keys=True, indent=4))
	print(json.dumps(data))


def show_all():
	# show_system_info()
	# show_cpu_usage(0.5)
	# show_cpu_count()
	# show_mem_usage()
	# show_smem_usage()
	# show_disks()
	# show_io_counters(True)
	# show_net_counters(True)
	# show_net_connections()
	# show_current_users()
	# show_boot()
	# show_processes()
	pass

def show_boot():
	boot = psutil.boot_time()
	print("Last boot:", get_date_string(boot))

def show_disks():
	disks = psutil.disk_partitions(all=True)
	for disk in disks:
		print("dev:", disk.device)
		print("\tmount:", disk.mountpoint)
		print("\tfstype:", disk.fstype)
		print("\toptions:", disk.opts)

def show_cpu_usage(given_interval, separate=False):
	usage = psutil.cpu_percent(interval=given_interval, percpu=separate)

	if separate:
		for i in range(len(usage)):
			print("Core", i, "usage", usage[i])
	else:
		print("Total cpu usage:", usage)

def show_processes(running_as_root=False):
	for proc in psutil.process_iter():
		try:
			pinfo = proc.as_dict()
		except psutil.NoSuchProcess:
			pass
		else:
			print("Process name:", pinfo['name'])
			print("\tCreation time:", get_date_string(pinfo['create_time']))
			print("\tOpen files:", pinfo['open_files'])
			print("\tIO counter:", pinfo['io_counters'])
			print("\tCPU times:", pinfo['cpu_times'])
			print("\tThreads num:", pinfo['num_threads'])
			print("\tMemory usage:", pinfo['memory_percent'], "%")
			print("\tContext switches:", pinfo['num_ctx_switches'])
			print("\tWorking directory:", pinfo['cwd'])
			print("\tParent pid:", pinfo['ppid'])
			print("\tThreads:", pinfo['threads'])
			print("\tStatus:", pinfo['status'])
			print("\tExecutable:", pinfo['exe'])
			print("\tPriority:", pinfo['nice'])
			# TODO: FIX SO THAT THIS WILL BE CHECKED ONLY ON WINDOWS
			try:
				print("\tHandles:", pinfo['num_handles'])
			except:
				pass
			print("\tUsername:", pinfo['username'])
			print("\tCpu_affinity", pinfo['cpu_affinity'])
			print("\tPID:", pinfo['pid'])
			print("\tCPU usage:", pinfo['cpu_percent'], "%")
			print("\tIO priority:", pinfo['ionice'])
			print("\tMem info", pinfo['memory_info_ex'])
			print("\tCommand:", pinfo['cmdline'])
			print("\tMemory maps:", pinfo['memory_maps'])
			print("\tConnections:")
			show_net_connection_from_array(pinfo['connections'])

def show_cpu_count():
	count_hard = psutil.cpu_count(logical=False)
	count_logi = psutil.cpu_count(logical=True)
	print("CPU found (logical/physical):", count_logi, "/", count_hard)

def show_mem_usage():
	mem = psutil.virtual_memory()
	print("Mem total:\t", round((mem.total/1024)/1024,2), "MB")
	print("Mem free:\t", round((mem.available/1024)/1024, 2), "MB")
	print("Mem used:\t", mem.percent,"%")

def show_smem_usage():
	smem = psutil.swap_memory()
	print("Swap total:\t", round((smem.total/1024)/1024,2), "MB")
	print("Swap free:\t", round((smem.free/1024)/1024, 2), "MB")
	print("Swap used:\t", smem.percent,"%")

def show_io_counters(separate=False):
	disks = psutil.disk_io_counters(perdisk=separate)
	for disk in disks.keys():
		data = disks[disk]
		print("Drive:", disk)
		print(" Read count:\t", data.read_count)
		print(" \t bytes:\t\t", data.read_bytes)
		print(" \t time:\t\t", data.read_time)
		print(" Write count:\t", data.write_count)
		print(" \t bytes:\t\t", data.write_bytes)
		print(" \t time:\t\t", data.write_time)

def show_system_info():
	uname = platform.uname()
	print("Hostname:       ", uname.node)
	print("System family:  ", uname.system)
	print("System release: ", uname.release)
	print("System version: ", uname.version)
	print("Instruction set:", uname.machine)

def show_net_counters(separate=False):
	cons = psutil.net_io_counters(pernic=True)
	for con in cons.keys():
		data = cons[con]
		print("Connection:", con)
		print("Bytes sent:", data.bytes_sent)
		print("Bytes recv:", data.bytes_recv)
		print("Packets sent:", data.packets_sent)
		print("Packets recv:", data.packets_recv)
		print("Err in/out/dropin/dropout:", data.errin, data.errout, data.dropin, data.dropout)

def show_current_users():
	users = psutil.users()
	for user in users:
		print("User name:", user.name)
		print("User terminal:", user.terminal)
		print("Logged from host:", user.host)
		print("Logged on since:", get_date_string(user.started))

def get_dict_system_info():
	uname = platform.uname()
	return {
		'family':   uname.system,
		'hostname': uname.node,
		'release':  uname.release,
		'version':  uname.version,
		'i_set':    uname.machine
	}

def show_net_connections(mykind='all'):
	""" Acceptable values are: inet, inet4, inet6, tcp, tcp4, tcp6, udp, udp4, udp6, unix, all """
	cons = psutil.net_connections(kind=mykind)
	for con in cons:
		print("Local address:", con.laddr)
		print("\tRemote address:", con.raddr)
		if con.family == socket.AF_INET:
			print("\tFamily: AF_INET")
		elif con.family == socket.AF_INET6:
			print("\tFamily: AF_INET6")
		else:
			print("\tFamily: UNKNWN")
		if con.type == socket.SOCK_STREAM:
			print("\tType: SOCK_STREAM")
		elif con.type == socket.SOCK_DGRAM:
			print("\tType: SOCK_DGRAM")
		print("\tStatus:", con.status)
		print("\tPid:", con.pid)

def show_net_connection_from_array(arr):
	cons = arr
	for con in cons:
		print("\t\tLocal address:", con.laddr)
		print("\t\tRemote address:", con.raddr)
		if con.family == socket.AF_INET:
			print("\t\tFamily: AF_INET")
		elif con.family == socket.AF_INET6:
			print("\t\tFamily: AF_INET6")
		else:
			print("\t\tFamily: UNKNWN")

		if con.type == socket.SOCK_STREAM:
			print("\t\tType: SOCK_STREAM")
		elif con.type == socket.SOCK_DGRAM:
			print("\t\tType: SOCK_DGRAM")
		print("\t\tStatus:", con.status)



def get_dict_disks():
	disks = psutil.disk_partitions(all=True)
	result = []
	for disk in disks:
		ele = {
			'device': disk.device,
		    'mount': disk.mountpoint,
		    'fstype': disk.fstype,
		    'options': disk.fstype
		}
		result.append(ele)
	return result

def get_date_string(date):
	return datetime.datetime.utcfromtimestamp(
        int(date)
    ).strftime('%Y-%m-%d %H:%M:%S')

def get_dict_boot_time():
	return {'boot': psutil.boot_time()}

def get_dict_processes(running_as_root=False):
	result = []
	for proc in psutil.process_iter():
		try:
			pinfo = proc.as_dict()
		except psutil.NoSuchProcess:
			pass
		else:
			ele = {
				'name': pinfo['name'],
			    'creation_time': pinfo['create_time'],
			    'open_files': pinfo['open_files'],
			    'io_counter': pinfo['io_counters'],
			    'cpu_times': pinfo['cpu_times'],
			    'threads_num': pinfo['num_threads'],
			    'mem_usage': pinfo['memory_percent'],
			    'context_switches': pinfo['num_ctx_switches'],
			    'working_directory': pinfo['cwd'],
			    'parent_pid': pinfo['ppid'],
			    'threads': pinfo['threads'],
			    'status': pinfo['status'],
			    'executable': pinfo['exe'],
			    'priority': pinfo['nice'],
			    'username': pinfo['username'],
			    'cpu_affinity': pinfo['cpu_affinity'],
			    'pid': pinfo['pid'],
			    'cpu_usage': pinfo['cpu_percent'],
			    'io_priority': pinfo['ionice'],
			    'mem_info': pinfo['memory_maps'],
			    'connections': get_dict_net_connection_from_array(pinfo['connections'])
			}
			uname = platform.uname()
			if uname.system == "Windows":
				ele.update({'handles':pinfo['num_handles']})
			result.append(ele)
	return result

def get_dict_cpu_usage(given_interval, separate=False):
	usage = psutil.cpu_percent(interval=given_interval, percpu=separate)
	usage_list = []
	if separate:
		for i in range(len(usage)):
			usage_list.append(usage[i])
	else:
		usage_list.append(usage)
	return usage_list

def get_dict_cpu_count():
	return { 'physical': psutil.cpu_count(logical=False), 'logical': psutil.cpu_count(logical=True) }

def get_dict_mem_usage():
	mem = psutil.virtual_memory()
	return {
		'total': mem.total,
	    'free': mem.available,
	    'used_percent': mem.percent
	}

def get_dict_smem_usage():
	smem = psutil.swap_memory()
	return {
		'total': smem.total,
	    'free': smem.free,
	    'used': smem.percent
	}

def get_dict_io_counters(separate=False):
	disks = psutil.disk_io_counters(perdisk=separate)
	result = []
	for disk in disks.keys():
		data = disks[disk]
		ele = {
			'disk': disk,
		    'r_count': data.read_count,
		    'r_bytes': data.read_bytes,
		    'r_time': data.read_time,
		    'w_count': data.write_count,
		    'w_bytes': data.write_bytes,
		    'w_time': data.write_time,
		}
		result.append(ele)
	return result

def get_dict_net_counters(separate=False):
	cons = psutil.net_io_counters(pernic=True)
	result = []
	for con in cons.keys():
		data = cons[con]
		ele = {
			'nic': con,
			'bytes_sent':   data.bytes_sent,
			'bytes_recv':   data.bytes_recv,
			'packets_sent': data.packets_sent,
			'packets_recv': data.packets_recv,
			'err_in':   data.errin,
			'err_out':  data.errout,
			'drop_in':  data.dropin,
			'drop_out': data.dropout
		}
		result.append(ele)
	return result

def get_dict_current_users():
	results = []
	users = psutil.users()
	for user in users:
		ele = {
			'name': user.name,
		    'terminal': user.terminal,
		    'host': user.host,
		    'logon_time': user.started
		}
		results.append(ele)
	return results

def get_dict_net_connections(mykind='all'):
	cons = psutil.net_connections(kind=mykind)
	result = []
	for con in cons:
		ele = {
			'local_address': con.laddr,
		    'remote_address': con.raddr,
		    'status': con.status,
		    'pid': con.pid
		}
		if con.family == socket.AF_INET:
			ele.update({'family':'AF_INET'})
		elif con.family == socket.AF_INET6:
			ele.update({'family':'AF_INET6'})
		else:
			ele.update({'family':'UNKNWN'})
		if con.type == socket.SOCK_STREAM:
			ele.update({'type':'STREAM'})
		elif con.type == socket.SOCK_DGRAM:
			ele.update({'type':'DATAGRAM'})
		else:
			ele.update({'type':'UNKNWN'})
		result.append(ele)
	return result

def get_dict_net_connection_from_array(arr):
	cons = arr
	result = []
	for con in cons:
		ele = {
			'local_address': con.laddr,
		    'remote_address': con.raddr,
		    'status': con.status,
		}
		if con.family == socket.AF_INET:
			ele.update({'family':'AF_INET'})
		elif con.family == socket.AF_INET6:
			ele.update({'family':'AF_INET6'})
		else:
			ele.update({'family':'UNKNWN'})
		if con.type == socket.SOCK_STREAM:
			ele.update({'type':'STREAM'})
		elif con.type == socket.SOCK_DGRAM:
			ele.update({'type':'DATAGRAM'})
		else:
			ele.update({'type':'UNKNWN'})
		result.append(ele)
	return result







if __name__ == "__main__":
	main()

