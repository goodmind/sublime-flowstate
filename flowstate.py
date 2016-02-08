import sublime, sublime_plugin
import functools

class FlowstateCommand(sublime_plugin.EventListener):
    pending = 0

    def __init__(self):
        self.s = sublime.load_settings('flowstate.sublime-settings')
    
    def handle_timeout(self, view):
        self.pending = self.pending - 1
        if self.pending == 0:
            # There are no more queued up calls to handleTimeout, so it must have
            # been 1000ms since the last modification
            self.on_idle(view)
  
    def on_modified(self, view):
        self.pending = self.pending + 1

        # Ask for handleTimeout to be called in 1000ms
        sublime.set_timeout(functools.partial(self.handle_timeout, view), self.s.get('flowstate_timeout'))
  
    def on_idle(self, view):
        print("No activity in the past {:d}ms in file {:s}".format(self.s.get('flowstate_timeout'), view.file_name()))
