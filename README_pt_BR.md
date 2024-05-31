# S3 Lifecycle Manager

O S3 Lifecycle Manager é um módulo projetado para gerenciar as políticas de ciclo de vida dos buckets S3. Ele permite processar, exportar e restaurar políticas de ciclo de vida, oferecendo funcionalidades para backup e gerenciamento dessas políticas.

## Autor

- **Nome:** Rodrigo de Souza Rampazzo
- **Email:** [rosorzz@protonmail.com](mailto:rosorzz@protonmail.com)
- **GitHub:** [rzz0](https://github.com/rzz0)

## Descrição

O S3 Lifecycle Manager é uma ferramenta poderosa para gerenciar as políticas de ciclo de vida dos buckets S3. As políticas de ciclo de vida do S3 ajudam a definir regras para a transição e expiração de objetos no S3, permitindo a otimização do armazenamento e a redução de custos. Este módulo facilita a administração dessas políticas, oferecendo funcionalidades para listar, exportar, salvar e restaurar configurações de ciclo de vida.

### Principais Funcionalidades

- **Listar Buckets:** Lista todos os buckets S3 disponíveis na conta AWS.
- **Obter Políticas de Ciclo de Vida:** Recupera configurações de ciclo de vida para buckets especificados.
- **Exportar Políticas:** Exporta políticas de ciclo de vida para arquivos JSON, criando backups das configurações.
- **Restaurar Políticas:** Restaura políticas de ciclo de vida a partir de arquivos de backup.
- **Salvar Políticas em CSV:** Salva políticas de ciclo de vida em um arquivo CSV para análise e documentação.

## Instalação

Para instalar o S3 Lifecycle Manager, você pode usar o `pip`. Primeiro, certifique-se de ter o Python 3.6 ou superior instalado e, em seguida, execute o seguinte comando:

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

As principais funcionalidades do S3 Lifecycle Manager estão acessíveis através da interface de linha de comando `s3_lifecycle_manager`.

### Configurando Credenciais AWS

Antes de executar o S3 Lifecycle Manager, certifique-se de que suas credenciais AWS estão configuradas. Você pode usar a função `configure_aws_credentials` para solicitar as credenciais, caso ainda não estejam configuradas:

```python
from s3_lifecycle_manager.auth import configure_aws_credentials

configure_aws_credentials()
```

### Executando o S3 Lifecycle Manager

Para executar o S3 Lifecycle Manager com funcionalidade de backup, use o seguinte comando:

```bash
s3_lifecycle_manager
```

Este comando processará todos os buckets S3, salvará suas políticas de ciclo de vida em um arquivo CSV e exportará as políticas de ciclo de vida atuais para arquivos de backup.

### Restaurando Políticas de Ciclo de Vida

Para restaurar políticas de ciclo de vida a partir de um arquivo de backup, você pode usar o `S3LifecycleBackupManager`:

```python
from s3_lifecycle_manager.backup_manager import S3LifecycleBackupManager

backup_manager = S3LifecycleBackupManager('./backups')
backup_manager.restore_lifecycle_policies('your-bucket-name')
```

## Estrutura do Projeto

O projeto tem a seguinte estrutura:

- **`src/`**: Contém o código-fonte do S3 Lifecycle Manager.
- **`tests/`**: Contém os casos de teste do projeto.
- **`README.md`**: Este arquivo.
- **`setup.py`**: Script de configuração do pacote.
- **`pyproject.toml`**: Arquivo de configuração para o sistema de build.

## Funcionalidades Futuras

Algumas das funcionalidades planejadas para versões futuras:

- **Suporte a Argumentos (Args):** Permitirá a configuração de parâmetros diretamente na linha de comando para maior flexibilidade e automação.
- **Novos Módulos:**
  - **Relatórios Detalhados:** Ferramentas para gerar relatórios detalhados sobre o uso e a eficácia das políticas de ciclo de vida.
  - **Amazon S3 Storage Lens:** Funcionalidades para configurar e obter informações do Amazon S3 Storage Lens em conjunto com o CloudWatch.
- **Integração com Outras Ferramentas AWS:** Melhorar a integração com outros serviços AWS, como CloudWatch, para monitoramento e logging aprimorados.

Se você tiver sugestões ou funcionalidades específicas que gostaria de ver no S3 Lifecycle Manager, por favor, abra uma issue no nosso repositório do GitHub.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Se você tiver alguma dúvida ou feedback, sinta-se à vontade para entrar em contato via email em [rosorzz@protonmail.com](mailto:rosorzz@protonmail.com).
