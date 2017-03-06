import os
from django.conf import settings
from collectd_rest.models import Graph, GraphGroup
from .models import Device, GraphManager

if hasattr(settings, 'COLLECTD_RRD_DIR'):
	RRD_DIR = settings.COLLECTD_RRD_DIR
else:
	RRD_DIR = "/var/lib/collectd/rrd/"

def make_cpu_graph(cpurrd, group, core):
	cpu_args = [
		'-s end-1h',
	#	'-e 1303382682',
		'-w 600' ,
		'-h 240' ,
		'-t cpu' ,
		'-v Percent' ,
		'-E' ,
		'-r' ,
		'-u 100' ,
		'DEF:idle_min='+cpurrd+'/cpu-idle.rrd:value:MIN' ,
		'DEF:idle_avg='+cpurrd+'/cpu-idle.rrd:value:AVERAGE' ,
		'DEF:idle_max='+cpurrd+'/cpu-idle.rrd:value:MAX' ,
		'CDEF:idle_nnl=idle_avg,UN,0,idle_avg,IF' ,
		'DEF:wait_min='+cpurrd+'/cpu-wait.rrd:value:MIN' ,
		'DEF:wait_avg='+cpurrd+'/cpu-wait.rrd:value:AVERAGE' ,
		'DEF:wait_max='+cpurrd+'/cpu-wait.rrd:value:MAX' ,
		'CDEF:wait_nnl=wait_avg,UN,0,wait_avg,IF' ,
		'DEF:nice_min='+cpurrd+'/cpu-nice.rrd:value:MIN' ,
		'DEF:nice_avg='+cpurrd+'/cpu-nice.rrd:value:AVERAGE' ,
		'DEF:nice_max='+cpurrd+'/cpu-nice.rrd:value:MAX' ,
		'CDEF:nice_nnl=nice_avg,UN,0,nice_avg,IF' ,
		'DEF:user_min='+cpurrd+'/cpu-user.rrd:value:MIN' ,
		'DEF:user_avg='+cpurrd+'/cpu-user.rrd:value:AVERAGE' ,
		'DEF:user_max='+cpurrd+'/cpu-user.rrd:value:MAX' ,
		'CDEF:user_nnl=user_avg,UN,0,user_avg,IF' ,
		'DEF:system_min='+cpurrd+'/cpu-system.rrd:value:MIN' ,
		'DEF:system_avg='+cpurrd+'/cpu-system.rrd:value:AVERAGE' ,
		'DEF:system_max='+cpurrd+'/cpu-system.rrd:value:MAX' ,
		'CDEF:system_nnl=system_avg,UN,0,system_avg,IF' ,
		'DEF:softirq_min='+cpurrd+'/cpu-softirq.rrd:value:MIN' ,
		'DEF:softirq_avg='+cpurrd+'/cpu-softirq.rrd:value:AVERAGE' ,
		'DEF:softirq_max='+cpurrd+'/cpu-softirq.rrd:value:MAX' ,
		'CDEF:softirq_nnl=softirq_avg,UN,0,softirq_avg,IF' ,
		'DEF:interrupt_min='+cpurrd+'/cpu-interrupt.rrd:value:MIN' ,
		'DEF:interrupt_avg='+cpurrd+'/cpu-interrupt.rrd:value:AVERAGE' ,
		'DEF:interrupt_max='+cpurrd+'/cpu-interrupt.rrd:value:MAX' ,
		'CDEF:interrupt_nnl=interrupt_avg,UN,0,interrupt_avg,IF' ,
		'DEF:steal_min='+cpurrd+'/cpu-steal.rrd:value:MIN' ,
		'DEF:steal_avg='+cpurrd+'/cpu-steal.rrd:value:AVERAGE' ,
		'DEF:steal_max='+cpurrd+'/cpu-steal.rrd:value:MAX' ,
		'CDEF:steal_nnl=steal_avg,UN,0,steal_avg,IF' ,
		'CDEF:steal_stk=steal_nnl' ,
		'CDEF:interrupt_stk=interrupt_nnl,steal_stk,+' ,
		'CDEF:softirq_stk=softirq_nnl,interrupt_stk,+' ,
		'CDEF:system_stk=system_nnl,softirq_stk,+' ,
		'CDEF:user_stk=user_nnl,system_stk,+' ,
		'CDEF:nice_stk=nice_nnl,user_stk,+' ,
		'CDEF:wait_stk=wait_nnl,nice_stk,+' ,
		'CDEF:idle_stk=idle_nnl,wait_stk,+' ,
		'AREA:idle_stk#CEFFEA' ,
		'"LINE1:idle_stk#CEFFEA:idle     "' ,
		'"GPRINT:idle_min:MIN:%6.1lf Min,"' ,
		'"GPRINT:idle_avg:AVERAGE:%6.1lf Avg,"' ,
		'"GPRINT:idle_max:MAX:%6.1lf Max,"' ,
		'"GPRINT:idle_avg:LAST:%6.1lf Last\\l"' ,
		'AREA:wait_stk#ffebbf' ,
		'"LINE1:wait_stk#ffb000:wait     "' ,
		'"GPRINT:wait_min:MIN:%6.1lf Min,"' ,
		'"GPRINT:wait_avg:AVERAGE:%6.1lf Avg,"' ,
		'"GPRINT:wait_max:MAX:%6.1lf Max,"' ,
		'"GPRINT:wait_avg:LAST:%6.1lf Last\\l"' ,
		'AREA:nice_stk#bff7bf' ,
		'"LINE1:nice_stk#00e000:nice     "' ,
		'"GPRINT:nice_min:MIN:%6.1lf Min,"' ,
		'"GPRINT:nice_avg:AVERAGE:%6.1lf Avg,"' ,
		'"GPRINT:nice_max:MAX:%6.1lf Max,"' ,
		'"GPRINT:nice_avg:LAST:%6.1lf Last\\l"' ,
		'AREA:user_stk#bfbfff' ,
		'"LINE1:user_stk#0000ff:user     "' ,
		'"GPRINT:user_min:MIN:%6.1lf Min,"' ,
		'"GPRINT:user_avg:AVERAGE:%6.1lf Avg,"' ,
		'"GPRINT:user_max:MAX:%6.1lf Max,"' ,
		'"GPRINT:user_avg:LAST:%6.1lf Last\\l"' ,
		'AREA:system_stk#ffbfbf' ,
		'"LINE1:system_stk#ff0000:system   "' ,
		'"GPRINT:system_min:MIN:%6.1lf Min,"' ,
		'"GPRINT:system_avg:AVERAGE:%6.1lf Avg,"' ,
		'"GPRINT:system_max:MAX:%6.1lf Max,"' ,
		'"GPRINT:system_avg:LAST:%6.1lf Last\\l"' ,
		'AREA:softirq_stk#ffbfff' ,
		'"LINE1:softirq_stk#ff00ff:softirq  "' ,
		'"GPRINT:softirq_min:MIN:%6.1lf Min,"' ,
		'"GPRINT:softirq_avg:AVERAGE:%6.1lf Avg,"' ,
		'"GPRINT:softirq_max:MAX:%6.1lf Max,"' ,
		'"GPRINT:softirq_avg:LAST:%6.1lf Last\\l"' ,
		'AREA:interrupt_stk#e7bfe7' ,
		'"LINE1:interrupt_stk#a000a0:interrupt"' ,
		'"GPRINT:interrupt_min:MIN:%6.1lf Min,"' ,
		'"GPRINT:interrupt_avg:AVERAGE:%6.1lf Avg,"' ,
		'"GPRINT:interrupt_max:MAX:%6.1lf Max,"' ,
		'"GPRINT:interrupt_avg:LAST:%6.1lf Last\\l"' ,
		'AREA:steal_stk#bfbfbf' ,
		'"LINE1:steal_stk#000000:steal    "' ,
		'"GPRINT:steal_min:MIN:%6.1lf Min,"' ,
		'"GPRINT:steal_avg:AVERAGE:%6.1lf Avg,"' ,
		'"GPRINT:steal_max:MAX:%6.1lf Max,"' ,
		'"GPRINT:steal_avg:LAST:%6.1lf Last\\l"'
	]
	cpu_line_args = " ".join(cpu_args)
	graph = Graph(name="cpu-"+core, group=group)
	graph.title="Cpu core "+core
	graph.command=cpu_line_args
	graph.priority=0
	graph.save()

def make_memory_graph(memoryrrd, group):
	memory_args = [
		'-s end-1h',
	#	'-e 1303382682',
		'-w 600',
		'-h 240',
		'-t memory' ,
		'-E' ,
		'-b 1024' ,
		'-v Bytes' ,
		'-l 0',
		'-M',
		'DEF:free_min='+memoryrrd+'/memory-free.rrd:value:MIN' ,
		'DEF:free_avg='+memoryrrd+'/memory-free.rrd:value:AVERAGE' ,
		'DEF:free_max='+memoryrrd+'/memory-free.rrd:value:MAX' ,
		'CDEF:free_nnl=free_avg,UN,0,free_avg,IF' ,
		'DEF:cached_min='+memoryrrd+'/memory-cached.rrd:value:MIN' ,
		'DEF:cached_avg='+memoryrrd+'/memory-cached.rrd:value:AVERAGE' ,
		'DEF:cached_max='+memoryrrd+'/memory-cached.rrd:value:MAX' ,
		'CDEF:cached_nnl=cached_avg,UN,0,cached_avg,IF' ,
		'DEF:buffered_min='+memoryrrd+'/memory-buffered.rrd:value:MIN' ,
		'DEF:buffered_avg='+memoryrrd+'/memory-buffered.rrd:value:AVERAGE' ,
		'DEF:buffered_max='+memoryrrd+'/memory-buffered.rrd:value:MAX' ,
		'CDEF:buffered_nnl=buffered_avg,UN,0,buffered_avg,IF' ,
		'DEF:used_min='+memoryrrd+'/memory-used.rrd:value:MIN' ,
		'DEF:used_avg='+memoryrrd+'/memory-used.rrd:value:AVERAGE' ,
		'DEF:used_max='+memoryrrd+'/memory-used.rrd:value:MAX' ,
		'CDEF:used_nnl=used_avg,UN,0,used_avg,IF' ,
		'CDEF:used_stk=used_nnl' ,
		'CDEF:buffered_stk=buffered_nnl,used_stk,+' ,
		'CDEF:cached_stk=cached_nnl,buffered_stk,+' ,
		'CDEF:free_stk=free_nnl,cached_stk,+' ,
		'AREA:free_stk#bff7bf' ,
		'"LINE1:free_stk#00e000:free    "' ,
		'"GPRINT:free_min:MIN:%5.1lf%s Min,"' ,
		'"GPRINT:free_avg:AVERAGE:%5.1lf%s Avg,"' ,
		'"GPRINT:free_max:MAX:%5.1lf%s Max,"' ,
		'"GPRINT:free_avg:LAST:%5.1lf%s Last\\l"' ,
		'AREA:cached_stk#bfbfff' ,
		'"LINE1:cached_stk#0000ff:cached  "' ,
		'"GPRINT:cached_min:MIN:%5.1lf%s Min,"' ,
		'"GPRINT:cached_avg:AVERAGE:%5.1lf%s Avg,"' ,
		'"GPRINT:cached_max:MAX:%5.1lf%s Max,"' ,
		'"GPRINT:cached_avg:LAST:%5.1lf%s Last\\l"' ,
		'AREA:buffered_stk#ffebbf' ,
		'"LINE1:buffered_stk#ffb000:buffered"' ,
		'"GPRINT:buffered_min:MIN:%5.1lf%s Min,"' ,
		'"GPRINT:buffered_avg:AVERAGE:%5.1lf%s Avg,"' ,
		'"GPRINT:buffered_max:MAX:%5.1lf%s Max,"' ,
		'"GPRINT:buffered_avg:LAST:%5.1lf%s Last\\l"' ,
		'AREA:used_stk#ffbfbf' ,
		'"LINE1:used_stk#ff0000:used    "' ,
		'"GPRINT:used_min:MIN:%5.1lf%s Min,"' ,
		'"GPRINT:used_avg:AVERAGE:%5.1lf%s Avg,"' ,
		'"GPRINT:used_max:MAX:%5.1lf%s Max,"' ,
		'"GPRINT:used_avg:LAST:%5.1lf%s Last\\l"'
	]
	memory_line_args = " ".join(memory_args)
	graph = Graph(name="memory", group=group)
	graph.title="Memory"
	graph.command=memory_line_args
	graph.priority=0
	graph.save()

def make_interface_graph(interfacerrd, group, interface_name):
	interface_args = [
		'-s end-1h',
	#	'-e 1303382682',
		'-w 600',
		'-h 240',
		'-t if_octets-eth0' ,
		'-v Bits/s' ,
		'-E' ,
		'--units=si' ,
		'DEF:out_min_raw='+interfacerrd+'/if_octets.rrd:tx:MIN' ,
		'DEF:out_avg_raw='+interfacerrd+'/if_octets.rrd:tx:AVERAGE' ,
		'DEF:out_max_raw='+interfacerrd+'/if_octets.rrd:tx:MAX' ,
		'DEF:inc_min_raw='+interfacerrd+'/if_octets.rrd:rx:MIN' ,
		'DEF:inc_avg_raw='+interfacerrd+'/if_octets.rrd:rx:AVERAGE' ,
		'DEF:inc_max_raw='+interfacerrd+'/if_octets.rrd:rx:MAX' ,
		'CDEF:out_min=out_min_raw,8,*' ,
		'CDEF:out_avg=out_avg_raw,8,*' ,
		'CDEF:out_max=out_max_raw,8,*' ,
		'CDEF:inc_min=inc_min_raw,8,*' ,
		'CDEF:inc_avg=inc_avg_raw,8,*' ,
		'CDEF:inc_max=inc_max_raw,8,*' ,
		'CDEF:overlap=out_avg,inc_avg,GT,inc_avg,out_avg,IF' ,
		'CDEF:mytime=out_avg_raw,TIME,TIME,IF' ,
		'CDEF:sample_len_raw=mytime,PREV(mytime),-' ,
		'CDEF:sample_len=sample_len_raw,UN,0,sample_len_raw,IF' ,
		'CDEF:out_avg_sample=out_avg_raw,UN,0,out_avg_raw,IF,sample_len,*' ,
		'CDEF:out_avg_sum=PREV,UN,0,PREV,IF,out_avg_sample,+' ,
		'CDEF:inc_avg_sample=inc_avg_raw,UN,0,inc_avg_raw,IF,sample_len,*' ,
		'CDEF:inc_avg_sum=PREV,UN,0,PREV,IF,inc_avg_sample,+' ,
		'AREA:out_avg#B7EFB7' ,
		'AREA:inc_avg#B7B7F7' ,
		'AREA:overlap#89B3C9' ,
		'"LINE1:out_avg#00E000:Outgoing"' ,
		'"GPRINT:out_avg:AVERAGE:%5.1lf%s Avg,"' ,
		'"GPRINT:out_max:MAX:%5.1lf%s Max,"' ,
		'"GPRINT:out_avg:LAST:%5.1lf%s Last"' ,
		'"GPRINT:out_avg_sum:LAST:(ca. %5.1lf%sB Total)\\l"' ,
		'"LINE1:inc_avg#0000FF:Incoming"' ,
		'"GPRINT:inc_avg:AVERAGE:%5.1lf%s Avg,"' ,
		'"GPRINT:inc_max:MAX:%5.1lf%s Max,"' ,
		'"GPRINT:inc_avg:LAST:%5.1lf%s Last"' ,
		'"GPRINT:inc_avg_sum:LAST:(ca. %5.1lf%sB Total)\\l"'
	]
	interface_line_args = " ".join(interface_args)
	graph = Graph(name="interface-"+interface_name, group=group)
	graph.title="Interface "+interface_name
	graph.command=interface_line_args
	graph.priority=0
	graph.save()

def make_load_graph(loadrrd, group):
	load_args = [
		'-s end-1h',
	#	'-e 1305798665',
		'-w 600',
		'-h 240',
		'-v "System load"',
		'-t Load',
	#	'-E',
		'-l 0',
		'-X 0',
		'-Y',
		'DEF:s_avg='+loadrrd+'/load.rrd:shortterm:AVERAGE',
		'DEF:s_min='+loadrrd+'/load.rrd:shortterm:MIN',
		'DEF:s_max='+loadrrd+'/load.rrd:shortterm:MAX',
		'DEF:m_avg='+loadrrd+'/load.rrd:midterm:AVERAGE',
		'DEF:m_min='+loadrrd+'/load.rrd:midterm:MIN',
		'DEF:m_max='+loadrrd+'/load.rrd:midterm:MAX',
		'DEF:l_avg='+loadrrd+'/load.rrd:longterm:AVERAGE',
		'DEF:l_min='+loadrrd+'/load.rrd:longterm:MIN',
		'DEF:l_max='+loadrrd+'/load.rrd:longterm:MAX',
		'AREA:s_max#B7EFB7',
		'AREA:s_min#FFFFFF',
		'"LINE1:s_avg#FF0000: 1m average"',
		'"GPRINT:s_min:MIN:%4.2lf Min,"',
		'"GPRINT:s_avg:AVERAGE:%4.2lf Avg,"',
		'"GPRINT:s_max:MAX:%4.2lf Max,"',
		'"GPRINT:s_avg:LAST:%4.2lf Last\\n"',
		'"LINE1:m_avg#FF6600: 5m average"',
		'"GPRINT:m_min:MIN:%4.2lf Min,"',
		'"GPRINT:m_avg:AVERAGE:%4.2lf Avg,"',
		'"GPRINT:m_max:MAX:%4.2lf Max,"',
		'"GPRINT:m_avg:LAST:%4.2lf Last\\n"',
		'"LINE1:l_avg#FFAA00:15m average"',
		'"GPRINT:l_min:MIN:%4.2lf Min,"',
		'"GPRINT:l_avg:AVERAGE:%4.2lf Avg,"',
		'"GPRINT:l_max:MAX:%4.2lf Max,"',
		'"GPRINT:l_avg:LAST:%4.2lf Last\\n"'
	]
	load_line_args = " ".join(load_args)
	graph = Graph(name="load", group=group)
	graph.title="Load"
	graph.command=load_line_args
	graph.priority=0
	graph.save()

def make_graphs(device):
	hostname = str(device.config.id)
	path = RRD_DIR + hostname + "/"
	cpugroup,created = GraphGroup.objects.get_or_create(name="cpu-"+hostname, title="cpu")
	if not created:
		cpugroup.graphs.all().delete()
	memorygroup,created = GraphGroup.objects.get_or_create(name="memory-"+hostname, title="memory")
	if not created:
		memorygroup.graphs.all().delete()
	interfacegroup,created = GraphGroup.objects.get_or_create(name="interface-"+hostname, title="interface")
	if not created:
		interfacegroup.graphs.all().delete()
	loadgroup,created = GraphGroup.objects.get_or_create(name="load-"+hostname, title="load")
	if not created:
		loadgroup.graphs.all().delete()
	for file in os.listdir(path):
		if file.startswith("cpu"):
			make_cpu_graph(path+file, cpugroup, file[4:])
		if file.startswith("memory"):
			make_memory_graph(path+file, memorygroup)
		if file.startswith("interface"):
			make_interface_graph(path+file, interfacegroup, file[10:])
		if file.startswith("load"):
			make_load_graph(path+file, loadgroup)
	graphmanager,created = GraphManager.objects.get_or_create(device=device,
						cpugraphs = cpugroup,
						memorygraphs = memorygroup,
						interfacegraphs = interfacegroup,
						loadgraphs = loadgroup,
								)
