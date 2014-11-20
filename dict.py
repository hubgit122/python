#!/usr/bin/python # Filename: using_dict.py

# 'ab' is short for 'a'ddress'b'ook

ab = { 'Swaroop' : 'swaroopch@byteofpython.info', 'Larry' : 'larry@wall.org', 'Matsumoto' : 'matz@ruby-lang.org', 'Spammer' : 'spammer@hotmail.com',3:5 }

print "Swaroop's address is %s" % ab['Swaroop']

# Adding a key/value pair ab['Guido'] = 'guido@python.org'
#ab['Guido'] = 'guido2@python.org'

# Deleting a key/value pair 
del ab['Spammer']

print '\nThere are %d contacts in the address-book\n' % len(ab) 
for name, address in ab.items(): print 'Contact %s at %s' % (name, address)

if 'Guido' in ab: # OR ab.has_key('Guido') 
 print "\nGuido's address is %s" % ab['Guido']
 
print ab.items()
print ab