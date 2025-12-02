# CRUD Sistema de Agendamento de Consultas em Unidade Básica de Saúde
## Participantes:
- Miguel Pereira de Lemos (Líder técnico)
- Breno Luiz de Lima Cruz
- Lauan Gonçalves dos Santos
- Lucas Aprigio dos Santos
- Lucas Felipe Barreto Cavalcante
- Pablo Arthur Eustáquio de Lima
- Thiago Cardozo da Conceição
# Sistema de Agendamento de Consultas em Unidade Básica de Saúde – CRUD em Terminal
## Objetivo do Sistema

O sistema foi desenvolvido para gerenciar agendamentos de consultas em uma Unidade Básica de Saúde (UBS) utilizando um CRUD executado no terminal.
Ele resolve o problema da organização manual de pacientes, médicos e consultas, oferecendo uma solução centralizada, simples e eficiente.

### Usuários-alvo:
- Atendentes de unidades de saúde
- Funcionários administrativos
- Estudantes e desenvolvedores que desejam aprender CRUD com banco de dados

## Funcionalidades Principais
### 1. Módulo de Pacientes
- Cadastrar novos pacientes
- Listar pacientes cadastrados
- Atualizar dados de pacientes
- Remover pacientes do sistema

### 2. Módulo de Médicos
- Cadastrar médicos
- Listar médicos com IDs e nomes
- Editar informações cadastrais
- Excluir médicos registrados

### 3. Módulo de Consultas
- Criar novas consultas associadas a pacientes e médicos
- Listar todas as consultas existentes
- Atualizar informações de uma consulta
- Cancelar ou excluir consultas

### 4. Módulo de Relatórios
- Relatório de pacientes cadastrados
- Relatório de médicos
- Relatório de consultas agendadas
- Consultas por paciente
- Consultas por médico
- Dados apresentados em formato organizado para análise e conferência

### 5. Sistema de Menu
- Interface textual amigável
- Navegação fácil entre módulos
- Validação de entradas e tratamento de erros (IDs inexistentes, horários inválidos, falhas de conexão, etc.)

## Instruções de Execução

### 1. Pré-requisitos

#### Antes de executar o sistema, instale:
- Python 3.10+
- MySQL Server (ou SQLite, caso você tenha adaptado)
- Biblioteca de conexão MySQL:
``` pip install mysql-connector-python ```


