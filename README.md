# CRUD Sistema de Agendamento de Consultas em Unidade Básica de Saúde
## Participantes:
- Miguel Pereira de Lemos (Líder técnico)
- Breno Luiz de Lima Cruz
- Lauan Gonçalves dos Santos
- Lucas Aprigio dos Santos
- Lucas Felipe Barreto Cavalcante
- Pablo Arthur Eustáquio de Lima
- Thiago Cardozo da Conceição

# **Sistema de Agendamento de Consultas -- CRUD em Terminal**

## 📌 Objetivo do Sistema

O sistema foi desenvolvido para **gerenciar agendamentos de consultas em
uma Unidade Básica de Saúde (UBS)** utilizando um CRUD executado no
terminal.
Ele resolve o problema da **organização manual de pacientes, médicos e
consultas**, oferecendo uma solução centralizada, simples e eficiente.

**Usuários-alvo:**
- Atendentes de unidades de saúde
- Funcionários administrativos
- Estudantes e desenvolvedores que desejam aprender CRUD com banco de
dados

------------------------------------------------------------------------

## 📦 Funcionalidades Principais

### **1. Módulo de Pacientes**

-   Cadastrar novos pacientes
-   Listar pacientes cadastrados
-   Atualizar dados de pacientes
-   Remover pacientes do sistema

------------------------------------------------------------------------

### **2. Módulo de Médicos**

-   Cadastrar médicos
-   Listar médicos com IDs e nomes
-   Editar informações cadastrais
-   Excluir médicos registrados

------------------------------------------------------------------------

### **3. Módulo de Consultas**

-   Criar novas consultas associadas a pacientes e médicos
-   Listar todas as consultas existentes
-   Atualizar informações de uma consulta
-   Cancelar ou excluir consultas

------------------------------------------------------------------------

### **4. Módulo de Relatórios**

-   Relatório de pacientes cadastrados
-   Relatório de médicos
-   Relatório de consultas agendadas
-   Consultas por paciente
-   Consultas por médico
-   Dados apresentados em formato organizado para análise e conferência

------------------------------------------------------------------------

### **5. Sistema de Menu**

-   Interface textual amigável
-   Navegação fácil entre módulos
-   Validação de entradas e tratamento de erros (IDs inexistentes, rários inválidos, falhas de conexão, etc.)

------------------------------------------------------------------------

## 🚀 Instruções de Execução

### **1. Pré-requisitos**

Antes de executar o sistema, instale: 
- **Python 3.10+**
- **MySQLServer** (ou SQLite, caso você tenha adaptado)
- Biblioteca de conexão MySQL:
- `bash   pip install mysql-connector-python`

------------------------------------------------------------------------

### **2. Configurando o Banco de Dados**

1.  No MySQL, crie o banco de dados:

    ``` sql
    CREATE DATABASE banco;
    ```

2.  Importe as tabelas necessárias (pacientes, médicos, consultas).

3.  Configure o arquivo `db.py`:

    ``` python
    def obter_conexao():
        return mysql.connector.connect(
            host="localhost",
            user="seu_usuario",
            password="sua_senha",
            database="banco"
        )
    ```

------------------------------------------------------------------------

### **3. Executando o Sistema**

1.  Abra o terminal e navegue até a pasta do projeto:

    ``` bash
    cd nome_da_pasta_do_projeto
    ```

2.  Execute o arquivo principal:

    ``` bash
    python menu.py
    ```

3.  Utilize o menu para acessar:

    -   CRUD de Pacientes
    -   CRUD de Médicos
    -   CRUD de Consultas
    -   Relatórios
    -   Sair

------------------------------------------------------------------------

### **4. Observações**

-   O sistema roda totalmente no terminal, sem interface gráfica.
-   Há tratamento de erros para situações comuns como:
    -   Conexão falha ao banco
    -   IDs não encontrados
    -   Formatos de horário inválidos

## 📚 Detalhamento de Funções Principais

### **Módulo: CRUDPacientes**

**`cadastrar_paciente()`**
- Realiza o cadastro completo de um novo paciente no sistema
- Valida dados obrigatórios: nome (mín. 3 caracteres), CPF (11 dígitos), data de nascimento, telefone (10-11 dígitos), endereço e CEP (8 dígitos)
- Insere os dados validados na tabela `pacientes` do banco de dados

**`ler_paciente()`**
- Lista todos os pacientes cadastrados no sistema
- Exibe informações em formato tabular: ID, nome, CPF, nascimento, telefone, endereço e CEP
- Formata datas para visualização brasileira (DD/MM/AAAA)

**`atualizar_paciente()`**
- Permite atualizar dados de um paciente específico buscando pelo CPF
- Oferece menu para escolher qual campo alterar: nome, nascimento, telefone, endereço ou CEP
- Valida a existência do paciente antes de realizar a atualização

**`deletar_paciente()`**
- Remove um paciente do sistema através do CPF
- Verifica se o paciente existe antes de executar a exclusão
- Exibe a lista de pacientes antes da remoção para facilitar a seleção

---

### **Módulo: CRUDMedicos**

**`criar_medico()`**
- Cadastra um novo médico no sistema
- Valida CRM (mínimo 4 números), telefone (apenas dígitos) e horários de atendimento (formato HH:MM)
- Armazena dados completos: nome, CRM, especialidade, telefone, horário de início e fim do expediente

**`ler_medicos()`**
- Exibe lista completa de médicos cadastrados
- Apresenta: ID, nome, CRM, especialidade, telefone e horários de atendimento
- Retorna a lista para uso em outras funções do sistema

**`atualizar_medico()`**
- Permite editar informações de um médico existente através do ID
- Menu interativo para atualizar campos individuais: nome, CRM, especialidade, telefone ou horários
- Aplica validações específicas para cada tipo de dado durante a atualização

**`deletar_medico()`**
- Exclui um médico do sistema pelo ID
- Exibe lista de médicos antes da exclusão para confirmar a seleção

---

### **Módulo: CRUDConsultas**

**`criar_consulta()`**
- Agenda uma nova consulta vinculando paciente e médico
- Valida a existência do paciente e médico no banco de dados
- Verifica disponibilidade de horário do médico e impede agendamentos no passado
- Define status inicial como "AGENDADO" e permite adicionar observações

**`listar_consulta()`**
- Exibe todas as consultas cadastradas ordenadas por data/hora
- Apresenta: ID da consulta, data/hora formatada, nome do paciente, nome do médico e status
- Usa JOIN entre tabelas para buscar nomes completos de pacientes e médicos

**`atualizar_consulta()`**
- Permite modificar três aspectos de uma consulta existente:
  - Status (Agendada, Concluída, Cancelada, Falta)
  - Data e horário (com nova verificação de conflitos)
  - Observações
- Exibe dados atuais antes da alteração e valida disponibilidade ao reagendar

**`deletar_consulta()`**
- Remove uma consulta do sistema através do ID
- Validação simples e direta para exclusão definitiva

**`verificar_conflito_horario()`**
- Verifica se existe outra consulta agendada para o mesmo médico no horário solicitado
- Considera consultas existentes ao permitir reagendamento (exclui a própria consulta da verificação)
- Previne dupla marcação e conflitos de agenda

---

### **Módulo: Relatorios**

**`relatorioMedicos()`**
- Gera relatório detalhado de todas as consultas de um médico específico
- Lista médicos disponíveis e solicita seleção por ID
- Exibe para cada consulta: dados do paciente, dados do médico, ID da consulta, data/hora, status e observações
- Trata casos de registros não encontrados

**`relatorioData()`**
- Cria relatório de todas as consultas realizadas em uma data específica
- Exibe datas disponíveis e solicita seleção no formato AAAA-MM-DD
- Apresenta informações completas de cada consulta: paciente, médico, status e observações
- Útil para análise de movimento diário da unidade

**`menu_relatorio()`**
- Interface principal do módulo de relatórios
- Oferece navegação entre os tipos de relatório disponíveis
- Inclui opção de retorno ao menu principal e saída do sistema
