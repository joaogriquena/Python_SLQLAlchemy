import sqlalchemy
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, create_engine, inspect, select
from sqlalchemy import Integer, String, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'users_account'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    
    addresses = relationship(
        "Address", back_populates="user", cascade="all"
    )
    
    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("users_account.id"), nullable=False)
    
    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address})"

# Conexão com o banco de dados
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# Investigando o esquema do banco de dados
inspector_engine = inspect(engine)
print(inspector_engine.has_table("users_account"))
print(inspector_engine.get_table_names())
print(inspector_engine.default_schema_name)

with Session(engine) as session:
    juliana = User(
        name='juliana',
        fullname='Juliana Mascarenhas',
        addresses=[Address(email_address='julianam@email.com')]
    )
    
    sandy = User(
        name='sandy',
        fullname='Sandy Cardoso',
        addresses=[Address(email_address='sandy@email.br'),
                   Address(email_address='sandy@email.org')]
    )
    
    patrick = User(
        name='patrick',
        fullname='Patrick Cardoso'
    )
    
    # Enviando para o BD (persistência de dados)
    session.add_all([juliana, sandy, patrick])
    session.commit()
    
stmt = select(User).where(User.name.in_(['juliana']))
print('Recuperando ususarios a partir de condições de filtragem')
for user in session.scalars(stmt): 
    print(user)
    
stmt_address = select(Address).where(Address.user_id.in_([2]))
print('Recuperando os endereçoes de email de Sandy')
for address in session.scalars(stmt_address):
    print(address)