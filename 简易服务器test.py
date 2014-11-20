#coding=utf-8
import android
import SimpleHTTPServer 
import SocketServer 
#import os

PORT = 80 
WEBDIR = "/mnt/sdcard"
class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler): 
  def translate_path(self,path): 
    os.chdir(WEBDIR) 
    return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(path) 
  
#help( SocketServer.TCPServer )
httpd = SocketServer.TCPServer(("127.0.0.1", PORT), Handler) 
print "dir %s serving at port %s"%(repr(WEBDIR), PORT) 
httpd.serve_forever() 