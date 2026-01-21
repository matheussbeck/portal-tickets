# 📚 SQLAlchemy para APIs REST e Analytics
## Tutorial Completo: Do Básico ao Avançado

**Autor**: Claude AI
**Data**: Janeiro 2026
**Contexto**: Sistema de Gerenciamento de Tickets/Projetos/Relatórios
**Stack**: Python + SQLAlchemy 2.0 + FastAPI + Pydantic

---

## 🎯 Sobre Este Tutorial

### O Que Você Vai Aprender

Este tutorial foi construído especificamente para desenvolvedores que estão criando **APIs REST profissionais** com necessidades de **analytics e relatórios**. Não é apenas um guia de sintaxe - é uma jornada completa do conceito básico até padrões arquiteturais de produção.

### Filosofia do Tutorial

**EXPLICAR antes de EXEMPLIFICAR**. Cada conceito é apresentado em camadas:

1. **Definição**: O que é e qual problema resolve
2. **Contexto**: Por que existe e quando usar
3. **Mecânica**: Como funciona por baixo dos panos
4. **Prática**: Exemplos de código comentados
5. **Trade-offs**: Vantagens, desvantagens e alternativas

### Como Usar Este Material

- **Iniciantes**: Leia sequencialmente, execute os exemplos
- **Intermediários**: Foque nos Módulos 2, 3 e 4 (relacionamentos e arquitetura)
- **Avançados**: Módulos 4 e 5 (performance e boas práticas)
- **Referência**: Use o índice para consultas rápidas

### Pré-requisitos

- Python 3.10+ (type hints modernos)
- Conhecimento básico de SQL (SELECT, JOIN, WHERE)
- Noções de programação orientada a objetos
- (Opcional) Familiaridade com APIs REST

---

## 📖 Jornada de Aprendizado

Este tutorial está organizado em **PASSOS** para garantir uma progressão linear e completa. Cada passo tem um checklist para você acompanhar seu progresso.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SUA JORNADA DE DESENVOLVEDOR                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PASSO 1        PASSO 2         PASSO 3         PASSO 4         PASSO 5    │
│  FUNDAÇÃO  ──►  MODELAGEM  ──►  ARQUITETURA ──►  SEGURANÇA  ──►  PRODUÇÃO  │
│  (Setup)       (Banco)         (Código)        (Auth)          (Deploy)    │
│                                                                             │
│  Módulo 0      Módulos 1-2     Módulos 3-5     Módulo 8        Módulos 6-7 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ PASSO 1: FUNDAÇÃO (Configuração Inicial)

*Antes de escrever qualquer código, configure o ambiente corretamente. Decisões tomadas aqui impactam TODO o projeto.*

### Checklist de Conclusão - PASSO 1
```
[ ] Ambiente virtual criado e ativado (venv)
[ ] Dependências instaladas (requirements.txt)
[ ] Estrutura de pastas criada (infra/, services/, api/, schemas/)
[ ] Arquivo .env configurado com variáveis de ambiente
[ ] Arquivo .gitignore configurado (NÃO commitar .env!)
[ ] Git iniciado (git init)
[ ] Alembic inicializado (alembic init alembic)
[ ] Conexão com banco testada
```

### Módulos deste Passo

**MÓDULO 0: SETUP E CONFIGURAÇÃO**
- 0.1 [Estrutura de Pastas do Projeto](#01-estrutura-de-pastas-do-projeto)
- 0.2 [Configuração do Ambiente](#02-configuração-do-ambiente)
- 0.3 [Configuração do Banco de Dados](#03-configuração-do-banco-de-dados)
- 0.4 [Variáveis de Ambiente](#04-variáveis-de-ambiente)
- 0.5 [Alembic - Migrations de Banco de Dados](#05-alembic---migrations-de-banco-de-dados) ⚠️ **CRÍTICO**
- 0.6 [SQL Essencial - O Que Você Precisa Saber](#06-sql-essencial---o-que-você-precisa-saber) 📚 **BASE**

---

## 🗄️ PASSO 2: MODELAGEM (Banco de Dados)

*Defina suas entidades e relacionamentos. Esta é a fundação de dados da sua aplicação.*

### Checklist de Conclusão - PASSO 2
```
[ ] Entendi a diferença entre ORM e SQL puro
[ ] Entendi o ciclo de vida da Session (Transient → Pending → Persistent → Detached)
[ ] Criei minhas entidades herdando de Base
[ ] Usei init=False em campos com default e relacionamentos
[ ] Configurei ForeignKeys com ondelete apropriado
[ ] Configurei lazy="raise" em TODOS os relationships
[ ] Criei migrations com Alembic (não usei create_all())
[ ] Apliquei migrations (alembic upgrade head)
[ ] Entendi a diferença entre CASCADE (Python) e ondelete (SQL)
[ ] Testei CRUD básico nas entidades
```

### Módulos deste Passo

**MÓDULO 1: FUNDAMENTOS**
- 1.1 [O Que É ORM e Por Que Usar?](#11-o-que-é-orm-e-por-que-usar)
- 1.2 [Anatomia de um Model SQLAlchemy](#12-anatomia-de-um-model-sqlalchemy)
- 1.2.5 [Session - O Coração do SQLAlchemy](#125-session---o-coração-do-sqlalchemy) ⚠️ **CRÍTICO**
- 1.3 [CRUD Básico - As 4 Operações Fundamentais](#13-crud-básico---as-4-operações-fundamentais)
- 1.4 [Tipos de Dados e Opções de Colunas](#14-tipos-de-dados-e-opções-de-colunas)
- 1.5 [Armadilhas Comuns do MappedAsDataclass](#15-armadilhas-comuns-do-mappedasdataclass) ⚠️ **CRÍTICO**

**MÓDULO 2: RELACIONAMENTOS**
- 2.1 [Foreign Keys - A Base dos Relacionamentos](#21-foreign-keys---a-base-dos-relacionamentos)
- 2.2 [Relationship - Navegação entre Objetos](#22-relationship---navegação-entre-objetos)
- 2.3 [Relacionamento N-1 (Many-to-One) - DETALHADO](#23-relacionamento-n-1-many-to-one---detalhado)
- 2.4 [O Parâmetro lazy - CRUCIAL para Performance](#24-o-parâmetro-lazy---crucial-para-performance)
- 2.5 [Eager Loading - Carregamento Explícito](#25-eager-loading---carregamento-explícito)
- 2.6 [Relacionamento N-N (Many-to-Many)](#26-relacionamento-n-n-many-to-many)
- 2.7 [Tabela de Associação com Atributos Extras](#27-tabela-de-associação-com-atributos-extras)
- 2.7.5 [Cascade - Propagação de Operações](#275-cascade---propagação-de-operações) ⚠️ **IMPORTANTE**
- 2.8 [Relacionamentos Avançados](#28-relacionamentos-avançados)
- 2.9 [Guia Completo: Implementação em AMBOS OS LADOS](#29-guia-completo-implementação-de-relacionamentos-em-ambos-os-lados)

---

## 🏛️ PASSO 3: ARQUITETURA (Organização do Código)

*Organize seu código em camadas. Separe responsabilidades para ter código testável e manutenível.*

### Checklist de Conclusão - PASSO 3
```
[ ] Entendi por que NÃO usar to_dict() nos models
[ ] Criei schemas Pydantic para cada entidade (Create, Update, Response)
[ ] Separei lógica de negócio em Services
[ ] Criei Repositories para acesso a dados
[ ] Criei Routes/Endpoints no FastAPI
[ ] Usei Dependency Injection para Session
[ ] Implementei eager loading explícito (joinedload, selectinload)
[ ] Criei queries de agregação quando necessário
[ ] Adicionei índices nas colunas de busca frequente
[ ] Escrevi testes unitários e de integração
```

### Módulos deste Passo

**MÓDULO 3: ARQUITETURA PROFISSIONAL**
- 3.1 [Por Que Não Usar to_dict() nos Models](#31-por-que-não-usar-to_dict-nos-models)
- 3.2 [Schemas com Pydantic](#32-schemas-com-pydantic)
- 3.3 [Services - Camada de Negócio](#33-services---camada-de-negócio)
- 3.4 [API Endpoints com FastAPI](#34-api-endpoints-com-fastapi)

**MÓDULO 4: ANALYTICS E PERFORMANCE**
- 4.1 [Queries de Agregação](#41-queries-de-agregação)
- 4.2 [Analytics Service](#42-analytics-service)
- 4.3 [Otimizações Avançadas](#43-otimizações-avançadas)
- 4.4 [Índices e Performance](#44-índices-e-performance)

**MÓDULO 5: BOAS PRÁTICAS**
- 5.1 [Checklist de Implementação](#51-checklist-de-implementação)
- 5.2 [Padrões de Nomenclatura](#52-padrões-de-nomenclatura)
- 5.3 [Segurança e Validação](#53-segurança-e-validação)
- 5.4 [Testes](#54-testes)
- 5.5 [Erros Comuns e Soluções](#55-erros-comuns-e-soluções)
- 5.6 [Ordem de Criação de Registros](#56-ordem-de-criação-de-registros)

---

## 🔐 PASSO 4: SEGURANÇA (Autenticação e Autorização)

*Proteja sua aplicação. Nunca vá para produção sem autenticação adequada.*

### Checklist de Conclusão - PASSO 4
```
[ ] Entendi por que NUNCA armazenar senhas em texto puro
[ ] Implementei hash de senha com bcrypt
[ ] Criei endpoint de registro com validação de senha forte
[ ] Criei endpoint de login que retorna JWT
[ ] Implementei refresh token para renovação
[ ] Criei middleware de autenticação (Depends)
[ ] Protegi rotas que exigem autenticação
[ ] Implementei autorização por roles (admin, user, etc)
[ ] Criei fluxo de recuperação de senha
[ ] Configurei CORS corretamente
[ ] SECRET_KEY é forte e está em variável de ambiente
```

### Módulos deste Passo

**MÓDULO 8: SEGURANÇA E AUTENTICAÇÃO** ⚠️ **CRÍTICO**
- 8.1 [Por Que Segurança Importa](#81-por-que-segurança-importa)
- 8.2 [Hash de Senhas com Bcrypt](#82-hash-de-senhas-com-bcrypt)
- 8.3 [JWT - JSON Web Tokens](#83-jwt---json-web-tokens)
- 8.4 [Autenticação no FastAPI](#84-autenticação-no-fastapi)
- 8.5 [Autorização e Roles](#85-autorização-e-roles)
- 8.6 [Recuperação de Senha](#86-recuperação-de-senha)
- 8.7 [Boas Práticas de Segurança](#87-boas-práticas-de-segurança)

---

## 🚀 PASSO 5: PRODUÇÃO (Deploy e Monitoramento)

*Coloque sua aplicação no ar de forma profissional e monitore seu funcionamento.*

### Checklist de Conclusão - PASSO 5
```
[ ] Criei Dockerfile otimizado
[ ] Configurei docker-compose com banco e aplicação
[ ] Variáveis de ambiente configuradas para produção
[ ] DEBUG=false em produção
[ ] Swagger/ReDoc desabilitados em produção (ou protegidos)
[ ] Logging estruturado em JSON
[ ] Health checks implementados (/health, /health/ready)
[ ] Métricas com Prometheus configuradas
[ ] Git configurado com branches e conventional commits
[ ] CI/CD configurado (GitHub Actions ou similar)
[ ] Backup de banco configurado
[ ] Alertas de erro configurados
```

### Módulos deste Passo

**MÓDULO 6: GUIA PRÁTICO PASSO A PASSO**
- 6.1 [Criando uma Nova Entidade](#61-criando-uma-nova-entidade)
- 6.2 [Criando um Novo Endpoint](#62-criando-um-novo-endpoint)
- 6.3 [Implementando CRUD Completo](#63-implementando-crud-completo)

**MÓDULO 7: PRODUÇÃO E DEPLOY**
- 7.1 [Docker - Containerização](#71-docker---containerização)
- 7.2 [Configuração para Produção](#72-configuração-para-produção)
- 7.3 [Observabilidade (Logging, Prometheus, Grafana)](#73-observabilidade)
- 7.4 [Configuração do FastAPI para Produção](#74-configuração-do-fastapi-para-produção)
- 7.5 [Git e GitHub - Versionamento Profissional](#75-git-e-github---versionamento-profissional)
- 7.6 [CI/CD com GitHub Actions](#76-cicd-com-github-actions) ⚠️ **IMPORTANTE**
- 7.7 [Checklist de Deploy](#77-checklist-de-deploy)

---

## 📚 APÊNDICE: REFERÊNCIA RÁPIDA

*Material de consulta rápida para o dia a dia.*

- A.1 [Tabela de Tipos](#a1-tabela-de-tipos)
- A.2 [Opções de ondelete](#a2-opções-de-ondelete)
- A.3 [Opções de lazy](#a3-opções-de-lazy)
- A.4 [Snippets Prontos](#a4-snippets-prontos)

---

# MÓDULO 0: SETUP E CONFIGURAÇÃO

## Por Que Este Módulo Existe?

A configuração inicial de um projeto determina **80% do sucesso futuro**. Decisões tomadas aqui impactam:

- **Manutenibilidade**: Código fácil ou difícil de manter
- **Escalabilidade**: Crescer sem reescrever tudo
- **Testabilidade**: Possível ou impossível testar
- **Onboarding**: Novos devs produtivos em dias ou meses

Este módulo não é apenas "copie e cole estes arquivos". Cada decisão tem uma razão, e você vai entender todas elas.

### O Que Você Vai Aprender

1. **Estrutura de pastas** - Por que separar em camadas e qual padrão arquitetural seguimos
2. **Classe Base** - Por que usar `MappedAsDataclass` e suas regras críticas
3. **Enums** - Por que usar `PyEnum` ao invés de strings
4. **Conexão com banco** - Por que Context Manager e pool de conexões
5. **Variáveis de ambiente** - Por que `pydantic-settings` e não `os.environ`
6. **Migrations** - Por que Alembic ao invés de `create_all()`

---

## 0.1 Estrutura de Pastas do Projeto

### Por Que a Estrutura de Pastas Importa?

Em projetos pequenos, colocar tudo em um arquivo funciona. Mas quando o projeto cresce:

```
projeto_bagunçado/
├── main.py          # 5000 linhas, models + routes + services misturados
├── utils.py         # 2000 linhas de "utilidades" sem relação
└── db.py            # Conexão, entidades, queries, tudo junto
```

**Problemas**:
- Impossível encontrar onde está algo específico
- Mudança em uma parte quebra outras partes
- Múltiplos desenvolvedores editando os mesmos arquivos
- Testes impossíveis (como testar uma função que depende de tudo?)

A solução é **separação de responsabilidades** - cada pasta/arquivo tem uma única responsabilidade.

### O Padrão Arquitetural: Layered Architecture

Usamos uma variação da **Arquitetura em Camadas**, onde cada camada só conhece a camada imediatamente abaixo:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  api/              → INTERFACE (como o mundo externo acessa)                │
│                      Recebe HTTP, valida entrada, retorna resposta          │
├─────────────────────────────────────────────────────────────────────────────┤
│  services/         → REGRAS DE NEGÓCIO (o que a aplicação FAZ)              │
│                      Lógica, validações de negócio, orquestração            │
├─────────────────────────────────────────────────────────────────────────────┤
│  infra/repos/      → ACESSO A DADOS (como buscar/salvar)                    │
│                      Queries, CRUD, abstração do banco                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  infra/entities/   → ESTRUTURA DOS DADOS (como os dados SÃO)                │
│                      Models, relacionamentos, tipos                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  infra/configs/    → INFRAESTRUTURA (conexões, configurações)               │
│                      Banco, settings, ambiente                              │
└─────────────────────────────────────────────────────────────────────────────┘

Fluxo de dependência (seta = "depende de"):
api/ → services/ → repositories/ → entities/ → configs/

REGRA: Nunca inverta a seta! (ex: entity não importa service)
```

### Por Que Esta Separação Específica?

| Camada | Responsabilidade | Por Que Separar? |
|--------|------------------|------------------|
| `api/` | HTTP, rotas, validação de entrada | Trocar FastAPI por Flask? Só muda aqui |
| `services/` | Lógica de negócio | Reutilizar lógica em CLI, scripts, testes |
| `repositories/` | Queries SQL/ORM | Trocar PostgreSQL por MongoDB? Só muda aqui |
| `entities/` | Estrutura das tabelas | Definição única da verdade sobre os dados |
| `configs/` | Conexões, settings | Ambiente dev/prod com mesma configuração |
| `schemas/` | Contratos da API | Entrada/saída da API separada dos models |

### Estrutura Recomendada

```
meu_projeto/
│
├── .env                          # Variáveis de ambiente (NÃO commitar!)
├── .env.example                  # Template das variáveis (commitar)
├── .gitignore
├── requirements.txt
├── alembic.ini                   # Configuração do Alembic
│
├── alembic/                      # Migrations
│   ├── versions/
│   └── env.py
│
├── infra/                        # Infraestrutura (banco, conexões)
│   ├── __init__.py
│   ├── configs/
│   │   ├── __init__.py
│   │   ├── connection.py         # Gerenciador de conexão
│   │   ├── database.py           # Base e configurações
│   │   └── settings.py           # Configurações do app
│   │
│   ├── entities/                 # Models/Entidades
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── team.py
│   │   └── ...
│   │
│   └── repositories/             # Acesso a dados
│       ├── __init__.py
│       ├── user_repository.py
│       └── ...
│
├── schemas/                      # Pydantic schemas
│   ├── __init__.py
│   ├── user_schema.py
│   └── ...
│
├── services/                     # Lógica de negócio
│   ├── __init__.py
│   ├── user_service.py
│   └── ...
│
├── api/                          # Endpoints
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   └── ...
│   └── dependencies.py
│
├── tests/                        # Testes
│   ├── __init__.py
│   ├── conftest.py
│   └── ...
│
└── main.py                       # Ponto de entrada
```

### Por Que Esta Estrutura?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SEPARAÇÃO DE RESPONSABILIDADES                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  infra/          → Tudo relacionado a DADOS (banco, entidades, repos)       │
│  schemas/        → CONTRATOS da API (entrada/saída)                         │
│  services/       → REGRAS DE NEGÓCIO                                        │
│  api/            → INTERFACE HTTP (endpoints)                               │
│                                                                             │
│  Cada camada só conhece a camada imediatamente abaixo:                      │
│                                                                             │
│  api/ → services/ → repositories/ → entities/                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 0.2 Configuração do Ambiente

### Passo 1: Criar Ambiente Virtual

```bash
# Criar pasta do projeto
mkdir meu_projeto
cd meu_projeto

# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate
```

### Passo 2: Instalar Dependências

**requirements.txt**:
```
# Core
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1

# Driver do banco (escolha um)
# SQLite (desenvolvimento)
# (já vem com Python)

# PostgreSQL (produção)
psycopg2-binary==2.9.9

# Utilitários
python-dotenv==1.0.0

# Segurança
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0

# Testes
pytest==7.4.4
httpx==0.26.0
```

```bash
# Instalar
pip install -r requirements.txt
```

### Passo 3: Criar Estrutura de Pastas

```bash
# Criar todas as pastas
mkdir -p infra/configs infra/entities infra/repositories
mkdir -p schemas services api/routes tests

# Criar arquivos __init__.py
touch infra/__init__.py
touch infra/configs/__init__.py
touch infra/entities/__init__.py
touch infra/repositories/__init__.py
touch schemas/__init__.py
touch services/__init__.py
touch api/__init__.py
touch api/routes/__init__.py
touch tests/__init__.py
```

---

## 0.3 Configuração do Banco de Dados

Este é o arquivo mais importante do projeto. Aqui definimos a **classe Base** que todas as entidades herdam. Antes de ver o código, você precisa entender **por que** cada decisão foi tomada.

### Por Que Usar MappedAsDataclass?

O SQLAlchemy 2.0 oferece duas formas de definir models:

**Forma 1: Tradicional (sem MappedAsDataclass)**
```python
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()

# Para criar um User, você precisa de um construtor manual:
user = User()
user.nome = "Matheus"  # Definir campo por campo
# OU
user = User(nome="Matheus")  # Funciona, mas sem autocomplete/validação
```

**Forma 2: Com MappedAsDataclass**
```python
class User(MappedAsDataclass, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome: Mapped[str] = mapped_column()

# Construtor automático com type hints e validação:
user = User(nome="Matheus")  # IDE mostra autocomplete, valida tipos
```

**Vantagens do MappedAsDataclass**:
| Aspecto | Tradicional | MappedAsDataclass |
|---------|-------------|-------------------|
| Construtor | Manual ou genérico | Gerado automaticamente |
| Autocomplete na IDE | Parcial | Completo |
| Validação de tipos | Não | Sim (em runtime) |
| `__repr__()` | Manual | Automático |
| `__eq__()` | Manual | Automático |

**Trade-off**: MappedAsDataclass tem regras mais rígidas sobre ordem de campos e valores default. Veremos essas regras a seguir.

### Por Que Usar PyEnum ao Invés de Strings?

Compare as duas abordagens para um campo de status:

**Abordagem 1: Strings puras**
```python
class User(Base):
    status: Mapped[str] = mapped_column(String(20))

# Uso:
user = User(status="ativo")
user = User(status="ATIVO")   # Diferente! Maiúsculo
user = User(status="activo")  # Typo não detectado
user = User(status="banana")  # Valor inválido aceito!
```

**Abordagem 2: Enum Python**
```python
from enum import Enum as PyEnum

class Status(PyEnum):
    ATIVO = "ativo"
    INATIVO = "inativo"

class User(Base):
    status: Mapped[Status] = mapped_column(Enum(Status))

# Uso:
user = User(status=Status.ATIVO)  # IDE sugere valores válidos
user = User(status="ativo")       # Erro! Tipo errado detectado
user = User(status=Status.BANANA) # Erro! Não existe
```

**Por que `PyEnum` (alias para `enum.Enum`)?**

Usamos `from enum import Enum as PyEnum` para evitar confusão com `sqlalchemy.Enum`:
```python
from enum import Enum as PyEnum      # Enum do Python (define os valores)
from sqlalchemy import Enum          # Enum do SQLAlchemy (tipo de coluna SQL)
```

### Por Que server_default ao Invés de default?

Esta é uma distinção crítica para timestamps:

```python
# ❌ ERRADO: default do Python
created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.now()  # Avaliado UMA VEZ quando a classe é definida!
)

# ❌ ERRADO: default com função (parece certo, mas...)
created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.now  # Sem parênteses, avaliado no INSERT
)

# ✅ CORRETO: server_default (banco gera o valor)
created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now()  # Banco de dados gera o timestamp
)
```

**Diferenças**:

| Aspecto | `default=` (Python) | `server_default=` (Banco) |
|---------|---------------------|---------------------------|
| Quem gera o valor | Código Python | Banco de dados |
| Consistência | Depende do relógio da aplicação | Relógio único do banco |
| INSERT direto no banco | Não funciona (valor NULL) | Funciona |
| Múltiplas instâncias da app | Relógios podem diferir | Sempre consistente |
| Aparece na migration | Não | Sim (DEFAULT NOW()) |

**Regra**: Use `server_default` para timestamps automáticos. O banco de dados é a fonte única de verdade para datas.

### Por Que init=False em Campos com Default?

Esta é a regra mais confusa do MappedAsDataclass, mas tem uma razão clara.

**O Problema**: Em Python dataclasses, campos com valor default devem vir **depois** de campos obrigatórios:

```python
@dataclass
class Exemplo:
    obrigatorio: str              # OK: sem default
    opcional: int = 0             # OK: com default, depois do obrigatório
    outro_obrigatorio: str        # ERRO! Obrigatório depois de opcional
```

**Com herança**, os campos da classe pai vêm primeiro:

```python
class Base:
    id: int = 0           # Campo 1: TEM default
    active: bool = True   # Campo 2: TEM default

class User(Base):
    nome: str             # Campo 3: OBRIGATÓRIO (sem default)
    # ERRO! nome (obrigatório) vem depois de active (default)
```

**A Solução**: `init=False` remove o campo do construtor:

```python
class Base:
    id: int = mapped_column(init=False)       # NÃO está no __init__
    active: bool = mapped_column(init=False)  # NÃO está no __init__

class User(Base):
    nome: str = mapped_column()               # Está no __init__

# Construtor gerado:
def __init__(self, nome: str): ...  # Só nome, sem id/active
```

**Regra Prática**:
- Campos auto-gerados (id, timestamps): `init=False`
- Campos com valor padrão na Base: `init=False`
- Relationships: **SEMPRE** `init=False`

### Arquivo: `infra/configs/database.py`

Agora que você entende o porquê, aqui está o código:

```python
"""
Configuração base do SQLAlchemy com MappedAsDataclass.

TODAS as entidades DEVEM herdar desta Base.
"""
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Integer, DateTime, Enum, func
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    Mapped,
    mapped_column
)


class Status(PyEnum):
    """
    Status padrão para soft delete.

    Por que Enum ao invés de string?
    - IDE sugere valores válidos (autocomplete)
    - Typos detectados em tempo de desenvolvimento
    - Refatoração segura (renomear propaga)
    """
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"
    BLOQUEADO = "bloqueado"


class Base(MappedAsDataclass, DeclarativeBase):
    """
    Classe base para todas as entidades.

    REGRAS CRÍTICAS do MappedAsDataclass:
    ┌────────────────────────────────────────────────────────────────────┐
    │ 1. Campos com default na Base → DEVEM ter init=False               │
    │ 2. Relationships → SEMPRE init=False                               │
    │ 3. Relationships → NUNCA default=None (causa bug de FK NULL!)      │
    │ 4. Após INSERT → usar refresh() para obter o ID                    │
    └────────────────────────────────────────────────────────────────────┘
    """
    __abstract__ = True  # Não cria tabela para Base

    # ══════════════════════════════════════════════════════════════════
    # CAMPOS HERDADOS POR TODAS AS ENTIDADES
    # Todos têm init=False: são auto-gerados ou têm default
    # ══════════════════════════════════════════════════════════════════

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        init=False  # Banco gera automaticamente
    )

    # Timestamps: server_default para o BANCO gerar (não o Python)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # Banco gera: DEFAULT NOW()
        init=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # Atualiza automaticamente em UPDATE
        init=False
    )

    # Auditoria de usuário (quem criou/atualizou)
    created_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False,
        default=None
    )

    updated_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False,
        default=None
    )

    # Soft delete
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
        default=None
    )

    deleted_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False,
        default=None
    )

    # Status ativo/inativo
    active: Mapped[Status] = mapped_column(
        Enum(Status),
        default=Status.ATIVO,
        init=False  # CRÍTICO: init=False porque tem default
    )
```

### Por Que Usar Context Manager para Conexões?

Conexões com banco de dados são **recursos escassos**. Se você abrir conexões e esquecer de fechar:

```python
# ❌ Problema: conexões vazando
def get_users():
    session = Session()
    users = session.query(User).all()
    # Esqueceu de fechar! Conexão fica aberta até o processo morrer
    return users

# Depois de algumas requisições:
# OperationalError: too many connections
```

**Context Manager** (`with`) garante que a conexão SEMPRE seja fechada:

```python
# ✅ Correto: conexão sempre fecha
def get_users():
    with DBConnectionHandler() as db:
        users = db.session.query(User).all()
        return users
    # Saiu do with → conexão fechada automaticamente
    # Mesmo se der exceção, __exit__ é chamado
```

### Por Que pool_pre_ping=True?

Conexões podem **morrer silenciosamente** (timeout do servidor, rede instável). Sem `pool_pre_ping`:

```python
# Conexão aberta há 8 horas (timeout do PostgreSQL = 8h)
# Requisição chega:
session.query(User).all()
# ❌ OperationalError: server closed the connection unexpectedly
```

Com `pool_pre_ping=True`, SQLAlchemy faz um "ping" antes de usar:

```python
# SQLAlchemy: "Conexão, você está viva?"
# Conexão: (silêncio - morta)
# SQLAlchemy: "OK, vou criar uma nova"
# (cria nova conexão)
# Requisição funciona normalmente
```

### Arquivo: `infra/configs/connection.py`

```python
"""
Gerenciador de conexão com o banco de dados.

Uso com Context Manager:
    with DBConnectionHandler() as db:
        db.session.query(User).all()
        # commit automático se não houver exceção
        # rollback automático se houver exceção
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from infra.configs.settings import settings


class DBConnectionHandler:
    """
    Context manager para conexões com o banco.

    Por que Context Manager?
    - Garante que conexão seja SEMPRE fechada
    - Commit/rollback automático baseado em exceções
    - Evita "connection leak" (conexões órfãs)
    """

    def __init__(self):
        self._engine = create_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,     # True = loga SQL (útil em dev)
            pool_pre_ping=True       # Verifica se conexão está viva
        )
        self._Session = sessionmaker(bind=self._engine)
        self.session: Session | None = None

    def __enter__(self) -> "DBConnectionHandler":
        """Abre sessão quando entra no 'with'."""
        self.session = self._Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Fecha sessão quando sai do 'with'.

        - Se houve exceção → rollback
        - Se não houve exceção → commit
        """
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def get_engine(self):
        """Retorna engine para criação de tabelas (usado pelo Alembic)."""
        return self._engine


def get_db():
    """
    Dependency injection para FastAPI.

    Uso:
        @app.get("/users")
        def list_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    handler = DBConnectionHandler()
    try:
        handler.session = handler._Session()
        yield handler.session
    finally:
        handler.session.close()
```

---

## 0.4 Variáveis de Ambiente

### Por Que Usar pydantic-settings ao Invés de os.environ?

Compare as abordagens:

**Abordagem 1: os.environ (frágil)**
```python
import os

# ❌ Problemas:
database_url = os.environ["DATABASE_URL"]  # KeyError se não existir
debug = os.environ.get("DEBUG")            # Retorna string "true", não bool
timeout = os.environ.get("TIMEOUT", 30)    # Retorna "30" (string), não int
```

**Abordagem 2: pydantic-settings (robusto)**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str                       # Obrigatório, erro claro se faltar
    DEBUG: bool = False                     # Converte "true"/"false" para bool
    TIMEOUT: int = 30                       # Converte para int automaticamente

settings = Settings()  # Carrega de .env automaticamente
```

**Vantagens do pydantic-settings**:

| Aspecto | os.environ | pydantic-settings |
|---------|------------|-------------------|
| Variável faltando | KeyError genérico | Erro claro dizendo qual falta |
| Conversão de tipos | Manual | Automática (str→bool, str→int) |
| Validação | Nenhuma | Valida tipos e formatos |
| Valores default | `.get(key, default)` | Declarativo na classe |
| Autocomplete IDE | Não | Sim (atributos tipados) |
| Carregar de .env | Manual com python-dotenv | Automático |

### Arquivo: `infra/configs/settings.py`

```python
"""
Configurações centralizadas usando Pydantic Settings.

Carrega variáveis do arquivo .env automaticamente.
Converte tipos (str→bool, str→int) automaticamente.
Valida que variáveis obrigatórias existem.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configurações da aplicação.

    Variáveis são carregadas de:
    1. Variáveis de ambiente do sistema
    2. Arquivo .env no diretório raiz

    Prioridade: variável de ambiente > .env > valor default
    """

    # Aplicação
    APP_NAME: str = "Minha API"
    DEBUG: bool = False  # "true"/"false" convertido automaticamente

    # Banco de dados
    DATABASE_URL: str = "sqlite:///./app.db"

    # Segurança
    SECRET_KEY: str = "sua-chave-secreta-aqui"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # "30" convertido para int

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """Retorna settings cacheado."""
    return Settings()


# Instância global
settings = get_settings()
```

### Arquivo: `.env`

```env
# Aplicação
APP_NAME=Portal de Chamados
DEBUG=true

# Banco de dados
# Desenvolvimento (SQLite)
DATABASE_URL=sqlite:///./portal.db

# Produção (PostgreSQL)
# DATABASE_URL=postgresql://user:password@localhost:5432/portal

# Segurança
SECRET_KEY=sua-chave-super-secreta-mude-em-producao
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Arquivo: `.env.example`

```env
# Copie este arquivo para .env e preencha os valores

# Aplicação
APP_NAME=Minha API
DEBUG=false

# Banco de dados
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Segurança
SECRET_KEY=gere-uma-chave-segura
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Arquivo: `.gitignore`

```gitignore
# Ambiente virtual
venv/
.venv/

# Variáveis de ambiente
.env

# Banco de dados local
*.db
*.sqlite

# Python
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/

# IDE
.vscode/
.idea/

# Logs
*.log
```

---

## 0.5 Alembic - Migrations de Banco de Dados

### O Problema: Como Evoluir o Banco de Dados?

Imagine que você já tem uma aplicação em produção com milhares de registros. Agora precisa adicionar uma coluna nova. O que fazer?

**Opção 1: `create_all()` (NÃO funciona)**
```python
Base.metadata.create_all(engine)
```

O `create_all()` só cria tabelas que **não existem**. Se a tabela já existe:
- ❌ Não adiciona colunas novas
- ❌ Não remove colunas antigas
- ❌ Não altera tipos de dados
- ❌ Não tem histórico de mudanças
- ❌ Não consegue reverter erros

```python
# Versão 1 do model:
class User(Base):
    nome: Mapped[str]

# create_all() cria a tabela users com coluna 'nome'
# Aplicação roda em produção por 6 meses...

# Versão 2 do model:
class User(Base):
    nome: Mapped[str]
    email: Mapped[str]  # Nova coluna!

# create_all() novamente...
# ❌ Coluna 'email' NÃO É CRIADA! Tabela já existe.
```

**Opção 2: DROP e CREATE (PERIGOSO)**
```python
Base.metadata.drop_all(engine)   # Deleta TUDO
Base.metadata.create_all(engine)  # Recria vazio
# ❌ TODOS OS DADOS FORAM PERDIDOS!
```

**Opção 3: SQL manual (propenso a erros)**
```sql
ALTER TABLE users ADD COLUMN email VARCHAR(100);
```
- ❌ Não tem histórico
- ❌ Não sincroniza com o código Python
- ❌ Não consegue reverter
- ❌ Diferentes desenvolvedores podem ter bancos diferentes

### A Solução: Migrations com Alembic

**Migration** é um arquivo que descreve UMA mudança no banco:

```python
# migrations/versions/001_add_email_to_users.py

def upgrade():
    """Aplica a mudança."""
    op.add_column('users', sa.Column('email', sa.String(100)))

def downgrade():
    """Reverte a mudança."""
    op.drop_column('users', 'email')
```

**Vantagens**:

| Aspecto | create_all() | Alembic |
|---------|--------------|---------|
| Criar tabelas novas | ✅ | ✅ |
| Adicionar colunas | ❌ | ✅ |
| Alterar colunas | ❌ | ✅ |
| Histórico de mudanças | ❌ | ✅ (versionado) |
| Reverter mudanças | ❌ | ✅ (downgrade) |
| Múltiplos desenvolvedores | ❌ (bancos diferentes) | ✅ (todos iguais) |
| Produção segura | ❌ | ✅ |

### Como Alembic Funciona?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. VOCÊ ALTERA O MODEL                                                     │
│     class User(Base):                                                       │
│         email: Mapped[str]  # ← Nova coluna                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  2. ALEMBIC DETECTA A DIFERENÇA                                             │
│     alembic revision --autogenerate -m "add email to users"                 │
│     # Compara models Python com tabelas do banco                            │
│     # Gera arquivo de migration automaticamente                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  3. VOCÊ REVISA E APLICA                                                    │
│     # Revisar o arquivo gerado (sempre!)                                    │
│     alembic upgrade head                                                    │
│     # Executa o SQL necessário no banco                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  4. EM PRODUÇÃO                                                             │
│     # Mesmo comando aplica a mudança                                        │
│     alembic upgrade head                                                    │
│     # Banco é atualizado sem perda de dados                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Passo 1: Instalar Alembic

```bash
pip install alembic
```

### Passo 2: Inicializar Alembic

```bash
# Na raiz do projeto
alembic init alembic
```

Isso cria:
```
projeto/
├── alembic/
│   ├── versions/          # Migrations ficam aqui
│   ├── env.py             # Configuração principal
│   ├── script.py.mako     # Template de migration
│   └── README
├── alembic.ini            # Configuração geral
```

### Passo 3: Configurar alembic.ini

⚠️ **CRÍTICO**: O arquivo `alembic.ini` PRECISA ter a seção de logging, senão você receberá o erro:
```
KeyError: 'formatters'
```

Este erro ocorre porque a função `fileConfig()` no `env.py` espera encontrar as seções de logging definidas no arquivo INI.

```ini
# alembic.ini
# ============================================================================
# CONFIGURAÇÃO DO ALEMBIC
# ============================================================================

[alembic]
# Onde estão os scripts de migration
script_location = alembic

# Permite imports relativos (necessário para importar suas entidades)
prepend_sys_path = .

# ============================================================================
# URL DO BANCO DE DADOS
# ============================================================================
# DESENVOLVIMENTO: SQLite local
sqlalchemy.url = sqlite:///database/portal.db

# PRODUÇÃO: PostgreSQL (descomente e configure)
# sqlalchemy.url = postgresql://user:password@localhost:5432/portal

# ============================================================================
# LOGGING - SEÇÃO OBRIGATÓRIA!
# ============================================================================
# Sem estas seções, Alembic retorna: KeyError: 'formatters'
# Isso acontece porque fileConfig() no env.py espera estas configurações

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

**Explicação das seções de logging**:

| Seção | Descrição |
|-------|-----------|
| `[loggers]` | Lista de loggers disponíveis (root, sqlalchemy, alembic) |
| `[handlers]` | Para onde os logs vão (console = terminal) |
| `[formatters]` | Como formatar as mensagens de log |
| `[logger_root]` | Logger padrão, nível WARN = só avisos e erros |
| `[logger_sqlalchemy]` | Logger do SQLAlchemy, WARN para não poluir |
| `[logger_alembic]` | Logger do Alembic, INFO para ver o progresso |
| `[handler_console]` | Envia para stderr (padrão para logs) |
| `[formatter_generic]` | Formato: `LEVEL [nome] mensagem` |

### Passo 4: Configurar env.py

Este é o arquivo mais importante. Ele conecta Alembic às suas entidades.

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ══════════════════════════════════════════════════════════════════
# IMPORTANTE: Importe sua Base e TODAS as entidades
# ══════════════════════════════════════════════════════════════════
from infra.configs.database import Base

# Importar todas as entidades para que Alembic as "veja"
from infra.entities.team import Team
from infra.entities.user import User
from infra.entities.report import Report
from infra.entities.project import Project
from infra.entities.ticket import Ticket
from infra.entities.form import Form
from infra.entities.chat import Chat
from infra.entities.message import Message
from infra.entities.associations import *  # Todas as tabelas de associação

# Configuração do Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Roda migrations em modo 'offline' (gera SQL sem conectar)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Roda migrations em modo 'online' (conecta ao banco)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Passo 5: Criar Primeira Migration

```bash
# Gera migration automaticamente comparando models com banco
alembic revision --autogenerate -m "criar tabelas iniciais"
```

Isso cria um arquivo em `alembic/versions/` como:
```
alembic/versions/
└── 2024_01_15_1234_criar_tabelas_iniciais.py
```

### Passo 6: Revisar a Migration

**SEMPRE revise** o arquivo gerado antes de aplicar:

```python
# alembic/versions/xxxx_criar_tabelas_iniciais.py

def upgrade() -> None:
    op.create_table('teams',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('team_name', sa.String(100), nullable=False),
        # ...
    )
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_team_id', sa.Integer(), sa.ForeignKey('teams.id')),
        # ...
    )

def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('teams')
```

### Passo 7: Aplicar Migration

```bash
# Aplicar todas as migrations pendentes
alembic upgrade head

# Ver status atual
alembic current

# Ver histórico
alembic history
```

### Passo 8: Criar Novas Migrations (quando alterar models)

Sempre que alterar um model:

```bash
# 1. Alterar o model em infra/entities/xxx.py

# 2. Gerar migration
alembic revision --autogenerate -m "adicionar coluna xyz em users"

# 3. Revisar o arquivo gerado

# 4. Aplicar
alembic upgrade head
```

### Comandos Úteis do Alembic

```bash
# Ver migration atual
alembic current

# Ver histórico de migrations
alembic history

# Aplicar até a última
alembic upgrade head

# Aplicar apenas uma
alembic upgrade +1

# Reverter uma migration
alembic downgrade -1

# Reverter todas
alembic downgrade base

# Gerar SQL sem aplicar (para produção)
alembic upgrade head --sql > migration.sql
```

### Fluxo em Produção

```bash
# 1. Em desenvolvimento: crie e teste a migration
alembic revision --autogenerate -m "nova feature"
alembic upgrade head
# Teste a aplicação

# 2. Commit da migration no git
git add alembic/versions/
git commit -m "migration: nova feature"

# 3. Em produção: apenas aplique
alembic upgrade head
```

### Quando Usar `create_all()` vs Alembic?

| Contexto | Use | Por quê |
|----------|-----|---------|
| **Testes automatizados** | `create_all()` | Banco temporário, não precisa de histórico |
| **Prototipagem inicial** | `create_all()` | Ainda não há dados para preservar |
| **Desenvolvimento ativo** | Alembic | Você já tem dados de teste que quer manter |
| **Produção** | Alembic | SEMPRE - dados são valiosos |

**Regra de ouro**: `create_all()` é aceitável para testes e desenvolvimento inicial. Em produção, **SEMPRE use Alembic**.

```python
# ❌ NUNCA faça isso em produção:
Base.metadata.create_all(engine)

# ✅ SEMPRE faça isso:
# $ alembic upgrade head
```

---

## 0.6 SQL Essencial - O Que Você Precisa Saber

Antes de mergulhar no ORM, você precisa entender SQL. O SQLAlchemy **gera SQL** - se você não entende o que está sendo gerado, não consegue debugar, otimizar ou corrigir problemas.

### Por Que Aprender SQL Mesmo Usando ORM?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    POR QUE SQL AINDA É IMPORTANTE?                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. DEBUG: Entender o que o ORM está gerando                               │
│  2. PERFORMANCE: Identificar queries ineficientes                           │
│  3. ANALYTICS: Queries complexas às vezes são mais simples em SQL          │
│  4. MIGRATIONS: Alembic gera SQL que você precisa revisar                   │
│  5. DBA: Comunicar com administradores de banco                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Os 4 Comandos Fundamentais (CRUD)

| Operação | SQL | SQLAlchemy | Descrição |
|----------|-----|------------|-----------|
| **C**reate | `INSERT` | `session.add()` | Inserir novo registro |
| **R**ead | `SELECT` | `session.query()` | Buscar registros |
| **U**pdate | `UPDATE` | `obj.campo = valor` | Modificar registro |
| **D**elete | `DELETE` | `session.delete()` | Remover registro |

#### INSERT (Criar)

```sql
-- SQL
INSERT INTO users (nome, email) VALUES ('Matheus', 'matheus@email.com');

-- Com múltiplos valores
INSERT INTO users (nome, email) VALUES
    ('Ana', 'ana@email.com'),
    ('Carlos', 'carlos@email.com');
```

```python
# SQLAlchemy equivalente (veremos em detalhes no Módulo 1.3)
user = User(nome="Matheus", email="matheus@email.com")
session.add(user)
session.commit()
```

#### SELECT (Ler)

```sql
-- Todos os registros
SELECT * FROM users;

-- Campos específicos
SELECT nome, email FROM users;

-- Com filtro
SELECT * FROM users WHERE id = 1;

-- Com ordenação
SELECT * FROM users ORDER BY nome ASC;

-- Com limite (paginação)
SELECT * FROM users LIMIT 10 OFFSET 20;  -- Página 3, 10 por página
```

```python
# SQLAlchemy equivalente
session.query(User).all()                              # Todos
session.query(User.nome, User.email).all()             # Campos específicos
session.query(User).filter(User.id == 1).first()       # Com filtro
session.query(User).order_by(User.nome).all()          # Com ordenação
session.query(User).limit(10).offset(20).all()         # Paginação
```

#### UPDATE (Atualizar)

```sql
-- Um registro
UPDATE users SET nome = 'Matheus Beck' WHERE id = 1;

-- Múltiplos registros
UPDATE users SET ativo = false WHERE ultimo_login < '2024-01-01';
```

```python
# SQLAlchemy equivalente
user = session.get(User, 1)
user.nome = "Matheus Beck"
session.commit()

# Em massa
session.query(User).filter(User.ultimo_login < data).update({User.ativo: False})
session.commit()
```

#### DELETE (Deletar)

```sql
-- Um registro
DELETE FROM users WHERE id = 1;

-- Múltiplos registros
DELETE FROM users WHERE ativo = false;
```

```python
# SQLAlchemy equivalente
user = session.get(User, 1)
session.delete(user)
session.commit()

# Em massa
session.query(User).filter(User.ativo == False).delete()
session.commit()
```

### WHERE - Filtros

```sql
-- Comparações
WHERE idade > 18
WHERE idade >= 18
WHERE idade < 18
WHERE idade <= 18
WHERE idade = 18
WHERE idade != 18

-- Texto
WHERE nome = 'Matheus'              -- Exato
WHERE nome LIKE 'Mat%'              -- Começa com "Mat"
WHERE nome LIKE '%Silva'            -- Termina com "Silva"
WHERE nome LIKE '%Beck%'            -- Contém "Beck"
WHERE nome ILIKE '%beck%'           -- Case insensitive (PostgreSQL)

-- Listas
WHERE id IN (1, 2, 3)
WHERE status NOT IN ('deletado', 'bloqueado')

-- NULL
WHERE manager_id IS NULL
WHERE manager_id IS NOT NULL

-- Ranges
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'

-- Lógica
WHERE idade > 18 AND status = 'ativo'
WHERE idade < 18 OR status = 'especial'
WHERE NOT (status = 'deletado')
```

### JOIN - Combinando Tabelas

**JOIN** combina dados de duas ou mais tabelas baseado em uma relação (geralmente FK).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TIPOS DE JOIN                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   INNER JOIN: Apenas registros que existem em AMBAS as tabelas              │
│   LEFT JOIN: Todos da esquerda + matches da direita (NULL se não houver)    │
│   RIGHT JOIN: Todos da direita + matches da esquerda (NULL se não houver)   │
│   FULL JOIN: Todos de ambas (NULL onde não houver match)                    │
│                                                                             │
│   users                    teams                                            │
│   ┌────┬─────────┐        ┌────┬─────────┐                                  │
│   │ id │ team_id │        │ id │  nome   │                                  │
│   ├────┼─────────┤        ├────┼─────────┤                                  │
│   │ 1  │    1    │        │ 1  │  Dev    │                                  │
│   │ 2  │    1    │        │ 2  │  QA     │                                  │
│   │ 3  │   NULL  │        │ 3  │  Ops    │  ← Sem usuários                  │
│   └────┴─────────┘        └────┴─────────┘                                  │
│         ↓                                                                    │
│   INNER JOIN: Usuários 1, 2 (apenas com time)                               │
│   LEFT JOIN:  Usuários 1, 2, 3 (3 com team = NULL)                          │
│   RIGHT JOIN: Usuários 1, 2 + time Ops (user = NULL)                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```sql
-- INNER JOIN: Apenas usuários COM time
SELECT users.nome, teams.nome as time
FROM users
INNER JOIN teams ON users.team_id = teams.id;

-- LEFT JOIN: Todos os usuários (com ou sem time)
SELECT users.nome, teams.nome as time
FROM users
LEFT JOIN teams ON users.team_id = teams.id;

-- Múltiplos JOINs
SELECT
    tickets.titulo,
    users.nome as cliente,
    teams.nome as time_responsavel
FROM tickets
INNER JOIN users ON tickets.client_id = users.id
LEFT JOIN teams ON users.team_id = teams.id;
```

Veremos como o SQLAlchemy traduz JOINs automaticamente no **Módulo 2 (Relacionamentos)**.

### GROUP BY e Agregações

**GROUP BY** agrupa registros para aplicar funções de agregação.

```sql
-- Contar usuários por time
SELECT
    teams.nome,
    COUNT(users.id) as total_usuarios
FROM teams
LEFT JOIN users ON users.team_id = teams.id
GROUP BY teams.nome;

-- Resultado:
-- | nome | total_usuarios |
-- |------|----------------|
-- | Dev  | 5              |
-- | QA   | 3              |
-- | Ops  | 0              |
```

**Funções de agregação**:

| Função | Descrição | Exemplo |
|--------|-----------|---------|
| `COUNT(*)` | Conta registros | `COUNT(*)` → 42 |
| `COUNT(campo)` | Conta não-NULL | `COUNT(manager_id)` → 35 |
| `SUM(campo)` | Soma valores | `SUM(valor)` → 1500.00 |
| `AVG(campo)` | Média | `AVG(idade)` → 28.5 |
| `MIN(campo)` | Menor valor | `MIN(created_at)` → '2024-01-01' |
| `MAX(campo)` | Maior valor | `MAX(salario)` → 15000.00 |

Veremos agregações em SQLAlchemy no **Módulo 4 (Analytics)**.

### epoch - Trabalhando com Datas

**epoch** é o número de segundos desde 1 de janeiro de 1970 (Unix timestamp). Usado frequentemente em cálculos de tempo.

```sql
-- EXTRACT epoch: Converte intervalo para segundos
EXTRACT(epoch FROM (closed_at - created_at))

-- Exemplo prático:
-- closed_at = '2024-01-01 14:00:00'
-- created_at = '2024-01-01 12:00:00'
-- Diferença = 2 horas = 7200 segundos

-- Para converter para horas:
EXTRACT(epoch FROM (closed_at - created_at)) / 3600  -- 7200 / 3600 = 2 horas

-- Para converter para dias:
EXTRACT(epoch FROM (closed_at - created_at)) / 86400  -- 86400 = segundos em 1 dia
```

**Por que usar epoch?**
- Cálculos matemáticos são mais simples com números
- Fácil converter para qualquer unidade (segundos → horas → dias)
- Funciona consistentemente em diferentes bancos

---

# MÓDULO 1: FUNDAMENTOS

## 1.1 O Que É ORM e Por Que Usar?

### Conceito: O Problema da Incompatibilidade

Bancos de dados relacionais e linguagens orientadas a objetos vivem em paradigmas diferentes. Essa diferença fundamental é chamada de **impedance mismatch** (incompatibilidade de impedância).

**O Conflito:**

```
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│   MUNDO PYTHON (OOP)            │     │   MUNDO SQL (RELACIONAL)        │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│  • Classes e Objetos            │     │  • Tabelas e Linhas             │
│  • Herança e Polimorfismo       │ ≠   │  • Foreign Keys e JOINs         │
│  • Navegação por referência     │     │  • Queries declarativas         │
│  • user.team.name               │     │  • SELECT com JOIN              │
│  • Listas e coleções            │     │  • Conjuntos de resultados      │
└─────────────────────────────────┘     └─────────────────────────────────┘
```

**ORM (Object-Relational Mapping)** é a ponte que conecta esses dois mundos. Ele traduz automaticamente entre objetos Python e registros SQL, permitindo que você trabalhe com o banco de dados usando código Python natural.

### Definição Formal

**ORM** é uma camada de abstração que:

1. **Mapeia** classes Python para tabelas SQL
2. **Converte** objetos em linhas (e vice-versa)
3. **Traduz** chamadas de métodos em queries SQL
4. **Gerencia** relacionamentos entre entidades automaticamente
5. **Sincroniza** estado entre memória (Python) e disco (banco de dados)

### Analogia: Tradutor Simultâneo

Imagine que você é brasileiro e precisa trabalhar com um time japonês. Um tradutor simultâneo:

- **Traduz** sua fala em português para japonês
- **Converte** idiomas em tempo real
- **Mantém** o contexto e significado
- **Esconde** a complexidade da tradução

Um ORM faz o mesmo entre Python e SQL:

```python
# Você fala "Python":
user = User(name="Matheus", email="matheus@email.com")
session.add(user)
session.commit()

# ORM traduz para "SQL":
INSERT INTO users (name, email) VALUES ('Matheus', 'matheus@email.com');
```

### Por Que Existe?

Desenvolver sem ORM significa:

1. **Escrever SQL manualmente** (strings, interpolação perigosa)
2. **Converter linhas em objetos** manualmente (row[0], row[1]...)
3. **Gerenciar relacionamentos** manualmente (múltiplos SELECTs, JOINs complexos)
4. **Manter sincronizado** código Python e esquema SQL
5. **Lidar com diferentes bancos** (PostgreSQL vs MySQL vs SQLite)

**ORM automatiza tudo isso.**

### Comparação Prática

**❌ SEM ORM (SQL puro com sqlite3)**:
```python
import sqlite3

# Conectar ao banco
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Criar tabela
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE
    )
""")

# Inserir usuário
cursor.execute(
    "INSERT INTO users (name, email) VALUES (?, ?)",
    ("Matheus Beck", "matheus@email.com")
)
conn.commit()

# Buscar usuário
cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
row = cursor.fetchone()

# Converter para dicionário manualmente
user_dict = {
    'id': row[0],
    'name': row[1],
    'email': row[2]
}

print(user_dict)

# Atualizar
cursor.execute(
    "UPDATE users SET name = ? WHERE id = ?",
    ("Matheus Silva Beck", 1)
)
conn.commit()

# Deletar
cursor.execute("DELETE FROM users WHERE id = ?", (1,))
conn.commit()

conn.close()
```

**✅ COM ORM (SQLAlchemy)**:
```python
from sqlalchemy.orm import Session
from models import User

# Criar usuário
user = User(
    name="Matheus Beck",
    email="matheus@email.com"
)
session.add(user)
session.commit()

# Buscar usuário
user = session.query(User).filter(User.id == 1).first()
print(user.name)  # Acesso direto ao atributo

# Atualizar
user.name = "Matheus Silva Beck"
session.commit()

# Deletar
session.delete(user)
session.commit()
```

### Tabela Comparativa

| Aspecto | SQL Puro | SQLAlchemy ORM |
|---------|----------|----------------|
| **Linhas de código** | ~40 linhas | ~15 linhas |
| **Legibilidade** | SQL strings | Python puro |
| **Type hints** | ❌ Não funciona | ✅ Funciona |
| **IDE autocomplete** | ❌ Limitado | ✅ Completo |
| **Refatoração** | ❌ Difícil (strings) | ✅ Fácil (IDE ajuda) |
| **Portabilidade** | ❌ Preso ao banco | ✅ Funciona em vários bancos |
| **Relacionamentos** | ❌ Manual (JOINs) | ✅ Automático |
| **Validação** | ❌ Manual | ✅ Integrada |
| **Performance** | ✅ Ótima (se otimizado) | ⚠️ Boa (pode gerar SQL subótimo) |
| **Curva aprendizado** | Baixa (SQL é padrão) | Alta (conceitos ORM) |

### Prós do ORM

✅ **Produtividade**: Código mais limpo e rápido de escrever
✅ **Type Safety**: Type hints funcionam, IDE detecta erros
✅ **Manutenibilidade**: Mais fácil refatorar e entender
✅ **Portabilidade**: Troca PostgreSQL ↔ MySQL sem mudar código
✅ **Relacionamentos**: Navegação entre objetos é natural
✅ **Validação**: Integração com Pydantic para validação automática
✅ **Migrations**: Ferramentas como Alembic geram migrations automaticamente

### Contras do ORM

❌ **Curva de Aprendizado**: Precisa entender conceitos ORM além de SQL
❌ **SQL Subótimo**: Pode gerar queries ineficientes se mal usado
❌ **Overhead**: Performance ~5-10% menor (geralmente imperceptível)
❌ **Debugging**: Às vezes difícil saber que SQL está sendo executado
❌ **Queries Complexas**: Algumas queries são mais simples em SQL puro

### Quando Usar ORM?

✅ **USE ORM** quando:
- CRUD típico (95% dos casos)
- APIs REST
- Aplicações web
- Projetos médio/grande porte
- Múltiplos desenvolvedores
- Produtividade importa mais que performance extrema

❌ **USE SQL PURO** quando:
- Data warehousing / ETL pesado
- Queries extremamente complexas com múltiplos subqueries
- Otimização crítica de performance (cada ms conta)
- Scripts one-off de migração
- Reporting com agregações complexas

⚖️ **USE HÍBRIDO** (melhor de ambos):
```python
# ORM para CRUD
user = session.query(User).filter(User.id == 1).first()

# SQL puro para query complexa
result = session.execute(text("""
    SELECT
        u.name,
        COUNT(t.id) as total_tickets,
        AVG(EXTRACT(epoch FROM (t.closed_at - t.created_at)) / 3600) as avg_hours
    FROM users u
    LEFT JOIN tickets t ON t.client_id = u.id
    GROUP BY u.name
    HAVING COUNT(t.id) > 100
    ORDER BY avg_hours DESC
"""))
```

---

## 1.2 Anatomia de um Model SQLAlchemy

### Entendendo o Conceito de Model

Um **Model** (ou **Entidade**) em SQLAlchemy é uma classe Python que representa uma tabela no banco de dados. Mas é mais do que uma simples estrutura de dados - é um **objeto vivo** que:

1. **Descreve** a estrutura da tabela (metadados)
2. **Valida** dados antes de salvar
3. **Gerencia** relacionamentos com outras tabelas
4. **Encapsula** comportamentos e regras de negócio
5. **Sincroniza** automaticamente com o banco de dados

### O Ciclo de Vida de um Model

```
DEFINIÇÃO (Código Python)
    ↓
METADATA (Instruções para criar tabela)
    ↓
CREATE TABLE (Alembic/migrations geram SQL)
    ↓
INSTÂNCIA (Objetos Python representando linhas)
    ↓
PERSISTÊNCIA (Session sincroniza com banco)
```

**Importante**: O model em si NÃO cria a tabela automaticamente em produção. Isso é feito por ferramentas de migração (Alembic). O model apenas:
- **Descreve** como a tabela deve ser
- **Valida** dados em tempo de execução
- **Facilita** operações CRUD

### Camadas de um Model

Um model SQLAlchemy tem 3 camadas distintas:

```python
class User(Base):  # ← Camada 1: Herança (conecta ao sistema ORM)

    __tablename__ = "users"  # ← Camada 2: Metadata (informações sobre a tabela)

    id: Mapped[int] = mapped_column(...)  # ← Camada 3: Colunas (estrutura de dados)

    def __repr__(self):  # ← Camada 4 (opcional): Comportamentos
        return f"<User {self.id}>"
```

Vamos explorar cada uma dessas camadas em detalhes.

### Estrutura Básica (Exemplo Completo Comentado)

```python
from sqlalchemy import Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from infra.configs.database import Base
from datetime import datetime

class User(Base):
    # ═══════════════════════════════════════════════
    # 1. METADATA DA TABELA
    # ═══════════════════════════════════════════════
    __tablename__ = "users"  # Nome da tabela no banco de dados

    # ═══════════════════════════════════════════════
    # 2. COLUNAS FÍSICAS (armazenadas no banco)
    # ═══════════════════════════════════════════════

    # Sintaxe SQLAlchemy 2.0+ (type hints obrigatórios):
    # nome_campo: Mapped[tipo_python] = mapped_column(tipo_sql, opções)

    # Chave primária (sempre obrigatória)
    id: Mapped[int] = mapped_column(
        Integer,           # Tipo no SQL: INTEGER
        primary_key=True,  # Define como chave primária
        autoincrement=True # Auto incremento (padrão para INTEGER PRIMARY KEY)
    )

    # Campo de texto obrigatório
    user_full_name: Mapped[str] = mapped_column(
        String(200),       # VARCHAR(200) no SQL
        nullable=False,    # NOT NULL (obrigatório)
        index=True         # Cria índice (busca mais rápida)
    )

    # Campo único (não pode repetir)
    user_email: Mapped[str] = mapped_column(
        String(100),
        unique=True,       # UNIQUE constraint
        nullable=False
    )

    # Campo booleano com valor padrão
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True       # Valor padrão em Python
    )

    # Campo opcional (pode ser None/NULL)
    user_photo: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True      # Pode ser NULL
    )

    # Timestamp automático (criação)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()  # Valor padrão no banco (CURRENT_TIMESTAMP)
    )

    # Timestamp automático (atualização)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),  # Atualiza automaticamente
        nullable=True
    )

    # ═══════════════════════════════════════════════
    # 3. MÉTODOS (opcional, mas útil)
    # ═══════════════════════════════════════════════

    def __repr__(self) -> str:
        """Representação para debug"""
        return f"<User(id={self.id}, name='{self.user_full_name}')>"

    def __str__(self) -> str:
        """Representação para usuário"""
        return self.user_full_name
```

### SQL Gerado

O código acima gera automaticamente:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_full_name VARCHAR(200) NOT NULL,
    user_email VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    user_photo VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX ix_users_user_full_name ON users(user_full_name);
```

### Explicação Detalhada da Sintaxe

#### O Que Significa `Mapped[tipo]`?

**`Mapped[]`** é um tipo genérico (type hint) introduzido no SQLAlchemy 2.0 que serve para:

1. **Documentar** o tipo do atributo para IDEs e desenvolvedores
2. **Validar** tipos em tempo de desenvolvimento (mypy, pylance)
3. **Inferir** automaticamente o tipo SQL correspondente
4. **Habilitar** autocomplete avançado nas IDEs

**Antes (SQLAlchemy 1.x):**
```python
# Sem type hints claros
class User(Base):
    name = Column(String)  # IDE não sabe que isso é str
```

**Agora (SQLAlchemy 2.0+):**
```python
# Type hints explícitos e autocomplete funciona
class User(Base):
    name: Mapped[str] = mapped_column(String)  # IDE sabe que é str
```

#### Anatomia Completa de uma Coluna

```python
user_email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
#     ↓         ↓                ↓            ↓              ↓
#     │         │                │            │              │
#     │         │                │            │              └─────── 4. Constraint (NOT NULL)
#     │         │                │            └──────────────────── 3. Constraint (UNIQUE)
#     │         │                └───────────────────────────────── 2. Tipo SQL (VARCHAR(100))
#     │         └────────────────────────────────────────────────── 1b. Tipo Python (str)
#     └──────────────────────────────────────────────────────────── 1a. Nome do campo
```

**Decompondo**:

```python
user_email              # 1a. Nome do atributo Python
                        #     - Também será o nome da coluna no banco
                        #     - Use snake_case

Mapped[str]             # 1b. Tipo Python esperado
                        #     - str: campo obrigatório (não aceita None)
                        #     - str | None: campo opcional (aceita None)
                        #     - IDE usa para autocomplete
                        #     - mypy usa para validação estática

mapped_column(...)      # Função que cria a coluna
                        #     - Retorna um objeto Column
                        #     - Contém todas as informações para o banco

String(100)             # 2. Tipo SQL
                        #     - VARCHAR(100) no PostgreSQL/MySQL
                        #     - TEXT(100) no SQLite
                        #     - Pode ser omitido (inferido de Mapped[str])

unique=True             # 3. Constraint UNIQUE
                        #     - Garante que valores não se repetem
                        #     - CREATE UNIQUE INDEX automaticamente

nullable=False          # 4. Constraint NOT NULL
                        #     - Garante que campo não pode ser NULL
                        #     - Se Mapped[str] (sem | None), nullable=False é inferido
```

#### A Dualidade: Tipo Python vs Tipo SQL

**Por que dois tipos?**

SQLAlchemy precisa saber **dois** tipos diferentes:

```python
user_age: Mapped[int] = mapped_column(Integer)
#              ↓                         ↓
#         Tipo Python              Tipo SQL
#         (em memória)          (no disco/banco)
```

**Tipo Python** (`Mapped[int]`):
- Para código Python (if, for, funções)
- Para IDE (autocomplete, validação)
- Para type checkers (mypy, pylance)
- Existe apenas durante execução

**Tipo SQL** (`Integer`):
- Para banco de dados (CREATE TABLE)
- Para queries (WHERE, SELECT)
- Para validações do banco (CHECK, DEFAULT)
- Persiste no disco

**Fluxo de conversão:**

```
Python (memória) → SQLAlchemy → SQL (disco)
     int         →   Integer   →  INTEGER
     str         →   String    →  VARCHAR
     bool        →   Boolean   →  BOOLEAN
     datetime    →   DateTime  →  TIMESTAMP
```

#### Quando Omitir o Tipo SQL

SQLAlchemy 2.0 consegue **inferir** o tipo SQL do tipo Python em casos simples:

```python
# PODE omitir:
user_name: Mapped[str] = mapped_column()  # Infere String
user_age: Mapped[int] = mapped_column()   # Infere Integer
is_active: Mapped[bool] = mapped_column() # Infere Boolean

# DEVE especificar:
user_email: Mapped[str] = mapped_column(String(100))  # Precisa do tamanho
description: Mapped[str] = mapped_column(Text)        # String vs Text
price: Mapped[Decimal] = mapped_column(Numeric(10,2)) # Precisão específica
```

**Regra prática**: Se o tipo SQL precisa de **parâmetros** (tamanho, precisão), especifique. Caso contrário, pode omitir.

#### Tabela de Correspondências

| Tipo Python | Mapped[] | Tipo SQL (inferido) | Tipo SQL (explícito) |
|-------------|----------|---------------------|----------------------|
| `int` | `Mapped[int]` | `Integer` | `Integer` |
| `str` | `Mapped[str]` | `String` | `String(n)`, `Text` |
| `bool` | `Mapped[bool]` | `Boolean` | `Boolean` |
| `float` | `Mapped[float]` | `Float` | `Float`, `Double` |
| `Decimal` | `Mapped[Decimal]` | `Numeric` | `Numeric(precision, scale)` |
| `datetime` | `Mapped[datetime]` | `DateTime` | `DateTime(timezone=True)` |
| `date` | `Mapped[date]` | `Date` | `Date` |
| `bytes` | `Mapped[bytes]` | `LargeBinary` | `LargeBinary` |
| `dict` | `Mapped[dict]` | `JSON` | `JSON` |
| `Enum` | `Mapped[MyEnum]` | - | `Enum(MyEnum)` |

#### Opcional vs Obrigatório

```python
# Campo OBRIGATÓRIO (NOT NULL)
user_name: Mapped[str] = mapped_column()
#                 ↑
#             Sem | None → nullable=False automático

# Campo OPCIONAL (pode ser NULL)
user_photo: Mapped[str | None] = mapped_column()
#                      ↑
#                  | None → nullable=True automático

# Explicit is better than implicit (pode deixar explícito também):
user_name: Mapped[str] = mapped_column(nullable=False)
user_photo: Mapped[str | None] = mapped_column(nullable=True)
```

**Componentes Finais**:

1. **`user_email`**: Nome do atributo Python (e nome da coluna no banco)
2. **`Mapped[str]`**: Tipo esperado no Python (str obrigatório) - usado por IDE e mypy
3. **`Mapped[str | None]`**: Tipo esperado no Python (str ou None) - campo opcional
4. **`mapped_column()`**: Função que define a coluna no banco
5. **`String(100)`**: Tipo SQL (VARCHAR(100)) - pode ser inferido em casos simples
6. **`unique=True`**: Constraint UNIQUE - valor não pode repetir
7. **`nullable=False`**: Constraint NOT NULL - valor obrigatório (inferido se Mapped[str] sem | None)

---

## 1.2.5 Session - O Coração do SQLAlchemy

### O Que É Session?

A **Session** é o objeto central do SQLAlchemy. Ela é responsável por:

1. **Rastrear** objetos carregados do banco (Identity Map)
2. **Gerenciar** transações (BEGIN, COMMIT, ROLLBACK)
3. **Sincronizar** mudanças entre Python e banco (Unit of Work)
4. **Cachear** objetos para evitar queries repetidas

**Analogia**: A Session é como um "carrinho de compras" no e-commerce. Você adiciona itens (objetos), modifica quantidades (atualiza atributos), remove itens - mas nada é cobrado (salvo no banco) até você finalizar a compra (commit).

### Estados de um Objeto

Um objeto SQLAlchemy pode estar em 5 estados diferentes em relação à Session:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CICLO DE VIDA DO OBJETO                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────┐   add()    ┌──────────┐   flush()   ┌────────────┐          │
│   │TRANSIENT │ ────────► │ PENDING  │ ──────────► │ PERSISTENT │          │
│   │(novo)    │           │(na sessão)│             │ (no banco) │          │
│   └──────────┘           └──────────┘             └────────────┘          │
│        ↑                                                │                   │
│        │ User()                          expunge() ou   │                   │
│        │                                 close()        ▼                   │
│                                              ┌────────────┐                 │
│                                              │  DETACHED  │                 │
│                                              │(fora sessão)│                 │
│                                              └────────────┘                 │
│                                                                             │
│   delete() + flush()                                                        │
│        │                                                                    │
│        ▼                                                                    │
│   ┌──────────┐                                                              │
│   │ DELETED  │                                                              │
│   │(marcado) │                                                              │
│   └──────────┘                                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Explicação de cada estado**:

| Estado | Descrição | Na Session? | No Banco? |
|--------|-----------|-------------|-----------|
| **Transient** | Objeto criado, não adicionado | ❌ | ❌ |
| **Pending** | Adicionado com `add()`, aguardando flush | ✅ | ❌ |
| **Persistent** | Sincronizado com banco (após flush/commit) | ✅ | ✅ |
| **Detached** | Foi removido da session (expunge/close) | ❌ | ✅ |
| **Deleted** | Marcado para deleção (após flush do delete) | ✅ | ❌ |

```python
from sqlalchemy.orm import Session
from sqlalchemy import inspect

# TRANSIENT: Objeto criado, não na session
user = User(user_full_name="Matheus", user_email="matheus@email.com")
print(inspect(user).transient)  # True

# PENDING: Adicionado à session, ainda não no banco
session.add(user)
print(inspect(user).pending)  # True

# PERSISTENT: Após flush ou commit, sincronizado com banco
session.flush()  # Ou session.commit()
print(inspect(user).persistent)  # True
print(user.id)  # Agora tem ID!

# DETACHED: Removido da session
session.expunge(user)
print(inspect(user).detached)  # True

# Tentar acessar relationships de objeto detached:
# user.team  # ❌ DetachedInstanceError!
```

### flush() vs commit() - A Diferença Crucial

Esta é uma das confusões mais comuns em SQLAlchemy:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          flush() vs commit()                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   flush()                              commit()                              │
│   ┌─────────────────────┐             ┌─────────────────────┐              │
│   │ • Envia SQL ao banco │             │ • Chama flush()     │              │
│   │ • NÃO finaliza       │             │ • Finaliza transação│              │
│   │   transação          │             │ • Torna permanente  │              │
│   │ • Pode ser revertido │             │ • NÃO pode reverter │              │
│   │   com rollback()     │             │ • Inicia nova       │              │
│   │ • Automático antes   │             │   transação         │              │
│   │   de queries         │             │                     │              │
│   └─────────────────────┘             └─────────────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Exemplo prático**:

```python
# Cenário: Criar usuário e ticket em uma transação

# Passo 1: Criar usuário
user = User(user_full_name="Ana", user_email="ana@email.com", user_team_id=1)
session.add(user)
session.flush()  # SQL enviado, user.id disponível, mas NÃO commitado
print(user.id)  # 42

# Passo 2: Criar ticket usando o ID do usuário
ticket = Ticket(
    ticket_title="Bug report",
    ticket_client_id=user.id,  # Usa o ID gerado
    ticket_status=TicketStatus.ABERTO
)
session.add(ticket)

# Passo 3: Algo deu errado?
if algo_errado:
    session.rollback()  # REVERTE TUDO (user E ticket)
    # user.id volta a ser None!
else:
    session.commit()  # Torna permanente
```

**Quando usar flush() explicitamente**:

1. **Precisa do ID antes do commit**:
   ```python
   session.add(user)
   session.flush()  # Agora user.id está disponível
   ticket.client_id = user.id  # Usa o ID
   ```

2. **Validar constraints antes de continuar**:
   ```python
   try:
       session.add(user)
       session.flush()  # Testa se email é único AGORA
   except IntegrityError:
       session.rollback()
       raise ValueError("Email já existe")
   ```

3. **Em repositories (deixar commit pro service)**:
   ```python
   class UserRepository:
       def create(self, user):
           self.session.add(user)
           self.session.flush()  # Não commit aqui!
           return user

   class UserService:
       def create_user_with_ticket(self, ...):
           user = self.user_repo.create(user)
           ticket = self.ticket_repo.create(ticket)
           self.session.commit()  # Commit aqui - uma transação
   ```

**Por que essa separação?**

A separação entre `flush()` no Repository e `commit()` no Service segue o princípio de **atomicidade transacional**:

- **Repository não sabe se é a última operação** - ele faz sua parte e passa adiante
- **Service sabe o contexto completo** - ele orquestra múltiplas operações
- **Transações são atômicas** - ou TUDO funciona ou NADA funciona

```python
class UserService:
    def create_user_with_audit(self, user_data):
        # Operação 1: Criar usuário
        user = self.user_repo.create(user)  # flush() interno

        # Operação 2: Registrar auditoria
        self.audit_repo.log_create(user.id)  # flush() interno

        # Se audit falhar, user também não é salvo!
        self.db.commit()  # Torna AMBOS permanentes
```

Se o `audit_repo.log_create()` falhar antes do commit, o rollback desfaz TUDO - inclusive o usuário. Isso garante consistência dos dados.

### Identity Map - O Cache da Session

A Session mantém um **Identity Map** - um dicionário que mapeia (tabela, id) → objeto Python.

```python
# Query 1: Busca user 1
user1 = session.get(User, 1)
print(id(user1))  # 140234567890

# Query 2: Busca user 1 novamente
user2 = session.get(User, 1)
print(id(user2))  # 140234567890 - MESMO OBJETO!

# São o mesmo objeto em memória!
print(user1 is user2)  # True

# NENHUMA query SQL foi executada na segunda chamada!
# Session retornou do cache (Identity Map)
```

**Por que isso importa?**

1. **Performance**: Evita queries repetidas
2. **Consistência**: Mesmo objeto, mesmas mudanças
3. **Memória**: Cuidado com sessions de longa duração

**Problema com sessions longas**:
```python
# ❌ Session acumula objetos em memória
session = Session()
for i in range(1_000_000):
    user = session.get(User, i)  # Todos ficam no Identity Map!
# Memória explode!

# ✅ Solução: expire_all() ou nova session
session = Session()
for batch in batches:
    for user_id in batch:
        user = session.get(User, user_id)
    session.expire_all()  # Limpa cache, permite GC
```

### expire_on_commit

Após `commit()`, a Session "expira" todos os objetos por padrão. Isso significa que o próximo acesso fará uma nova query.

```python
user = session.get(User, 1)
print(user.user_full_name)  # "Matheus" - do cache

session.commit()  # Expira todos os objetos

print(user.user_full_name)  # Nova query! Pode ter mudado no banco
```

**Controlar este comportamento**:
```python
# Desabilitar expire_on_commit (cuidado!)
Session = sessionmaker(bind=engine, expire_on_commit=False)

# Ou usar refresh() explícito
session.commit()
session.refresh(user)  # Recarrega do banco
```

### Resumo: Quando Usar O Quê

| Operação | Quando Usar |
|----------|-------------|
| `add()` | Adicionar objeto novo à session |
| `flush()` | Enviar SQL sem finalizar transação (precisa do ID, validar constraints) |
| `commit()` | Finalizar transação, tornar mudanças permanentes |
| `rollback()` | Desfazer mudanças da transação atual |
| `refresh(obj)` | Recarregar objeto do banco |
| `expire(obj)` | Marcar objeto para recarregar no próximo acesso |
| `expire_all()` | Marcar todos os objetos para recarregar |
| `expunge(obj)` | Remover objeto da session (detach) |
| `close()` | Fechar session (expunge all + rollback) |

---

## 1.3 CRUD Básico - As 4 Operações Fundamentais

### Setup Inicial

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Criar engine (conexão com banco)
engine = create_engine("sqlite:///database.db", echo=True)  # echo=True mostra SQL

# Criar todas as tabelas
Base.metadata.create_all(engine)

# Criar session factory
SessionLocal = sessionmaker(bind=engine)

# Usar session
session = SessionLocal()
```

### CREATE - Criar Registros

#### Método 1: Um por vez

```python
def create_user(session: Session, name: str, email: str) -> User:
    """Cria um usuário no banco"""

    # Passo 1: Criar objeto Python
    user = User(
        user_full_name=name,
        user_email=email,
        is_active=True
    )

    # Passo 2: Adicionar à sessão (staging)
    session.add(user)

    # Passo 3: Commit (salva no banco)
    session.commit()

    # Passo 4: Refresh (pega ID gerado e outros campos com defaults)
    session.refresh(user)

    print(f"Usuário criado com ID: {user.id}")
    return user

# Uso:
user = create_user(session, "Matheus Beck", "matheus@email.com")
```

**SQL Gerado**:
```sql
INSERT INTO users (user_full_name, user_email, is_active, created_at)
VALUES ('Matheus Beck', 'matheus@email.com', true, CURRENT_TIMESTAMP)
RETURNING id, created_at;
```

#### Método 2: Em massa (bulk insert)

```python
def create_many_users(session: Session, users_data: list[dict]) -> list[User]:
    """Cria múltiplos usuários de uma vez (mais eficiente)"""

    # Criar lista de objetos
    users = [User(**data) for data in users_data]

    # Adicionar todos de uma vez
    session.add_all(users)

    # Commit único
    session.commit()

    # Refresh todos (para pegar IDs)
    for user in users:
        session.refresh(user)

    return users

# Uso:
users_data = [
    {"user_full_name": "Ana Silva", "user_email": "ana@email.com"},
    {"user_full_name": "Carlos Santos", "user_email": "carlos@email.com"},
    {"user_full_name": "Julia Costa", "user_email": "julia@email.com"},
]

users = create_many_users(session, users_data)
```

**Comparação de Performance**:

| Método | 1 registro | 100 registros | 10,000 registros |
|--------|------------|---------------|------------------|
| Um por vez | ~5ms | ~500ms | ~50s |
| Bulk insert | ~5ms | ~50ms | ~2s |

#### Método 3: Bulk insert SEM objetos (máxima performance)

```python
def bulk_insert_users(session: Session, users_data: list[dict]):
    """Inserção em massa SEM criar objetos Python"""

    session.execute(
        User.__table__.insert(),
        users_data
    )
    session.commit()

# Uso:
bulk_insert_users(session, users_data)  # ~10x mais rápido
```

**Trade-offs**:

| Método | Performance | Validação | Retorna objetos | Quando usar |
|--------|-------------|-----------|-----------------|-------------|
| `add()` | Lento | ✅ Sim | ✅ Sim | 1-10 registros |
| `add_all()` | Médio | ✅ Sim | ✅ Sim | 10-1000 registros |
| `bulk_insert()` | Rápido | ❌ Não | ❌ Não | 1000+ registros, ETL |

### READ - Ler Registros

#### Busca Básica

```python
# Por ID (chave primária) - mais rápido
user = session.get(User, 1)
if user:
    print(user.user_full_name)

# Por outro campo - precisa de query
user = session.query(User).filter(User.user_email == "matheus@email.com").first()

# Retorna None se não encontrar
if user is None:
    print("Usuário não encontrado")
```

**SQL Gerado**:
```sql
-- session.get(User, 1):
SELECT * FROM users WHERE id = 1;

-- query().filter().first():
SELECT * FROM users WHERE user_email = 'matheus@email.com' LIMIT 1;
```

#### Múltiplos Registros

```python
# Todos os registros (⚠️ CUIDADO: pode sobrecarregar memória!)
all_users = session.query(User).all()

# Com filtro
active_users = session.query(User).filter(User.is_active == True).all()

# Com limite (paginação)
first_20 = session.query(User).limit(20).all()

# Com offset (página 3, 20 por página)
page_3 = session.query(User).limit(20).offset(40).all()

# Com ordenação
users_by_name = session.query(User).order_by(User.user_full_name).all()
users_desc = session.query(User).order_by(User.created_at.desc()).all()

# Contar registros (SEM carregar dados)
total = session.query(User).count()
active_count = session.query(User).filter(User.is_active == True).count()
```

#### Filtros Avançados

```python
from sqlalchemy import and_, or_, not_

# AND (E lógico) - Método 1
users = session.query(User).filter(
    and_(
        User.is_active == True,
        User.user_email.like("%@gmail.com")
    )
).all()

# AND - Método 2 (mais limpo, vírgula = AND)
users = session.query(User).filter(
    User.is_active == True,
    User.user_email.like("%@gmail.com")
).all()

# OR (OU lógico)
users = session.query(User).filter(
    or_(
        User.user_email == "matheus@email.com",
        User.user_email == "ana@email.com"
    )
).all()

# NOT (negação)
inactive_users = session.query(User).filter(
    not_(User.is_active == True)
).all()
# Ou mais simples:
inactive_users = session.query(User).filter(User.is_active != True).all()

# IN (dentro de lista)
specific_users = session.query(User).filter(
    User.id.in_([1, 2, 3, 4, 5])
).all()

# NOT IN
other_users = session.query(User).filter(
    User.id.notin_([1, 2, 3])
).all()

# LIKE (padrões de texto)
users = session.query(User).filter(
    User.user_full_name.like("Matheus%")  # Começa com "Matheus"
).all()

users = session.query(User).filter(
    User.user_full_name.like("%Silva%")  # Contém "Silva"
).all()

# ILIKE (case insensitive - PostgreSQL)
users = session.query(User).filter(
    User.user_full_name.ilike("%silva%")  # "Silva", "SILVA", "silva"
).all()

# IS NULL
users_without_photo = session.query(User).filter(
    User.user_photo.is_(None)
).all()

# IS NOT NULL
users_with_photo = session.query(User).filter(
    User.user_photo.isnot(None)
).all()

# BETWEEN
from datetime import datetime, timedelta

last_week = datetime.now() - timedelta(days=7)
recent_users = session.query(User).filter(
    User.created_at.between(last_week, datetime.now())
).all()

# Comparações
recent = session.query(User).filter(User.created_at > last_week).all()
old = session.query(User).filter(User.created_at <= last_week).all()
```

#### Queries para Grandes Volumes

```python
# ❌ NÃO FAÇA: Carrega tudo na memória
all_users = session.query(User).all()  # 1 milhão de users = crash!

# ✅ FAÇA: Itere em batches
for user in session.query(User).yield_per(1000):
    process_user(user)  # Processa 1000 por vez
```

### UPDATE - Atualizar Registros

#### Método 1: Objeto individual (recomendado para poucos registros)

```python
def update_user_name(session: Session, user_id: int, new_name: str) -> User | None:
    """Atualiza nome do usuário"""

    # Buscar usuário
    user = session.get(User, user_id)

    if user:
        # Modificar atributo
        user.user_full_name = new_name

        # Commit (atualiza no banco)
        session.commit()

        # Refresh (pega updated_at atualizado)
        session.refresh(user)

    return user

# Uso:
user = update_user_name(session, 1, "Matheus Silva Beck")
```

**SQL Gerado**:
```sql
UPDATE users
SET user_full_name = 'Matheus Silva Beck', updated_at = CURRENT_TIMESTAMP
WHERE id = 1;
```

#### Método 2: Update em massa (eficiente para muitos registros)

```python
def deactivate_users_by_domain(session: Session, domain: str) -> int:
    """Desativa todos os usuários de um domínio"""

    affected_rows = (
        session.query(User)
        .filter(User.user_email.like(f"%@{domain}"))
        .update({User.is_active: False})
    )

    session.commit()

    return affected_rows  # Número de linhas afetadas

# Uso:
count = deactivate_users_by_domain(session, "oldcompany.com")
print(f"{count} usuários desativados")
```

**SQL Gerado**:
```sql
UPDATE users
SET is_active = false
WHERE user_email LIKE '%@oldcompany.com';
```

#### Comparação de Performance

| Método | 1 registro | 100 registros | 10,000 registros |
|--------|------------|---------------|------------------|
| Objeto individual | ~5ms | ~500ms | ~50s |
| Update em massa | ~5ms | ~10ms | ~100ms |

**Trade-offs**:

| Método | Performance | Validação Python | Triggers | updated_at automático |
|--------|-------------|------------------|----------|----------------------|
| Objeto | Lento | ✅ Sim | ✅ Sim | ✅ Sim |
| Massa | Rápido | ❌ Não | ⚠️ Depende | ⚠️ Precisa configurar |

### DELETE - Deletar Registros

#### Hard Delete vs Soft Delete

**⚠️ CONCEITO IMPORTANTE**:

- **Hard Delete**: Remove permanentemente do banco (DELETE FROM)
- **Soft Delete**: Marca como deletado (UPDATE deleted_at = NOW())

#### Implementação: Soft Delete (RECOMENDADO)

```python
# 1. Adicionar coluna ao model
class User(Base):
    __tablename__ = "users"

    # ... outros campos ...

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )

    deleted_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

# 2. Método de soft delete
def soft_delete_user(session: Session, user_id: int, deleted_by_user_id: int):
    """Marca usuário como deletado"""
    user = session.get(User, user_id)

    if user and user.deleted_at is None:  # Só deleta se não foi deletado antes
        user.deleted_at = datetime.now()
        user.deleted_by = deleted_by_user_id
        session.commit()

    return user

# 3. Queries ignoram deletados
def get_active_users(session: Session):
    """Retorna apenas usuários não deletados"""
    return session.query(User).filter(User.deleted_at.is_(None)).all()

# 4. Restaurar usuário deletado
def restore_user(session: Session, user_id: int):
    """Restaura usuário deletado"""
    user = session.get(User, user_id)

    if user and user.deleted_at is not None:
        user.deleted_at = None
        user.deleted_by = None
        session.commit()

    return user
```

**Vantagens do Soft Delete**:
- ✅ Auditoria completa (quem deletou, quando)
- ✅ Recuperação fácil
- ✅ Mantém integridade referencial
- ✅ Análises históricas

**Desvantagens do Soft Delete**:
- ❌ Banco cresce continuamente
- ❌ Queries mais complexas (sempre filtrar deleted_at)
- ❌ Índices únicos problemáticos (email deletado pode ser reutilizado?)

#### Hard Delete (usar com cautela)

```python
def hard_delete_user(session: Session, user_id: int):
    """Remove usuário permanentemente (⚠️ IRREVERSÍVEL)"""
    user = session.get(User, user_id)

    if user:
        session.delete(user)
        session.commit()

    return user

# Delete em massa
def hard_delete_inactive_users(session: Session) -> int:
    """Remove todos os usuários inativos (⚠️ IRREVERSÍVEL)"""
    count = (
        session.query(User)
        .filter(User.is_active == False)
        .delete()
    )
    session.commit()

    return count
```

**SQL Gerado**:
```sql
DELETE FROM users WHERE id = 1;
DELETE FROM users WHERE is_active = false;
```

**Quando usar Hard Delete**:
- ✅ Dados temporários (sessions, tokens)
- ✅ Logs muito antigos (após arquivamento)
- ✅ Dados de teste
- ✅ GDPR / "direito ao esquecimento"

**Quando NÃO usar Hard Delete**:
- ❌ Dados de negócio (users, tickets, projetos)
- ❌ Dados financeiros
- ❌ Qualquer coisa que precise de auditoria

---

## 1.4 Tipos de Dados e Opções de Colunas

### Tipos Comuns

| Tipo Python | SQLAlchemy | SQL (PostgreSQL) | SQL (SQLite) | Exemplo |
|-------------|------------|------------------|--------------|---------|
| `int` | `Integer` | `INTEGER` | `INTEGER` | IDs, contadores |
| `str` | `String(n)` | `VARCHAR(n)` | `VARCHAR(n)` | Nomes, emails |
| `str` | `Text` | `TEXT` | `TEXT` | Descrições longas |
| `float` | `Float` | `REAL` | `REAL` | Percentuais |
| `float` | `Double` | `DOUBLE PRECISION` | `REAL` | Valores financeiros (⚠️ use Decimal) |
| `Decimal` | `Numeric(10,2)` | `NUMERIC(10,2)` | `NUMERIC` | Dinheiro (precisão exata) |
| `bool` | `Boolean` | `BOOLEAN` | `INTEGER` | Flags |
| `datetime` | `DateTime` | `TIMESTAMP` | `TEXT` | Timestamps |
| `date` | `Date` | `DATE` | `TEXT` | Datas |
| `time` | `Time` | `TIME` | `TEXT` | Horários |
| `bytes` | `LargeBinary` | `BYTEA` | `BLOB` | Arquivos binários |
| `dict/list` | `JSON` | `JSONB` | `TEXT` | Dados estruturados |
| `Enum` | `Enum(MyEnum)` | `ENUM` | `VARCHAR` | Estados fixos |

### Exemplos Práticos

```python
from sqlalchemy import Integer, String, Text, Float, Numeric, Boolean, DateTime, Date, Time, JSON, Enum as SQLEnum, LargeBinary
from decimal import Decimal
import enum

class UserType(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class ExampleModel(Base):
    __tablename__ = "examples"

    # IDs e inteiros
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    count: Mapped[int] = mapped_column(Integer, default=0)

    # Strings de tamanho fixo
    code: Mapped[str] = mapped_column(String(10))  # Exatamente 10 chars
    email: Mapped[str] = mapped_column(String(255))  # Até 255 chars

    # Texto longo (sem limite)
    description: Mapped[str] = mapped_column(Text)

    # Números decimais
    percentage: Mapped[float] = mapped_column(Float)  # 0.0 a 1.0

    # ⚠️ IMPORTANTE: Use Numeric para dinheiro, NÃO Float!
    # Float tem imprecisão: 0.1 + 0.2 = 0.30000000000000004
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))  # 10 dígitos, 2 decimais

    # Booleano
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Data e hora
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    birth_date: Mapped[date] = mapped_column(Date)
    wake_up_time: Mapped[time] = mapped_column(Time)

    # JSON (PostgreSQL: JSONB, SQLite: TEXT)
    metadata: Mapped[dict] = mapped_column(JSON)
    tags: Mapped[list] = mapped_column(JSON)

    # Enum
    user_type: Mapped[UserType] = mapped_column(SQLEnum(UserType))

    # Binário (arquivos pequenos - NÃO recomendado para grandes)
    avatar: Mapped[bytes] = mapped_column(LargeBinary)
```

### Opções de Colunas

```python
class User(Base):
    __tablename__ = "users"

    # ═══ CHAVE PRIMÁRIA ═══
    id: Mapped[int] = mapped_column(
        primary_key=True,      # Define como PK
        autoincrement=True     # Auto incremento (padrão para Integer PK)
    )

    # ═══ NULLABLE ═══
    required_field: Mapped[str] = mapped_column(
        String,
        nullable=False         # NOT NULL (obrigatório)
    )

    optional_field: Mapped[str | None] = mapped_column(
        String,
        nullable=True          # Pode ser NULL
    )

    # ═══ UNIQUE ═══
    email: Mapped[str] = mapped_column(
        String,
        unique=True            # UNIQUE constraint
    )

    # ═══ DEFAULT ═══
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True           # Valor padrão no Python
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()  # Valor padrão no banco (SQL)
    )

    # ═══ ÍNDICES ═══
    name: Mapped[str] = mapped_column(
        String,
        index=True             # Cria índice simples
    )

    # ═══ INIT=FALSE ═══
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        init=False,            # Não aparece no __init__()
        onupdate=func.now()    # Atualiza automaticamente
    )

    # ═══ COMENTÁRIOS ═══
    special_field: Mapped[str] = mapped_column(
        String,
        comment="Este campo armazena dados especiais"  # Documentação no banco
    )
```

---

## 1.5 Armadilhas Comuns do MappedAsDataclass

> 📖 **Nota**: O `MappedAsDataclass` foi explicado em detalhes no **MÓDULO 0.3** junto com a configuração da classe Base. Esta seção foca nas **armadilhas práticas** que você vai encontrar ao usar esse recurso.

O `MappedAsDataclass` traz muitos benefícios (construtor automático, autocomplete, validação), mas também tem armadilhas sutis que podem causar horas de debugging. Aqui estão as mais comuns:

### Resumo Rápido das Regras Críticas

```
┌────────────────────────────────────────────────────────────────────────────┐
│  REGRAS DO MappedAsDataclass - MEMORIZE!                                   │
├────────────────────────────────────────────────────────────────────────────┤
│  1. Campos com default na Base → usar init=False                           │
│  2. Relationships → SEMPRE init=False                                      │
│  3. Relationships → NUNCA default=None (causa bug de FK NULL!)             │
│  4. Após INSERT → usar refresh() para obter o ID                           │
│  5. Múltiplas FKs entre tabelas → especificar foreign_keys=                │
└────────────────────────────────────────────────────────────────────────────┘
```

---

### ⚠️ ARMADILHA 1: Campos com Default na Herança

Este erro aparece quando você cria uma entidade que herda da Base:

```
TypeError: non-default argument 'team_name' follows default argument
```

**Por que acontece?**

A ordem dos campos no dataclass gerado segue a hierarquia de herança:
1. Primeiro vêm os campos da Base (id, active, etc.)
2. Depois vêm os campos da entidade filha

Se a Base tem campos com `default` e a entidade filha tem campos obrigatórios (sem default), a ordem fica:
```
Base.id (init=False) → Base.active (default) → Team.team_name (obrigatório)
                       ↑ com default            ↑ sem default = ERRO!
```

**Solução**: Todos os campos com default na Base devem ter `init=False`. Veja o MÓDULO 0.3 para a configuração correta da Base.

---

### ⚠️ ARMADILHA 2: O Bug do `default=None` em Relationships

#### Este É o Bug Mais Difícil de Encontrar!

```python
class User(Base):
    user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    # ❌ ERRADO - CAUSA BUG!
    team: Mapped["Team"] = relationship(
        back_populates="members",
        init=False,
        default=None  # ← ESTE É O PROBLEMA!
    )
```

#### O Que Acontece?

1. Você cria o User: `User(user_team_id=1, ...)`
2. O `user_team_id` é definido como `1` no objeto Python
3. Ao fazer `session.add(user)` e `session.flush()`...
4. **O INSERT vai com `user_team_id=NULL`!**

#### Por Que Isso Acontece?

O SQLAlchemy tem um mecanismo de **sincronização** entre relationships e FKs.

Quando você define `default=None` no relationship `team`, o SQLAlchemy interpreta:
> "O usuário quer que `team` seja `None` por padrão"

E então, na hora de persistir, ele **sincroniza** a FK com o relationship:
> "Se `team` é `None`, então `user_team_id` também deve ser `None`"

Isso **sobrescreve** o valor que você passou no construtor!

#### A Solução

**NUNCA** use `default=None` em relationships:

```python
# ❌ ERRADO - causa o bug!
team: Mapped["Team"] = relationship(
    back_populates="members",
    init=False,
    default=None  # REMOVA ISTO!
)

# ✅ CORRETO - funciona!
team: Mapped["Team | None"] = relationship(
    back_populates="members",
    init=False
    # Sem default!
)
```

#### Tabela de Referência

| Tipo de Campo | Usar `default=None`? |
|---------------|---------------------|
| `mapped_column` | Sim, se fizer sentido |
| `relationship` | **NUNCA!** |
| `relationship` (lista) | Use `default_factory=list` |

---

### ⚠️ ARMADILHA 3: ID Retorna None Após INSERT

#### O Erro

```python
def insert(self, nome: str):
    with DBConnectionHandler() as db:
        data = MinhaEntidade(nome=nome)
        db.session.add(data)
        db.session.flush()
        return data.id  # Retornava None!
```

#### Por Que Acontece?

Com `MappedAsDataclass`, o objeto é criado como um dataclass Python puro.
Quando o SQLAlchemy faz o INSERT, o **valor retornado pelo banco** nem sempre
é automaticamente atribuído de volta ao objeto Python.

#### A Solução

Use `session.refresh()` para forçar a atualização do objeto:

```python
def insert(self, nome: str):
    with DBConnectionHandler() as db:
        data = MinhaEntidade(nome=nome)
        db.session.add(data)
        db.session.flush()
        db.session.refresh(data)  # ← ADICIONE ISTO!
        return data.id  # Agora funciona!
```

#### O Que o `refresh()` Faz?

Executa um SELECT para buscar os valores atuais do banco e atualiza o objeto:

```sql
-- O refresh() executa algo assim:
SELECT * FROM minha_tabela WHERE id = ?
```

---

### ⚠️ ARMADILHA 4: Ambiguidade de Foreign Keys (AmbiguousForeignKeysError)

#### O Erro

Quando duas tabelas têm **múltiplas FKs** entre si, o SQLAlchemy não sabe qual usar:

```
sqlalchemy.exc.AmbiguousForeignKeysError: Could not determine join condition
between 'teams' and 'users'; tables have more than one foreign key constraint
relationship between them.
```

#### Quando Acontece?

Exemplo clássico: User pode ser **membro** de um Team E também **gerente** de um Team.

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Team                                  User                              │
├──────────────────────────────────────────────────────────────────────────┤
│  id                                    id                                │
│  team_name                             user_full_name                    │
│  team_manager_id (FK→User) ───────────→                                  │
│                         ←─────────────  user_team_id (FK→Team)           │
│                                                                          │
│  2 FKs entre as tabelas = AMBIGUIDADE!                                   │
└──────────────────────────────────────────────────────────────────────────┘
```

#### A Solução

Especifique **explicitamente** qual FK usar com o parâmetro `foreign_keys`:

```python
class User(Base):
    __tablename__ = "users"

    user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    # ✅ CORRETO - Especifica a FK
    team: Mapped["Team"] = relationship(
        foreign_keys=[user_team_id],  # ← Qual FK usar
        back_populates="team_members",
        lazy="raise",
        init=False
    )
```

#### Regra: Quando Usar Variável vs String?

| Onde está a FK? | Sintaxe | Exemplo |
|-----------------|---------|---------|
| Na **MESMA** classe | `foreign_keys=[variavel]` | `foreign_keys=[user_team_id]` |
| Em **OUTRA** classe | `foreign_keys="[Classe.atributo]"` | `foreign_keys="[Team.team_manager_id]"` |

```python
# FK está AQUI (nesta classe) → use variável
team: Mapped["Team"] = relationship(
    foreign_keys=[user_team_id],  # ✅ Variável
    ...
)

# FK está em OUTRA classe → use string
managed_team: Mapped["Team | None"] = relationship(
    foreign_keys="[Team.team_manager_id]",  # ✅ String
    ...
)
```

> 📖 **Para exemplos completos e detalhados**, veja a seção **2.8 Relacionamentos Avançados** no MÓDULO 2, que cobre casos como Team↔User e Ticket→User com múltiplas FKs.

> 📖 **Para o padrão completo da classe Base**, veja o **MÓDULO 0.3** onde explicamos cada decisão em detalhes.

---

### ⚠️ Guia de `ondelete` em Foreign Keys

O parâmetro `ondelete` define o que acontece com os registros filhos quando o registro pai é deletado.

```python
# Sintaxe:
campo_id: Mapped[int] = mapped_column(
    ForeignKey("tabela.id", ondelete="OPÇÃO"),  # ← ondelete DENTRO do ForeignKey
    nullable=...
)
```

#### Opções Disponíveis

| Opção | Comportamento | Quando Usar |
|-------|---------------|-------------|
| `RESTRICT` | **Impede** deletar pai se tiver filhos | Relacionamentos obrigatórios (User → Team) |
| `CASCADE` | **Deleta filhos** junto com o pai | Dependência total (Ticket → Messages) |
| `SET NULL` | **Define FK como NULL** nos filhos | Relacionamentos opcionais (User → Manager) |
| `SET DEFAULT` | Define FK como valor default | Raro, evite usar |
| `NO ACTION` | Similar ao RESTRICT | Comportamento padrão do banco |

#### Exemplos Práticos

```python
# RESTRICT - Impede deletar Team se tiver Users
# Cenário: Não faz sentido deletar um time que ainda tem membros
user_team_id: Mapped[int] = mapped_column(
    ForeignKey("teams.id", ondelete="RESTRICT"),
    nullable=False
)

# CASCADE - Deleta Messages quando Ticket é deletado
# Cenário: Se o ticket sumiu, as mensagens não fazem sentido existir
message_ticket_id: Mapped[int] = mapped_column(
    ForeignKey("tickets.id", ondelete="CASCADE"),
    nullable=False
)

# SET NULL - Define manager_id como NULL quando Manager é deletado
# Cenário: User pode existir sem manager (relacionamento opcional)
user_manager_id: Mapped[int | None] = mapped_column(
    ForeignKey("users.id", ondelete="SET NULL"),
    nullable=True,  # ← OBRIGATÓRIO ser nullable para SET NULL
    init=False
)
```

#### Regra de Ouro

| Se o relacionamento é... | Use... | nullable |
|--------------------------|--------|----------|
| Obrigatório e crítico | `RESTRICT` | `False` |
| Dependência total (filho não vive sem pai) | `CASCADE` | `False` |
| Opcional (pode existir sem o pai) | `SET NULL` | `True` |

---

### Checklist Rápido para MappedAsDataclass

#### Na Classe Base
- [ ] `id` tem `init=False`?
- [ ] Todos os campos com `default` têm `init=False`?
- [ ] `created_at` e `updated_at` têm `server_default` e `init=False`?

#### Em Cada Entidade
- [ ] FKs obrigatórias têm `ForeignKey()`?
- [ ] FKs opcionais têm `nullable=True` e `init=False`?
- [ ] Tipo `Mapped` bate com `nullable`? (`Mapped[int]` vs `Mapped[int | None]`)

#### Em Cada Relationship
- [ ] Tem `init=False`?
- [ ] **NÃO** tem `default=None`?
- [ ] Se é lista, tem `default_factory=list`?
- [ ] Se há ambiguidade de FK, tem `foreign_keys=`?
- [ ] Tem `lazy="raise"`?

#### Em Cada Repository
- [ ] `insert()` tem `db.session.refresh(data)` antes do `return data.id`?

---

# MÓDULO 2: RELACIONAMENTOS

## Introdução: Por Que Relacionamentos São Complexos?

Relacionamentos são o coração de aplicações que usam bancos de dados relacionais. Entender profundamente como eles funcionam é a diferença entre uma aplicação performática e uma aplicação lenta com bugs sutis.

### O Desafio: Duas Perspectivas

Quando trabalhamos com relacionamentos, precisamos conciliar duas perspectivas diferentes:

```
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│   PERSPECTIVA DO BANCO (SQL)    │     │   PERSPECTIVA DO CÓDIGO (OOP)   │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│  • Foreign Keys (IDs numéricos) │     │  • Referências (objetos)        │
│  • JOINs explícitos             │     │  • Navegação natural            │
│  • WHERE user_id = X            │     │  • user.team.name               │
│  • Constraints e índices        │     │  • Listas e coleções            │
└─────────────────────────────────┘     └─────────────────────────────────┘
```

**Foreign Keys** gerenciam a perspectiva do banco.
**Relationships** gerenciam a perspectiva do código.

Ambos são necessários e complementares.

### ⚠️ REGRA FUNDAMENTAL: Relacionamentos Têm DOIS LADOS

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   TODO RELACIONAMENTO TEM DOIS LADOS QUE PRECISAM SER CONFIGURADOS!        │
│                                                                            │
│   Lado "UM" (Team)              ←→              Lado "MUITOS" (User)       │
│   - NÃO tem FK                                  - TEM a FK                 │
│   - Relationship retorna LISTA                  - Relationship retorna 1   │
│   - back_populates aponta pro outro             - back_populates aponta pro│
│                                                   outro                    │
│                                                                            │
│   SE UM LADO ESTIVER ERRADO, O OUTRO NÃO FUNCIONA!                         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 📋 Referência Rápida: Tipos de Relationship

Antes de entrar nos detalhes, aqui está uma visão geral dos tipos de relacionamento:

| Tipo | Type Hint | uselist | Exemplo |
|------|-----------|---------|---------|
| **N-1** (muitos para um) | `Mapped["Entidade"]` | False (padrão) | User → Team |
| **1-N** (um para muitos) | `Mapped[list["Entidade"]]` | True (padrão) | Team → Users |
| **1-1** (um para um) | `Mapped["Entidade"]` | False (explícito) | User → Profile |
| **N-N** (muitos para muitos) | `Mapped[list["Assoc"]]` | True (padrão) | User ↔ Project (via tabela) |

**Legenda**:
- **uselist**: Quando `True`, o relationship retorna uma **lista**. Quando `False`, retorna um **objeto único**.
- O SQLAlchemy **infere** `uselist` do tipo `Mapped`: se for `list[...]`, assume `True`; se for apenas `"Entidade"`, assume `False`.

> 📌 **Dica**: Guarde esta tabela! Ela será detalhada nas seções 2.3 (N-1), 2.4 (lazy), 2.5 (1-N), 2.6 (N-N) e 2.7 (múltiplos relacionamentos).

---

## 2.1 Foreign Keys - A Base dos Relacionamentos

### Definição: O Que É Foreign Key?

**Foreign Key (Chave Estrangeira)** é uma coluna no banco de dados que armazena o ID de um registro em outra tabela, criando um vínculo entre elas.

**Analogia**: Pense em uma biblioteca. Cada livro tem um campo "autor_id" que aponta para um registro na tabela de autores. O "autor_id" é uma foreign key - ela cria o relacionamento, mas não duplica os dados do autor dentro do livro.

### Por Que Foreign Keys Existem?

Sem foreign keys, você teria duas opções ruins:

1. **Duplicar dados** (denormalização):
   ```python
   # Ticket armazena TODOS os dados do cliente
   ticket = {
       'id': 1,
       'title': 'Bug no relatório',
       'client_name': 'Matheus Beck',      # ❌ Duplicado
       'client_email': 'matheus@email.com', # ❌ Duplicado
       'client_phone': '123456'             # ❌ Duplicado
   }
   # Problema: Se cliente muda email, precisa atualizar TODOS os tickets
   ```

2. **Buscar tudo sempre** (sem relacionamento):
   ```python
   # Sem foreign key, como saber qual cliente?
   ticket = {'id': 1, 'title': 'Bug'}
   # ❌ Não tem como relacionar com cliente!
   ```

**Com foreign key** (correto):
```python
ticket = {
    'id': 1,
    'title': 'Bug no relatório',
    'client_id': 42  # ✅ Apenas o ID (4 bytes), não todos os dados
}
# Para pegar dados do cliente: JOIN ou relationship
```

### Anatomia de uma Foreign Key

```python
class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(100))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(200))

    # ═══ FOREIGN KEY ═══
    # Coluna física que armazena o ID do time
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),  # Referencia teams.id
        nullable=False           # Usuário PRECISA ter um time
    )
```

**SQL Gerado**:
```sql
CREATE TABLE teams (
    id INTEGER PRIMARY KEY,
    team_name VARCHAR(100)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    user_full_name VARCHAR(200),
    user_team_id INTEGER NOT NULL,
    FOREIGN KEY (user_team_id) REFERENCES teams(id)
);
```

### Regras de Foreign Key

```python
# ❌ ERRADO: Tipo errado
user_team_id: Mapped[Team] = mapped_column(ForeignKey("teams.id"))
# FK deve armazenar um INTEGER (ID), não o objeto Team!

# ✅ CORRETO: Tipo int
user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))


# ❌ ERRADO: String como tipo SQL
user_team_id: Mapped[int] = mapped_column(String, ForeignKey("teams.id"))

# ✅ CORRETO: Integer como tipo SQL (ou omite, pega automaticamente)
user_team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id"))
# Ou mais simples:
user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))


# ❌ ERRADO: Referencia tabela inexistente
user_team_id: Mapped[int] = mapped_column(ForeignKey("time.id"))  # Tabela "time" não existe

# ✅ CORRETO: Nome exato da tabela (__tablename__)
user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
```

### Naming Convention (Convenção de Nomes)

**PADRÃO RECOMENDADO**:

```python
# Foreign Key: nome_singular + _id
user_team_id      # FK para teams
ticket_client_id  # FK para users (cliente do ticket)
project_owner_id  # FK para users (dono do projeto)

# Relationship: nome_singular (objeto) ou nome_plural (lista)
team              # Relationship que retorna 1 Team
tickets           # Relationship que retorna lista de Tickets
```

### ON DELETE e ON UPDATE

#### ⚠️ ERRO COMUM: ondelete NO LUGAR ERRADO!

```python
# ❌ ERRADO! ondelete está em mapped_column, não em ForeignKey
user_team_id: Mapped[int] = mapped_column(
    ForeignKey("teams.id"),
    nullable=False,
    ondelete="RESTRICT"  # ❌ ERRADO! Isso é ignorado!
)

# ✅ CORRETO! ondelete DENTRO de ForeignKey
user_team_id: Mapped[int] = mapped_column(
    ForeignKey("teams.id", ondelete="RESTRICT"),  # ✅ CORRETO!
    nullable=False
)
```

**Por que isso importa?**
- `mapped_column()` configura a COLUNA Python
- `ForeignKey()` configura a CONSTRAINT no banco
- `ondelete` é uma configuração de constraint, então vai DENTRO de ForeignKey

#### Sintaxe Correta

```python
class User(Base):
    __tablename__ = "users"

    # Cascata: deletar team deleta usuários
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE")  # ✅ DENTRO de ForeignKey
    )

    # Restrito: não pode deletar team com usuários
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT")  # ✅ DENTRO de ForeignKey
    )

    # Set NULL: deletar team coloca NULL no user_team_id
    user_team_id: Mapped[int | None] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL"),  # ✅ DENTRO de ForeignKey
        nullable=True  # Precisa ser nullable para SET NULL funcionar
    )
```

**Opções de ondelete**:

| Opção | O que acontece quando registro pai é deletado |
|-------|-----------------------------------------------|
| `CASCADE` | Deleta registros filhos automaticamente |
| `RESTRICT` | Impede deleção (erro) se houver filhos |
| `SET NULL` | Coloca NULL nos FKs dos filhos |
| `SET DEFAULT` | Coloca valor padrão nos FKs dos filhos |
| `NO ACTION` | Padrão do banco (geralmente igual RESTRICT) |

**Recomendações por caso de uso**:

```python
# Para dados que PERTENCEM ao pai (composição):
# Exemplo: Mensagens pertencem a um Chat
message_chat_id: Mapped[int] = mapped_column(
    ForeignKey("chats.id", ondelete="CASCADE")
)
# Se deletar chat, deleta mensagens também ✅

# Para dados INDEPENDENTES (associação):
# Exemplo: Usuário pertence a um Time
user_team_id: Mapped[int] = mapped_column(
    ForeignKey("teams.id", ondelete="RESTRICT")
)
# Não pode deletar time se tiver usuários ✅

# Para referências opcionais:
# Exemplo: Report pode ter um usuário que atualizou por último
report_last_updated_by: Mapped[int | None] = mapped_column(
    ForeignKey("users.id", ondelete="SET NULL"),
    nullable=True
)
# Se deletar user, report continua existindo com campo NULL ✅
```

### 🚫 Resumo de Erros Comuns em Foreign Keys

```python
# ❌ ERRO 1: Tipo errado (objeto ao invés de int)
user_team_id: Mapped[Team] = mapped_column(ForeignKey("teams.id"))

# ✅ CORRETO: FK armazena INTEGER, não objeto
user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))


# ❌ ERRO 2: ondelete fora de ForeignKey
user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), ondelete="RESTRICT")

# ✅ CORRETO: ondelete DENTRO de ForeignKey
user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="RESTRICT"))


# ❌ ERRO 3: Tentar armazenar lista de IDs em Integer
team_reports: Mapped[int] = mapped_column(Integer)  # "1-N reports.id"

# ✅ CORRETO: Use relationship para 1-N, não coluna Integer
team_reports: Mapped[list["Report"]] = relationship(back_populates="team")


# ❌ ERRO 4: Nome de tabela errado
user_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))  # "team" não existe!

# ✅ CORRETO: Use o __tablename__ exato
user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))  # "teams" com s
```

---

## 2.2 Relationship - Navegação entre Objetos

### Conceito Fundamental: Física vs Virtual

Esta é **a distinção mais importante** em SQLAlchemy. Entender isso evita 90% dos erros comuns.

#### Colunas FÍSICAS (Foreign Keys)

```python
class User(Base):
    user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    #      ↑                                         ↑
    #   FÍSICA                                   FÍSICA
    #   - Existe no banco de dados
    #   - Armazena INTEGER (4 bytes)
    #   - Ocupa espaço em disco
    #   - Pode ter índice
    #   - Aparece no SELECT *
```

**Características**:
- ✅ Existe no esquema do banco (CREATE TABLE)
- ✅ Armazena dados reais (INTEGER)
- ✅ Pode ser indexada
- ✅ Constraint de integridade referencial
- ✅ Aparece em queries SQL
- ❌ Armazena apenas o ID, não o objeto inteiro

#### Colunas VIRTUAIS (Relationships)

```python
class User(Base):
    team: Mapped["Team"] = relationship(back_populates="team_members")
    #  ↑                                     ↑
    # VIRTUAL                            VIRTUAL
    # - NÃO existe no banco de dados
    # - Não armazena nada
    # - Não ocupa espaço em disco
    # - É apenas um "atalho" Python
    # - NÃO aparece no SELECT *
```

**Características**:
- ❌ NÃO existe no esquema do banco
- ❌ NÃO armazena dados
- ❌ NÃO pode ser indexada
- ❌ NÃO é uma constraint
- ❌ NÃO aparece em queries SQL diretas
- ✅ Facilita navegação em Python (user.team.name)
- ✅ SQLAlchemy gera JOINs automaticamente quando necessário

### Visualização: O Que Existe Onde?

```
═══════════════════════════════════════════════════════════════
                          BANCO DE DADOS
───────────────────────────────────────────────────────────────
TABLE users:
┌────┬───────────────┬──────────────┐
│ id │ user_name     │ user_team_id │  ← FÍSICO (ForeignKey)
├────┼───────────────┼──────────────┤
│ 1  │ Matheus Beck  │ 5            │  ← Armazena apenas o ID
│ 2  │ Ana Silva     │ 5            │
│ 3  │ Carlos Santos │ 3            │
└────┴───────────────┴──────────────┘
                            ↑
                       Coluna REAL
                       Ocupa espaço
═══════════════════════════════════════════════════════════════
                          PYTHON (Memória)
───────────────────────────────────────────────────────────────
user = session.get(User, 1)

user.user_team_id  →  5              ← FÍSICO: valor do banco
user.team          →  <Team object>  ← VIRTUAL: gerado por relationship

# Quando você acessa user.team:
# 1. SQLAlchemy vê que é um relationship
# 2. Pega o valor de user.user_team_id (5)
# 3. Faz SELECT * FROM teams WHERE id = 5
# 4. Retorna objeto Team preenchido
═══════════════════════════════════════════════════════════════
```

### Exemplo Completo: Lado a Lado

```python
class Team(Base):
    __tablename__ = "teams"

    # ═══ COLUNAS FÍSICAS (existem no banco) ═══
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(100))

    # ═══ COLUNA VIRTUAL (só existe em Python) ═══
    team_members: Mapped[list["User"]] = relationship(
        back_populates="team"
    )
    # ↑ Não cria coluna! É apenas um "atalho" para fazer:
    # SELECT * FROM users WHERE user_team_id = <este team.id>


class User(Base):
    __tablename__ = "users"

    # ═══ COLUNAS FÍSICAS (existem no banco) ═══
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(200))
    user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    # ↑ ESTA É A ÚNICA coluna que cria relacionamento no BANCO

    # ═══ COLUNA VIRTUAL (só existe em Python) ═══
    team: Mapped["Team"] = relationship(back_populates="team_members")
    # ↑ Não cria coluna! É apenas um "atalho" para fazer:
    # SELECT * FROM teams WHERE id = <este user.user_team_id>
```

**SQL gerado (apenas colunas físicas)**:
```sql
CREATE TABLE teams (
    id INTEGER PRIMARY KEY,
    team_name VARCHAR(100)
    -- NÃO TEM team_members! É virtual!
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    user_full_name VARCHAR(200),
    user_team_id INTEGER,  -- ← ÚNICA coluna de relacionamento
    FOREIGN KEY (user_team_id) REFERENCES teams(id)
    -- NÃO TEM team! É virtual!
);
```

### O Papel do Relationship

**Relationship NÃO cria relacionamento no banco.** Ele apenas facilita a navegação em Python.

```python
# ❌ ERRO CONCEITUAL:
"Relationship cria o relacionamento entre tabelas"
# ✅ CORRETO:
"ForeignKey cria o relacionamento no banco"
"Relationship facilita navegação em Python"

# ❌ ERRO CONCEITUAL:
"Relationship armazena dados"
# ✅ CORRETO:
"Relationship é um atalho que gera queries automáticas"
```

**O que Relationship realmente faz**:

```python
# Sem relationship (manual):
user = session.get(User, 1)
team_id = user.user_team_id  # Pega o ID
team = session.get(Team, team_id)  # Busca o team
print(team.team_name)

# Com relationship (automático):
user = session.get(User, 1)
print(user.team.team_name)  # SQLAlchemy faz o acima automaticamente
```

Por baixo dos panos, `user.team` dispara:
```sql
SELECT teams.id, teams.team_name
FROM teams
WHERE teams.id = <user.user_team_id>;
```

### Definição Formal de Relationship

**Relationship** é um atributo de classe que:

1. **Instrui** SQLAlchemy sobre como navegar entre models
2. **Gera** queries SQL automaticamente quando acessado
3. **Carrega** objetos relacionados do banco (lazy ou eager)
4. **Mantém** bidireção com `back_populates`
5. **Valida** integridade em nível de aplicação (não banco)

```python
from sqlalchemy.orm import relationship

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(100))

    # ═══ RELATIONSHIP (coluna VIRTUAL) ═══
    # Não existe no banco, apenas no Python
    team_members: Mapped[list["User"]] = relationship(back_populates="team")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(200))

    # ═══ FOREIGN KEY (coluna FÍSICA) ═══
    user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    # ═══ RELATIONSHIP (coluna VIRTUAL) ═══
    team: Mapped["Team"] = relationship(back_populates="team_members")
```

**Uso**:

```python
# Buscar time
team = session.get(Team, 1)

# Acessar membros (sem escrever JOIN!)
for member in team.team_members:  # SQLAlchemy faz SELECT automático
    print(member.user_full_name)

# Buscar usuário
user = session.get(User, 1)

# Acessar time (sem escrever JOIN!)
print(user.team.team_name)  # SQLAlchemy faz SELECT automático
```

**SQL Gerado Automaticamente**:
```sql
-- team.team_members:
SELECT users.id, users.user_full_name, users.user_team_id
FROM users
WHERE users.user_team_id = 1;

-- user.team:
SELECT teams.id, teams.team_name
FROM teams
WHERE teams.id = 1;
```

### Relationship NÃO vai no banco!

```python
# ❌ ERRO COMUM: Achar que relationship cria coluna
class Team(Base):
    team_members: Mapped[list["User"]] = relationship(...)
    # Isso NÃO cria coluna no banco!
    # É apenas atalho Python para fazer queries

# ✅ CORRETO: Entender que só FK cria coluna
class User(Base):
    user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    # ISSO cria coluna no banco ✅

    team: Mapped["Team"] = relationship(...)
    # ISSO é só Python, não cria coluna ✅
```

### back_populates: Conectando os Dois Lados

**`back_populates`** é o parâmetro que CONECTA os dois lados de um relacionamento. É OBRIGATÓRIO para relacionamentos bidirecionais funcionarem.

#### ⚠️ REGRA CRÍTICA: back_populates Deve Corresponder!

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   O valor de back_populates em A = NOME do relationship em B              │
│   O valor de back_populates em B = NOME do relationship em A              │
│                                                                            │
│   Team.team_members  ←─ back_populates="team" ─→      User.team           │
│   (lista de users)       corresponde ao NOME          (1 team)            │
│                          do relationship                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

#### Sintaxe Correta

```python
# ═══════════════════════════════════════════════════════════════════════════
# LADO "UM" - Team
# ═══════════════════════════════════════════════════════════════════════════
class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(100))

    # Relationship: Este time tem MUITOS usuários (lista)
    team_members: Mapped[list["User"]] = relationship(
        back_populates="team"  # ← Aponta para User.team
    )
    #              ↑
    #   ESTE NOME "team_members" é o que User.team vai referenciar


# ═══════════════════════════════════════════════════════════════════════════
# LADO "MUITOS" - User
# ═══════════════════════════════════════════════════════════════════════════
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(200))

    # FK: Coluna física que armazena o ID do time
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT")
    )

    # Relationship: Este usuário pertence a UM time (objeto único)
    team: Mapped["Team"] = relationship(
        back_populates="team_members"  # ← Aponta para Team.team_members
    )
    #   ↑
    #   ESTE NOME "team" é o que Team.team_members referencia
```

**Verificação**: Os valores correspondem?
| Em Team | back_populates | Em User | back_populates | ✓ |
|---------|----------------|---------|----------------|---|
| team_members | "team" | team | "team_members" | ✅ |

#### ⚠️ ERRO COMUM: back_populates Aponta para Nome Errado

```python
# ❌ ERRADO! back_populates aponta para nome de coluna FK, não relationship
class Team(Base):
    manager: Mapped["User | None"] = relationship(
        back_populates="managed_team"  # ✅ Correto
    )

class User(Base):
    managed_team: Mapped["Team | None"] = relationship(
        back_populates="manager_id"  # ❌ ERRADO! "manager_id" é FK, não relationship
    )
    # ✅ CORRETO: back_populates="manager" (nome do relationship no Team)
```

```python
# ✅ CORRETO! back_populates aponta para nome do RELATIONSHIP
class Team(Base):
    manager: Mapped["User | None"] = relationship(
        foreign_keys=[team_manager_id],
        back_populates="managed_team"  # ← Aponta para User.managed_team
    )

class User(Base):
    managed_team: Mapped["Team | None"] = relationship(
        foreign_keys="[Team.team_manager_id]",
        back_populates="manager"  # ← Aponta para Team.manager (não manager_id!)
    )
```

### 🚫 Resumo de Erros Comuns em Relationships

```python
# ❌ ERRO 1: Nomear relationship com "_id"
manager_id: Mapped["User"] = relationship(...)  # Parece FK, mas é relationship!

# ✅ CORRETO: Relationships NÃO têm "_id" no nome
manager: Mapped["User"] = relationship(...)


# ❌ ERRO 2: Usar mesmo nome para coluna E relationship
class Team(Base):
    team_reports: Mapped[int] = mapped_column(Integer)  # Coluna
    team_reports: Mapped[list["Report"]] = relationship(...)  # Relationship - CONFLITO!

# ✅ CORRETO: Remova a coluna Integer, use só relationship
class Team(Base):
    team_reports: Mapped[list["Report"]] = relationship(back_populates="team")


# ❌ ERRO 3: back_populates aponta para FK ao invés de relationship
back_populates="manager_id"  # manager_id é FK, não relationship!

# ✅ CORRETO: back_populates aponta para nome do RELATIONSHIP
back_populates="manager"  # manager é o relationship


# ❌ ERRO 4: Mapped[list["Ticket | None"]] - Union dentro de list
report_tickets: Mapped[list["Ticket | None"]] = relationship(...)

# ✅ CORRETO: Lista pode estar vazia, itens são Ticket
report_tickets: Mapped[list["Ticket"]] = relationship(...)


# ❌ ERRO 5: Esquecer de definir um dos lados
class Team(Base):
    team_members: Mapped[list["User"]] = relationship(back_populates="team")

class User(Base):
    # Esqueceu de definir o relationship "team"!
    pass

# ✅ CORRETO: Definir AMBOS os lados
class User(Base):
    team: Mapped["Team"] = relationship(back_populates="team_members")
```

### back_populates vs backref

**`back_populates`** (RECOMENDADO):
```python
class Team(Base):
    team_members: Mapped[list["User"]] = relationship(back_populates="team")

class User(Base):
    team: Mapped["Team"] = relationship(back_populates="team_members")
```

**Vantagens**:
- ✅ Explícito em ambos os lados
- ✅ Type hints funcionam melhor
- ✅ IDE autocomplete funciona
- ✅ Mais fácil debugar
- ✅ Você VÊ a estrutura completa

**`backref`** (ANTIGO, evite):
```python
class Team(Base):
    team_members: Mapped[list["User"]] = relationship(
        backref="team"  # Cria automaticamente User.team
    )

class User(Base):
    # Não precisa declarar team aqui, mas...
    # ❌ IDE não sabe que existe
    # ❌ Type hints não funcionam
    # ❌ Esconde metade do relacionamento
    pass
```

---

## 2.3 Relacionamento N-1 (Many-to-One) - DETALHADO

### Conceito

**N-1 (Many-to-One)**: Muitos registros apontam para 1.

**Exemplos**:
- Muitos usuários → 1 time
- Muitos tickets → 1 cliente
- Muitos reports → 1 time responsável

### ⚠️ REGRA: A FK Sempre Fica no Lado "MUITOS"

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   1 Team  ←───────────────  N Users                                        │
│      ↑                         ↑                                           │
│   Lado "UM"                 Lado "MUITOS"                                  │
│   NÃO tem FK                TEM a FK (user_team_id)                        │
│                                                                            │
│   Por quê? Porque uma coluna Integer só pode armazenar UM valor.           │
│   Se a FK ficasse no Team, como armazenar "users 1, 2, 3, 4"?              │
│   Não dá! Por isso cada User armazena SEU team_id.                         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Implementação Completa: AMBOS OS LADOS

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     LADO "UM" (Team)          LADO "MUITOS" (User)          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  COLUNAS FÍSICAS:                                                           │
│  ┌─────────────────┐                    ┌──────────────────────┐            │
│  │ id (PK)         │◄───────────────────│ user_team_id (FK)    │            │
│  │ team_name       │                    │ user_full_name       │            │
│  │                 │                    │                      │            │
│  │ ❌ NÃO TEM FK   │                    │ ✅ TEM A FK          │            │
│  └─────────────────┘                    └──────────────────────┘            │
│                                                                             │
│  RELATIONSHIPS (virtuais):                                                  │
│  ┌─────────────────┐                    ┌──────────────────────┐            │
│  │ team_members    │                    │ team                 │            │
│  │ Mapped[list[    │←──back_populates──→│ Mapped["Team"]       │            │
│  │   "User"]]      │                    │                      │            │
│  │ ✅ LISTA        │                    │ ✅ OBJETO ÚNICO      │            │
│  └─────────────────┘                    └──────────────────────┘            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### LADO "UM" - Team (NÃO tem FK)

```python
class Team(Base):
    """
    Lado "UM" do relacionamento 1-N com User.
    NÃO tem Foreign Key - apenas Relationship que retorna LISTA.
    """
    __tablename__ = "teams"

    # ════════════════════════════════════════════════════════════════
    # COLUNAS FÍSICAS (existem no banco)
    # ════════════════════════════════════════════════════════════════
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(100), unique=True)
    team_area: Mapped[Area] = mapped_column(Enum(Area))

    # ❌ ERRADO: Tentar criar coluna para armazenar "os usuários"
    # team_members: Mapped[int] = mapped_column(Integer)  # NÃO FUNCIONA!

    # ════════════════════════════════════════════════════════════════
    # RELATIONSHIPS (virtuais - NÃO existem no banco)
    # ════════════════════════════════════════════════════════════════

    # ✅ CORRETO: Relationship que retorna LISTA de Users
    team_members: Mapped[list["User"]] = relationship(
        back_populates="team",  # ← Nome do relationship NO USER
        lazy="raise"
    )
    # Quando acessado, gera: SELECT * FROM users WHERE user_team_id = <este team.id>
```

#### LADO "MUITOS" - User (TEM a FK)

```python
class User(Base):
    """
    Lado "MUITOS" do relacionamento N-1 com Team.
    TEM a Foreign Key + Relationship que retorna OBJETO ÚNICO.
    """
    __tablename__ = "users"

    # ════════════════════════════════════════════════════════════════
    # COLUNAS FÍSICAS (existem no banco)
    # ════════════════════════════════════════════════════════════════
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(200))
    user_email: Mapped[str] = mapped_column(String(200), unique=True)

    # ✅ FK: A Foreign Key FICA AQUI (lado "muitos")
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),  # ondelete DENTRO!
        nullable=False
    )

    # ════════════════════════════════════════════════════════════════
    # RELATIONSHIPS (virtuais - NÃO existem no banco)
    # ════════════════════════════════════════════════════════════════

    # ✅ Relationship que retorna OBJETO ÚNICO (1 Team)
    team: Mapped["Team"] = relationship(
        back_populates="team_members",  # ← Nome do relationship NO TEAM
        lazy="raise"
    )
    # Quando acessado, gera: SELECT * FROM teams WHERE id = <este user.user_team_id>
```

### Verificação: Os Dois Lados Estão Corretos?

| Checklist | Team | User |
|-----------|------|------|
| Tem FK? | ❌ Não | ✅ `user_team_id` |
| Tipo do Relationship | `list["User"]` | `"Team"` |
| back_populates aponta para | `"team"` (nome em User) | `"team_members"` (nome em Team) |
| lazy | `"raise"` | `"raise"` |

### Uso na Prática

```python
# Criar time
team = Team(team_name="Performance Agricola")
session.add(team)
session.commit()
session.refresh(team)  # Pega o ID gerado

# Criar usuário vinculado ao time
user = User(
    user_full_name="Matheus Beck",
    user_team_id=team.id  # Passa o ID do time
)
session.add(user)
session.commit()

# Navegar: User → Team
user = session.get(User, 1)
print(user.team.team_name)  # "Performance Agricola"

# Navegar: Team → Users
team = session.get(Team, 1)
for member in team.team_members:
    print(member.user_full_name)  # "Matheus Beck"
```

### ⚠️ Problema: Relacionamento N-N com Integer

```python
# ❌ ERRO COMUM: Tentar armazenar múltiplos IDs em Integer
class User(Base):
    user_reports_att: Mapped[int | None] = mapped_column(Integer)
    # Como armazenar IDs [1, 2, 3] num INTEGER? IMPOSSÍVEL!

# ✅ SOLUÇÃO 1: Relationship N-N (veremos em 2.6)
class User(Base):
    reports_att: Mapped[list["Report"]] = relationship(
        secondary="user_reports_association"
    )

# ✅ SOLUÇÃO 2: JSON (não recomendado para relacionamentos)
class User(Base):
    user_reports_att: Mapped[list[int] | None] = mapped_column(JSON)
    # Funciona, mas perde foreign key e índices
```

---

## 2.4 O Parâmetro lazy - CRUCIAL para Performance

### Entendendo o Problema: Quando Carregar Dados?

Quando você carrega um objeto do banco, SQLAlchemy enfrenta um dilema:

```python
user = session.get(User, 1)  # Carregou o user

# Agora, quando carregar o team?

# Opção A: Carregar AGORA (junto com user) - Eager
# Opção B: Carregar DEPOIS (quando user.team for acessado) - Lazy
# Opção C: NUNCA carregar automaticamente - Raise
```

Este dilema é chamado de **loading strategy** (estratégia de carregamento). O parâmetro `lazy` controla qual estratégia usar.

### Conceito: Lazy Loading

**Lazy Loading** (carregamento preguiçoso) é quando dados relacionados são carregados **sob demanda** - apenas quando você acessa o atributo pela primeira vez.

**Analogia**: Imagine um livro com referências bibliográficas ao final. Você pode:

1. **Lazy**: Ler o livro normalmente. Quando encontrar uma referência [1], você vai até o final do livro para ler.
2. **Eager**: Antes de ler o livro, já ler TODAS as referências (mesmo que não precise de todas).
3. **Raise**: Se encontrar uma referência [1] e não tiver as referências carregadas, o livro grita "ERRO! Referência não disponível!"

SQLAlchemy funciona da mesma forma com relacionamentos.

### O Problema N+1: A Armadilha Silenciosa

O problema N+1 é uma das piores armadilhas de performance em ORMs. Ele é **silencioso** - seu código funciona perfeitamente, mas é extremamente lento.

#### O Que É o Problema N+1?

```python
# Query 1: Buscar 10 users
users = session.query(User).limit(10).all()

# Queries 2-11: Buscar team de cada user (se lazy="select")
for user in users:
    print(user.team.team_name)  # Cada acesso = 1 query!
```

**Total de queries**: 1 (users) + 10 (teams) = **11 queries**

Se fossem 100 users? **101 queries!**
Se fossem 1000 users? **1001 queries!**

**Fórmula**: N (número de registros) + 1 (query inicial) = N+1 queries

#### Por Que É Um Problema?

```
Cenário: 100 users, cada query demora 10ms

Sem N+1 (2 queries):
    Query 1: 10ms
    Query 2: 10ms
    Total: 20ms  ✅

Com N+1 (101 queries):
    Query 1: 10ms
    Queries 2-101: 100 × 10ms = 1000ms
    Total: 1010ms ❌ (50x mais lento!)
```

Quanto mais registros, pior fica. Com 1000 users e latência de rede (30ms), pode demorar **30 SEGUNDOS** apenas para uma listagem simples!

#### Visualização do Problema

```
Lazy Loading (N+1 Problem):
┌──────────────────────────────────────────────────────┐
│ SELECT * FROM users LIMIT 10;  ← Query 1            │
├──────────────────────────────────────────────────────┤
│ SELECT * FROM teams WHERE id = 1;  ← Query 2        │
│ SELECT * FROM teams WHERE id = 1;  ← Query 3 (mesmo!)│
│ SELECT * FROM teams WHERE id = 2;  ← Query 4        │
│ SELECT * FROM teams WHERE id = 2;  ← Query 5 (mesmo!)│
│ SELECT * FROM teams WHERE id = 3;  ← Query 6        │
│ ...                                                  │
│ SELECT * FROM teams WHERE id = 5;  ← Query 11       │
└──────────────────────────────────────────────────────┘
Total: 11 queries (alguns duplicados!)

Eager Loading (Solução):
┌──────────────────────────────────────────────────────┐
│ SELECT users.*, teams.*                              │
│ FROM users                                           │
│ LEFT JOIN teams ON teams.id = users.user_team_id    │
│ LIMIT 10;                                            │
└──────────────────────────────────────────────────────┘
Total: 1 query! ✅
```

### Definindo: O Parâmetro lazy

**`lazy`** é um parâmetro do `relationship()` que define **quando** e **como** dados relacionados são carregados.

```python
class User(Base):
    team: Mapped["Team"] = relationship(
        lazy="select"  # ← Controla estratégia de carregamento
    )
```

**Valores possíveis**:
- `"select"` (padrão): Carrega quando acessado (problema N+1)
- `"joined"`: Carrega com JOIN automático (eager, uma query)
- `"selectin"`: Carrega com IN query (eager, duas queries)
- `"raise"`: NUNCA carrega automaticamente (força eager explícito)
- `"noload"`: Nunca carrega, retorna None
- `"write_only"`: Apenas escrita (coleções muito grandes)

### Opções do lazy

#### 1. `lazy="select"` (PADRÃO - Problema N+1)

```python
class User(Base):
    team: Mapped["Team"] = relationship(lazy="select")

# Query:
users = session.query(User).limit(10).all()

# Problema: 1 query inicial + 10 queries adicionais = 11 queries!
for user in users:
    print(user.team.team_name)  # Cada acesso faz SELECT separado
```

**SQL Gerado**:
```sql
-- Query 1: buscar users
SELECT * FROM users LIMIT 10;

-- Query 2-11: buscar team de cada user (N+1 PROBLEM!)
SELECT * FROM teams WHERE id = 1;
SELECT * FROM teams WHERE id = 2;
...
SELECT * FROM teams WHERE id = 10;
```

**Total: 11 queries!** ❌

#### 2. `lazy="joined"` (JOIN automático)

```python
class User(Base):
    team: Mapped["Team"] = relationship(lazy="joined")

# Query:
users = session.query(User).limit(10).all()

# Solução: 1 query com JOIN = 1 query total!
for user in users:
    print(user.team.team_name)  # Dados já estão carregados
```

**SQL Gerado**:
```sql
SELECT
    users.id,
    users.user_full_name,
    teams.id AS teams_id,
    teams.team_name
FROM users
LEFT OUTER JOIN teams ON teams.id = users.user_team_id
LIMIT 10;
```

**Total: 1 query!** ✅

**Desvantagem**: SEMPRE faz JOIN, mesmo quando não precisa.

#### 3. `lazy="selectin"` (IN query)

```python
class User(Base):
    team: Mapped["Team"] = relationship(lazy="selectin")

# Query:
users = session.query(User).limit(10).all()
for user in users:
    print(user.team.team_name)
```

**SQL Gerado**:
```sql
-- Query 1: buscar users
SELECT * FROM users LIMIT 10;

-- Query 2: buscar todos os teams de uma vez
SELECT * FROM teams WHERE teams.id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
```

**Total: 2 queries!** ✅

**Vantagens sobre joined**:
- Mais eficiente para relacionamentos 1-N
- Não duplica dados (JOIN duplica linhas)

#### 4. `lazy="raise"` (RECOMENDADO para APIs!)

```python
class User(Base):
    team: Mapped["Team"] = relationship(lazy="raise")

# Query:
users = session.query(User).all()

# ERRO: Tenta acessar relationship sem eager loading
for user in users:
    print(user.team.team_name)  # ❌ InvalidRequestError!
```

**Por que usar?**

- ✅ Força desenvolvedores a pensar em performance
- ✅ Previne N+1 queries acidentais
- ✅ Deixa explícito o que está sendo carregado

**Como usar** (veremos em 2.5):
```python
from sqlalchemy.orm import joinedload

# Carregamento EXPLÍCITO:
users = session.query(User).options(joinedload(User.team)).all()

# Agora funciona:
for user in users:
    print(user.team.team_name)  # ✅ OK!
```

### Comparação de Performance

Cenário: 100 usuários, cada um tem 1 time.

| lazy | Queries | Performance | Quando usar |
|------|---------|-------------|-------------|
| `select` | 101 | ❌ Lento (N+1) | Nunca |
| `joined` | 1 | ✅ Rápido | Sempre precisa do relacionamento |
| `selectin` | 2 | ✅ Rápido | Geralmente precisa |
| `raise` | 0 | ⚡ Máximo | APIs (controle total) |

### Recomendação

**Para APIs REST** (nosso caso):

```python
class User(Base):
    # SEMPRE use lazy="raise"
    team: Mapped["Team"] = relationship(
        back_populates="team_members",
        lazy="raise"  # ✅
    )
```

**Por quê?**

1. Previne N+1 acidentais
2. Força uso de eager loading (mais eficiente)
3. API pode escolher o que carregar (veremos em Módulo 3)

### Por Que Não Usar `lazy="joined"` em Todos os Relacionamentos?

**Pergunta comum**: Se eager loading é mais performático, por que não usar `lazy="joined"` como padrão em todos os relationships?

**Resposta**: Porque carregamento automático SEMPRE significa desperdício.

```python
# Com lazy="joined" em TODOS os relationships:
user = session.get(User, 1)

# SQLAlchemy faz JOIN com TODAS as tabelas relacionadas:
# users + teams + tickets + messages + projects + ...
# Mesmo que você só precise do nome do usuário!
```

**Os problemas**:

| Problema | Impacto |
|----------|---------|
| **Dados desnecessários** | Carrega gigabytes de dados que não vai usar |
| **JOINs pesados** | Cada JOIN adicional multiplica o tempo da query |
| **Duplicação de linhas** | JOIN com 1-N duplica linhas (1 user com 100 tickets = 100 linhas retornadas) |
| **Memória** | Objetos carregados ficam no Identity Map da Session |

**A solução com `lazy="raise"`**:

- Você ESCOLHE quando carregar (eager loading explícito)
- Cada endpoint carrega APENAS o que precisa
- Performance máxima, controle total

```python
# Listagem simples: só user
users = session.query(User).all()

# Detalhe com time: user + team
user = session.query(User).options(joinedload(User.team)).first()

# Relatório completo: user + team + tickets
user = session.query(User).options(
    joinedload(User.team),
    selectinload(User.tickets)
).first()
```

**Regra**: Prefira sempre controle explícito sobre comportamento automático.

---

## 2.5 Eager Loading - Carregamento Explícito

### Conceito

Com `lazy="raise"`, você PRECISA usar **eager loading** para carregar relacionamentos.

### joinedload - JOIN na mesma query

```python
from sqlalchemy.orm import joinedload

# Carregar users + teams num JOIN
users = session.query(User).options(
    joinedload(User.team)
).all()

# Agora pode acessar:
for user in users:
    print(user.team.team_name)  # ✅ Dados já estão aqui
```

**SQL Gerado**:
```sql
SELECT
    users.*,
    teams.*
FROM users
LEFT OUTER JOIN teams ON teams.id = users.user_team_id;
```

**Quando usar**:
- ✅ Relacionamento N-1 (cada user tem 1 team)
- ✅ Sempre precisa dos dados relacionados
- ❌ Evite para 1-N (pode duplicar muitas linhas)

### selectinload - IN query separada

```python
from sqlalchemy.orm import selectinload

# Carregar teams + members
teams = session.query(Team).options(
    selectinload(Team.team_members)
).all()

for team in teams:
    for member in team.team_members:
        print(member.user_full_name)  # ✅ Dados já estão aqui
```

**SQL Gerado**:
```sql
-- Query 1:
SELECT * FROM teams;

-- Query 2:
SELECT * FROM users WHERE user_team_id IN (1, 2, 3, ...);
```

**Quando usar**:
- ✅ Relacionamento 1-N (1 team tem N users)
- ✅ Evita duplicação de dados
- ✅ Geralmente mais eficiente que joinedload para 1-N

### Carregamento Aninhado

```python
from sqlalchemy.orm import joinedload, selectinload

# Carregar: Ticket → Client → Team
tickets = session.query(Ticket).options(
    joinedload(Ticket.client).selectinload(User.team)
).all()

for ticket in tickets:
    print(f"{ticket.ticket_title}")
    print(f"Cliente: {ticket.client.user_full_name}")
    print(f"Time do cliente: {ticket.client.team.team_name}")
```

**SQL Gerado**:
```sql
-- Query 1: Tickets + Clients (JOIN)
SELECT tickets.*, users.*
FROM tickets
LEFT OUTER JOIN users ON users.id = tickets.ticket_client_id;

-- Query 2: Teams (IN)
SELECT * FROM teams WHERE id IN (...);
```

### contains_eager - Para quando JÁ fez JOIN manual

```python
from sqlalchemy.orm import contains_eager

# JOIN manual + aproveitar resultado
users = (
    session.query(User)
    .join(User.team)
    .filter(Team.team_name == "Performance Agricola")
    .options(contains_eager(User.team))
    .all()
)

# team já está carregado (sem query adicional)
for user in users:
    print(user.team.team_name)
```

---

## 2.6 Relacionamento N-N (Many-to-Many)

### Conceito

**N-N**: Muitos registros se relacionam com muitos.

**Exemplos**:
- Usuários → Tickets (um usuário atende vários tickets, um ticket é atendido por vários usuários)
- Projetos → Tags (um projeto tem várias tags, uma tag está em vários projetos)

### Tabela de Associação Simples

```python
from sqlalchemy import Table

# Tabela de associação (SEM atributos extras)
user_tickets_association = Table(
    "user_tickets_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("ticket_id", ForeignKey("tickets.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(200))

    # Relationship N-N
    tickets_att: Mapped[list["Ticket"]] = relationship(
        secondary=user_tickets_association,
        back_populates="attendants",
        lazy="raise"
    )


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_title: Mapped[str] = mapped_column(String(200))

    # Relationship N-N (lado oposto)
    attendants: Mapped[list["User"]] = relationship(
        secondary=user_tickets_association,
        back_populates="tickets_att",
        lazy="raise"
    )
```

**SQL Gerado**:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    user_full_name VARCHAR(200)
);

CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    ticket_title VARCHAR(200)
);

CREATE TABLE user_tickets_association (
    user_id INTEGER NOT NULL,
    ticket_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, ticket_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
);
```

### Uso

```python
# Criar usuário e ticket
user = User(user_full_name="Matheus Beck")
ticket = Ticket(ticket_title="Corrigir relatório CCT")

# Associar
user.tickets_att.append(ticket)  # Ou: ticket.attendants.append(user)

session.add(user)
session.commit()

# Navegar: User → Tickets
user = session.query(User).options(
    selectinload(User.tickets_att)
).first()

for ticket in user.tickets_att:
    print(ticket.ticket_title)

# Navegar: Ticket → Users
ticket = session.query(Ticket).options(
    selectinload(Ticket.attendants)
).first()

for attendant in ticket.attendants:
    print(attendant.user_full_name)
```

---

## 2.7 Tabela de Associação com Atributos Extras

### Problema

E se a tabela de associação precisar de campos extras?

**Exemplo**: User ↔ Ticket, mas queremos saber QUANDO user foi atribuído e QUAL papel.

### Solução: Model Completo (não Table)

```python
class UserTicketAssociation(Base):
    """Model completo para tabela de associação"""
    __tablename__ = "user_tickets_association"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id"),
        primary_key=True
    )

    # ═══ ATRIBUTOS EXTRAS ═══
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    role: Mapped[str] = mapped_column(
        String(50),
        default="attendant"  # "attendant", "reviewer", "approver"
    )

    # Relationships para navegar
    user: Mapped["User"] = relationship(back_populates="ticket_associations")
    ticket: Mapped["Ticket"] = relationship(back_populates="user_associations")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(200))

    # Relationship para a associação
    ticket_associations: Mapped[list["UserTicketAssociation"]] = relationship(
        back_populates="user",
        lazy="raise"
    )

    # Propriedade de conveniência (opcional)
    @property
    def tickets(self) -> list["Ticket"]:
        """Atalho para acessar tickets diretamente"""
        return [assoc.ticket for assoc in self.ticket_associations]


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_title: Mapped[str] = mapped_column(String(200))

    # Relationship para a associação
    user_associations: Mapped[list["UserTicketAssociation"]] = relationship(
        back_populates="ticket",
        lazy="raise"
    )

    @property
    def attendants(self) -> list["User"]:
        """Atalho para acessar usuários diretamente"""
        return [assoc.user for assoc in self.user_associations]
```

### Uso

```python
# Criar associação com atributos extras
user = session.get(User, 1)
ticket = session.get(Ticket, 1)

association = UserTicketAssociation(
    user_id=user.id,
    ticket_id=ticket.id,
    role="reviewer",
    assigned_at=datetime.now()
)

session.add(association)
session.commit()

# Acessar atributos extras
user = session.query(User).options(
    selectinload(User.ticket_associations).selectinload(UserTicketAssociation.ticket)
).first()

for assoc in user.ticket_associations:
    print(f"Ticket: {assoc.ticket.ticket_title}")
    print(f"Papel: {assoc.role}")
    print(f"Atribuído em: {assoc.assigned_at}")
```

### Por Que a Propriedade de Conveniência Não É o Padrão?

Você viu no código acima duas `@property` que simplificam o acesso:

```python
@property
def tickets(self) -> list["Ticket"]:
    return [assoc.ticket for assoc in self.ticket_associations]
```

**Por que isso não é automático no SQLAlchemy?**

**Resposta**: Performance e controle.

```python
# Se "tickets" fosse automático:
user = session.get(User, 1)
print(user.tickets)  # Faz query IMPLÍCITA para associations E tickets

# Você não sabe que 2 queries foram executadas!
# E se iterar sobre 100 users? 200 queries extras!
```

**Os problemas**:

| Problema | Consequência |
|----------|--------------|
| **Lazy loading implícito** | A propriedade acessa relationships, que podem fazer queries |
| **N+1 escondido** | Em loops, cada acesso pode disparar queries |
| **Incompatível com lazy="raise"** | Se relationships têm `lazy="raise"`, a propriedade falha |

**Quando usar**:

| Contexto | Usar? | Por quê |
|----------|-------|---------|
| Após eager loading explícito | ✅ Sim | Dados já carregados na memória |
| Acesso único (não em loop) | ✅ Sim | Uma ou duas queries não importam |
| Em listagens/loops | ❌ Não | Prefira query direta com join |
| Com lazy="raise" sem eager | ❌ Não | Vai lançar exceção |

**Uso correto**:

```python
# ✅ CORRETO: Eager loading primeiro
user = session.query(User).options(
    selectinload(User.ticket_associations)
        .selectinload(UserTicketAssociation.ticket)
).first()

# Agora a propriedade é segura (dados já estão na memória)
for ticket in user.tickets:  # Usa a @property
    print(ticket.title)

# ❌ INCORRETO: Sem eager loading
user = session.get(User, 1)
for ticket in user.tickets:  # ERRO com lazy="raise"!
    print(ticket.title)
```

**Regra**: A propriedade de conveniência é um **atalho de leitura**, não uma estratégia de carregamento.

---

## 2.7.5 Cascade - Propagação de Operações

### O Que É Cascade?

**Cascade** define como operações em um objeto devem se propagar para objetos relacionados. É diferente de `ondelete` da FK (que é no banco) - cascade é controlado pelo SQLAlchemy no Python.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CASCADE vs ONDELETE                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ondelete (ForeignKey)                cascade (relationship)               │
│   ┌─────────────────────┐             ┌─────────────────────┐              │
│   │ • Executado no BANCO │             │ • Executado no PYTHON│              │
│   │ • SQL: ON DELETE ... │             │ • Antes de enviar SQL│              │
│   │ • Funciona mesmo com │             │ • Requer carregar    │              │
│   │   DELETE direto      │             │   objetos na session │              │
│   │ • Mais performático  │             │ • Mais controle/hooks│              │
│   └─────────────────────┘             └─────────────────────┘              │
│                                                                             │
│   RECOMENDAÇÃO: Use AMBOS para garantir consistência!                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Opções de Cascade

```python
class Team(Base):
    members: Mapped[list["User"]] = relationship(
        back_populates="team",
        cascade="save-update, merge"  # ← Opções de cascade
    )
```

| Opção | O Que Faz | Quando Usar |
|-------|-----------|-------------|
| `save-update` | add() no pai adiciona filhos automaticamente | **Padrão**, quase sempre |
| `merge` | merge() no pai propaga para filhos | **Padrão**, quase sempre |
| `delete` | delete() no pai deleta filhos | Quando filhos pertencem ao pai |
| `delete-orphan` | Filhos sem pai são deletados | Com `delete`, composição forte |
| `expunge` | expunge() propaga para filhos | Raramente necessário |
| `refresh-expire` | refresh()/expire() propaga | Raramente necessário |
| `all` | Atalho para todos exceto delete-orphan | Composição com cuidado |

### Exemplos Práticos

#### 1. Cascade Padrão (save-update, merge)

```python
class Team(Base):
    members: Mapped[list["User"]] = relationship(
        back_populates="team"
        # cascade="save-update, merge" é o PADRÃO
    )

# Comportamento:
team = Team(team_name="Dev")
user = User(user_full_name="Ana", user_team_id=None)

team.members.append(user)  # Adiciona user à lista
session.add(team)          # Adiciona team à session

# save-update: user também é adicionado automaticamente!
session.commit()  # Salva team E user
```

#### 2. Cascade Delete (Composição)

Use quando filhos **pertencem** ao pai e não fazem sentido sozinhos:

```python
class Chat(Base):
    """Chat pertence a um ticket."""
    __tablename__ = "chats"

    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        cascade="all, delete-orphan",  # ← Deleta mensagens junto
        lazy="raise"
    )

class Message(Base):
    """Mensagem não faz sentido sem chat."""
    __tablename__ = "messages"

    message_chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE")  # ← Banco também deleta
    )

    chat: Mapped["Chat"] = relationship(back_populates="messages")

# Comportamento:
chat = session.get(Chat, 1)
session.delete(chat)  # Deleta chat
session.commit()      # Mensagens também são deletadas!
```

#### 3. Delete-Orphan (Remoção da Lista = Deleção)

```python
class Team(Base):
    members: Mapped[list["User"]] = relationship(
        back_populates="team",
        cascade="all, delete-orphan"  # ← Órfãos são deletados
    )

# Comportamento:
team = session.get(Team, 1)
user = team.members[0]

team.members.remove(user)  # Remove user da lista do team
# delete-orphan: user agora é "órfão" (sem team)
session.commit()  # User é DELETADO do banco!

# ⚠️ CUIDADO: Isso pode não ser o que você quer!
# Use apenas quando o filho não pode existir sem o pai.
```

#### 4. Sem Cascade Delete (Associação)

Use quando filhos são **independentes** do pai:

```python
class Team(Base):
    members: Mapped[list["User"]] = relationship(
        back_populates="team",
        cascade="save-update, merge"  # ← SEM delete
    )

class User(Base):
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT")  # ← Banco impede deleção
    )

# Comportamento:
team = session.get(Team, 1)
session.delete(team)
session.commit()  # ❌ IntegrityError! Tem users vinculados.

# Precisa remover users primeiro ou usar SET NULL
```

### Padrão Recomendado

```python
# Para COMPOSIÇÃO (filhos pertencem ao pai):
# Ex: Chat → Messages, Order → OrderItems
messages: Mapped[list["Message"]] = relationship(
    back_populates="chat",
    cascade="all, delete-orphan",  # Python deleta filhos
    lazy="raise"
)
# + ondelete="CASCADE" na FK (banco deleta se for DELETE direto)

# Para ASSOCIAÇÃO (filhos são independentes):
# Ex: Team → Users, Category → Products
members: Mapped[list["User"]] = relationship(
    back_populates="team",
    cascade="save-update, merge",  # Padrão, sem delete
    lazy="raise"
)
# + ondelete="RESTRICT" na FK (banco impede deleção)
```

### Armadilha: Cascade sem ondelete

```python
# ❌ PROBLEMA: cascade="delete" mas ondelete não definido
class Chat(Base):
    messages: Mapped[list["Message"]] = relationship(
        cascade="all, delete-orphan"  # Python deleta
    )

class Message(Base):
    message_chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id")  # ← Sem ondelete!
    )

# Se alguém fizer DELETE direto no banco:
# DELETE FROM chats WHERE id = 1;
# ❌ Messages ficam órfãs com FK inválida!

# ✅ CORRETO: Defina AMBOS
ForeignKey("chats.id", ondelete="CASCADE")  # Banco também deleta
```

---

## 2.8 Relacionamentos Avançados

### Self-Referential (Autoreferência)

**Exemplo**: Ticket pode ter subtarefas (outros tickets).

```python
class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_title: Mapped[str] = mapped_column(String(200))

    # FK para ticket pai (opcional)
    parent_ticket_id: Mapped[int | None] = mapped_column(
        ForeignKey("tickets.id"),
        nullable=True
    )

    # Relationship para ticket pai
    parent_ticket: Mapped["Ticket | None"] = relationship(
        "Ticket",
        remote_side=[id],  # Define qual lado é o "pai"
        back_populates="subtasks",
        lazy="raise"
    )

    # Relationship para subtarefas
    subtasks: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="parent_ticket",
        lazy="raise"
    )
```

**Uso**:
```python
# Criar ticket pai
parent = Ticket(ticket_title="Migração de banco de dados")
session.add(parent)
session.commit()

# Criar subtarefas
subtask1 = Ticket(ticket_title="Backup do banco", parent_ticket_id=parent.id)
subtask2 = Ticket(ticket_title="Executar migration", parent_ticket_id=parent.id)
session.add_all([subtask1, subtask2])
session.commit()

# Navegar
parent = session.query(Ticket).options(selectinload(Ticket.subtasks)).first()
for subtask in parent.subtasks:
    print(subtask.ticket_title)
```

### Múltiplas FKs para a Mesma Tabela

Quando você tem múltiplas FKs apontando para a mesma tabela, SQLAlchemy não consegue inferir automaticamente qual FK usar para cada relationship. Você PRECISA especificar o parâmetro `foreign_keys`.

#### Caso 1: Ticket → User (cliente E atendente)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   Ticket tem DUAS FKs para User:                                           │
│                                                                            │
│   ┌──────────────┐                         ┌──────────────┐                │
│   │   Ticket     │    ticket_client_id ───→│    User      │                │
│   │              │    ticket_attendant_id ─→│              │                │
│   └──────────────┘                         └──────────────┘                │
│                                                                            │
│   SQLAlchemy: "Qual FK usar para relationship 'client'?"                   │
│   Você: "foreign_keys=[ticket_client_id]"                                  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

**Implementação AMBOS OS LADOS**:

```python
# ═══════════════════════════════════════════════════════════════════════════
# LADO QUE TEM AS FKs - Ticket
# ═══════════════════════════════════════════════════════════════════════════
class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_title: Mapped[str] = mapped_column(String(200))

    # FK para cliente (User)
    ticket_client_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT")
    )

    # FK para atendente (User) - opcional
    ticket_attendant_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    # Relationships - PRECISA especificar foreign_keys!
    client: Mapped["User"] = relationship(
        foreign_keys=[ticket_client_id],       # ← QUAL FK usar
        back_populates="tickets_as_client",    # ← Nome no User
        lazy="raise"
    )

    attendant: Mapped["User | None"] = relationship(
        foreign_keys=[ticket_attendant_id],    # ← QUAL FK usar
        back_populates="tickets_as_attendant", # ← Nome no User
        lazy="raise"
    )


# ═══════════════════════════════════════════════════════════════════════════
# LADO REVERSO - User
# ═══════════════════════════════════════════════════════════════════════════
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(200))

    # Relationship reverso (como cliente) - retorna LISTA
    tickets_as_client: Mapped[list["Ticket"]] = relationship(
        foreign_keys="[Ticket.ticket_client_id]",  # ← String com nome completo
        back_populates="client",
        lazy="raise"
    )

    # Relationship reverso (como atendente) - retorna LISTA
    tickets_as_attendant: Mapped[list["Ticket"]] = relationship(
        foreign_keys="[Ticket.ticket_attendant_id]",  # ← String com nome completo
        back_populates="attendant",
        lazy="raise"
    )
```

#### Caso 2: Team ↔ User (membro E manager) - O CASO QUE VOCÊ PERGUNTOU!

Este caso é diferente porque:
- User TEM uma FK para Team (como membro): `user_team_id`
- Team TEM uma FK para User (como manager): `team_manager_id`

```
┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│   FKs em AMBAS as tabelas:                                                 │
│                                                                            │
│   ┌──────────────┐                         ┌──────────────┐                │
│   │   Team       │    team_manager_id ────→│    User      │                │
│   │              │←─── user_team_id ───────│              │                │
│   └──────────────┘                         └──────────────┘                │
│                                                                            │
│   Relacionamentos:                                                         │
│   1. User.team (membro) ← usa user_team_id (FK no User)                    │
│   2. User.managed_team (manager) ← usa team_manager_id (FK no TEAM!)       │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

**Implementação AMBOS OS LADOS**:

```python
# ═══════════════════════════════════════════════════════════════════════════
# Team - TEM FK para manager
# ═══════════════════════════════════════════════════════════════════════════
class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(100), unique=True)
    team_area: Mapped[Area] = mapped_column(Enum(Area))

    # FK para o manager - está AQUI no Team!
    team_manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        init=False
    )

    # ════════════════════════════════════════════════════════════════
    # RELATIONSHIPS
    # ════════════════════════════════════════════════════════════════

    # Relationship para o manager (1 Team → 1 User como manager)
    # PRECISA de foreign_keys porque há múltiplas relações Team ↔ User
    manager: Mapped["User | None"] = relationship(
        foreign_keys=[team_manager_id],      # ← Usa a FK LOCAL (nesta classe)
        back_populates="managed_team",       # ← Nome em User
        lazy="raise"
    )
    # ⚠️ NÃO chame de "manager_id" - relationships não têm "_id"!

    # Relationship para os membros (1 Team → N Users como membros)
    team_members: Mapped[list["User"]] = relationship(
        foreign_keys="[User.user_team_id]",  # ← A FK está no USER!
        back_populates="team",               # ← Nome em User
        lazy="raise"
    )


# ═══════════════════════════════════════════════════════════════════════════
# User - TEM FK para team (como membro)
# ═══════════════════════════════════════════════════════════════════════════
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(200))

    # FK para o time (como membro) - está AQUI no User!
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False
    )

    # ════════════════════════════════════════════════════════════════
    # RELATIONSHIPS
    # ════════════════════════════════════════════════════════════════

    # Relationship: Este user PERTENCE a um Team (como membro)
    team: Mapped["Team"] = relationship(
        foreign_keys=[user_team_id],         # ← Usa a FK LOCAL (nesta classe)
        back_populates="team_members",       # ← Nome em Team
        lazy="raise"
    )

    # Relationship: Este user GERENCIA um Team (como manager)
    # ⚠️ A FK NÃO está aqui, está no Team!
    managed_team: Mapped["Team | None"] = relationship(
        foreign_keys="[Team.team_manager_id]",  # ← A FK está no TEAM!
        back_populates="manager",                # ← Nome em Team
        uselist=False,                          # ← Retorna 1 objeto, não lista
        lazy="raise"
    )
```

#### ⚠️ Dica: `foreign_keys` - Quando Usar Variável vs String?

```python
# Quando a FK está NA MESMA CLASSE, use a variável diretamente:
foreign_keys=[ticket_client_id]      # ✅ Variável
foreign_keys=[team_manager_id]       # ✅ Variável
foreign_keys=[user_team_id]          # ✅ Variável

# Quando a FK está em OUTRA CLASSE, use string:
foreign_keys="[User.user_team_id]"   # ✅ String (FK está em User)
foreign_keys="[Team.team_manager_id]" # ✅ String (FK está em Team)
foreign_keys="[Ticket.ticket_client_id]" # ✅ String (FK está em Ticket)
```

---

## 2.9 Guia Completo: Implementação de Relacionamentos em AMBOS OS LADOS

Esta seção é um guia definitivo para você nunca mais errar na implementação de relacionamentos. Vamos analisar cada tipo com diagramas, código completo e explicações de **O QUE VAI EM CADA LADO**.

### 🎯 Conceito Fundamental: Quem Tem a FK?

Antes de tudo, você precisa entender a **regra de ouro**:

```
┌────────────────────────────────────────────────────────────────────────────┐
│  A FOREIGN KEY SEMPRE FICA NO LADO "MUITOS" DO RELACIONAMENTO              │
│                                                                            │
│  1 Team  → N Users     →  FK fica em User (user_team_id)                   │
│  1 User  → N Reports   →  FK fica em Report (report_owner)                 │
│  1 Report → N Tickets  →  FK fica em Ticket (ticket_report_id)             │
└────────────────────────────────────────────────────────────────────────────┘
```

**Por quê?** Porque você não pode armazenar "múltiplos IDs" em uma única coluna Integer. Você precisa que cada registro do lado "muitos" aponte para o registro do lado "um".

### 📊 Diagrama Visual: Os Dois Lados

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     LADO "UM" (Team)          LADO "MUITOS" (User)          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FÍSICO (COLUNAS):                                                          │
│  ┌─────────────────┐                    ┌──────────────────────┐            │
│  │ id (PK)         │◄───────────────────│ user_team_id (FK)    │            │
│  │ team_name       │                    │ user_full_name       │            │
│  │                 │                    │ user_email           │            │
│  │ ❌ NÃO TEM FK   │                    │ ✅ TEM A FK          │            │
│  └─────────────────┘                    └──────────────────────┘            │
│                                                                             │
│  VIRTUAL (RELATIONSHIPS):                                                   │
│  ┌─────────────────┐                    ┌──────────────────────┐            │
│  │ team_members    │                    │ team                 │            │
│  │ Mapped[list[    │←──back_populates──→│ Mapped["Team"]       │            │
│  │   "User"]]      │                    │                      │            │
│  │ ✅ LISTA        │                    │ ✅ OBJETO ÚNICO      │            │
│  └─────────────────┘                    └──────────────────────┘            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 🔧 Implementação 1-N: Team → Users (COMPLETA)

#### LADO "UM" - Team (não tem FK, tem lista no relationship)

```python
# team.py
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Team(Base):
    __tablename__ = "teams"

    # ════════════════════════════════════════════════════════════════
    # COLUNAS FÍSICAS (existem no banco de dados)
    # ════════════════════════════════════════════════════════════════
    team_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    team_area: Mapped[Area] = mapped_column(Enum(Area), nullable=False)

    # ❌ ERRO COMUM: Criar coluna para armazenar "os usuários"
    # team_members: Mapped[int] = mapped_column(Integer)  # ERRADO!
    # ↑ Uma coluna Integer NÃO PODE armazenar múltiplos IDs!

    # ════════════════════════════════════════════════════════════════
    # COLUNAS VIRTUAIS (relationships - NÃO existem no banco)
    # ════════════════════════════════════════════════════════════════

    # O lado "UM" tem uma LISTA do lado "muitos"
    team_members: Mapped[list["User"]] = relationship(
        back_populates="team",    # Nome do relationship NO OUTRO LADO
        lazy="raise"              # Força eager loading explícito
    )

    # ↑ Mapeamento:
    # - Mapped[list["User"]] → É uma lista de objetos User
    # - back_populates="team" → O User tem um relationship chamado "team"
    # - NÃO precisa de foreign_keys porque só há uma FK User→Team
```

#### LADO "MUITOS" - User (TEM a FK, tem objeto único no relationship)

```python
# user.py
from sqlalchemy import ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    # ════════════════════════════════════════════════════════════════
    # COLUNAS FÍSICAS (existem no banco de dados)
    # ════════════════════════════════════════════════════════════════
    user_full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    user_email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

    # ✅ A FK FICA AQUI - no lado "muitos"
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),  # ← ondelete DENTRO de ForeignKey!
        nullable=False
    )

    # ════════════════════════════════════════════════════════════════
    # COLUNAS VIRTUAIS (relationships - NÃO existem no banco)
    # ════════════════════════════════════════════════════════════════

    # O lado "MUITOS" tem um OBJETO ÚNICO do lado "um"
    team: Mapped["Team"] = relationship(
        back_populates="team_members",  # Nome do relationship NO OUTRO LADO
        lazy="raise"
    )

    # ↑ Mapeamento:
    # - Mapped["Team"] → É um único objeto Team (não lista!)
    # - back_populates="team_members" → O Team tem um relationship chamado "team_members"
    # - NÃO precisa de foreign_keys porque só há uma FK
```

### 🔧 Implementação N-1 com Múltiplas FKs: User como Manager E Membro

Este é o caso que você perguntou: como implementar `User.managed_team` quando o User já é membro de um Team?

#### O Problema

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  User PODE ter DOIS relacionamentos com Team:                                │
│                                                                              │
│  1. Como MEMBRO  → user_team_id (FK) → Relationship: team                    │
│  2. Como MANAGER → team_manager_id (FK no Team!) → Relationship: managed_team│
│                                                                              │
│  O segundo caso é ESPECIAL porque a FK está no TEAM, não no User!            │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### Diagrama Visual

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ┌──────────────────────────────────────────┐                              │
│   │               Team                       │                              │
│   ├──────────────────────────────────────────┤                              │
│   │ id (PK)                                  │                              │
│   │ team_name                                │                              │
│   │ team_manager_id (FK→User) ──────────────────┐   ← FK para o manager     │
│   ├──────────────────────────────────────────┤  │                           │
│   │ RELATIONSHIPS:                           │  │                           │
│   │ • manager (Mapped["User | None"])        │◄─┘                           │
│   │ • team_members (Mapped[list["User"]])    │◄────┐                        │
│   └──────────────────────────────────────────┘     │                        │
│                          ▲                         │                        │
│                          │ back_populates          │ back_populates         │
│                          │ "managed_team"          │ "team"                 │
│                          │                         │                        │
│   ┌──────────────────────┴───────────────────┐     │                        │
│   │               User                       │     │                        │
│   ├──────────────────────────────────────────┤     │                        │
│   │ id (PK)                                  │     │                        │
│   │ user_full_name                           │     │                        │
│   │ user_team_id (FK→Team) ─────────────────────────┘   ← FK para o time    │
│   ├──────────────────────────────────────────┤                              │
│   │ RELATIONSHIPS:                           │                              │
│   │ • team (Mapped["Team"])                  │    Como membro               │
│   │ • managed_team (Mapped["Team | None"])   │    Como manager              │
│   └──────────────────────────────────────────┘                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### IMPLEMENTAÇÃO COMPLETA - Team (com FK para manager)

```python
# team.py
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Team(Base):
    __tablename__ = "teams"

    # ════════════════════════════════════════════════════════════════
    # COLUNAS FÍSICAS
    # ════════════════════════════════════════════════════════════════
    team_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    team_area: Mapped[Area] = mapped_column(Enum(Area), nullable=False)
    team_description: Mapped[str | None] = mapped_column(String(500), nullable=True, init=False)

    # FK para o manager (User) - OPCIONAL porque nem todo time tem manager
    team_manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),  # Se o user for deletado, manager vira NULL
        nullable=True,
        init=False  # Não é obrigatório no construtor
    )

    # ❌ ERRADO: Colunas Integer para armazenar relacionamentos 1-N
    # team_reports: Mapped[int | None] = mapped_column(Integer)  # NÃO FAZ ISSO!
    # team_projects: Mapped[int | None] = mapped_column(Integer)  # NÃO FAZ ISSO!

    # ════════════════════════════════════════════════════════════════
    # COLUNAS VIRTUAIS (Relationships)
    # ════════════════════════════════════════════════════════════════

    # Relationship para o manager
    # ⚠️ PRECISA de foreign_keys porque há múltiplas FKs entre Team e User
    manager: Mapped["User | None"] = relationship(
        foreign_keys=[team_manager_id],      # Especifica QUAL FK usar
        back_populates="managed_team",       # Nome no User
        lazy="raise"
    )
    # ↑ Notas:
    # - Mapped["User | None"] → Pode ser None (time sem manager)
    # - foreign_keys=[team_manager_id] → USA A VARIÁVEL, não string!
    # - NÃO chame de "manager_id" - relationships não têm "_id"!

    # Relationship para os membros
    team_members: Mapped[list["User"]] = relationship(
        foreign_keys="[User.user_team_id]",  # Pode ser string quando a FK está no outro lado
        back_populates="team",
        lazy="raise"
    )
```

#### IMPLEMENTAÇÃO COMPLETA - User (com managed_team)

```python
# user.py
from sqlalchemy import ForeignKey, String, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    # ════════════════════════════════════════════════════════════════
    # COLUNAS FÍSICAS
    # ════════════════════════════════════════════════════════════════
    user_corporative_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    user_full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    user_email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)

    # FK para o time do usuário (como membro)
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False
    )

    # ════════════════════════════════════════════════════════════════
    # COLUNAS VIRTUAIS (Relationships)
    # ════════════════════════════════════════════════════════════════

    # Relationship: Este user PERTENCE a um Team (como membro)
    team: Mapped["Team"] = relationship(
        foreign_keys=[user_team_id],         # Especifica a FK
        back_populates="team_members",       # Nome no Team
        lazy="raise"
    )

    # Relationship: Este user GERENCIA um Team (como manager)
    # ⚠️ A FK está no Team (team_manager_id), não aqui!
    managed_team: Mapped["Team | None"] = relationship(
        foreign_keys="[Team.team_manager_id]",  # FK está na OUTRA tabela!
        back_populates="manager",                # Nome no Team
        uselist=False,                          # Um user gerencia no máximo 1 time
        lazy="raise"
    )
    # ↑ Notas:
    # - Mapped["Team | None"] → O user pode não gerenciar nenhum time
    # - foreign_keys="[Team.team_manager_id]" → A FK está no Team, não no User!
    # - uselist=False → Retorna objeto único, não lista
```

### 🔧 Implementação N-N: User ↔ Report (Tabela de Associação)

Para relacionamentos N-N, você PRECISA de uma tabela de associação.

#### Por Que Não Pode Usar Integer?

```python
# ❌ ERRADO - Isso NÃO funciona!
class User(Base):
    user_reports_follow: Mapped[int | None] = mapped_column(Integer)
    # ↑ Uma coluna Integer só armazena UM número!
    # Como você guardaria: "Este user segue os reports 1, 5, 12, 23"?
    # Resposta: NÃO DÁ.
```

#### Solução: Tabela de Associação

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ┌──────────────┐      ┌────────────────────────┐      ┌────────────────┐  │
│   │    User      │      │   user_report_follow   │      │     Report     │  │
│   ├──────────────┤      ├────────────────────────┤      ├────────────────┤  │
│   │ id (PK)      │◄─────│ user_id (FK, PK)       │      │ id (PK)        │  │
│   │ user_name    │      │ report_id (FK, PK) ────────────►report_name    │  │
│   │              │      │ followed_at            │      │                │  │
│   │              │      │ notification_enabled   │      │                │  │
│   └──────────────┘      └────────────────────────┘      └────────────────┘  │
│                                                                             │
│   Um User pode seguir MUITOS Reports                                        │
│   Um Report pode ser seguido por MUITOS Users                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Implementação Completa N-N

```python
# association_tables.py
from sqlalchemy import Table, Column, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from infra.configs.database import Base

# Tabela de associação SIMPLES (sem atributos extras)
user_report_follow = Table(
    "user_report_follow",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("report_id", ForeignKey("reports.id", ondelete="CASCADE"), primary_key=True)
)

# OU Tabela de associação COM atributos extras
class UserReportFollow(Base):
    __tablename__ = "user_report_follow"

    # PKs compostas
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Atributos extras do relacionamento
    followed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    notification_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships para navegação
    user: Mapped["User"] = relationship(back_populates="report_follows")
    report: Mapped["Report"] = relationship(back_populates="followers")
```

#### No User

```python
# user.py
class User(Base):
    __tablename__ = "users"

    # ... outras colunas ...

    # ❌ ERRADO: Colunas Integer para N-N
    # user_reports_follow: Mapped[int | None] = mapped_column(Integer)

    # ✅ CERTO: Relationship com tabela de associação
    # Opção 1: Tabela simples (sem atributos)
    followed_reports: Mapped[list["Report"]] = relationship(
        secondary=user_report_follow,  # Nome da tabela de associação
        back_populates="followers",
        lazy="raise"
    )

    # Opção 2: Tabela com atributos (Association Object)
    report_follows: Mapped[list["UserReportFollow"]] = relationship(
        back_populates="user",
        lazy="raise"
    )
```

#### No Report

```python
# report.py
class Report(Base):
    __tablename__ = "reports"

    # ... outras colunas ...

    # ✅ CERTO: Relationship reverso
    # Opção 1: Tabela simples
    followers: Mapped[list["User"]] = relationship(
        secondary=user_report_follow,
        back_populates="followed_reports",
        lazy="raise"
    )

    # Opção 2: Tabela com atributos
    followers: Mapped[list["UserReportFollow"]] = relationship(
        back_populates="report",
        lazy="raise"
    )
```

### 📋 Checklist de Validação: back_populates

Use esta tabela para validar seus relacionamentos:

| Relationship em A | back_populates | Relationship em B | back_populates | ✓ |
|-------------------|----------------|-------------------|----------------|---|
| Team.manager | "managed_team" | User.managed_team | "manager" | ✅ |
| Team.team_members | "team" | User.team | "team_members" | ✅ |
| Report.team | "team_reports" | Team.team_reports | "team" | ✅ |
| Report.owner | "user_reports" | User.user_reports | "owner" | ✅ |

**Regra**: O `back_populates` de A deve ser o NOME do relationship em B, e vice-versa.

### 🚫 Erros Comuns e Correções

#### Erro 1: Nomear relationship com "_id"

```python
# ❌ ERRADO
manager_id: Mapped["User"] = relationship(...)  # "_id" é para FK, não relationship!

# ✅ CERTO
manager: Mapped["User"] = relationship(...)
```

#### Erro 2: Usar Integer para relacionamentos 1-N ou N-N

```python
# ❌ ERRADO
team_reports: Mapped[int | None] = mapped_column(Integer)  # Uma coluna = um valor!

# ✅ CERTO
team_reports: Mapped[list["Report"]] = relationship(back_populates="team")
```

#### Erro 3: Duplicar nome entre coluna e relationship

```python
# ❌ ERRADO - Mesmo nome "team_reports" para coluna E relationship!
team_reports: Mapped[int | None] = mapped_column(Integer)  # Linha 28
team_reports: Mapped[list["Report"]] = relationship(...)   # Linha 35

# ✅ CERTO - Remova a coluna Integer, use apenas o relationship
team_reports: Mapped[list["Report"]] = relationship(back_populates="team")
```

#### Erro 4: ondelete no lugar errado

```python
# ❌ ERRADO - ondelete em mapped_column
user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), ondelete="RESTRICT")

# ✅ CERTO - ondelete DENTRO de ForeignKey
user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="RESTRICT"))
```

#### Erro 5: Mapped[list["Ticket | None"]]

```python
# ❌ ERRADO - Union dentro de list não faz sentido
report_tickets: Mapped[list["Ticket | None"]] = relationship(...)

# ✅ CERTO - A lista pode estar vazia, mas os itens são Ticket
report_tickets: Mapped[list["Ticket"]] = relationship(...)
```

#### Erro 6: to_dict() referenciando campos inexistentes

```python
# ❌ ERRADO
def to_dict(self):
    return {
        'report_client_owner': self.report_client_owner,  # Campo não existe!
        'report_active_tickets': self.report_active_tickets,  # Campo não existe!
    }

# ✅ CERTO - Use os nomes reais das colunas
def to_dict(self):
    return {
        'report_owner': self.report_owner,  # Nome correto
        # report_active_tickets não é coluna, é um relationship (se existir)
    }
```

### 📊 Tabela Resumo: O Que Vai em Cada Lado

| Tipo | Lado "UM" | Lado "MUITOS" |
|------|-----------|---------------|
| **Coluna FK** | ❌ Não tem | ✅ Tem |
| **Relationship** | `Mapped[list["X"]]` | `Mapped["Y"]` |
| **back_populates** | Nome do relationship no lado MUITOS | Nome do relationship no lado UM |
| **foreign_keys** | Necessário se múltiplas FKs | Necessário se múltiplas FKs |

---

# MÓDULO 3: ARQUITETURA PROFISSIONAL

## Por Que Este Módulo É Crítico?

Você pode ter o melhor código SQLAlchemy do mundo, mas se a **arquitetura** estiver errada, sua aplicação vai:
- Ser impossível de testar
- Ter bugs difíceis de encontrar
- Ser lenta e não escalar
- Ser um pesadelo para manter

Este módulo ensina a arquitetura que **empresas de verdade** usam em produção.

---

## Background: Padrões Arquiteturais

Antes de mostrar a arquitetura que usamos, você precisa entender **por que** ela existe e quais eram as alternativas.

### O Problema: Código Espaguete

Sem arquitetura definida, código tende a virar "espaguete":

```python
# ❌ Tudo misturado (código espaguete)
@app.post("/tickets")
def create_ticket(data: dict):
    # Validação manual
    if not data.get("title"):
        raise HTTPException(400, "Título obrigatório")
    if len(data["title"]) > 200:
        raise HTTPException(400, "Título muito longo")

    # Lógica de negócio misturada
    user = session.query(User).get(data["user_id"])
    if not user:
        raise HTTPException(404, "Usuário não encontrado")
    if user.active != Status.ATIVO:
        raise HTTPException(400, "Usuário inativo")

    # Criação misturada com envio de email
    ticket = Ticket(**data)
    session.add(ticket)
    session.commit()

    # Email misturado com resposta
    send_email(user.email, "Ticket criado", ticket.title)

    # Serialização manual
    return {
        "id": ticket.id,
        "title": ticket.title,
        "user": {"id": user.id, "name": user.name}
    }
```

**Problemas**:
- 🔴 **Testabilidade zero**: Como testar só a validação? Só o email?
- 🔴 **Duplicação**: Mesma validação em 10 endpoints diferentes
- 🔴 **Fragilidade**: Mudar email quebra criação de ticket
- 🔴 **Performance**: Não tem como otimizar queries isoladamente

### Padrões Arquiteturais Existentes

| Padrão | Descrição | Prós | Contras |
|--------|-----------|------|---------|
| **MVC** | Model-View-Controller | Simples, familiar | Controller vira "god class" |
| **Clean Architecture** | Camadas com dependência unidirecional | Muito testável | Complexo para projetos pequenos |
| **Hexagonal** | Portas e Adaptadores | Muito flexível | Curva de aprendizado alta |
| **DDD** | Domain-Driven Design | Ótimo para domínios complexos | Overkill para CRUDs |
| **Layered** | Camadas simples | Fácil de entender | Pode virar "lasanha" |

### Nossa Escolha: Layered Architecture Simplificada

Usamos uma **Layered Architecture** (arquitetura em camadas) simplificada, inspirada em Clean Architecture mas sem a complexidade excessiva.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           NOSSA ARQUITETURA                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ API LAYER (endpoints)                                                │   │
│  │ - Recebe HTTP requests                                               │   │
│  │ - Valida entrada com Schemas                                         │   │
│  │ - Chama Services                                                     │   │
│  │ - Retorna HTTP responses                                             │   │
│  └───────────────────────────────────┬─────────────────────────────────┘   │
│                                      ↓                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ SERVICE LAYER (lógica de negócio)                                    │   │
│  │ - Regras de negócio                                                  │   │
│  │ - Orquestração de operações                                          │   │
│  │ - Validações de domínio                                              │   │
│  │ - Transações                                                         │   │
│  └───────────────────────────────────┬─────────────────────────────────┘   │
│                                      ↓                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ REPOSITORY LAYER (acesso a dados)                                    │   │
│  │ - Queries SQL/ORM                                                    │   │
│  │ - CRUD operations                                                    │   │
│  │ - Abstração do banco                                                 │   │
│  └───────────────────────────────────┬─────────────────────────────────┘   │
│                                      ↓                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ ENTITY LAYER (models)                                                │   │
│  │ - Estrutura das tabelas                                              │   │
│  │ - Relacionamentos                                                    │   │
│  │ - Sem lógica de negócio!                                             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

REGRA DE OURO: Seta só aponta para BAIXO (nunca para cima!)
- API conhece Service, mas Service não conhece API
- Service conhece Repository, mas Repository não conhece Service
```

### Por Que Esta Arquitetura?

| Critério | Nossa Arquitetura | MVC Tradicional |
|----------|-------------------|-----------------|
| **Testabilidade** | ✅ Mock de cada camada | ❌ Controller testa tudo junto |
| **Reutilização** | ✅ Service usado em API, CLI, tasks | ❌ Lógica presa no Controller |
| **Manutenção** | ✅ Mudança isolada por camada | ❌ Mudança propaga |
| **Performance** | ✅ Queries otimizadas no Repository | ❌ N+1 espalhado |
| **Curva de aprendizado** | ⚠️ Média | ✅ Baixa |

### Extensibilidade: Módulos Futuros

Esta arquitetura facilita adicionar funcionalidades sem modificar o existente:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MÓDULOS FUTUROS (mesma arquitetura)                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📧 Email Service              │  📊 Excel Export              │           │
│  - Notificações de ticket      │  - Relatórios em planilha     │           │
│  - Usa TicketService           │  - Usa ReportService          │           │
│                                │                                │           │
│  🔄 Task Queue (Celery)        │  📱 Webhooks                   │           │
│  - Processos assíncronos       │  - Integrações externas        │           │
│  - Usa Services existentes     │  - Usa Services existentes     │           │
│                                                                             │
│  Todos reutilizam a MESMA camada de Services!                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Introdução: Da Simplicidade à Escala

Quando você começa um projeto, `to_dict()` nos models parece perfeito. É simples, direto, funciona. Mas conforme a aplicação cresce, problemas sutis aparecem e se tornam críticos.

### A Evolução Natural de uma API

```
FASE 1: Protótipo (funciona)
┌────────────────────────────┐
│ Model com to_dict()        │  ← Simples, rápido de fazer
│        ↓                   │
│ return model.to_dict()     │  ← "Funciona!"
└────────────────────────────┘

FASE 2: Produção (problemas começam)
┌────────────────────────────┐
│ 1000 users, cada um tem    │  ← N+1 queries
│ team, team tem members...  │  ← Recursão infinita
│                            │  ← Performance terrível
│ ❌ to_dict() não escala    │
└────────────────────────────┘

FASE 3: Maturidade (arquitetura correta)
┌────────────────────────────┐
│ Models (apenas estrutura)  │
│        ↓                   │
│ Services (lógica)          │
│        ↓                   │
│ Schemas (serialização)     │
│        ↓                   │
│ API (endpoints)            │
└────────────────────────────┘
```

Este módulo ensina a arquitetura da **Fase 3** - aquela que escala e se mantém.

### Por Que Arquitetura Importa?

**Sem arquitetura** (tudo misturado):
```python
@app.get("/users")
def get_users():
    # ❌ Tudo no endpoint
    users = session.query(User).all()
    return [
        {
            'id': u.id,
            'name': u.name,
            'team': u.team.to_dict() if u.team else None  # N+1!
        }
        for u in users
    ]
```

**Problemas**:
- ❌ Lógica de negócio no endpoint (difícil testar)
- ❌ Serialização manual (propenso a erros)
- ❌ N+1 queries (performance)
- ❌ Sem validação (segurança)
- ❌ Sem documentação automática
- ❌ Difícil manter e evoluir

**Com arquitetura** (separação de responsabilidades):
```python
# Model: apenas estrutura
class User(Base):
    # Sem to_dict()!

# Schema: serialização
class UserList(BaseModel):
    id: int
    name: str

# Service: lógica
class UserService:
    def list_users(self) -> list[User]:
        return self.repo.list_active()

# Endpoint: coordenação
@app.get("/users", response_model=list[UserList])
def get_users(service: UserService = Depends()):
    return service.list_users()
```

**Vantagens**:
- ✅ Cada camada tem responsabilidade clara
- ✅ Fácil testar (mock services)
- ✅ Performance controlada (eager loading no service)
- ✅ Validação automática (Pydantic)
- ✅ Documentação automática (OpenAPI)
- ✅ Fácil manter e evoluir

---

## 3.1 Por Que Não Usar to_dict() nos Models

### Entendendo o Contexto

`to_dict()` é um padrão comum em tutoriais e projetos pequenos. A ideia é simples: converter o model em dicionário para retornar no JSON.

```python
class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

# Uso:
user = session.get(User, 1)
return user.to_dict()  # {'id': 1, 'name': 'Matheus'}
```

**Parece perfeito... mas tem problemas graves.**

### O Problema: Três Falhas Fatais

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_full_name: Mapped[str] = mapped_column(String(200))

    # Relationship
    team: Mapped["Team"] = relationship(back_populates="team_members")

    def to_dict(self) -> dict:
        """❌ PROBLEMA: Como serializar relationship?"""
        return {
            'id': self.id,
            'user_full_name': self.user_full_name,
            'team': self.team  # ❌ Não é JSON serializável!
        }
```

### 3 Problemas Fatais

#### 1. Recursão Infinita

```python
class Team(Base):
    team_members: Mapped[list["User"]] = relationship(...)

    def to_dict(self):
        return {
            'id': self.id,
            'team_members': [member.to_dict() for member in self.team_members]
        }

class User(Base):
    team: Mapped["Team"] = relationship(...)

    def to_dict(self):
        return {
            'id': self.id,
            'team': self.team.to_dict()  # ❌ Chama team_members.to_dict() que chama user.to_dict()...
        }

# Uso:
user = session.get(User, 1)
user.to_dict()  # ❌ RecursionError: maximum recursion depth exceeded!
```

**Ciclo infinito**:
```
user.to_dict()
  → team.to_dict()
    → member.to_dict()
      → team.to_dict()
        → member.to_dict()
          → ... INFINITO!
```

#### 2. Não é JSON Serializável

```python
user = session.get(User, 1)
data = user.to_dict()

# ❌ TypeError: Object of type User is not JSON serializable
json.dumps(data)
```

**Tipos problemáticos**:
- Objetos SQLAlchemy (User, Team, etc.)
- datetime, date
- Decimal
- Enum

#### 3. Performance Desastrosa (N+1 Queries)

```python
# Buscar 100 users
users = session.query(User).limit(100).all()

# Serializar
users_dict = [user.to_dict() for user in users]
# ❌ Se to_dict() acessa relationships, faz 100+ queries adicionais!
```

### Solução: Não Use to_dict()!

**Em vez de** to_dict() no model:
```python
# ❌ NÃO FAÇA:
class User(Base):
    def to_dict(self):
        return {...}
```

**Use** Pydantic schemas (veremos em 3.2):
```python
# ✅ FAÇA:
class UserSchema(BaseModel):
    id: int
    user_full_name: str

    class Config:
        from_attributes = True  # Permite criar de ORM model
```

---

## 3.2 Schemas com Pydantic

### Entendendo o Problema de Serialização

Quando você retorna dados de uma API, precisa resolver vários desafios:

1. **Serialização**: Converter objetos Python em JSON
2. **Validação**: Garantir que dados estão corretos
3. **Documentação**: Gerar docs automáticas
4. **Versionamento**: Múltiplas versões da mesma entidade
5. **Segurança**: Ocultar campos sensíveis (senha, tokens)
6. **Performance**: Controlar o que é incluído

`to_dict()` resolve apenas o #1 (mal). **Pydantic schemas** resolvem todos.

### Conceito: O Que São Schemas?

**Schema** (ou **DTO** - Data Transfer Object) é uma classe que define a **forma dos dados** que entram ou saem da API.

**Analogia**: Imagine que seus models são documentos internos da empresa (com tudo, incluindo dados confidenciais). Schemas são **formulários públicos** - você escolhe exatamente quais campos mostrar para cada situação.

```
Model (documento interno completo):
┌─────────────────────────────┐
│ User                        │
│ - id                        │
│ - name                      │
│ - email                     │
│ - password_hash  ← Sensível │
│ - salary         ← Sensível │
│ - created_at                │
│ - deleted_at     ← Interno  │
└─────────────────────────────┘

Schema UserList (formulário público para listagem):
┌─────────────────────────────┐
│ - id                        │  ← Apenas campos públicos
│ - name                      │     e relevantes para
│ - email                     │     esta operação
└─────────────────────────────┘

Schema UserDetail (formulário para detalhes):
┌─────────────────────────────┐
│ - id                        │  ← Mais campos, mas ainda
│ - name                      │     sem dados sensíveis
│ - email                     │
│ - created_at                │
└─────────────────────────────┘
```

### Definição: Pydantic Schemas

**Pydantic schemas** são classes Python que:

1. **Definem estrutura** de dados de entrada/saída
2. **Validam automaticamente** tipos e valores
3. **Serializam** para JSON (datetime → string, Enum → valor)
4. **Documentam** API (gera OpenAPI/Swagger)
5. **Isolam** regras de apresentação dos models

```python
from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int              # ← Validação automática (deve ser int)
    name: str            # ← Validação automática (deve ser str)
    email: str           # ← Validação automática (deve ser str)

    class Config:
        from_attributes = True  # Permite criar de ORM models
```

### Por Que Pydantic?

**Antes do Pydantic** (serialização manual):
```python
def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'created_at': user.created_at.isoformat() if user.created_at else None,  # Manual!
        'role': user.role.value if user.role else None  # Manual!
    }
```

**Com Pydantic** (automático):
```python
class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    role: UserRoles

    model_config = ConfigDict(from_attributes=True)

# Uso:
user_schema = UserSchema.from_orm(user)  # ✅ Tudo automático!
```

**Vantagens**:
- ✅ datetime → ISO string (automático)
- ✅ Enum → valor (automático)
- ✅ None handling (automático)
- ✅ Validação de tipos (automático)
- ✅ Documentação OpenAPI (automático)

### Instalação

```bash
pip install pydantic
```

### Schema Básico

```python
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserSchema(BaseModel):
    """Schema básico de User (sem relacionamentos)"""
    id: int
    user_full_name: str
    user_email: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    # from_attributes=True permite criar de ORM objects


# Uso:
user = session.get(User, 1)  # User ORM object
user_schema = UserSchema.from_orm(user)  # Converte para Pydantic
print(user_schema.model_dump())  # {'id': 1, 'user_full_name': '...', ...}
print(user_schema.model_dump_json())  # JSON string
```

### Múltiplos Schemas por Entidade

**PADRÃO RECOMENDADO**: Criar vários schemas para diferentes contextos.

```python
# ═══ 1. UserList - Para listagens ═══
class UserList(BaseModel):
    """Mínimo para listar usuários"""
    id: int
    user_full_name: str
    user_email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# ═══ 2. UserDetail - Para detalhes ═══
class UserDetail(BaseModel):
    """Mais campos, sem relacionamentos pesados"""
    id: int
    user_full_name: str
    user_email: str
    user_photo: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


# ═══ 3. UserWithTeam - Com relacionamento ═══
class TeamSimple(BaseModel):
    """Team simplificado (evita recursão)"""
    id: int
    team_name: str

    model_config = ConfigDict(from_attributes=True)


class UserWithTeam(BaseModel):
    """User com team incluído"""
    id: int
    user_full_name: str
    user_email: str
    is_active: bool
    team: TeamSimple  # Relationship incluído

    model_config = ConfigDict(from_attributes=True)


# ═══ 4. UserCreate - Para criação ═══
class UserCreate(BaseModel):
    """Dados necessários para criar user"""
    user_full_name: str
    user_email: str
    user_password: str
    user_team_id: int
    # Não inclui id, created_at (gerados automaticamente)


# ═══ 5. UserUpdate - Para atualização ═══
class UserUpdate(BaseModel):
    """Campos que podem ser atualizados (todos opcionais)"""
    user_full_name: str | None = None
    user_email: str | None = None
    user_photo: str | None = None
    is_active: bool | None = None
```

### Uso com FastAPI

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/users", response_model=list[UserList])
def list_users(db: Session = Depends(get_db)):
    """Lista usuários (schema simplificado)"""
    users = db.query(User).filter(User.deleted_at.is_(None)).all()
    return users  # FastAPI converte automaticamente usando UserList


@app.get("/users/{user_id}", response_model=UserWithTeam)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Detalhe do usuário (com team)"""
    user = (
        db.query(User)
        .options(joinedload(User.team))  # Eager load!
        .filter(User.id == user_id)
        .first()
    )
    return user  # FastAPI converte usando UserWithTeam


@app.post("/users", response_model=UserDetail)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Cria usuário"""
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

### Sintaxe Avançada do Pydantic

#### Field() - Configuração de Campos

`Field()` permite configurar validações, metadados e comportamentos de campos.

```python
from pydantic import BaseModel, Field
from typing import Annotated

class UserCreate(BaseModel):
    # ═══════════════════════════════════════════════════════════════════════
    # FIELD() - OPÇÕES COMPLETAS
    # ═══════════════════════════════════════════════════════════════════════

    # Obrigatório com validação de tamanho
    user_full_name: str = Field(
        ...,                          # ... = obrigatório (sem default)
        min_length=3,                 # Mínimo 3 caracteres
        max_length=100,               # Máximo 100 caracteres
        title="Nome completo",        # Para documentação
        description="Nome completo do usuário",
        examples=["Matheus Beck"]     # Exemplos no Swagger
    )

    # Email com regex
    user_email: str = Field(
        ...,
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",  # Regex de validação
        title="Email"
    )

    # Senha com validação de tamanho
    user_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        title="Senha",
        description="Mínimo 8 caracteres"
    )

    # Numérico com range
    idade: int = Field(
        default=None,
        ge=0,                         # >= 0
        le=150,                       # <= 150
        title="Idade"
    )

    # Com valor default
    is_active: bool = Field(default=True)

    # Com alias (nome diferente no JSON)
    team_id: int = Field(..., alias="teamId")
    # JSON: {"teamId": 5} → Python: team_id = 5

    # Campo excluído da serialização
    internal_field: str = Field(default="", exclude=True)

# ═══════════════════════════════════════════════════════════════════════════
# ANNOTATED - ALTERNATIVA MODERNA (Python 3.9+)
# ═══════════════════════════════════════════════════════════════════════════

from typing import Annotated
from pydantic import StringConstraints

# Tipo reutilizável com validação
NameStr = Annotated[str, StringConstraints(min_length=3, max_length=100)]
EmailStr = Annotated[str, StringConstraints(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")]

class UserCreateAnnotated(BaseModel):
    user_full_name: NameStr
    user_email: EmailStr
```

#### Validators - Validação Customizada

```python
from pydantic import BaseModel, field_validator, model_validator

class UserCreate(BaseModel):
    user_full_name: str
    user_email: str
    user_password: str
    password_confirm: str

    # ═══════════════════════════════════════════════════════════════════════
    # @field_validator - Valida UM campo específico
    # ═══════════════════════════════════════════════════════════════════════

    @field_validator("user_email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Valida e normaliza email."""
        if "@" not in v:
            raise ValueError("Email deve conter @")

        # Normalizar (lowercase)
        return v.lower().strip()

    @field_validator("user_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Valida força da senha."""
        if len(v) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")

        if not any(c.isupper() for c in v):
            raise ValueError("Senha deve ter pelo menos uma letra maiúscula")

        if not any(c.isdigit() for c in v):
            raise ValueError("Senha deve ter pelo menos um número")

        return v

    # ═══════════════════════════════════════════════════════════════════════
    # @model_validator - Valida MÚLTIPLOS campos juntos
    # ═══════════════════════════════════════════════════════════════════════

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "UserCreate":
        """Valida que password e password_confirm são iguais."""
        if self.user_password != self.password_confirm:
            raise ValueError("Senhas não conferem")
        return self

    # mode="before" - Executa ANTES da validação de campos
    @model_validator(mode="before")
    @classmethod
    def check_card_number_omitted(cls, data: dict) -> dict:
        """Exemplo: processar dados antes da validação."""
        if isinstance(data, dict):
            # Remover espaços de todos os campos string
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = value.strip()
        return data
```

#### computed_field - Campos Calculados

```python
from pydantic import BaseModel, computed_field

class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: str

    model_config = {"from_attributes": True}

    # ═══════════════════════════════════════════════════════════════════════
    # @computed_field - Campo calculado automaticamente
    # ═══════════════════════════════════════════════════════════════════════

    @computed_field
    @property
    def full_name(self) -> str:
        """Nome completo calculado."""
        return f"{self.first_name} {self.last_name}"

    @computed_field
    @property
    def email_domain(self) -> str:
        """Domínio do email."""
        return self.email.split("@")[-1]


# Uso:
user = UserResponse(first_name="Matheus", last_name="Beck", email="matheus@email.com")
print(user.full_name)      # "Matheus Beck"
print(user.email_domain)   # "email.com"
print(user.model_dump())
# {'first_name': 'Matheus', 'last_name': 'Beck', 'email': 'matheus@email.com',
#  'full_name': 'Matheus Beck', 'email_domain': 'email.com'}
```

#### model_config - Configurações do Schema

```python
from pydantic import BaseModel, ConfigDict

class UserSchema(BaseModel):
    id: int
    user_name: str
    user_email: str

    # ═══════════════════════════════════════════════════════════════════════
    # MODEL_CONFIG - Todas as opções importantes
    # ═══════════════════════════════════════════════════════════════════════

    model_config = ConfigDict(
        # ORM Mode - Permite criar de objetos SQLAlchemy
        from_attributes=True,

        # Validação
        strict=False,             # True = não converte tipos (str→int falha)
        validate_default=True,    # Valida valores default também
        validate_assignment=True, # Valida ao atribuir (user.name = 123 → erro)

        # Campos extras
        extra="forbid",           # "forbid" = erro se campos extras
                                  # "ignore" = ignora campos extras
                                  # "allow" = aceita campos extras

        # Serialização
        populate_by_name=True,    # Permite usar alias OU nome original
        use_enum_values=True,     # Enum → valor (não objeto Enum)

        # JSON
        json_schema_extra={       # Metadados extras para OpenAPI
            "examples": [
                {"id": 1, "user_name": "Matheus", "user_email": "m@e.com"}
            ]
        },

        # Alias
        alias_generator=lambda x: x.replace("_", "-"),  # user_name → user-name
    )
```

#### Herança de Schemas

```python
from pydantic import BaseModel

# ═══════════════════════════════════════════════════════════════════════════
# BASE SCHEMA - Campos comuns
# ═══════════════════════════════════════════════════════════════════════════

class UserBase(BaseModel):
    """Campos comuns a todos os schemas de User."""
    user_full_name: str
    user_email: str


# ═══════════════════════════════════════════════════════════════════════════
# SCHEMAS ESPECÍFICOS - Herdam de Base
# ═══════════════════════════════════════════════════════════════════════════

class UserCreate(UserBase):
    """Para criação - herda Base + adiciona senha."""
    user_password: str


class UserUpdate(BaseModel):
    """Para atualização - todos opcionais."""
    user_full_name: str | None = None
    user_email: str | None = None
    user_photo: str | None = None


class UserResponse(UserBase):
    """Para resposta - herda Base + adiciona campos do banco."""
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithRelations(UserResponse):
    """Para resposta com relacionamentos."""
    team: "TeamSimple | None" = None
    tickets_count: int = 0
```

#### Métodos de Serialização

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str  # Sensível!

user = User(id=1, name="Matheus", email="m@e.com", password_hash="xxx")

# ═══════════════════════════════════════════════════════════════════════════
# MÉTODOS DE SERIALIZAÇÃO
# ═══════════════════════════════════════════════════════════════════════════

# model_dump() - Converte para dict
user.model_dump()
# {'id': 1, 'name': 'Matheus', 'email': 'm@e.com', 'password_hash': 'xxx'}

# model_dump() com opções
user.model_dump(
    include={"id", "name"},       # Apenas estes campos
    exclude={"password_hash"},    # Excluir campos
    exclude_none=True,            # Remover campos None
    exclude_unset=True,           # Remover campos não setados
    exclude_defaults=True,        # Remover campos com valor default
    by_alias=True,                # Usar alias ao invés do nome
    mode="json"                   # Serializar para tipos JSON (datetime→str)
)

# model_dump_json() - Converte direto para JSON string
user.model_dump_json()
# '{"id": 1, "name": "Matheus", "email": "m@e.com", "password_hash": "xxx"}'

user.model_dump_json(indent=2, exclude={"password_hash"})
# {
#   "id": 1,
#   "name": "Matheus",
#   "email": "m@e.com"
# }

# model_copy() - Cria cópia com modificações
user2 = user.model_copy(update={"name": "Matheus Beck"})
# user2.name = "Matheus Beck", demais campos iguais

# model_validate() - Cria de dict com validação
user3 = User.model_validate({"id": 2, "name": "Ana", "email": "a@e.com", "password_hash": "yyy"})

# model_validate_json() - Cria de JSON string
user4 = User.model_validate_json('{"id": 3, "name": "Carlos", "email": "c@e.com", "password_hash": "zzz"}')
```

### Vantagens dos Schemas

| Aspecto | to_dict() | Pydantic Schemas |
|---------|-----------|------------------|
| **Recursão** | ❌ Problema | ✅ Controlado |
| **JSON** | ❌ Manual | ✅ Automático |
| **Validação** | ❌ Não | ✅ Sim |
| **Documentação** | ❌ Não | ✅ Swagger automático |
| **Múltiplas respostas** | ❌ Difícil | ✅ Fácil (vários schemas) |
| **Type hints** | ⚠️ Parcial | ✅ Total |
| **Controle campos** | ❌ Tudo ou nada | ✅ Granular |

---

## 3.3 Services - Camada de Negócio

### Arquitetura em Camadas

```
┌─────────────────────────────────────┐
│   API Layer (FastAPI)               │  ← Endpoints HTTP
│   - Validação de input              │
│   - Serialização de output          │
│   - HTTP status codes               │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│   Service Layer                     │  ← Lógica de negócio
│   - Regras de negócio               │
│   - Composição de operações         │
│   - Eager loading                   │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│   Repository Layer                  │  ← Acesso a dados
│   - CRUD básico                     │
│   - Queries específicas             │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│   Models (SQLAlchemy)               │  ← Estrutura do banco
│   - Definição de tabelas            │
│   - Relationships                   │
└─────────────────────────────────────┘
```

### Repository (Acesso a Dados)

```python
# infra/repositories/user_repository.py
from sqlalchemy.orm import Session
from infra.entities.user import User

class UserRepository:
    """Operações de acesso a dados (CRUD)"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        """Busca user por ID"""
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        """Busca user por email"""
        return (
            self.db.query(User)
            .filter(User.user_email == email)
            .filter(User.deleted_at.is_(None))
            .first()
        )

    def list_active(self, limit: int = 100, offset: int = 0) -> list[User]:
        """Lista users ativos"""
        return (
            self.db.query(User)
            .filter(User.deleted_at.is_(None))
            .filter(User.is_active == True)
            .limit(limit)
            .offset(offset)
            .all()
        )

    def create(self, user: User) -> User:
        """Cria user"""
        self.db.add(user)
        self.db.flush()  # Flush sem commit (deixa pra service)
        return user

    def update(self, user: User) -> User:
        """Atualiza user"""
        self.db.flush()
        return user

    def delete(self, user: User):
        """Delete físico"""
        self.db.delete(user)
        self.db.flush()
```

### Service (Lógica de Negócio)

```python
# services/user_service.py
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from infra.repositories.user_repository import UserRepository
from infra.entities.user import User, UserTipo, UserRoles

class UserService:
    """Lógica de negócio de usuários"""

    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def get_user_with_team(self, user_id: int) -> User | None:
        """Busca user com eager loading de team"""
        return (
            self.db.query(User)
            .options(joinedload(User.team))  # Eager load
            .filter(User.id == user_id)
            .filter(User.deleted_at.is_(None))
            .first()
        )

    def create_user(
        self,
        full_name: str,
        email: str,
        password: str,
        team_id: int,
        role: UserRoles,
        tipo: UserTipo
    ) -> User:
        """Cria usuário com validações de negócio"""

        # Validação: email já existe?
        existing = self.repo.get_by_email(email)
        if existing:
            raise ValueError(f"Email {email} já está em uso")

        # Criar user
        user = User(
            user_full_name=full_name,
            user_email=email,
            user_password=hash_password(password),  # Hash da senha
            user_team_id=team_id,
            user_role=role,
            user_tipo=tipo
        )

        self.repo.create(user)
        self.db.commit()  # Service faz commit
        self.db.refresh(user)

        return user

    def update_user(self, user_id: int, **updates) -> User:
        """Atualiza usuário"""
        user = self.repo.get_by_id(user_id)

        if not user:
            raise ValueError(f"User {user_id} não encontrado")

        if user.deleted_at:
            raise ValueError(f"User {user_id} foi deletado")

        # Atualizar campos
        for key, value in updates.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)

        self.repo.update(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def soft_delete_user(self, user_id: int, deleted_by: int):
        """Soft delete de usuário"""
        user = self.repo.get_by_id(user_id)

        if not user:
            raise ValueError(f"User {user_id} não encontrado")

        if user.deleted_at:
            raise ValueError(f"User {user_id} já foi deletado")

        # Soft delete
        user.deleted_at = datetime.now()
        user.deleted_by = deleted_by

        self.repo.update(user)
        self.db.commit()
```

### Vantagens do Service Layer

✅ **Separação de responsabilidades**
- Repository: SQL/banco
- Service: Regras de negócio
- API: HTTP/validação

✅ **Reusabilidade**
- Services podem ser chamados de múltiplos endpoints
- Lógica não fica duplicada

✅ **Testabilidade**
- Services podem ser testados sem FastAPI
- Repositories podem ser mockados

✅ **Manutenibilidade**
- Lógica de negócio em um só lugar
- Fácil encontrar onde alterar

### Devo Popular Dados Usando Services ou Repositories?

**Pergunta comum**: Ao criar dados de teste ou popular o banco, devo usar o Service (com validação) ou o Repository (direto)?

**Resposta**: Depende do contexto e da origem dos dados.

| Contexto | Use | Por quê |
|----------|-----|---------|
| **Produção (dados de usuário)** | Service | Validações de negócio são aplicadas |
| **Testes unitários** | Repository | Mais rápido, sem overhead de validação |
| **Seed/Fixtures iniciais** | Service | Garante dados válidos |
| **Migração de dados legados** | Repository | Performance, dados já foram validados antes |

**Em produção (sempre Service)**:

```python
# ✅ Service valida e aplica regras de negócio
user = user_service.create_user(
    full_name="Matheus",
    email="matheus@email.com",
    password="Pass123!",  # Service faz hash
    team_id=1
)
# O service:
# - Valida email único
# - Faz hash da senha
# - Verifica se team existe
# - Aplica regras de negócio
```

**Em testes (pode ser Repository)**:

```python
# Repository é mais rápido para criar dados de teste
user = User(
    user_full_name="Test User",
    user_email="test@test.com",
    user_password="already_hashed_password",  # Você controla
    user_team_id=1
)
repo.create(user)
# Sem validações = mais rápido para setup de testes
```

**Regra geral**: Se os dados vêm de **fora do sistema** (usuário, API externa, input humano), use Service. Se você **controla os dados** (testes automatizados, migrations de dados já validados), pode usar Repository.

---

## 3.4 API Endpoints com FastAPI

### O Que É FastAPI?

**FastAPI** é um framework web moderno para Python que combina:
- **Performance**: Uma das APIs mais rápidas do Python (comparável a Go e Node.js)
- **Type hints**: Validação automática usando Python type hints
- **Documentação automática**: Swagger UI e ReDoc gerados automaticamente
- **Async nativo**: Suporte a async/await para alta concorrência

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    POR QUE FASTAPI?                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PRODUTIVIDADE                                                              │
│  • Menos código para escrever                                               │
│  • Validação automática de entrada                                          │
│  • Documentação gerada automaticamente                                      │
│  • IDE autocomplete excelente (type hints)                                  │
│                                                                             │
│  PERFORMANCE                                                                │
│  • Baseado em Starlette (ASGI) e Pydantic                                   │
│  • Comparável a Node.js e Go                                                │
│  • Suporte nativo a async                                                   │
│                                                                             │
│  PADRÕES MODERNOS                                                           │
│  • OpenAPI (Swagger) automático                                             │
│  • JSON Schema automático                                                   │
│  • OAuth2 e JWT prontos                                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Conceitos Fundamentais

#### Routers e Organização

```python
# api/routes/users.py
from fastapi import APIRouter

# Criar router com prefixo e tags
router = APIRouter(
    prefix="/users",           # Todas as rotas começam com /users
    tags=["users"],            # Agrupamento no Swagger
    responses={404: {"description": "Not found"}}  # Respostas padrão
)

# Rotas são definidas no router
@router.get("")              # GET /users
@router.get("/{user_id}")    # GET /users/123
@router.post("")             # POST /users
@router.patch("/{user_id}")  # PATCH /users/123
@router.delete("/{user_id}") # DELETE /users/123
```

```python
# main.py - Incluir todos os routers
from fastapi import FastAPI
from api.routes import users, teams, tickets

app = FastAPI(
    title="Portal de Chamados API",
    description="API para gerenciamento de tickets, projetos e relatórios",
    version="1.0.0"
)

# Incluir routers
app.include_router(users.router)
app.include_router(teams.router)
app.include_router(tickets.router, prefix="/v1")  # Versionamento

# Acesse a documentação em:
# http://localhost:8000/docs      (Swagger UI)
# http://localhost:8000/redoc     (ReDoc)
```

#### Decorators - Sintaxe dos Endpoints

```python
from fastapi import APIRouter, status

router = APIRouter(prefix="/users", tags=["users"])

# ═══════════════════════════════════════════════════════════════════════════
# SINTAXE: @router.METODO("path", opções)
# ═══════════════════════════════════════════════════════════════════════════

@router.get("")                                    # GET /users
@router.get("/", response_model=list[UserSchema])  # Com response model
@router.get("/{id}")                               # Path parameter
@router.get("/{id}", status_code=200)              # Status code explícito

@router.post("", status_code=status.HTTP_201_CREATED)  # POST retorna 201
@router.put("/{id}")                               # PUT (substituição total)
@router.patch("/{id}")                             # PATCH (atualização parcial)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)  # DELETE 204

# ═══════════════════════════════════════════════════════════════════════════
# OPÇÕES DO DECORATOR
# ═══════════════════════════════════════════════════════════════════════════

@router.get(
    "/{user_id}",
    response_model=UserResponse,        # Schema da resposta
    response_model_exclude_none=True,   # Remove campos None
    status_code=200,                    # Status code
    summary="Buscar usuário",           # Título no Swagger
    description="Retorna detalhes...",  # Descrição longa
    deprecated=False,                   # Marcar como obsoleto
    tags=["users", "admin"],            # Tags extras
    responses={                         # Respostas possíveis
        404: {"description": "Usuário não encontrado"},
        422: {"description": "Dados inválidos"}
    }
)
def get_user(user_id: int):
    ...
```

#### Path Parameters (Parâmetros de URL)

```python
from fastapi import Path

# ═══════════════════════════════════════════════════════════════════════════
# PATH PARAMETERS: Vêm da URL
# ═══════════════════════════════════════════════════════════════════════════

# Básico - tipo inferido do type hint
@router.get("/{user_id}")
def get_user(user_id: int):  # user_id é int, FastAPI converte automaticamente
    ...

# Com validação usando Path()
@router.get("/{user_id}")
def get_user(
    user_id: int = Path(
        ...,                          # ... = obrigatório
        title="ID do usuário",
        description="ID único do usuário",
        ge=1,                         # >= 1
        le=1000000,                   # <= 1000000
        example=42
    )
):
    ...

# Múltiplos path params
@router.get("/{team_id}/users/{user_id}")
def get_team_user(team_id: int, user_id: int):
    ...
```

#### Query Parameters (Parâmetros de Busca)

```python
from fastapi import Query
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════
# QUERY PARAMETERS: Vêm após ? na URL
# GET /users?limit=10&offset=0&search=matheus
# ═══════════════════════════════════════════════════════════════════════════

@router.get("")
def list_users(
    # Obrigatório (sem default)
    status: str,

    # Opcional com default
    limit: int = 100,
    offset: int = 0,

    # Opcional sem default (None se não informado)
    search: Optional[str] = None,

    # Com validação usando Query()
    limit: int = Query(
        default=100,          # Valor padrão
        ge=1,                 # >= 1
        le=1000,              # <= 1000
        title="Limite",
        description="Máximo de resultados"
    ),

    # Query param como lista
    # GET /users?include=team&include=tickets
    include: list[str] = Query(default=[]),

    # Alias (nome diferente na URL)
    # GET /users?order-by=name
    order_by: str = Query(default="id", alias="order-by"),
):
    ...
```

#### Body (Corpo da Requisição)

```python
from fastapi import Body
from pydantic import BaseModel

# ═══════════════════════════════════════════════════════════════════════════
# BODY: Dados enviados no corpo (JSON)
# ═══════════════════════════════════════════════════════════════════════════

# Método 1: Schema Pydantic (RECOMENDADO)
class UserCreate(BaseModel):
    nome: str
    email: str
    idade: int

@router.post("")
def create_user(user: UserCreate):  # FastAPI valida automaticamente
    return {"nome": user.nome}

# Método 2: Body() para campos individuais
@router.post("/config")
def update_config(
    theme: str = Body(...),
    notifications: bool = Body(True)
):
    ...

# Método 3: Dict livre (evitar - sem validação)
@router.post("/raw")
def raw_data(data: dict = Body(...)):
    ...
```

#### Dependency Injection (Depends)

**Depends** é o mecanismo de injeção de dependências do FastAPI. Permite reutilizar código e gerenciar recursos.

```python
from fastapi import Depends
from sqlalchemy.orm import Session

# ═══════════════════════════════════════════════════════════════════════════
# DEPENDS: Injeção de dependências
# ═══════════════════════════════════════════════════════════════════════════

# Função geradora de dependência
def get_db():
    """Cria session do banco e fecha após uso."""
    db = SessionLocal()
    try:
        yield db  # yield = retorna e continua após o endpoint
    finally:
        db.close()

# Uso no endpoint
@router.get("")
def list_users(db: Session = Depends(get_db)):
    # db já é uma session aberta
    return db.query(User).all()
    # Após retornar, o finally do get_db() é executado

# ═══════════════════════════════════════════════════════════════════════════
# DEPENDÊNCIAS ENCADEADAS
# ═══════════════════════════════════════════════════════════════════════════

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Valida token e retorna usuário."""
    user = validate_token_and_get_user(token, db)
    if not user:
        raise HTTPException(401, "Token inválido")
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verifica se usuário está ativo."""
    if not current_user.is_active:
        raise HTTPException(400, "Usuário inativo")
    return current_user

# Uso: FastAPI resolve toda a cadeia automaticamente
@router.get("/me")
def get_me(user: User = Depends(get_current_active_user)):
    return user  # Token validado + usuário ativo
```

#### HTTPException (Tratamento de Erros)

```python
from fastapi import HTTPException, status

# ═══════════════════════════════════════════════════════════════════════════
# HTTPException: Erros HTTP com mensagem
# ═══════════════════════════════════════════════════════════════════════════

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    if user.deleted_at:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Usuário foi removido"
        )

    return user

# ═══════════════════════════════════════════════════════════════════════════
# CÓDIGOS HTTP COMUNS
# ═══════════════════════════════════════════════════════════════════════════

# 2xx Sucesso
status.HTTP_200_OK              # GET, PUT, PATCH com retorno
status.HTTP_201_CREATED         # POST criou recurso
status.HTTP_204_NO_CONTENT      # DELETE sem retorno

# 4xx Erro do Cliente
status.HTTP_400_BAD_REQUEST     # Requisição inválida
status.HTTP_401_UNAUTHORIZED    # Não autenticado
status.HTTP_403_FORBIDDEN       # Não autorizado (autenticado, mas sem permissão)
status.HTTP_404_NOT_FOUND       # Recurso não existe
status.HTTP_409_CONFLICT        # Conflito (ex: email já existe)
status.HTTP_422_UNPROCESSABLE_ENTITY  # Validação falhou

# 5xx Erro do Servidor
status.HTTP_500_INTERNAL_SERVER_ERROR  # Erro genérico
status.HTTP_503_SERVICE_UNAVAILABLE    # Serviço indisponível
```

#### Response Model (Controle de Resposta)

```python
from pydantic import BaseModel

# ═══════════════════════════════════════════════════════════════════════════
# RESPONSE MODEL: Controla o que é retornado
# ═══════════════════════════════════════════════════════════════════════════

class UserResponse(BaseModel):
    id: int
    nome: str
    email: str
    # NOTA: password_hash NÃO está aqui - não vai para a resposta!

    model_config = {"from_attributes": True}

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    # user tem password_hash, mas FastAPI filtra usando o response_model
    return user  # Resposta só tem id, nome, email

# Opções do response_model
@router.get(
    "",
    response_model=list[UserResponse],      # Lista de schemas
    response_model_exclude_none=True,       # Remove campos None
    response_model_exclude_unset=True,      # Remove campos não setados
    response_model_exclude={"email"},       # Exclui campos específicos
    response_model_include={"id", "nome"}   # Inclui apenas estes
)
def list_users():
    ...
```

### Arquitetura Completa

```python
# api/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Literal

from infra.configs.connection import get_db
from services.user_service import UserService
from schemas.user_schemas import (
    UserList,
    UserDetail,
    UserWithTeam,
    UserCreate,
    UserUpdate
)

router = APIRouter(prefix="/users", tags=["users"])


# ═══════════════════════════════════════════
# GET /users - Listar usuários
# ═══════════════════════════════════════════

@router.get("", response_model=list[UserList])
def list_users(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Lista usuários ativos"""
    service = UserService(db)
    users = service.repo.list_active(limit=limit, offset=offset)
    return users


# ═══════════════════════════════════════════
# GET /users/{user_id} - Detalhe do usuário
# ═══════════════════════════════════════════

@router.get("/{user_id}", response_model=UserWithTeam)
def get_user(
    user_id: int,
    include: list[str] = Query(None, description="Relationships: team, tickets"),
    db: Session = Depends(get_db)
):
    """
    Retorna detalhes do usuário.

    **Query params**:
    - `include`: Lista de relationships para incluir (ex: `?include=team&include=tickets`)
    """
    service = UserService(db)

    # include=team → carregar team
    if include and "team" in include:
        user = service.get_user_with_team(user_id)
    else:
        user = service.repo.get_by_id(user_id)

    if not user or user.deleted_at:
        raise HTTPException(status_code=404, detail="User não encontrado")

    return user


# ═══════════════════════════════════════════
# POST /users - Criar usuário
# ═══════════════════════════════════════════

@router.post("", response_model=UserDetail, status_code=201)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Cria novo usuário"""
    service = UserService(db)

    try:
        user = service.create_user(
            full_name=user_data.user_full_name,
            email=user_data.user_email,
            password=user_data.user_password,
            team_id=user_data.user_team_id,
            role=user_data.user_role,
            tipo=user_data.user_tipo
        )
        return user

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ═══════════════════════════════════════════
# PATCH /users/{user_id} - Atualizar usuário
# ═══════════════════════════════════════════

@router.patch("/{user_id}", response_model=UserDetail)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza usuário (campos opcionais)"""
    service = UserService(db)

    try:
        # Só passa campos não-None
        updates = user_data.model_dump(exclude_unset=True)
        user = service.update_user(user_id, **updates)
        return user

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ═══════════════════════════════════════════
# DELETE /users/{user_id} - Deletar usuário
# ═══════════════════════════════════════════

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    deleted_by: int = Query(..., description="ID do usuário que está deletando"),
    db: Session = Depends(get_db)
):
    """Soft delete de usuário"""
    service = UserService(db)

    try:
        service.soft_delete_user(user_id, deleted_by=deleted_by)
        return None  # 204 No Content

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Query Params Dinâmicos (include)

**Padrão RESTful**: Permitir cliente escolher o que incluir.

```python
@router.get("/{user_id}")
def get_user(
    user_id: int,
    include: list[str] = Query(None),
    db: Session = Depends(get_db)
):
    from sqlalchemy.orm import joinedload, selectinload

    query = db.query(User).filter(User.id == user_id)

    # Eager load dinâmico
    if include:
        if "team" in include:
            query = query.options(joinedload(User.team))

        if "tickets" in include:
            query = query.options(selectinload(User.tickets_att))

    user = query.first()

    if not user:
        raise HTTPException(404, "User não encontrado")

    return user


# Uso:
# GET /users/1                    → Só dados do user
# GET /users/1?include=team       → User + team
# GET /users/1?include=team&include=tickets → User + team + tickets
```

### Schemas de Resposta Dinâmicos

```python
from typing import Union

@router.get("/{user_id}", response_model=Union[UserDetail, UserWithTeam])
def get_user(...):
    # FastAPI escolhe o schema correto automaticamente
    pass
```

---

# MÓDULO 4: ANALYTICS E PERFORMANCE

## Introdução: Analytics Como Diferencial Competitivo

Analytics não é apenas "relatórios bonitos". É a capacidade de transformar dados brutos em **insights acionáveis** que direcionam decisões de negócio.

### Por Que Analytics É Crítico?

No seu contexto de gerenciamento de tickets/projetos/relatórios, analytics responde perguntas como:

```
Operacionais:
- Quais times estão sobrecarregados?
- Quais tickets estão demorando demais?
- Onde estão os gargalos?

Estratégicas:
- Como está a qualidade do atendimento?
- Quais áreas precisam de mais recursos?
- Qual o ROI de cada time/projeto?

Preditivas:
- Quantos tickets teremos no próximo mês?
- Quais projetos têm risco de atraso?
- Onde investir para maior impacto?
```

**Analytics mal feito = decisões ruins = prejuízo**
**Analytics bem feito = decisões informadas = vantagem competitiva**

### O Desafio: Performance vs Complexidade

```
┌────────────────────────────────────────┐
│ Queries Simples (rápidas, pouco úteis)│
│ SELECT COUNT(*) FROM tickets          │
│                                        │
│ ⬇️  Adiciona complexidade              │
│                                        │
│ Queries Complexas (úteis, podem ser   │
│ lentas se mal otimizadas)             │
│ SELECT                                 │
│   team,                                │
│   COUNT(*) as total,                   │
│   AVG(resolution_time) as avg,         │
│   percentile(resolution_time, 0.95)    │
│ FROM tickets                           │
│ JOIN users JOIN teams                  │
│ WHERE ... GROUP BY ... HAVING ...      │
└────────────────────────────────────────┘
```

Este módulo ensina como fazer queries complexas **mantendo performance**.

---

## 4.1 Queries de Agregação

### Entendendo Agregações

**Agregação** é quando você **resume múltiplos registros em um único valor**.

**Analogia**: Imagine uma pilha de 1000 notas fiscais. Agregação é quando você:
- **Soma** todas para saber o total gasto (SUM)
- **Conta** quantas notas tem (COUNT)
- **Calcula média** de valor por nota (AVG)
- **Pega** o maior valor (MAX)
- **Pega** o menor valor (MIN)

Sem agregação: 1000 registros
Com agregação: 1 número que resume tudo

### As 5 Funções de Agregação Básicas

#### 1. COUNT - Contar Registros

**O que faz**: Conta quantos registros existem.

```python
# Quantos tickets existem?
total = db.query(func.count(Ticket.id)).scalar()
# Retorna: 1523 (um número)
```

**SQL Equivalente**:
```sql
SELECT COUNT(tickets.id) AS count_1 FROM tickets;
-- Resultado: 1523
```

**Quando usar**:
- Total de registros
- Quantos tickets por status
- Quantos usuários ativos

**Variações**:
```python
# COUNT(*) - conta todas as linhas
db.query(func.count()).select_from(Ticket).scalar()

# COUNT(coluna) - conta apenas não-NULL
db.query(func.count(Ticket.closed_at)).scalar()  # Só tickets fechados

# COUNT(DISTINCT coluna) - conta valores únicos
db.query(func.count(Ticket.ticket_client_id.distinct())).scalar()  # Quantos clientes diferentes
```

**SQLs Equivalentes**:
```sql
-- COUNT(*)
SELECT COUNT(*) AS count_1 FROM tickets;

-- COUNT(coluna) - apenas não-NULL
SELECT COUNT(tickets.closed_at) AS count_1 FROM tickets;

-- COUNT(DISTINCT)
SELECT COUNT(DISTINCT tickets.ticket_client_id) AS count_1 FROM tickets;
```

#### 2. SUM - Somar Valores

**O que faz**: Soma valores numéricos.

```python
# Soma de horas trabalhadas
total_hours = db.query(func.sum(Ticket.hours_worked)).scalar()
# Retorna: 45234.5 (soma de todas as horas)
```

**SQL Equivalente**:
```sql
SELECT SUM(tickets.hours_worked) AS sum_1 FROM tickets;
-- Resultado: 45234.5
```

**Quando usar**:
- Total de valores financeiros
- Soma de horas/duração
- Total de itens

**⚠️ Cuidado**: SUM retorna None se não houver registros!
```python
# ✅ Seguro:
total = db.query(func.coalesce(func.sum(Ticket.hours_worked), 0)).scalar()
```

**SQL com COALESCE**:
```sql
SELECT COALESCE(SUM(tickets.hours_worked), 0) AS coalesce_1 FROM tickets;
-- Retorna 0 se não houver registros (ao invés de NULL)
```

#### 3. AVG - Calcular Média

**O que faz**: Calcula média aritmética.

```python
# Tempo médio de resolução (em horas)
avg_time = db.query(
    func.avg(
        extract('epoch', Ticket.closed_at - Ticket.created_at) / 3600
    )
).scalar()
# Retorna: 48.3 (horas)
```

**SQL Equivalente**:
```sql
SELECT AVG(
    EXTRACT(epoch FROM tickets.closed_at - tickets.created_at) / 3600
) AS avg_1
FROM tickets;
-- Resultado: 48.3 (média de horas para resolver tickets)
```

**Quando usar**:
- Tempo médio de atendimento
- Nota média de satisfação
- Valor médio por transação

**⚠️ Importante**: AVG ignora valores NULL automaticamente.

#### 4. MAX - Valor Máximo

**O que faz**: Retorna o maior valor.

```python
# Ticket mais antigo ainda aberto
oldest_open = db.query(func.min(Ticket.created_at)).filter(
    Ticket.ticket_status == TicketStatus.ABERTO
).scalar()
```

**SQL Equivalente**:
```sql
SELECT MIN(tickets.created_at) AS min_1
FROM tickets
WHERE tickets.ticket_status = 'aberto';
-- Resultado: '2024-01-15 09:30:00' (data do ticket aberto mais antigo)
```

**Quando usar**:
- Data mais recente/antiga
- Maior valor
- Pior performance

#### 5. MIN - Valor Mínimo

**O que faz**: Retorna o menor valor.

```python
# Ticket resolvido mais rápido
fastest = db.query(
    func.min(Ticket.closed_at - Ticket.created_at)
).scalar()
```

**SQL Equivalente**:
```sql
SELECT MIN(tickets.closed_at - tickets.created_at) AS min_1
FROM tickets;
-- Resultado: '00:15:00' (15 minutos - ticket mais rápido)
```

### Agregação com GROUP BY

**GROUP BY** divide registros em grupos e aplica agregação em cada grupo.

**Analogia**: Imagine gavetas organizadas por cor. GROUP BY separa em gavetas, agregação conta/soma dentro de cada gaveta.

```python
# Tickets POR STATUS (grupos)
status_counts = (
    db.query(
        Ticket.ticket_status,              # ← Coluna de agrupamento
        func.count(Ticket.id).label("count")  # ← Agregação
    )
    .group_by(Ticket.ticket_status)        # ← Divide em grupos
    .all()
)

# Resultado:
# [(TicketStatus.ABERTO, 45),
#  (TicketStatus.ATIVO, 123),
#  (TicketStatus.CONCLUIDO, 890)]
```

**SQL Equivalente**:
```sql
SELECT
    tickets.ticket_status,
    COUNT(tickets.id) AS count
FROM tickets
GROUP BY tickets.ticket_status;

-- Resultado:
-- ticket_status | count
-- --------------+-------
-- aberto        | 45
-- ativo         | 123
-- concluido     | 890
```

**Regra de Ouro do GROUP BY**:

```
Se você usa GROUP BY, só pode SELECT:
1. Colunas do GROUP BY
2. Funções de agregação (COUNT, SUM, etc.)

❌ ERRADO:
SELECT ticket_title, COUNT(*)  ← ticket_title não está no GROUP BY!
FROM tickets
GROUP BY ticket_status

✅ CORRETO:
SELECT ticket_status, COUNT(*)
FROM tickets
GROUP BY ticket_status
```

### COUNT, SUM, AVG, MIN, MAX - Exemplos Práticos

```python
from sqlalchemy import func

# Total de tickets
total_tickets = db.query(func.count(Ticket.id)).scalar()

# Tickets por status
status_counts = (
    db.query(
        Ticket.ticket_status,
        func.count(Ticket.id).label("count")
    )
    .group_by(Ticket.ticket_status)
    .all()
)

# Resultado: [(TicketStatus.ABERTO, 15), (TicketStatus.ATIVO, 23), ...]

# Tickets por time
team_stats = (
    db.query(
        Team.team_name,
        func.count(Ticket.id).label("total_tickets")
    )
    .join(User, Team.id == User.user_team_id)
    .join(Ticket, User.id == Ticket.ticket_client_id)
    .group_by(Team.team_name)
    .all()
)
```

### Agregações Complexas

```python
from sqlalchemy import case, extract

# Tempo médio de resolução por prioridade
avg_resolution_time = (
    db.query(
        Ticket.ticket_priority,
        func.avg(
            extract('epoch', Ticket.closed_at - Ticket.created_at) / 3600
        ).label("avg_hours")
    )
    .filter(Ticket.closed_at.isnot(None))
    .group_by(Ticket.ticket_priority)
    .all()
)

# Taxa de resolução por time
resolution_rate = (
    db.query(
        Team.team_name,
        func.count(Ticket.id).label("total"),
        func.sum(
            case((Ticket.ticket_status == TicketStatus.CONCLUIDO, 1), else_=0)
        ).label("resolved"),
        (
            func.sum(case((Ticket.ticket_status == TicketStatus.CONCLUIDO, 1), else_=0))
            * 100.0
            / func.count(Ticket.id)
        ).label("resolution_rate")
    )
    .join(User, Team.id == User.user_team_id)
    .join(Ticket, User.id == Ticket.ticket_attendant_id)
    .group_by(Team.team_name)
    .all()
)
```

---

## 4.2 Analytics Service

### Estrutura

```python
# services/analytics_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, case, extract
from datetime import datetime, timedelta

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_ticket_stats(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        team_id: int | None = None
    ) -> dict:
        """
        Estatísticas de tickets com filtros opcionais
        """
        query = self.db.query(Ticket)

        # Aplicar filtros
        if start_date:
            query = query.filter(Ticket.created_at >= start_date)
        if end_date:
            query = query.filter(Ticket.created_at <= end_date)
        if team_id:
            query = (
                query
                .join(User, Ticket.ticket_client_id == User.id)
                .filter(User.user_team_id == team_id)
            )

        # Agregações
        total = query.count()

        by_status = (
            query
            .with_entities(
                Ticket.ticket_status,
                func.count(Ticket.id).label("count")
            )
            .group_by(Ticket.ticket_status)
            .all()
        )

        avg_resolution = (
            query
            .filter(Ticket.closed_at.isnot(None))
            .with_entities(
                func.avg(
                    extract('epoch', Ticket.closed_at - Ticket.created_at) / 3600
                )
            )
            .scalar()
        )

        return {
            "total": total,
            "by_status": {status.value: count for status, count in by_status},
            "avg_resolution_hours": float(avg_resolution) if avg_resolution else None
        }

    def get_team_performance(self) -> list[dict]:
        """Performance de cada time"""
        results = (
            self.db.query(
                Team.id,
                Team.team_name,
                func.count(Ticket.id).label("total_tickets"),
                func.sum(
                    case((Ticket.ticket_status == TicketStatus.CONCLUIDO, 1), else_=0)
                ).label("resolved_tickets"),
                func.avg(
                    case(
                        (
                            Ticket.closed_at.isnot(None),
                            extract('epoch', Ticket.closed_at - Ticket.created_at) / 3600
                        )
                    )
                ).label("avg_resolution_hours")
            )
            .join(User, Team.id == User.user_team_id)
            .join(Ticket, User.id == Ticket.ticket_attendant_id)
            .group_by(Team.id, Team.team_name)
            .all()
        )

        return [
            {
                "team_id": r.id,
                "team_name": r.team_name,
                "total_tickets": r.total_tickets,
                "resolved_tickets": r.resolved_tickets,
                "resolution_rate": (r.resolved_tickets / r.total_tickets * 100) if r.total_tickets > 0 else 0,
                "avg_resolution_hours": float(r.avg_resolution_hours) if r.avg_resolution_hours else None
            }
            for r in results
        ]
```

### Endpoint de Analytics

```python
@router.get("/analytics/tickets")
def ticket_analytics(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    team_id: int | None = None,
    db: Session = Depends(get_db)
):
    """Estatísticas de tickets"""
    service = AnalyticsService(db)
    return service.get_ticket_stats(start_date, end_date, team_id)


@router.get("/analytics/teams")
def team_analytics(db: Session = Depends(get_db)):
    """Performance dos times"""
    service = AnalyticsService(db)
    return service.get_team_performance()
```

---

## 4.3 Otimizações Avançadas

### 1. Subqueries

```python
from sqlalchemy import select

# Subquery: total de tickets por usuário
tickets_count = (
    select(
        Ticket.ticket_client_id,
        func.count(Ticket.id).label("ticket_count")
    )
    .group_by(Ticket.ticket_client_id)
    .subquery()
)

# Query principal: usuários com contagem
users_with_count = (
    db.query(
        User.id,
        User.user_full_name,
        func.coalesce(tickets_count.c.ticket_count, 0).label("tickets")
    )
    .outerjoin(tickets_count, User.id == tickets_count.c.ticket_client_id)
    .all()
)
```

### 2. Window Functions

```python
from sqlalchemy import over

# Ranking de atendentes por número de tickets resolvidos
ranking = (
    db.query(
        User.user_full_name,
        func.count(Ticket.id).label("resolved"),
        func.rank().over(
            order_by=func.count(Ticket.id).desc()
        ).label("rank")
    )
    .join(Ticket, User.id == Ticket.ticket_attendant_id)
    .filter(Ticket.ticket_status == TicketStatus.CONCLUIDO)
    .group_by(User.user_full_name)
    .all()
)
```

### 3. Batch Loading

```python
# ❌ N+1 Problem
users = db.query(User).all()
for user in users:
    print(user.team.team_name)  # 1 query por user!

# ✅ Solução: selectinload
from sqlalchemy.orm import selectinload

users = db.query(User).options(selectinload(User.team)).all()
for user in users:
    print(user.team.team_name)  # Total: 2 queries!
```

---

## 4.4 Índices e Performance

### Entendendo Índices: A Analogia do Livro

**Problema**: Imagine que você precisa encontrar todas as páginas onde aparece a palavra "SQLAlchemy" em um livro de 1000 páginas.

**Sem índice**: Você lê TODAS as 1000 páginas, uma por uma. Demora horas.

**Com índice**: Você vai direto ao índice remissivo no final do livro, vê "SQLAlchemy: páginas 45, 123, 567" e vai direto lá. Demora segundos.

**Índices de banco de dados funcionam exatamente assim.**

### O Que É um Índice?

**Índice** é uma estrutura de dados auxiliar que permite ao banco encontrar registros rapidamente sem fazer um **table scan** (ler toda a tabela).

```
Sem Índice (Table Scan):
┌────────────────────────────────────────┐
│ users table (1 milhão de registros)   │
├────────────────────────────────────────┤
│ id=1  name=Ana    email=ana@...       │ ← Lê linha 1
│ id=2  name=Bruno  email=bruno@...     │ ← Lê linha 2
│ id=3  name=Carlos email=carlos@...    │ ← Lê linha 3
│ ...                                    │ ← Lê TUDO
│ id=999999 name=Zoe email=zoe@...      │ ← Lê linha 999999
│ id=1000000 name=Matheus email=...     │ ← ACHOU! (depois de ler tudo)
└────────────────────────────────────────┘
Tempo: ~5 segundos (lento!)

Com Índice em email:
┌────────────────────────────────────────┐
│ Índice (estrutura B-Tree ordenada)    │
├────────────────────────────────────────┤
│ ana@... → linha 1                      │
│ bruno@... → linha 2                    │
│ ...                                    │
│ matheus@... → linha 1000000            │ ← Busca binária
└────────────────────────────────────────┘
         ↓ (vai direto à linha)
┌────────────────────────────────────────┐
│ id=1000000 name=Matheus email=...     │ ← ACHOU! (direto)
└────────────────────────────────────────┘
Tempo: ~5 milissegundos (1000x mais rápido!)
```

### Tipos de Índices

#### 1. Primary Key (índice automático)

```python
class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    # ↑ Automaticamente cria índice único em id
```

**Características**:
- ✅ Sempre único
- ✅ Sempre indexado
- ✅ Busca por ID é O(log n) - muito rápida

#### 2. Índice Simples

```python
class Ticket(Base):
    ticket_title: Mapped[str] = mapped_column(String(200), index=True)
    #                                                        ↑
    #                                               Cria índice
```

**SQL Gerado**:
```sql
CREATE INDEX ix_tickets_ticket_title ON tickets(ticket_title);
```

**Quando usar**:
- Colunas usadas em WHERE frequentemente
- Colunas usadas em ORDER BY
- Colunas de relacionamento (foreign keys)

#### 3. Índice Único (UNIQUE)

```python
class User(Base):
    user_email: Mapped[str] = mapped_column(String(100), unique=True)
    #                                                      ↑
    #                                         Índice único + constraint
```

**SQL Gerado**:
```sql
CREATE UNIQUE INDEX ix_users_user_email ON users(user_email);
```

**Características**:
- ✅ Garante valores únicos
- ✅ Busca rápida
- ✅ Previne duplicatas

#### 4. Índice Composto (Múltiplas Colunas)

```python
class Ticket(Base):
    __tablename__ = "tickets"

    ticket_status: Mapped[TicketStatus] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()

    # Índice composto (status + data)
    __table_args__ = (
        Index("ix_ticket_status_created", "ticket_status", "created_at"),
    )
```

**SQL Gerado**:
```sql
CREATE INDEX ix_ticket_status_created ON tickets(ticket_status, created_at);
```

**Quando usar**:
- Queries que filtram por múltiplas colunas juntas
- A ordem das colunas IMPORTA!

**Ordem das Colunas**:

```python
# Índice: (status, created_at)

# ✅ USA o índice:
WHERE status = 'ABERTO'
WHERE status = 'ABERTO' AND created_at > '2024-01-01'

# ❌ NÃO USA o índice completo:
WHERE created_at > '2024-01-01'  # Só usa se status também estiver

# Regra: Índice (A, B, C) funciona para:
# - A
# - A, B
# - A, B, C
# MAS NÃO para: B, C ou apenas C
```

### Trade-offs de Índices

#### Vantagens

✅ **Busca extremamente rápida**
- Table scan: O(n) - lê tudo
- Índice: O(log n) - busca binária

✅ **ORDER BY mais rápido**
- Sem índice: precisa ordenar em memória
- Com índice: já está ordenado

✅ **JOIN mais eficiente**
- Foreign keys devem SEMPRE ter índice

#### Desvantagens

❌ **Ocupa espaço em disco**
- Cada índice duplica parte dos dados
- Índice pode ser maior que a própria tabela

❌ **INSERT/UPDATE/DELETE mais lentos**
- Precisa atualizar o índice também
- Mais índices = mais trabalho

❌ **Manutenção**
- Índices podem fragmentar
- Precisam de VACUUM/REINDEX periódico

### Quando Criar Índices

✅ **CRIE índices** quando:

1. **Coluna em WHERE frequente**
   ```python
   # Se você faz muito:
   WHERE user_email = '...'
   # Crie índice em user_email
   ```

2. **Coluna em JOIN**
   ```python
   # Foreign keys sempre devem ter índice
   user_team_id: Mapped[int] = mapped_column(
       ForeignKey("teams.id"),
       index=True  # ✅
   )
   ```

3. **Coluna em ORDER BY**
   ```python
   # Se você faz muito:
   ORDER BY created_at DESC
   # Crie índice em created_at
   ```

4. **Alta cardinalidade** (muitos valores únicos)
   ```python
   # ✅ Bom para índice:
   user_email: milhões de valores únicos
   user_cpf: milhões de valores únicos

   # ❌ Ruim para índice:
   is_active: apenas 2 valores (True/False)
   gender: apenas 3-4 valores
   ```

❌ **NÃO CRIE índices** quando:

1. **Tabela pequena** (< 1000 registros)
   - Table scan é rápido o suficiente
   - Overhead do índice não compensa

2. **Colunas atualizadas frequentemente**
   - Cada UPDATE precisa atualizar o índice
   - Pode ficar mais lento que o ganho

3. **Baixa cardinalidade** (poucos valores únicos)
   ```python
   # ❌ NÃO indexe:
   is_deleted: Mapped[bool]  # Apenas True/False
   ticket_priority: Mapped[Priority]  # Apenas 4 valores
   ```

4. **Colunas raramente usadas**
   - Se nunca filtra por essa coluna, não precisa

### Como Decidir: A Matriz de Decisão

```
                    Alta Cardinalidade    Baixa Cardinalidade
                    (muitos valores)      (poucos valores)

Filtrado            ✅ CRIE ÍNDICE        🤔 Depende
Frequentemente      Exemplo: email        Se > 10% dos dados
                                         não vale a pena

Filtrado            🤔 Considere          ❌ NÃO CRIE
Raramente           Se query é crítica    Overhead não
                                         compensa

Nunca               ❌ NÃO CRIE          ❌ NÃO CRIE
Filtrado            Desperdício          Desperdício
```

### Criando Índices

```python
from sqlalchemy import Index

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_title: Mapped[str] = mapped_column(String(200), index=True)  # Índice simples
    ticket_status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Índice composto
    __table_args__ = (
        Index("ix_ticket_status_created", "ticket_status", "created_at"),
    )
```

### Quando Criar Índices

✅ **Crie índices** em colunas que:
- São usadas em `WHERE` frequentemente
- São usadas em `JOIN` (FKs geralmente já têm)
- São usadas em `ORDER BY`
- Têm alta cardinalidade (muitos valores únicos)

❌ **Não crie índices** em colunas que:
- São atualizadas muito frequentemente
- Têm baixa cardinalidade (ex: boolean)
- Raramente são filtradas

### Analyze Query Performance

```python
from sqlalchemy import text

# Ver plano de execução (PostgreSQL)
query = db.query(Ticket).filter(Ticket.ticket_status == TicketStatus.ABERTO)
explain = db.execute(text(f"EXPLAIN ANALYZE {str(query.statement)}"))
print(explain.fetchall())
```

---

# MÓDULO 5: BOAS PRÁTICAS

## Introdução: Da Teoria à Prática

Você aprendeu os conceitos (Módulo 1-2), arquitetura (Módulo 3), e performance (Módulo 4). Agora é hora de **consolidar tudo** em padrões práticos e reutilizáveis.

### Por Que Boas Práticas Importam?

```
Código Sem Padrões:
┌─────────────────────────────────────┐
│ • Cada desenvolvedor faz diferente  │
│ • Difícil entender código alheio    │
│ • Bugs sutis e inconsistências      │
│ • Refatoração é arriscada           │
│ • Onboarding demora meses           │
└─────────────────────────────────────┘

Código Com Padrões:
┌─────────────────────────────────────┐
│ • Todos seguem mesma estrutura      │
│ • Código previsível e legível       │
│ • Bugs fáceis de encontrar          │
│ • Refatoração segura                │
│ • Onboarding em dias                │
└─────────────────────────────────────┘
```

**Boas práticas transformam conhecimento individual em conhecimento organizacional.**

### Os 3 Pilares de Código Sustentável

1. **Consistência**: Fazer sempre do mesmo jeito (convenções)
2. **Clareza**: Código que se explica (nomes, estrutura)
3. **Confiabilidade**: Funciona e continua funcionando (testes)

Este módulo fornece checklists, convenções e padrões para garantir os 3 pilares.

---

## 5.1 Checklist de Implementação

### O Que É Este Checklist?

Um **checklist** é uma lista de verificação que garante que você não esqueceu nada importante. Pilotos de avião usam checklists antes de cada voo - mesmo com décadas de experiência.

**Você também deveria.**

### Como Usar Este Checklist

```
ANTES de fazer commit:
1. Abra este checklist
2. Marque cada item que seu código cumpre
3. Se algum item não está marcado, corrija
4. Só faça commit quando 100% estiver marcado

DURANTE code review:
1. Revisor usa o checklist
2. Aponta itens não cumpridos
3. Desenvolvedor corrige

PERIODICAMENTE:
1. Audite código existente
2. Identifique padrões a melhorar
3. Refatore gradualmente
```

### Models

- [ ] Todos os models herdam de `Base`
- [ ] `__tablename__` definido
- [ ] Chave primária `id` presente
- [ ] Colunas obrigatórias têm `nullable=False`
- [ ] Colunas opcionais têm `nullable=True` e tipo `| None`
- [ ] FKs usam `ForeignKey("tabela.id")`
- [ ] FKs têm tipo `Mapped[int]`, não `Mapped[Model]`
- [ ] Relationships usam `lazy="raise"` (APIs)
- [ ] `back_populates` está correto em ambos os lados
- [ ] Sem imports circulares (use strings: `"User"`)
- [ ] Soft delete implementado (`deleted_at`, `deleted_by`)
- [ ] Timestamps (`created_at`, `updated_at`)
- [ ] Audit trail (`created_by`, `updated_by`)
- [ ] `__repr__()` implementado (debug)

### MappedAsDataclass (Se Usado) ⚠️

- [ ] Na classe `Base`: `id` tem `init=False`
- [ ] Na classe `Base`: Todos os campos com `default` têm `init=False`
- [ ] Na classe `Base`: `created_at`, `updated_at` têm `server_default` e `init=False`
- [ ] FKs opcionais têm `init=False`
- [ ] **Relationships**: TODOS têm `init=False`
- [ ] **Relationships**: NENHUM tem `default=None` (causa bug de FK NULL!)
- [ ] **Relationships** (lista): Usam `default_factory=list`
- [ ] **Repositories**: `insert()` usa `db.session.refresh(data)` antes de retornar ID

### Schemas

- [ ] Múltiplos schemas por entidade (List, Detail, WithRelations, Create, Update)
- [ ] `model_config = ConfigDict(from_attributes=True)`
- [ ] Campos opcionais em Update schemas
- [ ] Evitar recursão (schemas simplificados para relationships)
- [ ] Validações customizadas quando necessário

### Services

- [ ] Lógica de negócio no service (não no endpoint)
- [ ] Eager loading explícito
- [ ] Validações de negócio
- [ ] Tratamento de erros com exceções claras
- [ ] Transações (commit) no service
- [ ] Reutilização de repositories

### APIs

- [ ] Response models definidos
- [ ] HTTP status codes corretos (200, 201, 204, 400, 404, 500)
- [ ] Query params documentados
- [ ] Filtros opcionais (limit, offset, include)
- [ ] Tratamento de exceções com HTTPException
- [ ] Documentação (docstrings)

### Performance

- [ ] `lazy="raise"` forçando eager loading
- [ ] Queries otimizadas (sem N+1)
- [ ] Índices em colunas filtradas frequentemente
- [ ] Paginação em listagens
- [ ] Limites em queries (`.limit()`)

---

## 5.2 Padrões de Nomenclatura

### Por Que Nomenclatura Importa?

**Código é lido 10x mais vezes do que é escrito.** Nomes ruins tornam o código impossível de entender e manter.

```python
# ❌ Nomes ruins:
class U(Base):
    __tablename__ = "u"
    i: Mapped[int] = mapped_column(primary_key=True)
    n: Mapped[str] = mapped_column()
    tid: Mapped[int] = mapped_column(ForeignKey("t.id"))

# ✅ Nomes bons:
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_full_name: Mapped[str] = mapped_column()
    user_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
```

**Qual você prefere ler/manter?**

### Princípios de Nomenclatura

1. **Clareza sobre Brevidade**
   - `user_full_name` > `name` > `n`
   - `ticket_created_at` > `created` > `ts`

2. **Consistência Absoluta**
   - Se usa `user_team_id`, use `ticket_client_id` (não `ticket_clientId`)
   - Se usa `created_at`, use `updated_at` (não `update_time`)

3. **Evite Abreviações**
   - `description` > `desc` (desc = descending?)
   - `quantity` > `qty`
   - `password` > `pwd`
   - **Exceção**: Abreviações universais (id, url, api)

4. **Contexto no Nome**
   - Em `users` table: `user_email` (não apenas `email`)
   - Em `tickets` table: `ticket_title` (não apenas `title`)
   - **Por quê?**: Quando faz JOIN, fica claro de onde vem

### Convenções por Tipo

### Tabelas e Colunas

```python
# Tabelas: plural, snake_case
__tablename__ = "users"
__tablename__ = "tickets"
__tablename__ = "user_tickets_association"

# Colunas: prefixo da tabela + nome, snake_case
user_full_name       # users.user_full_name
user_email           # users.user_email
ticket_title         # tickets.ticket_title
ticket_description   # tickets.ticket_description

# FKs: singular + _id
user_team_id         # FK para teams.id
ticket_client_id     # FK para users.id
```

### Models e Relationships

```python
# Models: singular, PascalCase
class User(Base): ...
class Team(Base): ...
class Ticket(Base): ...

# Relationships N-1: singular (retorna 1 objeto)
team: Mapped["Team"] = relationship(...)

# Relationships 1-N: plural (retorna lista)
team_members: Mapped[list["User"]] = relationship(...)
tickets: Mapped[list["Ticket"]] = relationship(...)

# Relationships N-N: plural com contexto
tickets_att: Mapped[list["Ticket"]] = relationship(...)  # Tickets atendidos
tickets_follow: Mapped[list["Ticket"]] = relationship(...)  # Tickets seguidos
```

### Schemas

```python
# Schemas: Model + Propósito, PascalCase
UserList          # Listagem
UserDetail        # Detalhes
UserWithTeam      # Com relacionamento
UserCreate        # Criação
UserUpdate        # Atualização
TeamSimple        # Simplificado (evitar recursão)
```

### Services e Repositories

```python
# Repositories: Model + Repository
UserRepository
TeamRepository
TicketRepository

# Services: Model + Service
UserService
TeamService
AnalyticsService
```

---

## 5.3 Segurança e Validação

### Por Que Segurança É Crítica?

**Uma falha de segurança pode**:
- ❌ Expor dados sensíveis de clientes
- ❌ Resultar em multas de LGPD/GDPR
- ❌ Destruir reputação da empresa
- ❌ Causar prejuízos financeiros
- ❌ Levar a processos judiciais

**Segurança não é opcional. É obrigatória.**

### As 3 Camadas de Segurança

```
┌─────────────────────────────────────┐
│ Camada 1: Validação de Entrada     │  ← Pydantic
│ (Garante que dados são válidos)    │
├─────────────────────────────────────┤
│ Camada 2: Sanitização              │  ← SQLAlchemy
│ (Previne SQL Injection)            │
├─────────────────────────────────────┤
│ Camada 3: Autenticação/Autorização │  ← Hash, JWT
│ (Garante que usuário pode acessar) │
└─────────────────────────────────────┘
```

Todas as 3 camadas são necessárias.

### Top 5 Vulnerabilidades em APIs

```
1. SQL Injection          ← Atacante executa SQL malicioso
2. Broken Authentication  ← Senhas fracas, sem hash
3. Sensitive Data Exposure← Retornar senha/token na API
4. Mass Assignment        ← Cliente muda campos protegidos
5. Lack of Rate Limiting  ← DoS via requisições infinitas
```

Este tutorial foca nas 3 primeiras (escopo do ORM).

### Validação de Entrada: A Primeira Linha de Defesa

**Princípio**: NUNCA confie em dados vindos do cliente.

```python
# ❌ VULNERÁVEL:
@app.post("/users")
def create_user(data: dict):  # Aceita qualquer coisa!
    user = User(**data)  # Perigoso!
    db.add(user)
    db.commit()

# ✅ SEGURO:
@app.post("/users")
def create_user(data: UserCreate):  # Pydantic valida!
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
```

### Validação de Entrada com Pydantic

```python
from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
    user_full_name: str = Field(..., min_length=3, max_length=200)
    user_email: EmailStr  # Valida formato de email
    user_password: str = Field(..., min_length=8)
    user_team_id: int = Field(..., gt=0)

    @validator("user_password")
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Senha deve ter ao menos 1 letra maiúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("Senha deve ter ao menos 1 número")
        return v
```

### Hash de Senhas

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### SQL Injection (Prevenção)

```python
# ✅ SQLAlchemy previne automaticamente
user = db.query(User).filter(User.user_email == email).first()

# ❌ NUNCA faça:
db.execute(f"SELECT * FROM users WHERE email = '{email}'")  # VULNERÁVEL!

# ✅ Se precisar de SQL puro, use parâmetros:
from sqlalchemy import text
db.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {"email": email}
)
```

---

## 5.4 Testes

### O Que É pytest?

**pytest** é o framework de testes mais popular do Python. É simples, poderoso e extensível.

```bash
# Instalação
pip install pytest pytest-cov httpx

# pytest: Framework de testes
# pytest-cov: Coverage (cobertura de código)
# httpx: Cliente HTTP para testes de API (usado pelo FastAPI)
```

### Sintaxe Básica do pytest

```python
# tests/test_exemplo.py

# ═══════════════════════════════════════════════════════════════════════════
# REGRA 1: Arquivos devem começar com "test_" ou terminar com "_test.py"
# REGRA 2: Funções devem começar com "test_"
# REGRA 3: Classes devem começar com "Test" (sem __init__)
# ═══════════════════════════════════════════════════════════════════════════

def test_soma():
    """Teste simples - nome começa com test_"""
    resultado = 2 + 2
    assert resultado == 4


def test_divisao():
    """Outro teste simples"""
    assert 10 / 2 == 5


class TestCalculadora:
    """Classe de testes - nome começa com Test"""

    def test_multiplicacao(self):
        assert 3 * 4 == 12

    def test_subtracao(self):
        assert 10 - 3 == 7
```

### Executando Testes

```bash
# ═══════════════════════════════════════════════════════════════════════════
# COMANDOS BÁSICOS
# ═══════════════════════════════════════════════════════════════════════════

# Rodar TODOS os testes
pytest

# Rodar com output verboso
pytest -v

# Rodar arquivo específico
pytest tests/test_users.py

# Rodar teste específico
pytest tests/test_users.py::test_create_user

# Rodar testes que contêm "user" no nome
pytest -k "user"

# Rodar testes que contêm "user" E "create"
pytest -k "user and create"

# Parar no primeiro erro
pytest -x

# Parar após N erros
pytest --maxfail=3

# Mostrar print() e logs
pytest -s

# Rodar em paralelo (precisa: pip install pytest-xdist)
pytest -n auto

# ═══════════════════════════════════════════════════════════════════════════
# COVERAGE (COBERTURA DE CÓDIGO)
# ═══════════════════════════════════════════════════════════════════════════

# Rodar com coverage
pytest --cov=.

# Coverage com report detalhado
pytest --cov=. --cov-report=term-missing

# Gerar HTML do coverage
pytest --cov=. --cov-report=html
# Abre htmlcov/index.html no browser

# Coverage mínimo (falha se < 80%)
pytest --cov=. --cov-fail-under=80
```

### Assertions no pytest

```python
# ═══════════════════════════════════════════════════════════════════════════
# ASSERTIONS BÁSICAS
# ═══════════════════════════════════════════════════════════════════════════

def test_assertions_basicas():
    # Igualdade
    assert 1 + 1 == 2
    assert "hello" == "hello"

    # Desigualdade
    assert 1 != 2

    # Booleano
    assert True
    assert not False

    # None
    assert None is None
    assert "valor" is not None

    # Containment (in)
    assert "a" in "abc"
    assert 1 in [1, 2, 3]
    assert "key" in {"key": "value"}

    # Tipo
    assert isinstance(42, int)
    assert isinstance("hello", str)


def test_assertions_com_mensagem():
    """Mensagem customizada quando falha"""
    valor = 42
    assert valor == 42, f"Esperava 42, mas recebi {valor}"


# ═══════════════════════════════════════════════════════════════════════════
# TESTAR EXCEÇÕES
# ═══════════════════════════════════════════════════════════════════════════

import pytest

def funcao_que_falha():
    raise ValueError("Erro esperado")

def test_excecao():
    """Verifica que exceção é lançada"""
    with pytest.raises(ValueError):
        funcao_que_falha()

def test_excecao_com_mensagem():
    """Verifica exceção E mensagem"""
    with pytest.raises(ValueError, match="Erro esperado"):
        funcao_que_falha()

def test_excecao_capturada():
    """Captura exceção para inspecionar"""
    with pytest.raises(ValueError) as exc_info:
        funcao_que_falha()

    assert str(exc_info.value) == "Erro esperado"
    assert exc_info.type == ValueError


# ═══════════════════════════════════════════════════════════════════════════
# COMPARAÇÕES APROXIMADAS (floats)
# ═══════════════════════════════════════════════════════════════════════════

def test_float_aproximado():
    """Floats podem ter imprecisão"""
    # ❌ PERIGOSO: pode falhar por imprecisão
    # assert 0.1 + 0.2 == 0.3

    # ✅ CORRETO: usa aproximação
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 0.1 + 0.2 == pytest.approx(0.3, rel=1e-9)  # tolerância relativa
```

### Fixtures - Setup e Teardown

**Fixtures** são funções que preparam dados ou recursos para os testes.

```python
# tests/conftest.py
# ═══════════════════════════════════════════════════════════════════════════
# CONFTEST.PY: Fixtures compartilhadas por todos os testes
# ═══════════════════════════════════════════════════════════════════════════

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infra.configs.database import Base

@pytest.fixture
def db_engine():
    """Cria engine in-memory para testes."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(db_engine):
    """Cria session para testes - recebe db_engine como dependência."""
    Session = sessionmaker(bind=db_engine)
    session = Session()

    yield session  # ← O teste usa a session aqui

    session.rollback()  # Desfaz mudanças
    session.close()


@pytest.fixture
def sample_user(db_session):
    """Cria usuário de teste."""
    from infra.entities.user import User

    user = User(
        user_full_name="Test User",
        user_email="test@test.com",
        user_team_id=1
    )
    db_session.add(user)
    db_session.flush()
    db_session.refresh(user)

    return user
```

```python
# tests/test_users.py

def test_get_user(db_session, sample_user):
    """
    Fixtures são injetadas como parâmetros.

    Ordem de execução:
    1. db_engine (fixture)
    2. db_session (fixture, depende de db_engine)
    3. sample_user (fixture, depende de db_session)
    4. Este teste (recebe db_session e sample_user)
    """
    user = db_session.get(User, sample_user.id)
    assert user is not None
    assert user.user_email == "test@test.com"
```

#### Escopos de Fixtures

```python
# ═══════════════════════════════════════════════════════════════════════════
# ESCOPOS: Quando a fixture é criada/destruída
# ═══════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="function")  # DEFAULT
def fixture_por_teste():
    """Criada para CADA teste. Mais isolado, mais lento."""
    return create_resource()


@pytest.fixture(scope="class")
def fixture_por_classe():
    """Criada uma vez por CLASSE de testes."""
    return create_resource()


@pytest.fixture(scope="module")
def fixture_por_modulo():
    """Criada uma vez por ARQUIVO de testes."""
    return create_resource()


@pytest.fixture(scope="session")
def fixture_por_sessao():
    """Criada UMA VEZ para TODA a sessão de testes. Mais rápido."""
    return create_expensive_resource()


# EXEMPLO: Engine compartilhado, session por teste
@pytest.fixture(scope="session")
def db_engine():
    """Engine criado UMA VEZ (rápido)."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Session criada POR TESTE (isolamento)."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
```

### Parametrize - Múltiplos Casos de Teste

```python
import pytest

# ═══════════════════════════════════════════════════════════════════════════
# @pytest.mark.parametrize: Rodar mesmo teste com diferentes dados
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("entrada,esperado", [
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_quadrado(entrada, esperado):
    """Roda 4 vezes, uma para cada par (entrada, esperado)."""
    assert entrada ** 2 == esperado


@pytest.mark.parametrize("email,valido", [
    ("user@example.com", True),
    ("user@example", False),
    ("@example.com", False),
    ("user@", False),
    ("userexample.com", False),
])
def test_validar_email(email, valido):
    """Testa vários formatos de email."""
    resultado = is_valid_email(email)
    assert resultado == valido


# Múltiplos parâmetros combinados
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [3, 4])
def test_soma_combinacoes(a, b):
    """Roda 4 vezes: (1,3), (1,4), (2,3), (2,4)"""
    assert a + b > 0
```

### Marks - Categorizar Testes

```python
import pytest

# ═══════════════════════════════════════════════════════════════════════════
# @pytest.mark: Categorizar e filtrar testes
# ═══════════════════════════════════════════════════════════════════════════

@pytest.mark.slow
def test_operacao_lenta():
    """Marcado como lento."""
    import time
    time.sleep(5)
    assert True


@pytest.mark.integration
def test_integracao_banco():
    """Marcado como integração."""
    pass


@pytest.mark.skip(reason="Funcionalidade não implementada")
def test_funcionalidade_futura():
    """Pula este teste."""
    pass


@pytest.mark.skipif(
    condition=sys.platform == "win32",
    reason="Não funciona no Windows"
)
def test_apenas_linux():
    """Pula no Windows."""
    pass


@pytest.mark.xfail(reason="Bug conhecido #123")
def test_com_bug_conhecido():
    """Esperado falhar - não quebra o build."""
    assert False  # Falha esperada
```

```bash
# Rodar apenas testes marcados como "slow"
pytest -m slow

# Rodar EXCETO testes lentos
pytest -m "not slow"

# Rodar testes de integração OU unitários
pytest -m "integration or unit"
```

### Estrutura de Testes Recomendada

```
projeto/
├── infra/
├── services/
├── api/
└── tests/
    ├── __init__.py
    ├── conftest.py           # Fixtures globais
    ├── unit/                  # Testes unitários
    │   ├── __init__.py
    │   ├── test_validators.py
    │   └── test_utils.py
    ├── integration/           # Testes de integração
    │   ├── __init__.py
    │   ├── conftest.py        # Fixtures de integração (db_session)
    │   ├── test_user_service.py
    │   └── test_ticket_service.py
    └── api/                   # Testes de API
        ├── __init__.py
        ├── conftest.py        # TestClient fixture
        ├── test_users_api.py
        └── test_tickets_api.py
```

### Por Que Testar?

**Código sem testes é código legado desde o dia 1.**

```
Sem Testes:
┌─────────────────────────────────────┐
│ • Medo de refatorar                 │
│ • Bugs descobertos em produção     │
│ • Hotfixes às 3h da manhã          │
│ • "Funciona na minha máquina"      │
│ • Tech debt cresce exponencialmente │
└─────────────────────────────────────┘

Com Testes:
┌─────────────────────────────────────┐
│ • Refatoração com confiança         │
│ • Bugs pegos antes do deploy        │
│ • Deploy tranquilo, sem ansiedade   │
│ • Funciona em qualquer máquina      │
│ • Tech debt controlado              │
└─────────────────────────────────────┘
```

**Testar é investimento, não custo.**

### Tipos de Testes

#### 1. Testes Unitários (Rápidos, Isolados)

```python
# Testa UMA função isoladamente
def test_calculate_resolution_time():
    created = datetime(2024, 1, 1, 10, 0)
    closed = datetime(2024, 1, 1, 12, 0)

    result = calculate_resolution_time(created, closed)

    assert result == 2.0  # 2 horas
```

**Características**:
- ✅ Muito rápidos (< 1ms cada)
- ✅ Não acessam banco de dados
- ✅ Testam lógica pura
- ❌ Não pegam bugs de integração

#### 2. Testes de Integração (Médios, Com Banco)

```python
# Testa Service + Repository + Banco
def test_create_user_service(db_session):
    service = UserService(db_session)

    user = service.create_user(
        name="Test",
        email="test@test.com"
    )

    assert user.id is not None
    assert db_session.get(User, user.id) is not None
```

**Características**:
- ⚠️ Mais lentos (10-100ms cada)
- ✅ Acessam banco (in-memory)
- ✅ Testam integração entre camadas
- ✅ Pegam mais bugs reais

#### 3. Testes de API (Lentos, End-to-End)

```python
# Testa endpoint completo
def test_create_user_endpoint():
    client = TestClient(app)

    response = client.post("/users", json={
        "name": "Test",
        "email": "test@test.com"
    })

    assert response.status_code == 201
    assert response.json()["email"] == "test@test.com"
```

**Características**:
- ❌ Mais lentos (50-500ms cada)
- ✅ Testam sistema completo
- ✅ Simulam uso real
- ✅ Pegam bugs de ponta a ponta

### Pirâmide de Testes

```
        /\
       /  \        E2E (Poucos)
      /────\       10% - Lentos, caros
     /      \
    /────────\     Integração (Médio)
   /          \    30% - Médios
  /────────────\
 /              \  Unitários (Muitos)
/────────────────\ 60% - Rápidos, baratos
```

**Proporção ideal**: 60% unitários, 30% integração, 10% E2E

### Test com Database In-Memory

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infra.configs.database import Base

@pytest.fixture
def db_session():
    """Cria banco in-memory para testes"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


def test_create_user(db_session):
    """Testa criação de usuário"""
    from services.user_service import UserService

    service = UserService(db_session)
    user = service.create_user(
        full_name="Test User",
        email="test@test.com",
        password="Pass123!",
        team_id=1,
        role=UserRoles.N1,
        tipo=UserTipo.ATENDENTE
    )

    assert user.id is not None
    assert user.user_email == "test@test.com"


def test_email_unique(db_session):
    """Testa que email é único"""
    from services.user_service import UserService

    service = UserService(db_session)

    # Criar primeiro usuário
    service.create_user(
        full_name="User 1",
        email="test@test.com",
        password="Pass123!",
        team_id=1,
        role=UserRoles.N1,
        tipo=UserTipo.ATENDENTE
    )

    # Tentar criar com mesmo email
    with pytest.raises(ValueError, match="já está em uso"):
        service.create_user(
            full_name="User 2",
            email="test@test.com",  # Mesmo email
            password="Pass123!",
            team_id=1,
            role=UserRoles.N1,
            tipo=UserTipo.ATENDENTE
        )
```

### Test de Endpoints

```python
from fastapi.testclient import TestClient

def test_list_users_endpoint():
    """Testa endpoint de listagem"""
    client = TestClient(app)

    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user_endpoint():
    """Testa endpoint de criação"""
    client = TestClient(app)

    user_data = {
        "user_full_name": "Test User",
        "user_email": "test@test.com",
        "user_password": "Pass123!",
        "user_team_id": 1,
        "user_role": "atendente",
        "user_tipo": "atendente"
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 201
    assert response.json()["user_email"] == "test@test.com"
```

---

## 5.5 Erros Comuns e Soluções

Esta seção consolida os erros mais frequentes ao usar SQLAlchemy com MappedAsDataclass.

### Erro 1: "non-default argument follows default argument"

**Mensagem:**
```
TypeError: non-default argument 'campo' follows default argument
```

**Causa:** Campo sem default vem depois de campo com default na hierarquia dataclass.

**Solução:** Adicione `init=False` a todos os campos com default na classe `Base`:

```python
# ❌ ERRADO
active: Mapped[Status] = mapped_column(default=Status.ATIVO)

# ✅ CORRETO
active: Mapped[Status] = mapped_column(default=Status.ATIVO, init=False)
```

---

### Erro 2: "AmbiguousForeignKeysError"

**Mensagem:**
```
sqlalchemy.exc.AmbiguousForeignKeysError: Could not determine join condition...
```

**Causa:** Múltiplas FKs entre duas tabelas e SQLAlchemy não sabe qual usar.

**Exemplo do problema:**
```python
# User tem duas FKs para Team:
# - user_team_id (time do usuário)
# - Team.team_manager_id (usuário é manager de algum time)
```

**Solução:** Especifique `foreign_keys=` no relationship:

```python
# ✅ CORRETO
team: Mapped["Team"] = relationship(
    foreign_keys=[user_team_id],  # Especifica QUAL FK usar
    back_populates="team_members",
    lazy="raise",
    init=False
)
```

---

### Erro 3: "NOT NULL constraint failed" (FK fica NULL)

**Mensagem:**
```
sqlalchemy.exc.IntegrityError: NOT NULL constraint failed: users.user_team_id
```

**Causa:** Usar `default=None` no relationship faz a FK ficar NULL.

```python
# ❌ ERRADO - CAUSA O BUG!
team: Mapped["Team"] = relationship(
    ...,
    init=False,
    default=None  # ← ISSO CAUSA O BUG!
)
```

**Solução:** NUNCA use `default=None` em relationships:

```python
# ✅ CORRETO
team: Mapped["Team"] = relationship(
    ...,
    init=False
    # SEM default=None!
)
```

---

### Erro 4: ID retorna None após INSERT

**Código com problema:**
```python
def insert(self, ...):
    data = User(...)
    db.session.add(data)
    db.session.flush()
    return data.id  # ← Retorna None!
```

**Causa:** Com MappedAsDataclass, o `id` não é atualizado automaticamente após INSERT.

**Solução:** Use `refresh()` após `flush()`:

```python
# ✅ CORRETO
def insert(self, ...):
    data = User(...)
    db.session.add(data)
    db.session.flush()
    db.session.refresh(data)  # ← NECESSÁRIO!
    return data.id  # Agora funciona!
```

---

### Erro 5: Imports circulares

**Mensagem:**
```
ImportError: cannot import name 'User' from partially initialized module
```

**Causa:** Duas entidades importando uma à outra.

**Solução:** Use strings para type hints:

```python
# ❌ ERRADO
from infra.entities.user import User  # No arquivo team.py
team_members: Mapped[list[User]]

# ✅ CORRETO
team_members: Mapped[list["User"]]  # String, sem import
```

---

### Erro 6: InvalidRequestError com lazy="raise"

**Mensagem:**
```
sqlalchemy.exc.InvalidRequestError: 'User.team' is not available due to lazy='raise'
```

**Causa:** Tentando acessar relationship sem eager loading.

**Solução:** Use `joinedload` ou `selectinload`:

```python
# ✅ CORRETO
users = (
    db.query(User)
    .options(joinedload(User.team))  # Carrega junto
    .all()
)
for user in users:
    print(user.team.team_name)  # Agora funciona!
```

---

### Tabela de Diagnóstico Rápido

| Erro | Causa Provável | Solução |
|------|----------------|---------|
| `non-default argument follows default` | Campo com default antes de campo obrigatório | Adicionar `init=False` |
| `AmbiguousForeignKeysError` | Múltiplas FKs entre tabelas | Usar `foreign_keys=` |
| `NOT NULL constraint failed` (FK) | `default=None` em relationship | Remover `default=None` |
| ID retorna None | MappedAsDataclass não atualiza automaticamente | Usar `refresh()` após `flush()` |
| `ImportError` circular | Imports cruzados entre entidades | Usar strings: `"User"` |
| `InvalidRequestError` lazy raise | Acesso sem eager loading | Usar `joinedload` |

---

## 5.6 Ordem de Criação de Registros

Ao popular o banco, você DEVE respeitar as dependências de FK.

### Ordem Correta (respeitando FKs)

```
1. Teams          (sem dependências)
2. Users          (depende de Teams via user_team_id)
3. set_manager    (associar gerente ao Team após criar User)
4. Reports        (depende de Teams e Users)
5. Projects       (depende de Teams e Users)
6. Forms          (sem dependências)
7. Tickets        (depende de Users e Forms)
8. Associações    (assign_to_report, etc.)
9. Chats          (depende de Tickets)
10. Messages      (depende de Chats e Users)
```

### Exemplo Completo de app.py para Popular Banco

```python
# app.py - Exemplo de como popular o banco
from infra.configs.database import Base
from infra.configs.connection import DBConnectionHandler
from infra.repositories import (
    TeamRepository, UserRepository, ReportRepository,
    ProjectRepository, TicketRepository, FormRepository,
    ChatRepository, MessageRepository
)
from infra.entities.team import Area
from infra.entities.user import UserRoles, UserTipo
from infra.entities.report import ReportFrequency, ReportStatus, ReportTags
from infra.entities.project import ProjectStatus, ProjectTags
from infra.entities.ticket import TicketClasse, TicketTipo, TicketStatus
from infra.entities.form import FormClasse, FormTipo
from datetime import date

# Criar banco e tabelas
db_handler = DBConnectionHandler()
engine = db_handler.get_engine()
Base.metadata.drop_all(engine)  # Cuidado: apaga tudo!
Base.metadata.create_all(engine)

# Instanciar repositories
team_repo = TeamRepository()
user_repo = UserRepository()
report_repo = ReportRepository()
project_repo = ProjectRepository()
form_repo = FormRepository()
ticket_repo = TicketRepository()
chat_repo = ChatRepository()
message_repo = MessageRepository()

# ════════════════════════════════════════════════════════════════
# 1. TEAMS (primeiro - sem dependências)
# ════════════════════════════════════════════════════════════════
team1_id = team_repo.insert(
    team_name="Performance Agricola",
    team_area=Area.EAB
)
team2_id = team_repo.insert(
    team_name="Planejamento Agricola",
    team_area=Area.PROJETOS
)

# ════════════════════════════════════════════════════════════════
# 2. USERS (depende de Teams)
# ════════════════════════════════════════════════════════════════
user1_id = user_repo.insert(
    user_corporative_id=416149,
    user_full_name='Matheus Beck',
    user_email='matheus@empresa.com',
    user_password='senhaSegura123',
    user_team_id=team1_id,  # ← FK para team
    user_role=UserRoles.N1,
    user_tipo=UserTipo.ATENDENTE
)
user2_id = user_repo.insert(
    user_corporative_id=123456,
    user_full_name='Ana Silva',
    user_email='ana.silva@empresa.com',
    user_password='senhaSegura123',
    user_team_id=team2_id,
    user_role=UserRoles.GESTOR,
    user_tipo=UserTipo.ATENDENTE
)

# ════════════════════════════════════════════════════════════════
# 3. SET MANAGER (após criar users)
# ════════════════════════════════════════════════════════════════
team_repo.set_manager(team1_id, user1_id)
team_repo.set_manager(team2_id, user2_id)

# ════════════════════════════════════════════════════════════════
# 4. REPORTS (depende de Teams e Users)
# ════════════════════════════════════════════════════════════════
report1_id = report_repo.insert(
    report_name='Dashboard CCT',
    report_link='https://powerbi.com/cct',
    report_description='Relatório de Corte, Carregamento e Transporte',
    report_frequency=ReportFrequency.HORARIO,
    report_team_responsible_id=team1_id,
    report_owner_id=user1_id,
    report_status=ReportStatus.ATIVO,
    report_tags=ReportTags.CCT,
    report_public=True
)

# ════════════════════════════════════════════════════════════════
# 5. PROJECTS
# ════════════════════════════════════════════════════════════════
project1_id = project_repo.insert(
    project_name='Otimização Rotas',
    project_directory='/projects/otimizacao',
    project_description='Otimização de rotas de transporte',
    project_team_responsible_id=team1_id,
    project_manager_id=user2_id,
    project_tags=ProjectTags.ATRIBUIDO,
    project_status=ProjectStatus.ATIVO,
    project_start_date=date(2024, 1, 15),
    project_expected_end_date=date(2024, 6, 30),
    project_planned_budget=150000.0,
    project_public=True
)

# ════════════════════════════════════════════════════════════════
# 6. FORMS
# ════════════════════════════════════════════════════════════════
form1_id = form_repo.insert(
    form_name='Formulário Correção',
    form_ticket_class=FormClasse.RELATORIO,
    form_type=FormTipo.CORRECAO,
    form_fields='{"fields":[{"name":"descricao","type":"textarea"}]}'
)

# ════════════════════════════════════════════════════════════════
# 7. TICKETS (depende de Users e Forms)
# ════════════════════════════════════════════════════════════════
ticket1_id = ticket_repo.insert(
    ticket_title='Correção valores Dashboard',
    ticket_class=TicketClasse.RELATORIO,
    ticket_type=TicketTipo.CORRECAO,
    ticket_client_id=user2_id,  # ← FK para User
    ticket_description='Valores divergentes no dashboard',
    ticket_form_id=form1_id,    # ← FK para Form
    ticket_status=TicketStatus.ABERTO
)

# ════════════════════════════════════════════════════════════════
# 8. ASSOCIAÇÕES (após criar entidades relacionadas)
# ════════════════════════════════════════════════════════════════
ticket_repo.assign_to_report(ticket1_id, report1_id)

# ════════════════════════════════════════════════════════════════
# 9. CHATS (depende de Tickets)
# ════════════════════════════════════════════════════════════════
chat1_id = chat_repo.insert(chat_ticket_id=ticket1_id)

# ════════════════════════════════════════════════════════════════
# 10. MESSAGES (depende de Chats e Users)
# ════════════════════════════════════════════════════════════════
message_repo.insert(
    message_chat_id=chat1_id,
    message_user_id=user2_id,
    message_content='Boa tarde, identifiquei divergência nos valores.',
    message_type='text',
    message_is_internal=False
)

print("✅ Banco criado e populado com sucesso!")
print(f"Teams: {team1_id}, {team2_id}")
print(f"Users: {user1_id}, {user2_id}")
print(f"Reports: {report1_id}")
print(f"Projects: {project1_id}")
print(f"Tickets: {ticket1_id}")
print(f"Chats: {chat1_id}")
```

### Validação Final

Execute e verifique:
```bash
python app.py
```

Saída esperada:
```
✅ Banco criado e populado com sucesso!
Teams: 1, 2
Users: 1, 2
Reports: 1
Projects: 1
Tickets: 1
Chats: 1
```

---

# MÓDULO 6: GUIA PRÁTICO PASSO A PASSO

Este módulo é um guia prático para implementar funcionalidades do zero ao deploy. Cada passo tem uma explicação do **porquê** é necessário, garantindo que você entenda não apenas *como* fazer, mas *por que* fazer.

---

## 6.1 Criando uma Nova Entidade

Quando você precisa adicionar uma nova tabela ao banco de dados, deve seguir uma sequência específica de passos. A ordem importa porque cada camada depende da anterior.

### Passo 1: Definir a Entidade

**Por que este é o primeiro passo?**
A entidade é a representação Python da tabela no banco. Sem ela, nada mais pode existir - não há migration para gerar, repository para consultar, nem schema para validar. É o alicerce de tudo.

**O que acontece se pular?**
Você não conseguirá criar migrations (Alembic não tem o que detectar) nem fazer queries (SQLAlchemy não sabe que a tabela existe).

```python
# infra/entities/category.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.configs.database import Base


class Category(Base):
    """Categoria de tickets."""
    __tablename__ = "categories"

    # Campos obrigatórios (sem default, entram no __init__)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Campos opcionais (init=False)
    category_description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        init=False,
        default=None
    )

    # Relationships (SEMPRE init=False, NUNCA default=None)
    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="category",
        lazy="raise",
        init=False,
        default_factory=list
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.category_name}')>"
```

### Passo 2: Exportar no `__init__.py`

**Por que exportar?**
O `__init__.py` funciona como um "catálogo" público do pacote. Ao exportar a entidade aqui, outros módulos podem importar de forma limpa: `from infra.entities import Category` em vez de `from infra.entities.category import Category`.

**O que acontece se pular?**
O Alembic pode não detectar a entidade nas migrations (ele importa de `infra.entities`). Você terá imports mais verbosos e inconsistentes no projeto.

```python
# infra/entities/__init__.py
from infra.entities.category import Category
# ... outros imports
```

### Passo 3: Criar Migration

**Por que migrations são obrigatórias?**
A entidade Python define a estrutura *no código*, mas o banco de dados ainda não sabe que essa tabela existe. Sem migration, a tabela não é criada no banco - você receberá `Table 'categories' doesn't exist` ao tentar inserir dados.

**Por que não usar `Base.metadata.create_all()`?**
Ver MÓDULO 0.5 - `create_all()` não versiona mudanças, não funciona em produção com múltiplas instâncias, e não permite rollback.

```bash
# 1. Gera arquivo de migration com as mudanças detectadas
alembic revision --autogenerate -m "criar tabela categories"

# 2. Aplica a migration no banco (cria a tabela de fato)
alembic upgrade head
```

**Dica:** Sempre revise o arquivo de migration gerado antes de aplicar. O `--autogenerate` pode errar em casos complexos (renomeação de colunas, por exemplo).

### Passo 4: Criar Repository

**Por que usar Repository?**
O Repository isola o acesso ao banco de dados. Sem ele, você teria queries SQLAlchemy espalhadas pelo código (em services, routes, etc.), dificultando testes e manutenção.

**O que o Repository fornece:**
- Ponto único para queries dessa entidade
- Facilita mock em testes (você mocka o repository, não o banco)
- Permite trocar o ORM no futuro sem reescrever toda aplicação

```python
# infra/repositories/category_repository.py
from sqlalchemy.orm import Session

from infra.entities.category import Category
from infra.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: Session):
        super().__init__(session, Category)

    def get_by_name(self, name: str) -> Category | None:
        return self.session.query(Category).filter(
            Category.category_name == name
        ).first()
```

### Passo 5: Criar Schemas

**Por que Schemas separados da Entity?**
A Entity representa o banco de dados. O Schema representa o contrato da API. Eles têm propósitos diferentes:

| Aspecto | Entity | Schema |
|---------|--------|--------|
| Propósito | Mapear tabela do banco | Validar entrada/saída da API |
| Campos | Todos os campos da tabela | Apenas campos expostos na API |
| Validação | Constraints do banco | Regras de negócio (min_length, regex) |
| Senhas | Armazenada com hash | Recebida em texto, nunca retornada |

**Por que 3 schemas (Create, Update, Response)?**
- **Create:** Campos obrigatórios para criar (sem id, sem created_at)
- **Update:** Todos campos opcionais (PATCH permite atualização parcial)
- **Response:** O que a API retorna (pode omitir campos sensíveis)

```python
# schemas/category_schema.py
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    category_name: str = Field(..., min_length=2, max_length=100)
    category_description: str | None = Field(None, max_length=500)


class CategoryUpdate(BaseModel):
    category_name: str | None = Field(None, min_length=2, max_length=100)
    category_description: str | None = Field(None, max_length=500)


class CategoryResponse(BaseModel):
    id: int
    category_name: str
    category_description: str | None

    class Config:
        from_attributes = True  # Permite converter Entity → Schema automaticamente
```

### Passo 6: Criar Service

**Por que Service se já tenho Repository?**
O Repository faz queries. O Service implementa **regras de negócio**. São camadas distintas:

| Camada | Responsabilidade | Exemplo |
|--------|------------------|---------|
| Repository | Persistir/buscar dados | `get_by_email()`, `create()` |
| Service | Regras de negócio | "Não pode criar usuário com email duplicado" |

**O que acontece sem Service?**
Regras de negócio ficam espalhadas nas routes, duplicadas, difíceis de testar. Quando a regra muda, você precisa alterar em vários lugares.

```python
# services/category_service.py
from sqlalchemy.orm import Session

from infra.entities.category import Category
from infra.repositories.category_repository import CategoryRepository
from schemas.category_schema import CategoryCreate, CategoryResponse
from infra.exceptions import ConflictException, NotFoundException


class CategoryService:
    def __init__(self, session: Session):
        self.repo = CategoryRepository(session)

    def create(self, data: CategoryCreate) -> CategoryResponse:
        if self.repo.get_by_name(data.category_name):
            raise ConflictException(f"Categoria '{data.category_name}' já existe")

        category = Category(category_name=data.category_name)
        if data.category_description:
            category.category_description = data.category_description

        created = self.repo.create(category)
        return CategoryResponse.model_validate(created)

    def get(self, id: int) -> CategoryResponse:
        category = self.repo.get_by_id(id)
        if not category:
            raise NotFoundException("Category", id)
        return CategoryResponse.model_validate(category)
```

### Passo 7: Criar Routes

**Por que Routes são a última camada?**
Routes são a "porta de entrada" da API. Elas dependem de tudo que criamos antes (Service, Schema), mas nada depende delas. Por isso são criadas por último.

**O que Routes fazem:**
- Recebem requisições HTTP
- Validam entrada usando Schemas (automático no FastAPI)
- Delegam para Service
- Retornam resposta formatada

**O que Routes NÃO devem fazer:**
- Queries diretas no banco (isso é Repository)
- Regras de negócio (isso é Service)
- Lógica complexa (mantenha routes simples)

```python
# api/routes/category_routes.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from infra.configs.connection import get_db
from services.category_service import CategoryService
from schemas.category_schema import CategoryCreate, CategoryResponse


router = APIRouter(prefix="/categories", tags=["Categories"])


def get_service(session: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(session)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, service: CategoryService = Depends(get_service)):
    return service.create(data)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, service: CategoryService = Depends(get_service)):
    return service.get(category_id)
```

### Passo 8: Registrar Router

**Por que é necessário registrar?**
Criar o arquivo de routes não é suficiente. O FastAPI não sabe que esse arquivo existe. Você precisa explicitamente dizer "inclua essas rotas na aplicação".

**O que acontece se pular?**
Suas rotas simplesmente não existirão. Requisições para `/api/v1/categories` retornarão 404 Not Found.

**Organização com prefixo:**
O `prefix="/api/v1"` no main.py + `prefix="/categories"` no router resulta em `/api/v1/categories`. Isso permite versionamento da API e organização clara.

```python
# main.py
from api.routes import category_routes

app.include_router(category_routes.router, prefix="/api/v1")
```

---

## 6.2 Criando um Novo Endpoint

Nem sempre você precisa criar uma entidade nova. Às vezes precisa apenas adicionar um endpoint a uma entidade existente.

**Quando criar novo endpoint vs nova entidade?**
- **Nova entidade:** Quando precisa de uma nova tabela no banco
- **Novo endpoint:** Quando precisa de uma nova forma de acessar dados existentes

### Endpoint de Listagem com Filtros

**Por que adicionar filtros?**
Um endpoint `GET /tickets` que retorna TODOS os tickets é inútil em produção. Com milhares de registros, a resposta seria gigante e lenta. Filtros permitem que o cliente peça apenas o que precisa.

**Por que paginação (skip/limit)?**
Mesmo com filtros, o resultado pode ser grande. Paginação divide em "páginas" menores, melhorando performance e UX.

```python
# api/routes/ticket_routes.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from infra.configs.connection import get_db
from services.ticket_service import TicketService
from schemas.ticket_schema import TicketResponse, TicketStatus


router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("/", response_model=list[TicketResponse])
def list_tickets(
    status: Optional[TicketStatus] = Query(None, description="Filtrar por status"),
    team_id: Optional[int] = Query(None, description="Filtrar por time"),
    client_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_db)
):
    """
    Lista tickets com filtros opcionais.

    - **status**: Filtrar por status (aberto, pendente, encerrado)
    - **team_id**: Filtrar por ID do time
    - **client_id**: Filtrar por ID do cliente
    """
    service = TicketService(session)
    return service.list_tickets(
        status=status,
        team_id=team_id,
        client_id=client_id,
        skip=skip,
        limit=limit
    )
```

---

## 6.3 Implementando CRUD Completo

Este é o resumo visual de tudo que você aprendeu. Quando precisar criar uma funcionalidade completa, siga este fluxo.

**Por que seguir esta ordem?**
Cada camada depende da anterior. Se você tentar criar o Repository antes da Entity, não terá o que consultar. Se tentar criar Routes antes do Service, não terá regras de negócio para chamar.

**Checklist mental para cada nova funcionalidade:**
1. ✅ Entity existe? Se não, criar
2. ✅ Migration aplicada? Se não, gerar e aplicar
3. ✅ Repository com métodos necessários? Se não, adicionar
4. ✅ Schemas para entrada/saída? Se não, criar
5. ✅ Service com regras de negócio? Se não, implementar
6. ✅ Route expondo a funcionalidade? Se não, criar
7. ✅ Router registrado no app? Se não, incluir
8. ✅ Testes cobrindo o fluxo? Se não, escrever

### Fluxo Completo: Entity → API

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  1. ENTITY (infra/entities/product.py)                                      │
│     - Definir campos, FKs, relationships                                    │
│     - Herdar de Base                                                        │
│     - Seguir regras do MappedAsDataclass                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  2. MIGRATION (alembic revision --autogenerate)                             │
│     - Gerar migration                                                       │
│     - Revisar SQL gerado                                                    │
│     - Aplicar: alembic upgrade head                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  3. REPOSITORY (infra/repositories/product_repository.py)                   │
│     - Herdar de BaseRepository                                              │
│     - Adicionar métodos específicos (get_by_code, search, etc.)             │
├─────────────────────────────────────────────────────────────────────────────┤
│  4. SCHEMAS (schemas/product_schema.py)                                     │
│     - ProductCreate (entrada)                                               │
│     - ProductUpdate (entrada parcial)                                       │
│     - ProductResponse (saída)                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  5. SERVICE (services/product_service.py)                                   │
│     - Regras de negócio                                                     │
│     - Validações                                                            │
│     - Orquestração de repositories                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  6. ROUTES (api/routes/product_routes.py)                                   │
│     - POST / (create)                                                       │
│     - GET /{id} (read one)                                                  │
│     - GET / (read all)                                                      │
│     - PATCH /{id} (update)                                                  │
│     - DELETE /{id} (delete)                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  7. REGISTER (main.py)                                                      │
│     - app.include_router(product_routes.router)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  8. TEST                                                                    │
│     - tests/test_product_repository.py                                      │
│     - tests/test_product_service.py                                         │
│     - tests/test_product_routes.py                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# MÓDULO 7: PRODUÇÃO E DEPLOY

Este módulo cobre tudo que você precisa para colocar sua aplicação em produção de forma profissional.

---

## 7.1 Docker - Containerização

### O Que É Docker?

**Docker** é uma plataforma que permite empacotar aplicações com todas as suas dependências em **containers** - unidades isoladas que rodam de forma idêntica em qualquer ambiente.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONCEITOS FUNDAMENTAIS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IMAGEM (Image)                                                             │
│  • Template READ-ONLY para criar containers                                 │
│  • Contém: código, runtime, bibliotecas, variáveis de ambiente              │
│  • Criada a partir de um Dockerfile                                         │
│  • Pode ser compartilhada (Docker Hub, registry privado)                    │
│  • Analogia: Classe em OOP                                                  │
│                                                                             │
│  CONTAINER                                                                  │
│  • Instância de uma imagem em execução                                      │
│  • Isolado: tem seu próprio filesystem, rede, processos                     │
│  • Efêmero: pode ser destruído e recriado rapidamente                       │
│  • Analogia: Objeto (instância) em OOP                                      │
│                                                                             │
│  DOCKERFILE                                                                 │
│  • Arquivo de texto com instruções para criar uma imagem                    │
│  • Define: base, dependências, código, comandos                             │
│  • Versionável (git)                                                        │
│                                                                             │
│  DOCKER COMPOSE                                                             │
│  • Ferramenta para definir aplicações multi-container                       │
│  • Um arquivo YAML define todos os serviços (app, banco, redis...)          │
│  • Simplifica orquestração local                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Container vs Máquina Virtual

```
┌─────────────────────────────────────────────────────────────────────────────┐
│          MÁQUINA VIRTUAL                    CONTAINER                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌───────┐ ┌───────┐ ┌───────┐      ┌───────┐ ┌───────┐ ┌───────┐        │
│   │ App A │ │ App B │ │ App C │      │ App A │ │ App B │ │ App C │        │
│   ├───────┤ ├───────┤ ├───────┤      ├───────┤ ├───────┤ ├───────┤        │
│   │ Bins/ │ │ Bins/ │ │ Bins/ │      │ Bins/ │ │ Bins/ │ │ Bins/ │        │
│   │ Libs  │ │ Libs  │ │ Libs  │      │ Libs  │ │ Libs  │ │ Libs  │        │
│   ├───────┤ ├───────┤ ├───────┤      └───┬───┴───┬───┴───┬───┘            │
│   │Guest  │ │Guest  │ │Guest  │          │       │       │                 │
│   │  OS   │ │  OS   │ │  OS   │      ┌───┴───────┴───────┴───┐            │
│   └───┬───┴───┬───┴───┬───┘          │     Docker Engine     │            │
│   ┌───┴───────┴───────┴───┐          └───────────┬───────────┘            │
│   │      Hypervisor       │          ┌───────────┴───────────┐            │
│   └───────────┬───────────┘          │      Host OS          │            │
│   ┌───────────┴───────────┐          └───────────┬───────────┘            │
│   │      Host OS          │          ┌───────────┴───────────┐            │
│   └───────────┬───────────┘          │      Hardware         │            │
│   ┌───────────┴───────────┐          └───────────────────────┘            │
│   │      Hardware         │                                                │
│   └───────────────────────┘                                                │
│                                                                             │
│   • Cada VM tem SO completo         • Containers compartilham kernel       │
│   • Pesado (~GB por VM)             • Leve (~MB por container)             │
│   • Boot em minutos                 • Boot em segundos                     │
│   • Isolamento forte                • Isolamento via namespaces            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Comandos Docker Essenciais

```bash
# ═══════════════════════════════════════════════════════════════════════════
# IMAGENS
# ═══════════════════════════════════════════════════════════════════════════

# Construir imagem a partir do Dockerfile
docker build -t minha-api:1.0 .
#        -t = tag (nome:versão)
#        .  = contexto (diretório atual)

# Listar imagens locais
docker images

# Baixar imagem do Docker Hub
docker pull python:3.11-slim

# Remover imagem
docker rmi minha-api:1.0

# ═══════════════════════════════════════════════════════════════════════════
# CONTAINERS
# ═══════════════════════════════════════════════════════════════════════════

# Rodar container
docker run minha-api:1.0

# Rodar em background (daemon)
docker run -d minha-api:1.0

# Rodar com porta mapeada
docker run -d -p 8000:8000 minha-api:1.0
#             host:container

# Rodar com variável de ambiente
docker run -d -e DATABASE_URL=sqlite:///app.db minha-api:1.0

# Rodar com volume (persistência)
docker run -d -v /meu/diretorio:/app/data minha-api:1.0

# Rodar e entrar no shell
docker run -it minha-api:1.0 bash

# Listar containers rodando
docker ps

# Listar todos os containers (incluindo parados)
docker ps -a

# Ver logs de um container
docker logs <container_id>
docker logs -f <container_id>  # -f = follow (streaming)

# Entrar em container rodando
docker exec -it <container_id> bash

# Parar container
docker stop <container_id>

# Remover container
docker rm <container_id>

# Parar e remover todos os containers
docker stop $(docker ps -aq) && docker rm $(docker ps -aq)

# ═══════════════════════════════════════════════════════════════════════════
# DOCKER COMPOSE
# ═══════════════════════════════════════════════════════════════════════════

# Subir todos os serviços definidos no docker-compose.yml
docker-compose up

# Subir em background
docker-compose up -d

# Subir e rebuildar imagens
docker-compose up --build

# Ver logs de todos os serviços
docker-compose logs

# Ver logs de um serviço específico
docker-compose logs api

# Executar comando em um serviço
docker-compose exec api bash

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (⚠️ APAGA DADOS!)
docker-compose down -v

# Ver status dos serviços
docker-compose ps
```

### Por Que Docker?

Sem Docker, você tem o famoso problema "funciona na minha máquina":

```
Desenvolvedor: "Funciona no meu PC!"
DevOps: "Mas não funciona no servidor..."
Desenvolvedor: "Você instalou Python 3.11?"
DevOps: "Temos Python 3.9..."
Desenvolvedor: "E o PostgreSQL 15?"
DevOps: "Temos 12..."
(3 horas depois...)
```

**Docker resolve isso**: Empacota código + dependências + configurações em um container que roda igual em qualquer lugar.

### Dockerfile para FastAPI + SQLAlchemy

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema (para psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (cache de layers)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar usuário não-root (segurança)
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Porta da aplicação
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Explicação das decisões**:

| Linha | Por Que? |
|-------|----------|
| `python:3.11-slim` | Imagem menor (~150MB vs ~900MB da full) |
| `PYTHONDONTWRITEBYTECODE=1` | Não cria arquivos .pyc (desnecessário em container) |
| `PYTHONUNBUFFERED=1` | Logs aparecem imediatamente (não bufferiza) |
| `COPY requirements.txt` primeiro | Cache de Docker - só reinstala se requirements mudar |
| `adduser appuser` | Segurança - não roda como root |

### Docker Compose - Orquestração Local

```yaml
# docker-compose.yml
version: "3.9"

services:
  # ════════════════════════════════════════════════════════════════
  # BANCO DE DADOS
  # ════════════════════════════════════════════════════════════════
  db:
    image: postgres:15-alpine
    container_name: portal_db
    restart: unless-stopped
    environment:
      POSTGRES_USER: portal_user
      POSTGRES_PASSWORD: portal_pass  # Em produção: use secrets!
      POSTGRES_DB: portal_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"  # Expor apenas em dev
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U portal_user -d portal_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  # ════════════════════════════════════════════════════════════════
  # APLICAÇÃO
  # ════════════════════════════════════════════════════════════════
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: portal_api
    restart: unless-stopped
    environment:
      DATABASE_URL: postgresql://portal_user:portal_pass@db:5432/portal_db
      DEBUG: "false"
      SECRET_KEY: ${SECRET_KEY}  # Vem do .env
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy  # Espera banco estar pronto
    volumes:
      - ./logs:/app/logs  # Persistir logs

  # ════════════════════════════════════════════════════════════════
  # MIGRATIONS (roda uma vez e para)
  # ════════════════════════════════════════════════════════════════
  migrations:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: portal_migrations
    environment:
      DATABASE_URL: postgresql://portal_user:portal_pass@db:5432/portal_db
    depends_on:
      db:
        condition: service_healthy
    command: alembic upgrade head
    restart: "no"  # Roda uma vez e para

volumes:
  postgres_data:
```

### Comandos Essenciais

```bash
# Construir e subir tudo
docker-compose up --build

# Subir em background (daemon)
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Executar migration manualmente
docker-compose run --rm api alembic upgrade head

# Acessar shell do container
docker-compose exec api bash

# Parar tudo
docker-compose down

# Parar e remover volumes (⚠️ APAGA DADOS!)
docker-compose down -v
```

---

## 7.2 Configuração para Produção

### Variáveis de Ambiente Seguras

```python
# infra/configs/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações com validação para produção."""

    # ══════════════════════════════════════════════════════════════
    # APLICAÇÃO
    # ══════════════════════════════════════════════════════════════
    APP_NAME: str = "Portal de Chamados"
    DEBUG: bool = False
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")

    # ══════════════════════════════════════════════════════════════
    # BANCO DE DADOS
    # ══════════════════════════════════════════════════════════════
    DATABASE_URL: SecretStr  # Obrigatório, não tem default
    DB_POOL_SIZE: int = Field(default=5, ge=1, le=20)
    DB_MAX_OVERFLOW: int = Field(default=10, ge=0, le=50)
    DB_POOL_RECYCLE: int = Field(default=3600, description="Segundos para reciclar conexões")

    # ══════════════════════════════════════════════════════════════
    # SEGURANÇA
    # ══════════════════════════════════════════════════════════════
    SECRET_KEY: SecretStr  # Obrigatório
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_HOSTS: list[str] = ["*"]  # Em produção: especifique domínios

    # ══════════════════════════════════════════════════════════════
    # OBSERVABILIDADE
    # ══════════════════════════════════════════════════════════════
    LOG_LEVEL: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    LOG_FORMAT: str = "json"  # "json" para produção, "text" para dev

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

### Pool de Conexões para Produção

```python
# infra/configs/connection.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import logging

from infra.configs.settings import settings

logger = logging.getLogger(__name__)


def create_production_engine():
    """Engine otimizado para produção."""

    engine = create_engine(
        settings.DATABASE_URL.get_secret_value(),

        # ══════════════════════════════════════════════════════════
        # POOL DE CONEXÕES
        # ══════════════════════════════════════════════════════════
        poolclass=QueuePool,
        pool_size=settings.DB_POOL_SIZE,         # Conexões mantidas abertas
        max_overflow=settings.DB_MAX_OVERFLOW,   # Conexões extras em pico
        pool_recycle=settings.DB_POOL_RECYCLE,   # Recicla conexões velhas
        pool_pre_ping=True,                       # Verifica se conexão está viva

        # ══════════════════════════════════════════════════════════
        # PERFORMANCE
        # ══════════════════════════════════════════════════════════
        echo=settings.DEBUG,              # SQL no log apenas em debug
        echo_pool=settings.DEBUG,         # Pool info apenas em debug

        # ══════════════════════════════════════════════════════════
        # TIMEOUTS
        # ══════════════════════════════════════════════════════════
        connect_args={
            "connect_timeout": 10,        # Timeout de conexão
            "options": "-c statement_timeout=30000"  # Query timeout 30s
        }
    )

    # Logging de eventos do pool
    @event.listens_for(engine, "checkout")
    def receive_checkout(dbapi_connection, connection_record, connection_proxy):
        logger.debug(f"Conexão obtida do pool: {id(dbapi_connection)}")

    @event.listens_for(engine, "checkin")
    def receive_checkin(dbapi_connection, connection_record):
        logger.debug(f"Conexão devolvida ao pool: {id(dbapi_connection)}")

    return engine


engine = create_production_engine()
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """Dependency injection para FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 7.3 Observabilidade

### Logging Estruturado

```python
# infra/configs/logging_config.py
import logging
import sys
import json
from datetime import datetime
from typing import Any

from infra.configs.settings import settings


class JSONFormatter(logging.Formatter):
    """Formatter que gera JSON para análise em produção."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Adicionar exception se houver
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Adicionar campos extras
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        return json.dumps(log_data)


class TextFormatter(logging.Formatter):
    """Formatter legível para desenvolvimento."""

    def format(self, record: logging.LogRecord) -> str:
        return f"{record.levelname:8} | {record.name:30} | {record.getMessage()}"


def setup_logging():
    """Configura logging para a aplicação."""

    # Formatter baseado no ambiente
    if settings.LOG_FORMAT == "json":
        formatter = JSONFormatter()
    else:
        formatter = TextFormatter()

    # Handler para stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Configurar root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.handlers = [handler]

    # Silenciar loggers verbosos
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.DEBUG if settings.DEBUG else logging.WARNING
    )


# Chamar no startup
setup_logging()
```

### Logging de Requests

```python
# api/middleware/logging_middleware.py
import time
import logging
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Loga todas as requisições com timing."""

    async def dispatch(self, request: Request, call_next):
        # Gerar ID único para a requisição
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id

        # Timing
        start_time = time.perf_counter()

        # Log de entrada
        logger.info(
            f"[{request_id}] {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else None,
            }
        )

        # Processar requisição
        response = await call_next(request)

        # Calcular duração
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Log de saída
        logger.info(
            f"[{request_id}] {response.status_code} ({duration_ms:.2f}ms)",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            }
        )

        # Adicionar request_id no header da resposta
        response.headers["X-Request-ID"] = request_id

        return response
```

### Logging de Queries SQL

```python
# Ver todas as queries SQL (útil para debug)
import logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

# Output:
# DEBUG | sqlalchemy.engine | SELECT users.id, users.name FROM users WHERE id = 1
# DEBUG | sqlalchemy.engine | [generated in 0.00012s] (1,)
```

### Métricas com Prometheus + Grafana

**Stack de observabilidade open source mais popular:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STACK DE OBSERVABILIDADE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   FastAPI ──► Prometheus ──► Grafana                                        │
│   (métricas)    (coleta)     (visualização)                                 │
│                                                                             │
│   • Prometheus: Coleta e armazena métricas (time series database)           │
│   • Grafana: Dashboards bonitos, alertas, visualização                      │
│   • Ambos são open source e gratuitos                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**1. Instalar dependência:**

```bash
pip install prometheus-fastapi-instrumentator
```

**2. Configurar no main.py:**

```python
# main.py
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(...)

# Instrumentar DEPOIS de criar o app
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
```

**3. Métricas customizadas:**

```python
# infra/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Contador: Total de operações
tickets_created = Counter(
    "tickets_created_total",
    "Total de tickets criados",
    ["status", "team"]
)

# Histograma: Distribuição de tempo
query_duration = Histogram(
    "db_query_duration_seconds",
    "Tempo de queries no banco",
    ["query_type"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
)

# Gauge: Valor atual (pode subir ou descer)
active_connections = Gauge(
    "db_active_connections",
    "Conexões ativas no pool"
)

# Uso no código:
def create_ticket(ticket_data):
    with query_duration.labels(query_type="insert").time():
        # ... código que faz INSERT
        pass
    tickets_created.labels(status="aberto", team="dev").inc()
```

**4. Docker Compose com Prometheus + Grafana:**

```yaml
# docker-compose.observability.yml
version: "3.9"

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=15d'

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin  # Mude em produção!
    volumes:
      - grafana_data:/var/lib/grafana
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

volumes:
  prometheus_data:
  grafana_data:
```

**5. prometheus.yml:**

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['api:8000']  # Nome do service no docker-compose
    metrics_path: /metrics
```

**6. Acessar:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

**Métricas automáticas do instrumentator:**
- `http_requests_total` - Total de requisições
- `http_request_duration_seconds` - Tempo de resposta
- `http_requests_in_progress` - Requisições em andamento

### Health Check Endpoint

```python
# api/routes/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from infra.configs.connection import get_db, engine

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """Health check básico."""
    return {"status": "healthy"}


@router.get("/health/ready")
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness check - verifica se a aplicação está pronta.
    Kubernetes usa para saber quando enviar tráfego.
    """
    checks = {}

    # Verificar banco de dados
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"

    # Verificar pool de conexões
    pool = engine.pool
    checks["pool"] = {
        "size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
    }

    all_healthy = all(
        v == "healthy" or isinstance(v, dict)
        for v in checks.values()
    )

    return {
        "status": "ready" if all_healthy else "not_ready",
        "checks": checks
    }


@router.get("/health/live")
def liveness_check():
    """
    Liveness check - verifica se a aplicação está viva.
    Kubernetes usa para decidir se deve reiniciar o container.
    """
    return {"status": "alive"}
```

---

## 7.4 Configuração do FastAPI para Produção

### main.py Completo

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from infra.configs.settings import settings
from infra.configs.logging_config import setup_logging
from api.middleware.logging_middleware import RequestLoggingMiddleware
from api.routes import users, teams, tickets, health


# ════════════════════════════════════════════════════════════════════════════
# LIFECYCLE
# ════════════════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia startup e shutdown da aplicação."""
    # STARTUP
    setup_logging()
    print(f"🚀 Starting {settings.APP_NAME} in {settings.ENVIRONMENT} mode")

    yield

    # SHUTDOWN
    print(f"👋 Shutting down {settings.APP_NAME}")


# ════════════════════════════════════════════════════════════════════════════
# APP
# ════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,      # Swagger só em dev
    redoc_url="/redoc" if settings.DEBUG else None,    # ReDoc só em dev
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)


# ════════════════════════════════════════════════════════════════════════════
# MIDDLEWARE (ordem importa! Último adicionado = primeiro executado)
# ════════════════════════════════════════════════════════════════════════════

# 1. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Compressão GZip
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 3. Logging de requests
app.add_middleware(RequestLoggingMiddleware)


# ════════════════════════════════════════════════════════════════════════════
# ROTAS
# ════════════════════════════════════════════════════════════════════════════

app.include_router(health.router)
app.include_router(users.router, prefix="/api/v1")
app.include_router(teams.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")


# ════════════════════════════════════════════════════════════════════════════
# EXCEPTION HANDLERS
# ════════════════════════════════════════════════════════════════════════════

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Trata erros de integridade do banco (FK, UNIQUE, etc)."""
    logger.error(f"IntegrityError: {exc.orig}")
    return JSONResponse(
        status_code=409,
        content={"detail": "Conflito de dados. Verifique valores únicos e relacionamentos."}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handler genérico para erros não tratados."""
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor."}
    )
```

---

## 7.5 Git e GitHub - Versionamento Profissional

### Por Que Versionamento Importa?

Sem Git, você tem:
- `projeto_final.py`
- `projeto_final_v2.py`
- `projeto_final_v2_corrigido.py`
- `projeto_final_v2_corrigido_ESSE_FUNCIONA.py`

**Git resolve isso** mantendo histórico completo, permitindo voltar a qualquer versão, trabalhar em paralelo e colaborar com outros desenvolvedores.

### Comandos Básicos

```bash
# ════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO INICIAL (uma vez por máquina)
# ════════════════════════════════════════════════════════════════
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# ════════════════════════════════════════════════════════════════
# INICIANDO UM PROJETO
# ════════════════════════════════════════════════════════════════
# Criar repositório novo
git init

# Clonar repositório existente
git clone https://github.com/empresa/projeto.git

# ════════════════════════════════════════════════════════════════
# FLUXO BÁSICO DE TRABALHO
# ════════════════════════════════════════════════════════════════
# Ver status (arquivos modificados, staged, etc)
git status

# Adicionar arquivos para commit
git add arquivo.py           # Um arquivo
git add .                    # Todos os arquivos modificados
git add -p                   # Interativo (escolher partes)

# Fazer commit
git commit -m "Mensagem descritiva do que foi feito"

# Enviar para repositório remoto (GitHub)
git push

# Baixar atualizações do remoto
git pull

# ════════════════════════════════════════════════════════════════
# VERIFICAR HISTÓRICO
# ════════════════════════════════════════════════════════════════
# Ver commits
git log                      # Completo
git log --oneline           # Resumido
git log --graph             # Com visualização de branches

# Ver diferenças
git diff                     # Mudanças não staged
git diff --staged           # Mudanças staged
git diff HEAD~1             # Comparar com commit anterior
```

### Branches - Trabalhando em Paralelo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ESTRATÉGIA DE BRANCHES                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   main/master ──────────────────────────────────────────────► (produção)    │
│        │                                                                    │
│        └──► develop ────────────────────────────────────────► (staging)     │
│                  │                                                          │
│                  ├──► feature/login ──────┐                                 │
│                  │                        │ (merge após review)             │
│                  │                        ▼                                 │
│                  ├──► feature/dashboard ──┘                                 │
│                  │                                                          │
│                  └──► bugfix/fix-query ───► (hotfix para develop)           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```bash
# ════════════════════════════════════════════════════════════════
# TRABALHANDO COM BRANCHES
# ════════════════════════════════════════════════════════════════
# Listar branches
git branch              # Locais
git branch -r           # Remotas
git branch -a           # Todas

# Criar e mudar para nova branch
git checkout -b feature/nova-funcionalidade

# Mudar de branch
git checkout develop

# Deletar branch
git branch -d feature/concluida    # Local
git push origin --delete feature/concluida  # Remota

# ════════════════════════════════════════════════════════════════
# MERGE E REBASE
# ════════════════════════════════════════════════════════════════
# Merge: junta branches (cria commit de merge)
git checkout develop
git merge feature/nova-funcionalidade

# Rebase: reaplica commits em cima de outra branch (histórico linear)
git checkout feature/minha-feature
git rebase develop

# Após merge, deletar branch
git branch -d feature/nova-funcionalidade
```

### Fluxo para Multi-Equipes (Git Flow Simplificado)

```bash
# ════════════════════════════════════════════════════════════════
# 1. COMEÇAR NOVA FEATURE
# ════════════════════════════════════════════════════════════════
# Atualizar develop
git checkout develop
git pull origin develop

# Criar branch da feature
git checkout -b feature/TICKET-123-login-oauth

# ════════════════════════════════════════════════════════════════
# 2. TRABALHAR NA FEATURE
# ════════════════════════════════════════════════════════════════
# Fazer commits pequenos e frequentes
git add .
git commit -m "feat(auth): add OAuth provider configuration"

git add .
git commit -m "feat(auth): implement Google OAuth flow"

git add .
git commit -m "test(auth): add OAuth integration tests"

# ════════════════════════════════════════════════════════════════
# 3. MANTER ATUALIZADO COM DEVELOP
# ════════════════════════════════════════════════════════════════
# Periodicamente, pegar atualizações de develop
git fetch origin develop
git rebase origin/develop

# Resolver conflitos se houver
# ... editar arquivos conflitantes ...
git add .
git rebase --continue

# ════════════════════════════════════════════════════════════════
# 4. ENVIAR PARA REVIEW
# ════════════════════════════════════════════════════════════════
# Push da branch
git push -u origin feature/TICKET-123-login-oauth

# Criar Pull Request no GitHub
# → Título: feat(auth): Add OAuth login support
# → Descrição: O que foi feito, como testar
# → Reviewers: Membros do time

# ════════════════════════════════════════════════════════════════
# 5. APÓS APROVAÇÃO DO PR
# ════════════════════════════════════════════════════════════════
# Merge pelo GitHub (Squash and Merge recomendado)
# Deletar branch remota (GitHub faz automaticamente)
# Deletar branch local
git checkout develop
git pull origin develop
git branch -d feature/TICKET-123-login-oauth
```

### Conventional Commits - Boas Práticas em Mensagens

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FORMATO DE COMMIT                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   <tipo>(<escopo>): <descrição>                                             │
│                                                                             │
│   Exemplo: feat(auth): add JWT token refresh endpoint                       │
│                                                                             │
│   TIPOS:                                                                    │
│   • feat:     Nova funcionalidade                                           │
│   • fix:      Correção de bug                                               │
│   • docs:     Documentação                                                  │
│   • style:    Formatação (não afeta código)                                 │
│   • refactor: Refatoração (não adiciona feature nem corrige bug)            │
│   • test:     Testes                                                        │
│   • chore:    Manutenção (configs, deps, etc)                               │
│                                                                             │
│   ESCOPOS (exemplos):                                                       │
│   • auth, users, tickets, reports, api, db, config                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Exemplos de bons commits:**

```bash
# ✅ BOM: Específico, ação clara
git commit -m "feat(tickets): add filter by date range"
git commit -m "fix(users): prevent duplicate email registration"
git commit -m "refactor(db): optimize N+1 query in team listing"
git commit -m "test(auth): add integration tests for OAuth flow"
git commit -m "docs(api): add OpenAPI examples for ticket endpoints"
git commit -m "chore(deps): upgrade SQLAlchemy to 2.0.25"

# ❌ RUIM: Vago, não explica o quê
git commit -m "fix bug"
git commit -m "update code"
git commit -m "changes"
git commit -m "WIP"
```

### .gitignore Completo para Python/FastAPI

```gitignore
# ════════════════════════════════════════════════════════════════
# PYTHON
# ════════════════════════════════════════════════════════════════
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# ════════════════════════════════════════════════════════════════
# AMBIENTE VIRTUAL
# ════════════════════════════════════════════════════════════════
venv/
.venv/
ENV/
env/

# ════════════════════════════════════════════════════════════════
# VARIÁVEIS DE AMBIENTE (CRÍTICO!)
# ════════════════════════════════════════════════════════════════
.env
.env.local
.env.production
*.env

# ════════════════════════════════════════════════════════════════
# BANCO DE DADOS LOCAL
# ════════════════════════════════════════════════════════════════
*.db
*.sqlite
*.sqlite3

# ════════════════════════════════════════════════════════════════
# IDE
# ════════════════════════════════════════════════════════════════
.idea/
.vscode/
*.swp
*.swo
*~

# ════════════════════════════════════════════════════════════════
# TESTES
# ════════════════════════════════════════════════════════════════
.pytest_cache/
.coverage
htmlcov/
.tox/

# ════════════════════════════════════════════════════════════════
# LOGS
# ════════════════════════════════════════════════════════════════
*.log
logs/

# ════════════════════════════════════════════════════════════════
# DOCKER
# ════════════════════════════════════════════════════════════════
.docker/
```

### Pull Request Template

Crie `.github/pull_request_template.md`:

```markdown
## Descrição
<!-- O que foi feito neste PR? -->

## Tipo de mudança
- [ ] Bug fix (correção que não quebra funcionalidades existentes)
- [ ] Nova feature (mudança que adiciona funcionalidade)
- [ ] Breaking change (correção ou feature que quebra funcionalidades existentes)
- [ ] Documentação

## Como testar?
<!-- Passos para testar as mudanças -->

1.
2.
3.

## Checklist
- [ ] Código segue os padrões do projeto
- [ ] Self-review do código feito
- [ ] Comentários adicionados em código complexo
- [ ] Documentação atualizada (se necessário)
- [ ] Testes adicionados/atualizados
- [ ] Testes passando localmente
- [ ] Migrations geradas (se alterou models)

## Screenshots (se aplicável)
<!-- Adicione screenshots se houver mudanças visuais -->
```

---

## 7.6 CI/CD com GitHub Actions

### Por Que CI/CD?

**CI (Continuous Integration)**: Toda vez que código é enviado ao repositório, testes automatizados rodam para garantir que nada quebrou.

**CD (Continuous Deployment)**: Quando o código é aprovado, ele é automaticamente implantado em produção (ou staging).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FLUXO CI/CD                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Developer                                                                  │
│     │                                                                       │
│     ▼                                                                       │
│  git push ──► GitHub ──► GitHub Actions ──► Testes ──► Build ──► Deploy    │
│                            │                    │         │         │       │
│                            │                    ▼         ▼         ▼       │
│                            │               Se falhar → Notificar dev       │
│                            │               Se passar → Continuar           │
│                            │                                                │
│                            └──► lint, test, security scan                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### GitHub Actions Básico

Crie `.github/workflows/ci.yml`:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: "3.11"

jobs:
  # ════════════════════════════════════════════════════════════════
  # LINT E FORMATAÇÃO
  # ════════════════════════════════════════════════════════════════
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff black isort

      - name: Check formatting with Black
        run: black --check .

      - name: Check import sorting with isort
        run: isort --check-only .

      - name: Lint with Ruff
        run: ruff check .

  # ════════════════════════════════════════════════════════════════
  # TESTES
  # ════════════════════════════════════════════════════════════════
  test:
    name: Tests
    runs-on: ubuntu-latest
    needs: lint  # Só roda se lint passar

    services:
      # PostgreSQL para testes de integração
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov httpx

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          SECRET_KEY: test-secret-key-for-ci
          DEBUG: "false"
        run: |
          pytest tests/ -v --cov=. --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

  # ════════════════════════════════════════════════════════════════
  # SECURITY SCAN
  # ════════════════════════════════════════════════════════════════
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install bandit safety

      - name: Run Bandit (security linter)
        run: bandit -r . -x ./tests,./venv -ll

      - name: Check dependencies for vulnerabilities
        run: safety check -r requirements.txt
        continue-on-error: true  # Não falhar por vulnerabilidades conhecidas

  # ════════════════════════════════════════════════════════════════
  # BUILD DOCKER (apenas em push para main)
  # ════════════════════════════════════════════════════════════════
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [lint, test, security]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/portal-api:latest
            ${{ secrets.DOCKER_USERNAME }}/portal-api:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Deploy Automatizado

Crie `.github/workflows/deploy.yml`:

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:  # Permite deploy manual

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    environment: production  # Requer aprovação manual (configurar no GitHub)

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to server via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/portal-api
            git pull origin main
            docker compose pull
            docker compose up -d
            docker compose exec -T api alembic upgrade head
            docker compose exec -T api python -c "print('Deploy OK!')"

      - name: Notify on Slack
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: "Deploy para produção: ${{ job.status }}"
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
        if: always()
```

### Secrets Necessários

Configure em **Settings > Secrets and variables > Actions**:

| Secret | Descrição |
|--------|-----------|
| `DOCKER_USERNAME` | Usuário do Docker Hub |
| `DOCKER_PASSWORD` | Token de acesso do Docker Hub |
| `PROD_HOST` | IP/hostname do servidor de produção |
| `PROD_USER` | Usuário SSH do servidor |
| `PROD_SSH_KEY` | Chave privada SSH |
| `SLACK_WEBHOOK` | URL do webhook do Slack (opcional) |

### Badges no README

Adicione badges para mostrar status do CI:

```markdown
# Portal de Chamados

![CI](https://github.com/seu-usuario/portal-api/actions/workflows/ci.yml/badge.svg)
![Deploy](https://github.com/seu-usuario/portal-api/actions/workflows/deploy.yml/badge.svg)
[![codecov](https://codecov.io/gh/seu-usuario/portal-api/branch/main/graph/badge.svg)](https://codecov.io/gh/seu-usuario/portal-api)
```

---

## 7.7 Checklist de Deploy

### Antes de Ir para Produção

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CHECKLIST DE DEPLOY                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SEGURANÇA                                                                  │
│  [ ] SECRET_KEY é única e forte (32+ caracteres aleatórios)                 │
│  [ ] DEBUG=false em produção                                                │
│  [ ] Swagger/ReDoc desabilitados em produção                                │
│  [ ] CORS configurado com domínios específicos                              │
│  [ ] Senhas de banco não estão no código                                    │
│  [ ] .env não está no git (.gitignore)                                      │
│  [ ] Usuário do container não é root                                        │
│                                                                             │
│  BANCO DE DADOS                                                             │
│  [ ] Migrations aplicadas (alembic upgrade head)                            │
│  [ ] Backup configurado                                                     │
│  [ ] Pool de conexões dimensionado                                          │
│  [ ] Índices criados nas colunas de busca                                   │
│  [ ] pool_pre_ping=True habilitado                                          │
│                                                                             │
│  OBSERVABILIDADE                                                            │
│  [ ] Logging em JSON para produção                                          │
│  [ ] Health checks configurados (/health/ready, /health/live)               │
│  [ ] Request logging com request_id                                         │
│  [ ] Alertas configurados para erros                                        │
│                                                                             │
│  PERFORMANCE                                                                │
│  [ ] GZip middleware habilitado                                             │
│  [ ] Queries com lazy="raise" e eager loading explícito                     │
│  [ ] Paginação em endpoints de listagem                                     │
│  [ ] Timeouts configurados                                                  │
│                                                                             │
│  CONTAINER                                                                  │
│  [ ] Imagem construída e testada                                            │
│  [ ] Variáveis de ambiente documentadas                                     │
│  [ ] Healthcheck no docker-compose                                          │
│  [ ] Volumes para dados persistentes                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Exemplo de .env.production

```env
# .env.production (NUNCA commitar este arquivo!)

# Aplicação
APP_NAME=Portal de Chamados
DEBUG=false
ENVIRONMENT=production
SECRET_KEY=gere-uma-chave-aleatoria-de-32-caracteres-ou-mais

# Banco de dados
DATABASE_URL=postgresql://user:pass@db-host:5432/portal_prod
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_RECYCLE=3600

# Segurança
ALLOWED_HOSTS=["https://portal.empresa.com", "https://api.empresa.com"]
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

---

# MÓDULO 8: SEGURANÇA E AUTENTICAÇÃO

Este módulo é **CRÍTICO**. Uma aplicação sem autenticação adequada é como uma casa sem portas - qualquer um entra.

---

## 8.1 Por Que Segurança Importa

### O Custo de Ignorar Segurança

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CENÁRIOS DE FALHA DE SEGURANÇA                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SENHAS EM TEXTO PURO                                                       │
│  ❌ Hacker invade banco → Todas as senhas expostas                          │
│  ❌ Funcionário mal-intencionado vê senhas no banco                         │
│  ❌ Backup vazado → Todas as credenciais comprometidas                      │
│                                                                             │
│  SEM AUTENTICAÇÃO NOS ENDPOINTS                                             │
│  ❌ Qualquer pessoa acessa dados de outros usuários                         │
│  ❌ Bots fazem scraping de toda a base de dados                             │
│  ❌ Dados sensíveis expostos publicamente                                   │
│                                                                             │
│  JWT MAL CONFIGURADO                                                        │
│  ❌ Tokens que nunca expiram → Acesso eterno após roubo                     │
│  ❌ SECRET_KEY fraca → Tokens podem ser forjados                            │
│  ❌ Dados sensíveis no payload → Exposição de informações                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Princípios de Segurança

**1. Defense in Depth (Defesa em Profundidade)**
Múltiplas camadas de proteção. Se uma falhar, outras ainda protegem.

**2. Least Privilege (Menor Privilégio)**
Usuários só acessam o mínimo necessário para suas funções.

**3. Fail Secure (Falhar de Forma Segura)**
Em caso de erro, negar acesso. Nunca assumir que está OK.

**4. Don't Trust User Input (Nunca Confiar em Entrada do Usuário)**
Validar, sanitizar e escapar TODA entrada externa.

---

## 8.2 Hash de Senhas com Bcrypt

### Por Que Hash e Não Criptografia?

```python
# ❌ CRIPTOGRAFIA: Pode ser revertida
senha_criptografada = encrypt("minhasenha123", chave)
senha_original = decrypt(senha_criptografada, chave)  # Volta ao original!

# ✅ HASH: Via de mão única, IMPOSSÍVEL reverter
senha_hash = hash("minhasenha123")
# Não existe função para reverter hash → senha original
```

**Por que isso importa?**
- Se o banco é invadido e você usou criptografia, com a chave o hacker descriptografa tudo
- Com hash, mesmo com acesso total ao banco, senhas originais são irrecuperáveis

### Por Que Bcrypt Especificamente?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMPARAÇÃO DE ALGORITMOS DE HASH                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ALGORITMO     │ SEGURO PARA SENHAS? │ POR QUÊ?                            │
│  ──────────────┼─────────────────────┼────────────────────────────────────  │
│  MD5           │ ❌ NÃO              │ Rápido demais, rainbow tables       │
│  SHA-1         │ ❌ NÃO              │ Rápido demais, colisões             │
│  SHA-256       │ ❌ NÃO para senhas  │ Rápido demais (bilhões/seg)         │
│  bcrypt        │ ✅ SIM              │ Lento por design, salt automático   │
│  argon2        │ ✅ SIM              │ Mais novo, usa muita memória        │
│  scrypt        │ ✅ SIM              │ Similar ao argon2                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Bcrypt é "lento por design"**: Leva ~100ms para calcular um hash. Para o usuário, imperceptível. Para um atacante tentando bilhões de senhas, inviável.

### Implementação

```python
# infra/security/password.py
"""
Utilitários para hash de senha com bcrypt.

NUNCA MODIFIQUE O CUSTO (rounds) PARA MENOS DE 12 EM PRODUÇÃO!
"""
from passlib.context import CryptContext

# Configuração do bcrypt
# rounds=12 significa 2^12 = 4096 iterações (bom equilíbrio segurança/performance)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Aumentar se servidores ficarem mais rápidos
)


def hash_password(plain_password: str) -> str:
    """
    Gera hash da senha.

    O bcrypt automaticamente:
    1. Gera um salt aleatório (22 caracteres)
    2. Combina salt + senha
    3. Aplica 2^rounds iterações
    4. Retorna: $2b$12$salt...hash

    Exemplo de saída:
    $2b$12$LQv3c1yqBwdKxOPQvQVcruZa.KjNyR9.wMmJmY7.Qw1K8TA.eWzNm
    │    │  │                      │
    │    │  │                      └─ Hash final (31 chars)
    │    │  └─ Salt (22 chars)
    │    └─ Cost factor (12 rounds)
    └─ Identificador do algoritmo (bcrypt)
    """
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha corresponde ao hash.

    O bcrypt extrai o salt do hash armazenado, aplica na senha fornecida,
    e compara os resultados.

    IMPORTANTE: Esta função tem tempo constante para evitar timing attacks.
    """
    return pwd_context.verify(plain_password, hashed_password)


# Exemplo de uso:
if __name__ == "__main__":
    # Criar hash
    senha = "MinhaS3nh@Segura!"
    hash_gerado = hash_password(senha)
    print(f"Hash: {hash_gerado}")
    # $2b$12$LQv3c1yqBwdKxOPQvQVcruZa.KjNyR9.wMmJmY7.Qw1K8TA.eWzNm

    # Verificar senha correta
    print(verify_password("MinhaS3nh@Segura!", hash_gerado))  # True

    # Verificar senha errada
    print(verify_password("senhaerrada", hash_gerado))  # False
```

### Entidade User com Senha Hash

```python
# infra/entities/user.py
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from infra.configs.database import Base
from infra.security.password import hash_password, verify_password


class User(Base):
    """
    Entidade de usuário com autenticação.

    IMPORTANTE:
    - password_hash NUNCA deve ser exposto na API
    - Usar schemas Pydantic para controlar o que entra/sai
    """
    __tablename__ = "users"

    # Campos de identificação
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,  # Índice para busca rápida no login
        nullable=False
    )

    # NUNCA armazenar senha em texto puro!
    password_hash: Mapped[str] = mapped_column(
        String(255),  # Hash bcrypt tem ~60 caracteres
        nullable=False
    )

    # Campos de perfil
    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    # Controle de acesso
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        init=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        init=False
    )

    # Token para recuperação de senha
    reset_token: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        init=False,
        default=None
    )
    reset_token_expires: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
        default=None
    )

    def set_password(self, plain_password: str) -> None:
        """Define a senha (gera hash automaticamente)."""
        self.password_hash = hash_password(plain_password)

    def check_password(self, plain_password: str) -> bool:
        """Verifica se a senha está correta."""
        return verify_password(plain_password, self.password_hash)
```

### Schema para Registro (Entrada)

```python
# schemas/user_schema.py
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserCreate(BaseModel):
    """
    Schema para registro de novo usuário.

    Validações implementadas:
    - Email: Formato válido (via EmailStr)
    - Senha: Mínimo 8 chars, 1 maiúscula, 1 minúscula, 1 número, 1 especial
    - Nome: Entre 2 e 100 caracteres
    """
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    nome: str = Field(..., min_length=2, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Valida força da senha.

        Requisitos:
        - Mínimo 8 caracteres
        - Pelo menos 1 letra maiúscula
        - Pelo menos 1 letra minúscula
        - Pelo menos 1 número
        - Pelo menos 1 caractere especial (!@#$%^&*()_+-=[]{}|;:,.<>?)
        """
        if len(v) < 8:
            raise ValueError("Senha deve ter pelo menos 8 caracteres")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Senha deve conter pelo menos uma letra maiúscula")

        if not re.search(r"[a-z]", v):
            raise ValueError("Senha deve conter pelo menos uma letra minúscula")

        if not re.search(r"\d", v):
            raise ValueError("Senha deve conter pelo menos um número")

        if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", v):
            raise ValueError("Senha deve conter pelo menos um caractere especial")

        return v


class UserResponse(BaseModel):
    """
    Schema para resposta da API.

    IMPORTANTE: NUNCA incluir password_hash aqui!
    """
    id: int
    email: str
    nome: str
    is_active: bool

    model_config = {"from_attributes": True}
```

---

## 8.3 JWT - JSON Web Tokens

### O Que É JWT?

JWT é um token que contém informações codificadas (não criptografadas!) em formato JSON, assinado para garantir integridade.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ESTRUTURA DO JWT                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.                    ← HEADER         │
│  eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4ifQ.         ← PAYLOAD        │
│  SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c             ← SIGNATURE      │
│                                                                             │
│  HEADER (Base64):                                                           │
│  {                                                                          │
│    "alg": "HS256",    // Algoritmo de assinatura                           │
│    "typ": "JWT"       // Tipo do token                                      │
│  }                                                                          │
│                                                                             │
│  PAYLOAD (Base64):                                                          │
│  {                                                                          │
│    "sub": "123",      // Subject (ID do usuário)                           │
│    "exp": 1234567890, // Expiration (timestamp Unix)                        │
│    "iat": 1234567800  // Issued At (quando foi criado)                      │
│  }                                                                          │
│                                                                             │
│  SIGNATURE:                                                                 │
│  HMAC-SHA256(base64(header) + "." + base64(payload), SECRET_KEY)            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Por Que JWT ao Invés de Sessions?**

| Aspecto | Session (Server-side) | JWT (Stateless) |
|---------|----------------------|-----------------|
| Armazenamento | Servidor (memória/Redis) | Cliente (localStorage/cookie) |
| Escalabilidade | Precisa compartilhar sessões | Cada servidor valida sozinho |
| Invalidação | Fácil (deletar do servidor) | Difícil (esperar expirar) |
| Dados extras | Limitado | Pode incluir no payload |

### Implementação de JWT

```python
# infra/security/jwt.py
"""
Implementação de JWT para autenticação.

IMPORTANTE:
- SECRET_KEY deve ser forte (32+ caracteres aleatórios)
- SECRET_KEY deve estar em variável de ambiente
- NUNCA expor SECRET_KEY no código
- Tokens devem ter tempo de expiração curto (15-30 min)
"""
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt, JWTError
from pydantic import BaseModel

from infra.configs.settings import settings


# Configurações
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # 30 min
REFRESH_TOKEN_EXPIRE_DAYS = 7


class TokenPayload(BaseModel):
    """Estrutura do payload do token."""
    sub: str          # Subject (user_id como string)
    exp: datetime     # Expiration
    type: str         # "access" ou "refresh"


class TokenResponse(BaseModel):
    """Resposta com tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def create_access_token(user_id: int, extra_data: dict[str, Any] | None = None) -> str:
    """
    Cria token de acesso (curta duração).

    Usado para autenticar requisições à API.
    Expira em ACCESS_TOKEN_EXPIRE_MINUTES (padrão: 30 min).
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
        "iat": datetime.now(timezone.utc),  # Issued at
    }

    if extra_data:
        payload.update(extra_data)

    return jwt.encode(
        payload,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=ALGORITHM
    )


def create_refresh_token(user_id: int) -> str:
    """
    Cria token de refresh (longa duração).

    Usado apenas para obter novos access tokens.
    Expira em REFRESH_TOKEN_EXPIRE_DAYS (padrão: 7 dias).
    """
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh",
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=ALGORITHM
    )


def decode_token(token: str) -> TokenPayload | None:
    """
    Decodifica e valida um token.

    Retorna None se:
    - Token expirado
    - Assinatura inválida
    - Token malformado
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[ALGORITHM]
        )
        return TokenPayload(**payload)
    except JWTError:
        return None


def create_token_pair(user_id: int) -> TokenResponse:
    """Cria par de tokens (access + refresh)."""
    return TokenResponse(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id)
    )
```

### Por Que Access Token + Refresh Token?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FLUXO DE AUTENTICAÇÃO                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. LOGIN                                                                   │
│     Cliente ──► POST /auth/login {email, password}                          │
│     Servidor ◄── {access_token (30min), refresh_token (7 dias)}            │
│                                                                             │
│  2. REQUISIÇÕES NORMAIS                                                     │
│     Cliente ──► GET /api/users  (Header: Authorization: Bearer <access>)   │
│     Servidor ◄── 200 OK + dados                                            │
│                                                                             │
│  3. ACCESS TOKEN EXPIROU (após 30 min)                                      │
│     Cliente ──► GET /api/users  (Header: Authorization: Bearer <access>)   │
│     Servidor ◄── 401 Unauthorized                                          │
│                                                                             │
│  4. RENOVAR TOKEN                                                           │
│     Cliente ──► POST /auth/refresh {refresh_token}                          │
│     Servidor ◄── {access_token (novo), refresh_token (novo)}               │
│                                                                             │
│  5. REFRESH TOKEN EXPIROU (após 7 dias)                                     │
│     Cliente ──► POST /auth/refresh {refresh_token}                          │
│     Servidor ◄── 401 Unauthorized (precisa fazer login de novo)            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

Por que dois tokens?
• Access Token: Curto (30min) → Se roubado, dano limitado
• Refresh Token: Longo (7 dias) → Usuário não faz login toda hora
• Refresh Token só é enviado para /auth/refresh → Menor exposição
```

---

## 8.4 Autenticação no FastAPI

### Dependency de Autenticação

```python
# api/dependencies/auth.py
"""
Dependencies de autenticação para FastAPI.

Uso:
    @router.get("/protected")
    def protected_route(current_user: User = Depends(get_current_user)):
        return {"user": current_user.email}
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from infra.configs.connection import get_db
from infra.entities.user import User
from infra.security.jwt import decode_token


# OAuth2PasswordBearer: extrai token do header "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency que retorna o usuário autenticado.

    Fluxo:
    1. Extrai token do header Authorization
    2. Decodifica e valida o token
    3. Busca usuário no banco
    4. Retorna usuário ou 401

    Uso:
        @router.get("/me")
        def get_me(user: User = Depends(get_current_user)):
            return {"id": user.id, "email": user.email}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decodificar token
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    # Verificar se é access token (não refresh)
    if payload.type != "access":
        raise credentials_exception

    # Buscar usuário
    user_id = int(payload.sub)
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    return user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency que requer usuário superadmin.

    Uso:
        @router.delete("/users/{id}")
        def delete_user(id: int, admin: User = Depends(get_current_superuser)):
            # Só superusers chegam aqui
            ...
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada. Requer privilégios de administrador."
        )
    return current_user
```

### Routes de Autenticação

```python
# api/routes/auth.py
"""
Endpoints de autenticação.

Rotas:
- POST /auth/register: Criar nova conta
- POST /auth/login: Login (retorna tokens)
- POST /auth/refresh: Renovar access token
- POST /auth/logout: Invalidar tokens (se usando blacklist)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from infra.configs.connection import get_db
from infra.entities.user import User
from infra.security.jwt import (
    create_token_pair,
    decode_token,
    create_access_token,
    create_refresh_token,
    TokenResponse
)
from schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registra um novo usuário.

    Validações:
    - Email deve ser único
    - Senha deve atender requisitos de força
    """
    # Verificar se email já existe
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já cadastrado"
        )

    # Criar usuário
    user = User(
        email=user_data.email,
        nome=user_data.nome,
        password_hash=""  # Será setado abaixo
    )
    user.set_password(user_data.password)  # Gera hash

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Autentica usuário e retorna tokens.

    Parâmetros (form data):
    - username: Email do usuário
    - password: Senha

    Retorno:
    - access_token: Token de curta duração para API
    - refresh_token: Token de longa duração para renovação
    - token_type: "bearer"
    """
    # Buscar usuário por email
    user = db.query(User).filter(User.email == form_data.username).first()

    # Verificar credenciais
    # IMPORTANTE: Usar mesma mensagem para email errado e senha errada
    # Isso evita "user enumeration" (descobrir quais emails existem)
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar se está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta desativada"
        )

    # Gerar tokens
    return create_token_pair(user.id)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Renova o access token usando o refresh token.

    Quando usar:
    - Access token expirou (401 na API)
    - Quero renovar preventivamente
    """
    # Decodificar refresh token
    payload = decode_token(refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado"
        )

    # Verificar se é refresh token (não access)
    if payload.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    # Verificar se usuário ainda existe e está ativo
    user_id = int(payload.sub)
    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado ou inativo"
        )

    # Gerar novos tokens
    return create_token_pair(user.id)
```

### Protegendo Rotas

```python
# api/routes/users.py
"""
Exemplo de rotas protegidas por autenticação.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infra.configs.connection import get_db
from infra.entities.user import User
from api.dependencies.auth import get_current_user, get_current_superuser
from schemas.user_schema import UserResponse

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)  # ← Requer autenticação
):
    """Retorna dados do usuário logado."""
    return current_user


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← Requer autenticação
):
    """Lista todos os usuários (requer autenticação)."""
    return db.query(User).filter(User.is_active == True).all()


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_superuser)  # ← Requer ADMIN
):
    """
    Deleta um usuário.

    Requer: Usuário deve ser superadmin.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Soft delete
    user.is_active = False
    db.commit()
```

---

## 8.5 Autorização e Roles

### Sistema de Roles (Papéis)

```python
# infra/entities/role.py
from enum import Enum as PyEnum
from sqlalchemy import String, Enum, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.configs.database import Base


class RoleType(PyEnum):
    """Tipos de role disponíveis."""
    ADMIN = "admin"           # Acesso total
    MANAGER = "manager"       # Gerencia equipes
    ANALYST = "analyst"       # Visualiza relatórios
    USER = "user"             # Acesso básico
    VIEWER = "viewer"         # Apenas visualização


# Tabela de associação User <-> Role (N-N)
user_roles = Table(
    "user_roles",
    Base.metadata,
    mapped_column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    mapped_column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
)


class Role(Base):
    """Entidade de Role."""
    __tablename__ = "roles"

    name: Mapped[RoleType] = mapped_column(
        Enum(RoleType),
        unique=True,
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        init=False,
        default=None
    )

    # Relationship com users
    users: Mapped[list["User"]] = relationship(
        secondary=user_roles,
        back_populates="roles",
        lazy="raise",
        init=False,
        default_factory=list
    )
```

### Dependency de Roles

```python
# api/dependencies/roles.py
"""
Dependencies para verificação de roles/permissões.
"""
from functools import wraps
from typing import Callable

from fastapi import Depends, HTTPException, status

from infra.entities.user import User
from infra.entities.role import RoleType
from api.dependencies.auth import get_current_user


def require_roles(*required_roles: RoleType):
    """
    Dependency factory que verifica se usuário tem uma das roles necessárias.

    Uso:
        @router.get("/reports")
        def get_reports(
            user: User = Depends(require_roles(RoleType.ADMIN, RoleType.ANALYST))
        ):
            # Só ADMIN ou ANALYST chegam aqui
            ...
    """
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        # Superuser sempre passa
        if current_user.is_superuser:
            return current_user

        # Verificar se tem alguma das roles requeridas
        user_roles = {role.name for role in current_user.roles}
        if not user_roles.intersection(required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Requer uma das roles: {[r.value for r in required_roles]}"
            )

        return current_user

    return role_checker


def require_all_roles(*required_roles: RoleType):
    """
    Verifica se usuário tem TODAS as roles necessárias.

    Uso:
        @router.post("/critical-action")
        def critical(user: User = Depends(require_all_roles(RoleType.ADMIN, RoleType.MANAGER))):
            # Precisa ser ADMIN E MANAGER
            ...
    """
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.is_superuser:
            return current_user

        user_roles = {role.name for role in current_user.roles}
        if not set(required_roles).issubset(user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Requer todas as roles: {[r.value for r in required_roles]}"
            )

        return current_user

    return role_checker


# Exemplo de uso nas rotas:
"""
from api.dependencies.roles import require_roles
from infra.entities.role import RoleType

@router.get("/admin/dashboard")
def admin_dashboard(user: User = Depends(require_roles(RoleType.ADMIN))):
    return {"message": "Bem-vindo, admin!"}

@router.get("/reports")
def get_reports(user: User = Depends(require_roles(RoleType.ADMIN, RoleType.ANALYST))):
    # Admin OU Analyst podem acessar
    return {"reports": [...]}
"""
```

---

## 8.6 Recuperação de Senha

### Fluxo de Recuperação

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FLUXO DE RECUPERAÇÃO DE SENHA                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. SOLICITAR RESET                                                         │
│     Cliente ──► POST /auth/forgot-password {email}                          │
│     Servidor:                                                               │
│       - Gera token aleatório (32 chars)                                     │
│       - Salva hash do token no usuário (reset_token)                        │
│       - Define expiração (reset_token_expires)                              │
│       - Envia email com link: /reset-password?token=xyz                     │
│     Resposta ◄── 200 OK (sempre, mesmo se email não existe!)               │
│                                                                             │
│  2. RESETAR SENHA                                                           │
│     Cliente ──► POST /auth/reset-password {token, new_password}             │
│     Servidor:                                                               │
│       - Busca usuário pelo hash do token                                    │
│       - Verifica se não expirou                                             │
│       - Atualiza password_hash                                              │
│       - Limpa reset_token                                                   │
│     Resposta ◄── 200 OK ou 400 Bad Request                                 │
│                                                                             │
│  ⚠️ IMPORTANTE:                                                             │
│  - NÃO revelar se email existe (evita user enumeration)                    │
│  - Token expira em 1 hora                                                   │
│  - Token é de uso único (invalidado após uso)                               │
│  - Armazenar HASH do token, não o token em si                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Implementação

```python
# infra/security/reset_token.py
"""
Utilitários para tokens de recuperação de senha.
"""
import secrets
import hashlib
from datetime import datetime, timedelta, timezone


def generate_reset_token() -> tuple[str, str]:
    """
    Gera token de reset e seu hash.

    Retorna:
        (token_plain, token_hash)

    - token_plain: Enviado por email ao usuário
    - token_hash: Armazenado no banco (mais seguro)
    """
    # Token aleatório de 32 bytes (64 chars hex)
    token_plain = secrets.token_hex(32)

    # Hash do token para armazenar no banco
    # Se o banco for comprometido, tokens não são expostos
    token_hash = hashlib.sha256(token_plain.encode()).hexdigest()

    return token_plain, token_hash


def hash_token(token: str) -> str:
    """Gera hash de um token para comparação."""
    return hashlib.sha256(token.encode()).hexdigest()


def get_reset_token_expiry() -> datetime:
    """Retorna datetime de expiração (1 hora a partir de agora)."""
    return datetime.now(timezone.utc) + timedelta(hours=1)


def is_token_expired(expiry: datetime) -> bool:
    """Verifica se o token expirou."""
    return datetime.now(timezone.utc) > expiry
```

```python
# api/routes/auth.py (adicionar aos endpoints existentes)
from infra.security.reset_token import (
    generate_reset_token,
    hash_token,
    get_reset_token_expiry,
    is_token_expired
)


@router.post("/forgot-password")
def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Solicita recuperação de senha.

    SEMPRE retorna 200 OK, mesmo se email não existe.
    Isso evita "user enumeration" (descobrir quais emails existem).
    """
    user = db.query(User).filter(User.email == email).first()

    if user:
        # Gerar token
        token_plain, token_hash = generate_reset_token()

        # Salvar no usuário
        user.reset_token = token_hash
        user.reset_token_expires = get_reset_token_expiry()
        db.commit()

        # TODO: Enviar email
        # send_reset_email(user.email, token_plain)

        # Em desenvolvimento, logar o token (REMOVER EM PRODUÇÃO!)
        print(f"Reset token para {email}: {token_plain}")

    # Sempre retorna sucesso (não revela se email existe)
    return {
        "message": "Se o email estiver cadastrado, você receberá instruções de recuperação."
    }


@router.post("/reset-password")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """
    Reseta a senha usando o token recebido por email.
    """
    # Buscar usuário pelo hash do token
    token_hash = hash_token(token)
    user = db.query(User).filter(User.reset_token == token_hash).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado"
        )

    # Verificar expiração
    if is_token_expired(user.reset_token_expires):
        # Limpar token expirado
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expirado. Solicite um novo."
        )

    # Validar nova senha (reutilizar validador do UserCreate)
    # ... validação de força de senha ...

    # Atualizar senha
    user.set_password(new_password)

    # Invalidar token (uso único)
    user.reset_token = None
    user.reset_token_expires = None

    db.commit()

    return {"message": "Senha alterada com sucesso"}
```

---

## 8.7 Boas Práticas de Segurança

### Checklist de Segurança

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CHECKLIST DE SEGURANÇA                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SENHAS E AUTENTICAÇÃO                                                      │
│  [ ] Senhas hasheadas com bcrypt (rounds >= 12)                             │
│  [ ] Validação de força de senha (8+ chars, maiúscula, número, especial)    │
│  [ ] Limite de tentativas de login (rate limiting)                          │
│  [ ] Mensagens de erro não revelam se email existe                          │
│  [ ] Tokens JWT com expiração curta (15-30 min)                             │
│  [ ] SECRET_KEY forte (32+ chars aleatórios)                                │
│  [ ] SECRET_KEY em variável de ambiente                                     │
│                                                                             │
│  PROTEÇÃO DE DADOS                                                          │
│  [ ] HTTPS obrigatório em produção                                          │
│  [ ] Campos sensíveis nunca retornados na API (password_hash)               │
│  [ ] Dados sensíveis criptografados no banco se necessário                  │
│  [ ] Logs não contêm senhas ou tokens                                       │
│                                                                             │
│  PROTEÇÃO DE ENDPOINTS                                                      │
│  [ ] Todas as rotas sensíveis requerem autenticação                         │
│  [ ] Autorização por roles implementada                                     │
│  [ ] CORS configurado com domínios específicos                              │
│  [ ] Rate limiting em endpoints públicos                                    │
│                                                                             │
│  VALIDAÇÃO DE ENTRADA                                                       │
│  [ ] Todos os inputs validados com Pydantic                                 │
│  [ ] SQL injection prevenido (usar ORM, não SQL raw)                        │
│  [ ] XSS prevenido (escapar outputs HTML se houver)                         │
│  [ ] Path traversal prevenido (validar paths de arquivo)                    │
│                                                                             │
│  HEADERS DE SEGURANÇA                                                       │
│  [ ] X-Content-Type-Options: nosniff                                        │
│  [ ] X-Frame-Options: DENY                                                  │
│  [ ] Content-Security-Policy configurado                                    │
│  [ ] Strict-Transport-Security (HSTS) em produção                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Middleware de Segurança

```python
# api/middleware/security.py
"""
Middleware de headers de segurança.
"""
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adiciona headers de segurança em todas as respostas."""

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Prevenir MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevenir clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Habilitar XSS filter do browser
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Content Security Policy (ajustar conforme necessidade)
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response


# Em main.py:
# app.add_middleware(SecurityHeadersMiddleware)
```

### Rate Limiting

```python
# api/middleware/rate_limit.py
"""
Rate limiting para prevenir ataques de força bruta.
"""
from datetime import datetime, timedelta
from collections import defaultdict
from fastapi import HTTPException, status, Request


class RateLimiter:
    """
    Rate limiter simples em memória.

    Para produção, use Redis para compartilhar entre instâncias.
    """

    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests: dict[str, list[datetime]] = defaultdict(list)

    def is_rate_limited(self, key: str) -> bool:
        """Verifica se key está rate limited."""
        now = datetime.now()
        window_start = now - self.window

        # Limpar requests antigos
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > window_start
        ]

        # Verificar limite
        if len(self.requests[key]) >= self.max_requests:
            return True

        # Registrar nova request
        self.requests[key].append(now)
        return False


# Instância global (em produção, usar Redis)
login_limiter = RateLimiter(max_requests=5, window_seconds=60)


def check_login_rate_limit(request: Request):
    """
    Dependency para verificar rate limit em login.

    Uso:
        @router.post("/login")
        def login(
            form_data: ...,
            _: None = Depends(check_login_rate_limit)
        ):
            ...
    """
    client_ip = request.client.host

    if login_limiter.is_rate_limited(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas de login. Tente novamente em 1 minuto."
        )
```

### Exemplo Completo: Settings de Produção com Segurança

```python
# infra/configs/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, field_validator


class Settings(BaseSettings):
    """Configurações com validações de segurança."""

    # ══════════════════════════════════════════════════════════════
    # APLICAÇÃO
    # ══════════════════════════════════════════════════════════════
    APP_NAME: str = "Portal de Chamados"
    DEBUG: bool = False
    ENVIRONMENT: str = Field(
        default="development",
        pattern="^(development|staging|production)$"
    )

    # ══════════════════════════════════════════════════════════════
    # SEGURANÇA
    # ══════════════════════════════════════════════════════════════
    SECRET_KEY: SecretStr  # Obrigatório, sem default!

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=5, le=60)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, ge=1, le=30)

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # Rate limiting
    LOGIN_RATE_LIMIT_REQUESTS: int = 5
    LOGIN_RATE_LIMIT_WINDOW: int = 60  # segundos

    # ══════════════════════════════════════════════════════════════
    # VALIDAÇÕES
    # ══════════════════════════════════════════════════════════════

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: SecretStr) -> SecretStr:
        """Garante que SECRET_KEY é forte em produção."""
        secret = v.get_secret_value()

        if len(secret) < 32:
            raise ValueError("SECRET_KEY deve ter pelo menos 32 caracteres")

        return v

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, v: list[str], info) -> list[str]:
        """Não permite '*' em produção."""
        env = info.data.get("ENVIRONMENT", "development")

        if env == "production" and "*" in v:
            raise ValueError("CORS não pode usar '*' em produção")

        return v

    class Config:
        env_file = ".env"
        case_sensitive = True
```

---

# APÊNDICE: REFERÊNCIA RÁPIDA

---

## A.1 Tabela de Tipos

| Python | SQLAlchemy | PostgreSQL | SQLite |
|--------|------------|------------|--------|
| `int` | `Integer` | `INTEGER` | `INTEGER` |
| `str` | `String(n)` | `VARCHAR(n)` | `VARCHAR(n)` |
| `str` | `Text` | `TEXT` | `TEXT` |
| `bool` | `Boolean` | `BOOLEAN` | `INTEGER` |
| `float` | `Float` | `DOUBLE PRECISION` | `REAL` |
| `float` | `Double` | `DOUBLE PRECISION` | `REAL` |
| `Decimal` | `Numeric(p,s)` | `NUMERIC(p,s)` | `NUMERIC` |
| `datetime` | `DateTime(timezone=True)` | `TIMESTAMPTZ` | `DATETIME` |
| `date` | `Date` | `DATE` | `DATE` |
| `time` | `Time` | `TIME` | `TIME` |
| `dict`/`list` | `JSON` | `JSONB` | `TEXT` |
| `bytes` | `LargeBinary` | `BYTEA` | `BLOB` |
| `enum.Enum` | `Enum(MyEnum)` | `VARCHAR` | `VARCHAR` |

---

## A.2 Opções de ondelete

| Opção | Comportamento | Exemplo de Uso |
|-------|---------------|----------------|
| `RESTRICT` | Impede deletar se houver referências | Team com Users |
| `CASCADE` | Deleta relacionados junto | Ticket → Messages |
| `SET NULL` | Define FK como NULL | User → Manager opcional |
| `SET DEFAULT` | Define FK como valor default | Raro |
| `NO ACTION` | Similar a RESTRICT (default) | - |

```python
# Uso correto
user_team_id: Mapped[int] = mapped_column(
    ForeignKey("teams.id", ondelete="RESTRICT")  # ← DENTRO do ForeignKey
)
```

---

## A.3 Opções de lazy

| Valor | Comportamento | Queries | Quando Usar |
|-------|---------------|---------|-------------|
| `"select"` | Carrega sob demanda | N+1 | Evitar |
| `"joined"` | JOIN automático | 1 | Sempre precisa do relacionado |
| `"selectin"` | SELECT IN | 2 | Listas |
| `"subquery"` | Subquery | 2 | Similar ao selectin |
| `"raise"` | Erro se não carregado | 0 | Recomendado para APIs |
| `"noload"` | Nunca carrega | 0 | Nunca precisa |

---

## A.4 Snippets Prontos

### Campo PK

```python
id: Mapped[int] = mapped_column(
    Integer,
    primary_key=True,
    autoincrement=True,
    init=False
)
```

### Campo String Obrigatório

```python
nome: Mapped[str] = mapped_column(
    String(100),
    nullable=False
)
```

### Campo String Opcional

```python
descricao: Mapped[str | None] = mapped_column(
    String(500),
    nullable=True,
    init=False,
    default=None
)
```

### Campo Enum

```python
status: Mapped[MeuEnum] = mapped_column(
    Enum(MeuEnum),
    default=MeuEnum.VALOR_PADRAO,
    init=False
)
```

### Foreign Key Obrigatória

```python
team_id: Mapped[int] = mapped_column(
    ForeignKey("teams.id", ondelete="RESTRICT"),
    nullable=False
)
```

### Foreign Key Opcional

```python
manager_id: Mapped[int | None] = mapped_column(
    ForeignKey("users.id", ondelete="SET NULL"),
    nullable=True,
    init=False,
    default=None
)
```

### Relationship N-1 (Muitos para Um)

```python
team: Mapped["Team"] = relationship(
    foreign_keys=[team_id],
    back_populates="members",
    lazy="raise",
    init=False
    # NUNCA default=None!
)
```

### Relationship 1-N (Um para Muitos)

```python
members: Mapped[list["User"]] = relationship(
    foreign_keys="[User.team_id]",
    back_populates="team",
    lazy="raise",
    init=False,
    default_factory=list
)
```

### Relationship 1-1

```python
profile: Mapped["Profile | None"] = relationship(
    back_populates="user",
    lazy="raise",
    uselist=False,
    init=False
    # NUNCA default=None!
)
```

### Tabela de Associação N-N

```python
class UserProject(Base):
    """Associação N-N entre User e Project."""
    __tablename__ = "user_project"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )

    user: Mapped["User"] = relationship(back_populates="projects", lazy="raise", init=False)
    project: Mapped["Project"] = relationship(back_populates="members", lazy="raise", init=False)
```

### Query com Eager Loading

```python
from sqlalchemy.orm import joinedload, selectinload

# N-1: usar joinedload
users = session.query(User).options(
    joinedload(User.team)
).all()

# 1-N: usar selectinload
teams = session.query(Team).options(
    selectinload(Team.members)
).all()

# Encadeado
users = session.query(User).options(
    joinedload(User.team).selectinload(Team.projects)
).all()
```

### INSERT com Refresh

```python
def create(self, obj: T) -> T:
    self.session.add(obj)
    self.session.flush()
    self.session.refresh(obj)  # ← NECESSÁRIO para obter ID
    return obj
```

---

# 🎓 CONCLUSÃO

## Sua Jornada Completa

Você completou uma jornada de **5 PASSOS** para se tornar um desenvolvedor backend profissional:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SUA JORNADA COMPLETA                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ✅ PASSO 1: FUNDAÇÃO                                                       │
│     Ambiente configurado, estrutura de pastas, variáveis de ambiente,       │
│     Alembic para migrations, Git iniciado                                   │
│                                                                             │
│  ✅ PASSO 2: MODELAGEM                                                      │
│     Entidades criadas, relacionamentos configurados, lazy="raise",          │
│     ForeignKeys com ondelete, migrations aplicadas                          │
│                                                                             │
│  ✅ PASSO 3: ARQUITETURA                                                    │
│     Schemas Pydantic, Services separados, Repositories,                     │
│     Endpoints FastAPI, testes implementados                                 │
│                                                                             │
│  ✅ PASSO 4: SEGURANÇA                                                      │
│     Hash de senhas com bcrypt, JWT tokens, autenticação,                    │
│     autorização por roles, recuperação de senha                             │
│                                                                             │
│  ✅ PASSO 5: PRODUÇÃO                                                       │
│     Docker configurado, observabilidade, logging,                           │
│     Git flow, deploy checklist completo                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## O Que Você Aprendeu

### PASSO 1: Fundação
- ✅ Estrutura de pastas profissional (layered architecture)
- ✅ MappedAsDataclass e suas regras críticas
- ✅ Configuração com pydantic-settings
- ✅ Context Manager para conexões
- ✅ Alembic para migrations (nunca create_all() em produção!)

### PASSO 2: Modelagem (Banco de Dados)
- ✅ O que é ORM e quando usar
- ✅ Session e seus estados (Transient → Pending → Persistent → Detached)
- ✅ flush() vs commit() e quando usar cada um
- ✅ Foreign Keys com ondelete apropriado
- ✅ Relationships com lazy="raise" (prevenir N+1)
- ✅ Eager loading explícito (joinedload, selectinload)
- ✅ Relacionamentos N-1, 1-N, N-N
- ✅ Tabelas de associação com atributos extras
- ✅ Cascade vs ondelete

### PASSO 3: Arquitetura
- ✅ Por que NÃO usar to_dict() nos models
- ✅ Schemas Pydantic (Create, Update, Response)
- ✅ Services (camada de negócio)
- ✅ Repositories (camada de dados)
- ✅ Endpoints FastAPI
- ✅ Queries de agregação e analytics
- ✅ Índices e otimização de performance
- ✅ Testes unitários e de integração

### PASSO 4: Segurança
- ✅ Por que NUNCA armazenar senhas em texto puro
- ✅ Hash de senhas com bcrypt
- ✅ JWT tokens (access + refresh)
- ✅ Autenticação via dependencies
- ✅ Autorização por roles
- ✅ Fluxo de recuperação de senha
- ✅ Rate limiting
- ✅ Headers de segurança

### PASSO 5: Produção
- ✅ Docker e Docker Compose
- ✅ Pool de conexões para produção
- ✅ Logging estruturado (JSON)
- ✅ Prometheus + Grafana
- ✅ Health checks
- ✅ Git flow e conventional commits
- ✅ Checklist de deploy completo

## Checklist Final - Você Está Pronto?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CHECKLIST DE PRONTIDÃO                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CONHECIMENTO TÉCNICO                                                       │
│  [ ] Sei explicar por que usar MappedAsDataclass                            │
│  [ ] Sei a diferença entre flush() e commit()                               │
│  [ ] Sei configurar lazy="raise" e usar eager loading                       │
│  [ ] Sei criar schemas Pydantic adequados                                   │
│  [ ] Sei implementar autenticação JWT do zero                               │
│  [ ] Sei configurar Docker para produção                                    │
│                                                                             │
│  BOAS PRÁTICAS                                                              │
│  [ ] Uso Alembic para TODAS as mudanças de schema                           │
│  [ ] Nunca exponho password_hash na API                                     │
│  [ ] Uso variáveis de ambiente para configurações                           │
│  [ ] Escrevo testes para código crítico                                     │
│  [ ] Faço code review antes de merge                                        │
│  [ ] Sigo conventional commits                                              │
│                                                                             │
│  SEGURANÇA                                                                  │
│  [ ] Todas as senhas são hasheadas com bcrypt                               │
│  [ ] Tokens JWT têm expiração curta                                         │
│  [ ] SECRET_KEY é forte e está em variável de ambiente                      │
│  [ ] CORS está configurado corretamente                                     │
│  [ ] Rate limiting está implementado                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Recursos para Continuar Aprendendo

### Documentação Oficial
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/
- FastAPI: https://fastapi.tiangolo.com/
- Pydantic: https://docs.pydantic.dev/
- Alembic: https://alembic.sqlalchemy.org/

### Tópicos Avançados para Explorar
1. **Async SQLAlchemy**: Para alta concorrência
2. **GraphQL**: Alternativa a REST com Strawberry
3. **Event Sourcing**: Para auditoria completa
4. **CQRS**: Separar leitura e escrita
5. **Kubernetes**: Orquestração de containers
6. **Terraform**: Infrastructure as Code

---

**Este tutorial foi criado por Claude AI para o projeto de gerenciamento de tickets/projetos/relatórios.**

**Última atualização**: Janeiro 2026

**Versão**: 4.1.0 (Manual Supremo - Conhecimento Linear, FAQ Integrado aos Módulos)

