from app.models import categoria
from app.models import produto
from app.models import usuario
from app.models import movimentacao
from app.models import cliente
from app.models import venda


# Gerar a migration
# python -m alembic revision --autogenerate -m "criar tabelas categorias e produtos"

# python -m alembic upgrade head