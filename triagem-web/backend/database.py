"""
Configuração do banco de dados PostgreSQL para Railway
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
# URL do banco PostgreSQL do Railway
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/triagem_odq"
)
# Configuração do engine com pool de conexões
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=os.getenv("DB_ECHO", "false").lower() == "true"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    """
    Dependency para obter sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def create_tables():
    """
    Criar todas as tabelas no banco
    """
    Base.metadata.create_all(bind=engine)
def init_db():
    """
    Inicializar banco de dados com dados básicos
    """
    # Import aqui para evitar dependência circular
    from models import User
    db = SessionLocal()
    try:
        # Verificar se já existe usuário admin
        admin = db.query(User).filter(User.email == "admin@odq.com").first()
        if not admin:
            # Criar usuário admin padrão
            from services.auth_service import AuthService
            auth_service = AuthService()
            admin_user = User(
                name="Administrador",
                email="admin@odq.com",
                password_hash=auth_service.hash_password("admin123"),
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("Usuário admin criado: admin@odq.com / admin123")
        else:
            print("Usuário admin já existe")
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
        db.rollback()
    finally:
        db.close()
# Configuração para testes
def get_test_db():
    """
    Database para testes unitários
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    TEST_DATABASE_URL = "sqlite:///./test.db"
    test_engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

