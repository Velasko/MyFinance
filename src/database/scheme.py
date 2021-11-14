import datetime
import re

from croniter import croniter_range

from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy import Float, Integer, SmallInteger, Numeric
from sqlalchemy import String, Boolean
from sqlalchemy import Date, DateTime
from sqlalchemy import Enum

from sqlalchemy import create_engine
from sqlalchemy.event import listen
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from ..utils.date import slice_by_date

Base = declarative_base()

class Money(Numeric):
	def __init__(self, *args, **kwargs):
		kwargs['precision'] = 9
		kwargs['scale'] = 2
		super().__init__(*args, **kwargs)

class Currency(Base):
	__tablename__ = 'Currencies'

	id = Column(String(3), primary_key=True)
	name = Column(String(16), unique=True)

	#method to convert to another currency

class CurrencyExchange(Base):
	__tablename__ = 'CurrencyExchanges'

	date = Column(Date, primary_key=True)
	lower_currency = Column(String(3), ForeignKey('Currencies.id', onupdate='CASCADE'),  primary_key=True)
	higher_currency = Column(String(3), ForeignKey('Currencies.id', onupdate='CASCADE'),  primary_key=True)
	money = Column(Float, primary_key=True)

class Account(Base):
	__tablename__ = 'Accounts'

	id = Column(Integer, primary_key=True)
	nome = Column(String(16))

	import_regex = Column(String(64))
	comment = Column(String(255))

	default_currency = Column(String(3), ForeignKey('Currencies.id', onupdate='CASCADE'))

	# how to handle if history + prediction?

	# Get history, fetch on AccountBalenceHistory
	# def __getitem__(self, index):
	# 	date_interval = slice_by_date(index)

class AccountBalenceHistory(Base):
	__tablename__ = 'AccountBalenceHistories'

	bank_account = Column(String(16), ForeignKey('Accounts.id', onupdate='CASCADE'), primary_key=True)
	date = Column(Date, primary_key=True)
	money = Column(Money, primary_key=True)
	currency = Column(String(3), ForeignKey('Currencies.id', onupdate='CASCADE'),  primary_key=True)

class Category(Base):
	__tablename__ = 'Categories'

	name = Column(String(16), primary_key=True)
	description = Column(String(255))
	active = Column(Boolean, default=True)

	# how to handle if history + prediction?
 
	# Get history, fetch on Transaction; filtering by category, ofc
	# def __getitem__(self, index):
	# 	date_interval = slice_by_date(index)

class PredictedTransaction(Base):
	__tablename__ = 'PredictedTransactions'

	name = Column(String(16), primary_key=True)
	category = Column(String(16), ForeignKey('Categories.name', onupdate='CASCADE'), primary_key=True)
	bank_account = Column(String(16), ForeignKey('Accounts.id', onupdate='CASCADE'))

	value = Column(Money, nullable=False)
	schedule = Column(String(32), nullable=False)

	# Interesting feature:
	#  - check if future predictions won't make account go red

	def __getitem__(self, index):
		date_interval = slice_by_date(index)
		return [ocurrences for ocurrences in croniter_range(*date_interval, self.schedule)]

class Transaction(Base):
	__tablename__ = 'Transactions'

	date = Column(Date, primary_key=True)
	transaction_number = Column(SmallInteger, primary_key=True)
	bank_account = Column(String(16), ForeignKey('Accounts.id', onupdate='CASCADE'), nullable=False)
	peer = Column(String(16), nullable=False)
	value = Column(Money, nullable=False)
	category = Column(String(16), ForeignKey('Categories.name', onupdate='CASCADE'), nullable=False)
	comment = Column(String(255))

	# Get transaction history, globaly; ??? faz sentido ser aqui?
	# def __getitem__(self, index):
	# 	date_interval = slice_by_date(index)

class TransactionTag(Base):
	__tablename__ = 'TransactionTags'
	__table_args__ = (
		ForeignKeyConstraint(
			['date', 'transaction_number'],
			['Transactions.date', 'Transactions.transaction_number'],
			ondelete='CASCADE',
			onupdate='CASCADE'
		),
	)

	tag = Column(String(16), primary_key=True)
	#transaction id
	date = Column(Date, primary_key=True)
	transaction_number = Column(SmallInteger, primary_key=True)

class Investment(Base):
	__tablename__ = 'Investiments'

	id = Column(Integer, primary_key=True)
	expected_gain = Column(Float)

	flow_ammount = Column(Money)
	flow_schedule = Column(String(32))

	# Where the money came from?
	# how much was added?

	# How to register investments that money is added periodically?

class InvestmentOperation(Base):
	__tablename__ = 'InvestmentHistory'
	__mapper_args__ = {
		'polymorphic_identity' : 'InvestmentOperation',
		'polymorphic_on' : type
	}

	investment_id = Column(String(16), ForeignKey('Investiments.id', onupdate='CASCADE'), primary_key=True)
	date = Column(Date, primary_key=True)

class InvestmentFlow(InvestmentOperation):
	__tablename__ = 'InvestmentFlow'
	__mapper_args__ = {
		'polymorphic_identity': 'InvestmentFlow',
		# 'concrete': True
	}
	__table_args__ = (
		ForeignKeyConstraint(
			['date', 'transaction_number', 'value'],
			['Transactions.date', 'Transactions.transaction_number', 'Transactions.value'],
			ondelete='CASCADE',
			onupdate='CASCADE'
		),
		ForeignKeyConstraint(
			['investment_id', 'date',],
			['InvestmentHistory.investment_id', 'InvestmentHistory.date'],
			ondelete='CASCADE',
			onupdate='CASCADE'
		),
	)

	investment_id = Column(String(16), primary_key=True)
	date = Column(Date, primary_key=True)
	transaction_number = Column(SmallInteger, primary_key=True)
	value = Column(Money, nullable=False)

class InvestmentInterest(InvestmentOperation):
	__tablename__ = 'InvestmentInterest'
	__mapper_args__ = {
		'polymorphic_identity': 'InvestmentFlow',
		# 'concrete': True
	}
	__table_args__ = (
		ForeignKeyConstraint(
			['investment_id', 'date',],
			['InvestmentHistory.investment_id', 'InvestmentHistory.date'],
			ondelete='CASCADE',
			onupdate='CASCADE'
		),
	)

	investment_id = Column(String(16), primary_key=True)
	date = Column(Date, primary_key=True)


if __name__ == '__main__':
	pt = PredictedTransaction(
		name='nome',
		category='categoria',
		bank_account='bnco',
		value=13,
		schedule='0 0 * * mon'
	)


	terapia = pt['10/21': '11/21']
	print(len(terapia), terapia)