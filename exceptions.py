s=raw_input("Input your age:")
if s =="":
	raise Exception("Input must no be empty.")
try:
	i=int(s)
except ValueError:
 print "Could not convert data to an integer."
except:
 print "Unknown exception!"
else: # It isuseful forcode that must be executed ifthe tryclause does not raise an exception
 print "You are %d"%i,"years old"
finally: # Clean up action
 print "Goodbye!"