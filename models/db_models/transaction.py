from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()

# Модель для таблицы accounts_transaction_template
class AccountTransactionTemplate(Base):
    __tablename__ = 'accounts_transaction_template'
    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)