import psutil
import os
import platform
import socket
import datetime

def show_system_info():
	uname = platform.uname()
	print("Hostname:       ", uname.node)
	print("System family:  ", uname.system)
	print("System release: ", uname.release)
	print("System version: ", uname.version)
	print("Instruction set:", uname.machine)

def show_cpu_usage(given_interval, separate=False):
	usage = psutil.cpu_percent(interval=given_interval, percpu=separate)

	if separate:
		for i in range(len(usage)):
			print("Core", i, "usage", usage[i])
	else:
		print("Total cpu usage:", usage)

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

def show_disks():
	disks = psutil.disk_partitions(all=True)
	for disk in disks:
		print("dev:", disk.device)
		print("\tmount:", disk.mountpoint)
		print("\tfstype:", disk.fstype)
		print("\toptions:", disk.opts)

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

def show_current_users():
	users = psutil.users()
	for user in users:
		print("User name:", user.name)
		print("User terminal:", user.terminal)
		print("Logged from host:", user.host)
		print("Logged on since:", get_date_string(user.started))

def show_boot():
	boot = psutil.boot_time()
	print("Last boot:", get_date_string(boot))

def get_date_string(date):
	return datetime.datetime.utcfromtimestamp(
        int(date)
    ).strftime('%Y-%m-%d %H:%M:%S')

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
			# for con in pinfo['connections']:
			# 	print("\t\t",con)

def main():
	show_system_info()
	print()
	show_cpu_usage(0.5)
	print()
	show_cpu_count()
	print()
	show_mem_usage()
	print()
	show_smem_usage()
	print()
	# show_disks()
	# print()
	# show_io_counters(True)
	# print()
	# show_net_counters(True)
	# print()
	# show_net_connections()
	# print()
	show_current_users()
	# print()
	show_boot()
	# print()
	# show_processes()



	# pass

if __name__ == "__main__":
	main()