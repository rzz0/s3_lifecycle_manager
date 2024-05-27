"""
Main function to run the S3 bucket lifecycle manager.

Author: Rodrigo de Souza Rampazzo
E-mail: rosorzz@protonmail.com
GitHub: rzz0
url: https://github.com/rzz0/s3_lifecycle_manager
"""

from .manager import S3LifecycleManager
from .backup_manager import S3LifecycleBackupManager
from .logger import configure_logging


def main():
    """
    Main function to run the S3 bucket lifecycle manager with backup functionality.
    """
    configure_logging()

    # Diretório onde os backups serão armazenados
    backup_dir = './backups'
    manager = S3LifecycleManager()
    backup_manager = S3LifecycleBackupManager(backup_dir)

    # Processar os buckets e gerar backup das políticas de ciclo de vida
    manager.process_buckets()
    manager.save_policies_csv('lifecycle_buckets.csv')

    # Exportar as regras de ciclo de vida atuais
    bucket_names = [bucket['Name'] for bucket in manager.list_buckets()]
    backup_manager.export_lifecycle_policies(bucket_names)

    # Opcional: Restaurar as regras de ciclo de vida de um bucket específico
    # backup_manager.restore_lifecycle_policies('nome-do-bucket')


if __name__ == "__main__":
    main()
