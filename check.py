import numpy as np
times = np.load('times.npy')

f = open('order.csv','r')
lines = f.readlines()
f.close()
ordtimes = []
ordtos = []
ordfroms = []

for line in lines:
	ps = line.split(',')
	ordfroms.append(int(ps[1]))
	ordtos.append(int(ps[2]))
	ordtimes.append(int(ps[3]))

f = open("answer.txt",'r')
lines = f.readlines()
f.close()

completedorders = []
totalwin = 0



for line in lines:
	err = False
	localwin = 0
	ordsin = []
	localordscompleted = []
	try:
		ps = line.split(',')

		p = ps[0]
		params = p.split(' ')
		starttime = int(params[0])
		curtime = int(params[0])
		curpos = int(params[1])
		for io in range(2,len(params)):
			orderID = int(params[io])
			if orderID in completedorders:
				err = True
				break
			if not ordfroms[orderID] == curpos:
				err = True
				break
			if not curtime >= ordtimes[orderID]:
				err = True
				break
			if not curtime <= ordtimes[orderID] + 900:
				err = True
				break
			ordsin.append(orderID)
		if len(ordsin) > 3:
			err = True
		if err:
			continue

		for ip in range(1,len(ps)):
			prevpos = curpos
			p = ps[ip]
			params = p.split(' ')
			curpos = int(params[0])
			curtime = curtime + times[prevpos,curpos]
			for io in range(1,len(params)):
				orderID = int(params[io])
				if orderID in ordsin:
					if not ordtos[orderID] == curpos:
						err = True
						break
					ordsin.remove(orderID)
					localordscompleted.append(orderID)
				else:
					if orderID in completedorders:
						err = True
						break
					if orderID in localordscompleted:
						err = True
						break
					if not ordfroms[orderID] == curpos:
						err = True
						break
					if not curtime >= ordtimes[orderID]:
						err = True
						break
					if not curtime <= ordtimes[orderID] + 900:
						err = True
						break
					ordsin.append(orderID)
			if len(ordsin) > 3:
				err = True
			if err:
				break
		if ordsin:
			err = True
		if err:
			continue

		timespentifseparate = 0
		for order in localordscompleted:
			timespentifseparate = timespentifseparate + times[ordfroms[order],ordtos[order]]
			completedorders.append(order) 
		
		# import pdb
		# pdb.set_trace()
		localwin = timespentifseparate - (curtime - starttime)
		totalwin = totalwin + localwin
	except:
		continue

print(totalwin)
f = open("result.txt",'w')
f.write(str(totalwin))
f.close() 
