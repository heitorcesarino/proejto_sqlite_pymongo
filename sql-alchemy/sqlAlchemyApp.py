from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Float


Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    #atributos
    id = Column(Integer, primary_key=True)
    cpf = Column(Integer)
    name = Column(String)
    address = Column(String)

    account = relationship('Account', back_populates='customer', cascade='all, delete-orphan')

    def __repr__(self):
        return f"Customer(id={self.id}, cpf={self.cpf} ,name={self.name}, address={self.address})"
    

class Account(Base):
    __tablename__ = 'account'
    #atributos
    id =   Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_customer = Column(Integer, ForeignKey('customer.id'), nullable=False)
    saldo = Column(Float)

    customer = relationship('Customer', back_populates='account')

    def __repr__(self):
        return f"Account(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, id_customer={self.id_customer}, saldo={self.saldo})"
    
#Conexão com banco de dados
engine = create_engine("sqlite://")

#criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# criando inspetor, que investiga o schema 
insp = inspect(engine)

# pegando nome das tabelas no schema
print(insp.get_table_names())

#pegando nome do schema 
print(insp.default_schema_name)

with Session(engine) as session:
    #criando objeto/entidade que sera persistida no db
    saruman = Customer(
        cpf = 12345678900,
        name = "saruman",
        address = "Isengard, middle earth, 324",
        account = [Account(
            tipo = 'conta corrente',
            agencia = 5050,
            num = 12345678,
            saldo = 1329.23
        )]
    )

    gandalf = Customer(
        cpf = 98765432100,
        name = "gandalf",
        address = "nômade, middle earth, 555",
        account = [Account(
            tipo = 'conta corrente',
            agencia = 4545,
            num = 56734521,
            saldo = 32456.98
        )]
    )
    session.add_all([saruman, gandalf])
    session.commit()


stmt = select(Customer).where(Customer.name.in_(["saruman", "gandalf"]))
print("\nrecuperando os customers da tabela de customers")
for customer in session.scalars(stmt):
    print(customer)


stmt_account = select(Account).where(Account.id_customer.in_([2]))
print("\nrecuperando a conta do gandalf [user_id=2]")
for account in session.scalars(stmt_account):
    print(account)