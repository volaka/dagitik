#!/usr/bin/env python

import sys
import time
from multiprocessing import Process,Queue,Lock,current_process

def reader(read_size,read_queue):
	try:
		p=current_process()
		file_r=open("metin.txt","rb")
		data=''
		index=1
		while True:
			data=file_r.read(read_size)
			if data=='':
				break
			data_i=(data,index)
			read_queue.put(data_i)
			index+=1
		file_r.close()
	except Exception:
		file_r.close()
		print "in "+p.name+" error "
	read_queue.put(('',0))
 
def crypter(alphabet,key,read_queue,crypt_queue):
	p=current_process()
	print p.name,"started"
	data=''
	crypt=''
	while True:
		read_lock.acquire()
		if read_queue.empty():
			read_lock.release()
			time.sleep(0.2)
		else:
			text=read_queue.get()
			if text[1]==0:
				read_queue.put(text)
				read_lock.release()
				break
			read_lock.release()
			for c in text[0].lower():
				if c in alphabet:
					data+=key[alphabet.find(c)]
				else:
					data+=c
			
			crypt=(data,text[1])
			crypt_queue.put(crypt)
	crypt_queue.put(('',-1))
	print p.name,"Crypting finished"
	

def writer(crypt_queue,filename,thread_count):
	index=1
	f_write=open(filename,"wb")
	crypt_list=[]
	found=False
	finish=False
	while not finish:
		if len(crypt_list)!=0:
			for c in crypt_list:
				if c[1]==index:
					found=True
					f_write.write(c[0])
					crypt_list.pop(crypt_list.index(c))					
					index+=1
					break
			if found:
				found=False
			else:
				crypt_lock.acquire()
				if crypt_queue.empty():
					crypt_lock.release()
					time.sleep(0.1)
					continue
				crypt=crypt_queue.get()
				crypt_lock.release()
				if crypt[1]==index:
					f_write.write(crypt[0])
					index+=1
				else:
					crypt_list.append(crypt)
		else:
			crypt_lock.acquire()
			if crypt_queue.empty():
				crypt_lock.release()
				time.sleep(0.2)
				continue
			crypt=crypt_queue.get()
			crypt_lock.release()
			if crypt[1]==index:
				f_write.write(crypt[0])
				index+=1
			else:
				crypt_list.append(crypt)
		if len(crypt_list)==thread_count and crypt_queue.empty():
			for c in crypt_list:
				if c[1]!=-1:
					finish=False
					break
				finish=True
	print "Writing Finished"

if __name__=='__main__':
	if len(sys.argv) != 4:
		print "Usage: python odev03_process.py <shifting> <threads> <block_length>"
		sys.exit("Invalid arguments")
	else:
		s=int(sys.argv[1])
		n=int(sys.argv[2])
		l=int(sys.argv[3])
		alphabet="abcdefghijklmnopqrstuvwxyz"
		alphabet_len=len(alphabet)
		head,tail=alphabet[:alphabet_len-s],alphabet[alphabet_len-s:]
		key=tail+head
		key=key.upper()
		
		read_queue=Queue(1000)
		crypt_queue=Queue(1000)
		read_lock=Lock()
		crypt_lock=Lock()
		
		write_file_name="crypted_"+str(s)+"_"+ str(n)+"_"+str(l)+".txt"		
		reader_p=Process(name='Reader Process',target=reader,args=(l,read_queue,))
		reader_p.start()
				
		processes=[]
		for i in range(0,n):
			p=Process(name='Crypter Process '+str(i+1),target=crypter,args=(alphabet,key,read_queue,crypt_queue,))
			p.start()
			processes.append(p)
		writer_p=Process(name='Writer Process',target=writer,args=(crypt_queue,write_file_name,n,))
		writer_p.start()		
		reader_p.join()
		for p in processes:
			p.join
		writer_p.join()
		print "Exiting"		



