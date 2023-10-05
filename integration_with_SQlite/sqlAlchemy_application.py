from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DECIMAL
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select


base = declarative_base()


class Client(base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String(11), nullable=False)
    address = Column(String(10), nullable=False)

    account = relationship("Account", back_populates="client")

    def __repr__(self):
        return f"Client(id = {self.id}, name = {self.name}, cpf = {self.cpf}, address = {self.address})"


class Account(base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    type = Column(String, default="Conta corrente")
    agency = Column(String)
    number = Column(Integer, unique=True, nullable=False)
    balance = Column(DECIMAL)
    id_client = Column(Integer, ForeignKey("client.id"), nullable=False)

    client = relationship("Client", back_populates="account")

    def __repr__(self):
        return f"Account(id = {self.id}, type = {self.type}, agency = {self.agency}," \
               f" number = {self.number}, balance = R${self.balance:.2f})"


engine = create_engine("sqlite://")
base.metadata.create_all(engine)

inspect_engine = inspect(engine)

print(inspect_engine.get_table_names())

with Session(engine) as session:
    miguel = Client(
        name="Miguel Cavalcante",
        cpf="12345678901",
        address="SP",
        account=[Account(
            agency="Santander",
            number="0002",
            balance="7000"
        )]
    )

    joao = Client(
        name="João da Silva",
        cpf="09876543212",
        address="SC",
        account=[Account(
            agency="Itaú",
            number="0001",
            balance="1000"
        )]
    )

    session.add_all([miguel, joao])

    session.commit()

stmt_order_client = select(Client).order_by(Client.name)
for user in session.scalars(stmt_order_client):
    print(user)

stmt_order_account = select(Account).order_by(Account.id_client)
for account in session.scalars(stmt_order_account):
    print(account)
