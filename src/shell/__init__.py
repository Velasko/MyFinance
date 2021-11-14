from .prompt import Prompt

def main(parser, args):
	prompt = Prompt()
	global test
	# prompt.add_function(test)
	prompt.cmdloop()