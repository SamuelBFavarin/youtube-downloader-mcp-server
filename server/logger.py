import sys

class MCPLogger:
    def debug(self, msg):
        print(msg, file=sys.stderr)
    def warning(self, msg):
        print(msg, file=sys.stderr)
    def error(self, msg):
        print(msg, file=sys.stderr)