import sublime, sublime_plugin
import functools

def log(*args):
    sublime.status_message(' '.join([str(arg) for arg in args]))
    print(*args)

class FlowstateCommand(sublime_plugin.EventListener):
    pending = 0

    def __init__(self):
        s = sublime.load_settings('flowstate.sublime-settings')
        self.timeout = s.get('flowstate_timeout') or 5000

        log('Initialize Flowstate plugin...', s.get('flowstate_timeout'), self.timeout)
    
    def handle_timeout(self, view):
        self.pending = self.pending - 1
        if self.pending == 0:
            # There are no more queued up calls to handleTimeout, so it must have
            # been 1000ms since the last modification
            self.on_idle(view)
  
    def on_modified(self, view):
        self.pending = self.pending + 1

        # Ask for handleTimeout to be called in 1000ms
        sublime.set_timeout(functools.partial(self.handle_timeout, view), self.timeout)
  
    def on_idle(self, view):
        log("No activity in the past {:d}ms in file {:s}. Your work will be erased!".format(self.timeout, view.file_name()))
        sublime.set_timeout(lambda: view.run_command('undo'), self.timeout)
