import argparse
import datetime
import importlib
import logging
import os
import traceback

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument("execution_mode",
		choices=['shell', 'database', 'google']
	)


	log_group = parser.add_argument_group(title='Logging parameters')
	log_group.add_argument('--logfile',
		default=os.path.join(
			os.getcwd(),
			'logs',
			f"Execution - {datetime.datetime.utcnow().isoformat().replace(':', '-')}.log"
		),
		help='filename to be used as log'
	)

	log_group.add_argument('--log-level',
		default='info',
		choices=['debug', 'info', 'warning', 'error', 'critical'],
		help='selects the logging level'
	)

	log_group.add_argument('--block-logs',
		action='store_false',#true',
		help='show logs on terminal, instead of saving to logfile'
	)

	database = parser.add_argument_group(title='database parameters')
	database.add_argument(
		'operation',
		nargs='?',#None if temp_args.execution_mode != 'database' else '*',
		choices=['create', 'drop'],
		help='Database main operation'
	)

	args = parser.parse_args()

	if args.block_logs:
		logger = logging.getLogger()
		logger.disabled = True
	else:
		logging.basicConfig(
			filename=args.logfile,
			level=getattr(logging, args.log_level.upper())
		)
	
	try:
		module = importlib.import_module(
			f"{__package__}.{args.execution_mode}"
		)
		module.main(parser, args)
	except Exception as e:
		logging.error(traceback.format_exc())

		raise e