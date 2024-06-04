
# Gerenciador de Ciclo de Vida S3

O Gerenciador de Ciclo de Vida S3 é um módulo projetado para gerenciar as políticas de ciclo de vida dos buckets S3. Ele permite processar, exportar e restaurar políticas de ciclo de vida, fornecendo funcionalidades para backup e gerenciamento dessas políticas.

## Autor

- **Nome:** Rodrigo de Souza Rampazzo
- **Email:** [rosorzz@protonmail.com](mailto:rosorzz@protonmail.com)
- **GitHub:** [rzz0](https://github.com/rzz0)

## Descrição

O Gerenciador de Ciclo de Vida S3 é um pacote Python projetado para gerenciar as políticas de ciclo de vida dos buckets S3. As políticas de ciclo de vida do S3 ajudam a definir regras para a transição e expiração de objetos no S3, permitindo a otimização do armazenamento e a redução de custos. Este módulo facilita a administração dessas políticas, oferecendo funcionalidades para listar, exportar, salvar e restaurar configurações de ciclo de vida.

### Principais Funcionalidades

- **Listar Buckets:** Recupera e lista todos os buckets S3 na sua conta AWS.
- **Extrair Políticas de Ciclo de Vida:** Extrai políticas de ciclo de vida para cada bucket e as salva em um arquivo CSV.
- **Backup de Políticas:** Exporta políticas de ciclo de vida para um diretório especificado.
- **Restaurar Políticas:** Restaura políticas de ciclo de vida a partir de backups.
- **Caminhos de Log do AWS Glue:** Lista todos os caminhos temporários e caminhos de logs do Spark UI dos trabalhos do AWS Glue e gera relatórios.

## Instalação

Para instalar o Gerenciador de Ciclo de Vida S3, você pode usar o `pip`. Primeiro, certifique-se de ter o Python 3.6 ou superior instalado e execute o seguinte comando:

```bash
pip install s3_lifecycle_manager
```

Alternativamente, você pode clonar o repositório e instalar o pacote localmente:

```bash
git clone https://github.com/rzz0/s3_lifecycle_manager.git
cd s3_lifecycle_manager
pip install .
```

## Uso

As principais funcionalidades do Gerenciador de Ciclo de Vida S3 são acessíveis através da interface de linha de comando `s3_lifecycle_manager`.

### Executando o Gerenciador de Ciclo de Vida S3

Para executar o Gerenciador de Ciclo de Vida S3 com a funcionalidade de backup, use o seguinte comando:

```bash
s3_lifecycle_manager
```

Este comando processará todos os buckets S3, salvará suas políticas de ciclo de vida em um arquivo CSV e exportará as políticas de ciclo de vida atuais para arquivos de backup.

### Restaurando Políticas de Ciclo de Vida

Para restaurar políticas de ciclo de vida a partir de um arquivo de backup, você pode usar o `S3LifecycleBackupManager`:

```python
from s3_lifecycle_manager.backup_manager import S3LifecycleBackupManager

backup_manager = S3LifecycleBackupManager('./backups')
backup_manager.restore_lifecycle_policies('nome-do-seu-bucket')
```

## AWS Glue Log Paths

### Uso pela Linha de Comando

Você também pode usar o módulo pela linha de comando:

```bash
s3_lifecycle_manager --logs
```

Este comando processará os logs dos trabalhos do AWS Glue, salvará os relatórios e gerenciará as políticas de ciclo de vida do S3.

## Desenvolvimento

### Configurando o Ambiente

Configure um ambiente virtual e instale as dependências usando o `Makefile`:

```bash
make
```

### Executando Testes

Para executar os testes:

```bash
make test
```

### Limpando o Ambiente

Para limpar o ambiente:

```bash
make clean
```

### Formatando o Código

Para formatar o código:

```bash
make format
```

### Análise de Código

Para executar a análise estática do código:

```bash
make lint
```

### Verificação de Segurança

Para executar verificações de segurança:

```bash
make security
```

### Atualizando Dependências

Para atualizar as dependências:

```bash
make update
```

## Estrutura do Projeto

O projeto possui a seguinte estrutura:

- **`src/`**: Contém o código fonte do Gerenciador de Ciclo de Vida S3.
- **`tests/`**: Contém os casos de teste do projeto.
- **`README.md`**: Este arquivo.
- **`LICENSE`**: Licença MIT.
- **`setup.py`**: Script de configuração para o pacote.
- **`pyproject.toml`**: Arquivo de configuração para o sistema de build.
- **`Makefile`**: Configura um ambiente virtual e instala as dependências.
- **`pytest.ini`**: Configuração do pytest para o diretório src.

## Funcionalidades Futuras

Algumas das funcionalidades planejadas para versões futuras:

- **Suporte para Argumentos (Args):** Permitir configurar parâmetros diretamente da linha de comando para maior flexibilidade e automação.
- **Novos Módulos:**
  - **Relatórios Detalhados:** Ferramentas para gerar relatórios detalhados sobre o uso e a eficácia das políticas de ciclo de vida.
  - **Amazon S3 Storage Lens:** Recursos para configurar e obter informações do Amazon S3 Storage Lens em conjunto com o CloudWatch.
- **Integração com Outras Ferramentas da AWS:** Melhorar a integração com outros serviços da AWS, como o CloudWatch, para monitoramento e logging aprimorados.

Se você tiver sugestões ou funcionalidades específicas que gostaria de ver no Gerenciador de Ciclo de Vida S3, por favor, abra um problema em nosso repositório no GitHub.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Se você tiver alguma dúvida ou feedback, sinta-se à vontade para entrar em contato via email em [rosorzz@protonmail.com](mailto:rosorzz@protonmail.com).
