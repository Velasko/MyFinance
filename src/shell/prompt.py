from subprocess import PIPE, Popen

import argparse
import os
import re
import traceback
import sys

# from .cmd import Cmd
import cmd

DEBUG_MODE = True

BLUE = "\033[1;34;40m"
GREEN = "\033[1;32;40m"
WHITE = "\033[0;37;40m"
RED = "\033[0;31;40m"
PURPLE = "\033[0;35;40m"

FINANCE_PROMPT = f'{PURPLE}finance-shell>{WHITE} '
BLOCK_PROMPT = f'{PURPLE}block ...>{WHITE} '
CMD_PROMPT = lambda path: f'{GREEN}sys-shell{WHITE}>{BLUE}{path}{WHITE}$ '

#if windows
if os.name == 'nt':
	import colorama
	colorama.init()

def cmdline(command):
	process = Popen(
		args=command,
		stdout=PIPE,
		shell=True
	)
	return process.communicate()[0]

def imput(prompt):
	#if windows
	if os.name == 'nt':
		print(prompt, end='')
		line = input()
	else:
		line = input(f"{prompt} ")
	return line
cmd.input = imput


class Prompt(cmd.Cmd):
	intro = '''
Welcome to finantial shell (0.1.0)
It has an integration with python shell so it's capable to execute calculations and define functions.
Type "help" or "?" for more information
	'''
	prompt = FINANCE_PROMPT
	shell_mode = False
	notes_created = []

	def __init__(self, functions=[], *args, **kwargs):
		super().__init__(*args, **kwargs)
		for function in functions:
			self.add_function(function)

	def add_function(self, function):
		setattr(Prompt, f"do_{function.__name__}", function)
		setattr(
			Prompt, f"help_{function.__name__}",
			lambda self: print(function.__doc__)
		)

	def default(self, inp):
		if Prompt.shell_mode:
			os.system(inp)
			return

		i = 'a'
		while inp[-1] == ':' or i[0] in ('\t', ' '):
			sys.stdout.write(BLOCK_PROMPT)
			sys.stdout.flush()
			i = sys.stdin.readline()
			inp += f'\n{i}'
			if i == '': break

		command = inp#re.sub(roll.d_pattern, roll.d_string, inp)
		try:
			if 'os.' in command:
				raise Exception()
			e = eval(command)
			if e is not None: print(e)

		except Exception as e:
			try:
				exec(command, globals())
			except Exception as e:
				name = re.match("<class '(.+)'>", str(type(e))).groups()[0]
				if DEBUG_MODE:
					purge = "exec(inp, globals())"
					trace = traceback.format_exc()

					if purge in trace:
						trace = '\n'.join(trace.split('\n'))
					print(trace)
				print(f'{RED}(Python) {name}: {e}{WHITE}')

	def do_EOF(self, inp):
		print("Ctrl + D")
		return self.do_exit(inp)

	def do_exit(self, inp):
		if Prompt.shell_mode:
			self.do_rpgmode(inp)
			return False

		print('Exit.')
		return True

	def do_cd(self, inp):
		if Prompt.shell_mode:
			if inp.startswith('/'):
				os.chdir(inpd)
			else:
				retval = os.getcwd()
				if inp.startswith('./'): inp = inp[2:]
				os.chdir(f"{retval}/{inp}")
				Prompt.prompt = CMD_PROMPT(os.getcwd())

	def complete_cd(self, text, line, begidx, endidx):
		return [o for o in os.listdir('.') if os.path.isdir(o) and o.startswith(text)]

	def do_cmdmode(self, inp):
		Prompt.prompt = CMD_PROMPT(os.getcwd())
		Prompt.shell_mode = True

	def help_cmdmode(self):
		print("Executes system commands until rpgmode is called.")

	def do_financemode(self, inp):
		Prompt.prompt = FINANCE_PROMPT
		Prompt.shell_mode = False

	def help_financemode(self):
		print("Returns to the finance mode.")

	def do_clear(self, inp):
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')

	# def help_dependencies(self):
	# 	print("For this current version of the rpg-shell, for full functionality, " + \
	# 		"it's required to run on linux and have the following programs installed:\n" + \
	# 		"tmux\nnano")

	do_cls = do_clear

if __name__ == '__main__':
	Prompt().cmdloop()
