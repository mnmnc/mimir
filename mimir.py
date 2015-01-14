import psutil
import os
import platform

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
	show_disks()
	print()
	show_io_counters(True)
	print()
	show_net_counters(True)
	print()

	for con in psutil.net_connections(kind='inet'):
		print(con)
	#
	# print(psutil.users())
	# print(psutil.boot_time())
	# for proc in psutil.process_iter():
	# 	try:
	# 		pinfo = proc.as_dict(attrs=['pid', 'name'])
	# 		#pinfo = proc.as_dict()
	# 	except psutil.NoSuchProcess:
	# 		pass
	# 	else:
	# 		print(pinfo)
	# pass

if __name__ == "__main__":
	main()