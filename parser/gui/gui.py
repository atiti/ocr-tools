#!/usr/bin/python

import sys, thread, time
try:
	import pygtk
	pygtk.require('2.0')
except:
	pass
try:
	import gtk
	import gtk.glade
except:
	print "Failed to find python GTK bindings"
	sys.exit(1)


class Base:
	def __init__(self):
		self.progress = 0
		self.running = 0

		gtk.gdk.threads_init()

		# Load the gui XML
		self.gladefile = "gui.glade"
		self.wTree = gtk.glade.XML(self.gladefile)
		
		# Create the window, connect signals
		self.window = self.wTree.get_widget("MainWindow")
		if self.window:
			dic = {
				"on_runbutton_clicked": self.on_runbutton_clicked
			}

			self.window.connect("destroy", gtk.main_quit)
			self.wTree.signal_autoconnect(dic)
			self.window.show()
			self.update_progressbar(self.progress)

	def on_MainWindow_delete_event(self, widget, event):
		print "Quitting."
		gtk.main_quit()

	def update_progressbar(self, percent, text=None):
		if percent < 0 or percent > 100:
			return

		progress_widget = self.wTree.get_widget("progressbar1")
		if not text:
			text = str(percent)+" %"
		progress_widget.set_text(text)		
		progress_widget.set_fraction(float(percent)/100)

	def on_runbutton_clicked(self, widget):
		# If the worker thread is not running
		if not self.running:
			runocr = self.wTree.get_widget("runocr").get_active()
			runparser = self.wTree.get_widget("runparser").get_active()

			threads = self.wTree.get_widget("threads").get_value_as_int()

			sourcepath = self.wTree.get_widget("sourcechooser").get_filename()
			targetpath = self.wTree.get_widget("targetchooser").get_filename()
		
			options = {"threads": threads,
				   "runocr": runocr,
				   "runparser": runparser,
				   "source": sourcepath,
				   "target": targetpath}


			print "Run OCR:",runocr,"Parser:",runparser, "Threads:",threads
			print "Source path:",sourcepath
			print "Target path:",targetpath
		
			thread.start_new_thread(self.run_thread, (options,))
		# If the worker thread is already running, we want to stop it!
		else:
			self.running = 0	


	def run_thread(self, options):
		print "Runner thread launched: ",repr(options)
		# Disable UI components
		gtk.gdk.threads_enter()
		self.update_progressbar(0)
		runbutton_widget = self.wTree.get_widget("runbutton")
		sourcechooser_widget = self.wTree.get_widget("sourcechooser")
		targetchooser_widget = self.wTree.get_widget("targetchooser")
		runocr_widget = self.wTree.get_widget("runocr")
		runparser_widget = self.wTree.get_widget("runparser")
		threads_widget = self.wTree.get_widget("threads")
		runbutton_widget.set_label("STOP!")
                #runbutton_widget.set_sensitive(False)
                sourcechooser_widget.set_sensitive(False)
                targetchooser_widget.set_sensitive(False)
                runocr_widget.set_sensitive(False)
                runparser_widget.set_sensitive(False)
                threads_widget.set_sensitive(False)
		gtk.gdk.threads_leave()

		# Run the stuff
		cnt = 0
		while cnt < 10: 
			cnt += 1
			print cnt	
			gtk.gdk.threads_enter()
			self.update_progressbar(cnt*10)
			gtk.gdk.threads_leave()
			time.sleep(1)
		
		# Lets make sure we don't have boundary violations
		# Enable disabled UI components
		gtk.gdk.threads_enter()
		#runbutton_widget.set_sensitive(True)
		runbutton_widget.set_label("Run")
		sourcechooser_widget.set_sensitive(True)
		targetchooser_widget.set_sensitive(True)
		runocr_widget.set_sensitive(True)
		runparser_widget.set_sensitive(True)
		threads_widget.set_sensitive(True)
		gtk.gdk.threads_leave()
		self.running = 0
	

	def main(self):
		gtk.main()


if __name__ == "__main__":
	try:
		base = Base()
		base.main()
	except KeyboardInterrupt:
		sys.exit(0)
