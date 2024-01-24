import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, create_engine, inspect
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'users_account'
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    
    addresses = relationship(
        "Addresses", back_populates="user", cascade="all"
    )
    
    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"
    
class Addresses(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("users_account.id"), nullable=False)  # Corrigido o nome da tabela aqui
    
    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        return f"Address(id={self.id}, email={self.email_address})"


print(User.__tablename__)
print(Addresses.__table__)

#conexão com o banco de dados
engine = create_engine("sqlite://")

#criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# investiga o esquema do banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))

print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)
