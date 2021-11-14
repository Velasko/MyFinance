from . import methods

def main(parser, args):
	if args.operation is None:
		parser.error('the following arguments are required: operation')

	function = getattr(methods, f"{args.operation}_database")
	function()