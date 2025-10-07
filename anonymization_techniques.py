"""
Técnicas de Anonimização de Dados conforme LGPD
Implementa diversas técnicas para proteção de dados pessoais sensíveis
"""

import pandas as pd
import numpy as np
import hashlib
import re
from datetime import datetime, timedelta
import random
from anonymization_library import TextAnonymizer
import warnings
warnings.filterwarnings('ignore')

class DataAnonymizer:
    """
    Classe para implementar técnicas de anonimização de dados conforme LGPD
    """
    
    def __init__(self):
        self.text_anonymizer = TextAnonymizer()
    
    def k_anonymity(self, df, quasi_identifiers, k=3):
        """
        Técnica de K-Anonimidade
        Garante que cada registro seja indistinguível de pelo menos k-1 outros registros
        
        Args:
            df (pd.DataFrame): Dataset original
            quasi_identifiers (list): Lista de atributos quasi-identificadores
            k (int): Valor mínimo de k para anonimidade
            
        Returns:
            pd.DataFrame: Dataset com k-anonimidade
        """
        print(f"Implementando K-Anonimidade com k={k}")
        
        # Criar grupos baseados nos quasi-identificadores
        groups = df.groupby(quasi_identifiers)
        
        # Filtrar grupos com menos de k registros
        valid_groups = groups.filter(lambda x: len(x) >= k)
        
        print(f"Registros originais: {len(df)}")
        print(f"Registros após K-anonimidade: {len(valid_groups)}")
        print(f"Registros removidos: {len(df) - len(valid_groups)}")
        
        return valid_groups.reset_index(drop=True)
    
    def l_diversity(self, df, quasi_identifiers, sensitive_attribute, l=2):
        """
        Técnica de L-Diversidade
        Garante que cada grupo tenha pelo menos l valores distintos para o atributo sensível
        
        Args:
            df (pd.DataFrame): Dataset original
            quasi_identifiers (list): Lista de atributos quasi-identificadores
            sensitive_attribute (str): Atributo sensível
            l (int): Valor mínimo de diversidade
            
        Returns:
            pd.DataFrame: Dataset com l-diversidade
        """
        print(f"Implementando L-Diversidade com l={l}")
        
        # Criar grupos baseados nos quasi-identificadores
        groups = df.groupby(quasi_identifiers)
        
        # Filtrar grupos com pelo menos l valores distintos no atributo sensível
        valid_groups = groups.filter(lambda x: x[sensitive_attribute].nunique() >= l)
        
        print(f"Registros originais: {len(df)}")
        print(f"Registros após L-diversidade: {len(valid_groups)}")
        print(f"Registros removidos: {len(df) - len(valid_groups)}")
        
        return valid_groups.reset_index(drop=True)
    
    def generalization(self, df, columns_to_generalize):
        """
        Técnica de Generalização
        Substitui valores específicos por categorias mais amplas
        
        Args:
            df (pd.DataFrame): Dataset original
            columns_to_generalize (dict): Dicionário com colunas e regras de generalização
            
        Returns:
            pd.DataFrame: Dataset generalizado
        """
        print("Implementando Generalização")
        
        df_generalized = df.copy()
        
        for column, rules in columns_to_generalize.items():
            if column in df_generalized.columns:
                if rules['type'] == 'age_ranges':
                    # Generalizar idade em faixas etárias
                    df_generalized[column] = pd.cut(
                        df_generalized[column], 
                        bins=[0, 25, 35, 45, 55, 65, 100], 
                        labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
                    )
                
                elif rules['type'] == 'salary_ranges':
                    # Generalizar salário em faixas
                    df_generalized[column] = pd.cut(
                        df_generalized[column], 
                        bins=[0, 5000, 10000, 20000, 50000, float('inf')], 
                        labels=['Baixo', 'Médio-Baixo', 'Médio', 'Alto', 'Muito Alto']
                    )
                
                elif rules['type'] == 'location_generalization':
                    # Generalizar localização (manter apenas estado)
                    if column == 'cidade':
                        df_generalized[column] = 'Cidade Anonimizada'
                    elif column == 'endereco':
                        df_generalized[column] = 'Endereço Anonimizado'
        
        print("Generalização aplicada nas seguintes colunas:")
        for col in columns_to_generalize.keys():
            print(f"- {col}")
        
        return df_generalized
    
    def suppression(self, df, columns_to_suppress):
        """
        Técnica de Supressão
        Remove completamente atributos identificadores diretos
        
        Args:
            df (pd.DataFrame): Dataset original
            columns_to_suppress (list): Lista de colunas para suprimir
            
        Returns:
            pd.DataFrame: Dataset com supressão aplicada
        """
        print("Implementando Supressão")
        
        df_suppressed = df.copy()
        
        # Remover colunas identificadoras diretas
        columns_removed = []
        for col in columns_to_suppress:
            if col in df_suppressed.columns:
                df_suppressed = df_suppressed.drop(columns=[col])
                columns_removed.append(col)
        
        print(f"Colunas suprimidas: {columns_removed}")
        print(f"Colunas restantes: {len(df_suppressed.columns)}")
        
        return df_suppressed
    
    def pseudonymization(self, df, columns_to_pseudonymize):
        """
        Técnica de Pseudoanonimização
        Substitui identificadores por pseudônimos usando hash
        
        Args:
            df (pd.DataFrame): Dataset original
            columns_to_pseudonymize (list): Lista de colunas para pseudoanonimizar
            
        Returns:
            pd.DataFrame: Dataset pseudoanonimizado
        """
        print("Implementando Pseudoanonimização")
        
        df_pseudonymized = df.copy()
        
        for column in columns_to_pseudonymize:
            if column in df_pseudonymized.columns:
                # Usar hash SHA-256 para criar pseudônimos
                df_pseudonymized[column] = df_pseudonymized[column].apply(
                    lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
                )
        
        print(f"Colunas pseudoanonimizadas: {columns_to_pseudonymize}")
        
        return df_pseudonymized
    
    def noise_addition(self, df, columns_to_add_noise, noise_level=0.1):
        """
        Técnica de Adição de Ruído
        Adiciona ruído aleatório aos dados numéricos
        
        Args:
            df (pd.DataFrame): Dataset original
            columns_to_add_noise (list): Lista de colunas numéricas
            noise_level (float): Nível de ruído (0.1 = 10%)
            
        Returns:
            pd.DataFrame: Dataset com ruído adicionado
        """
        print(f"Implementando Adição de Ruído (nível: {noise_level*100}%)")
        
        df_noisy = df.copy()
        
        for column in columns_to_add_noise:
            if column in df_noisy.columns and df_noisy[column].dtype in ['int64', 'float64']:
                # Calcular desvio padrão
                std_dev = df_noisy[column].std()
                
                # Adicionar ruído gaussiano
                noise = np.random.normal(0, std_dev * noise_level, len(df_noisy))
                df_noisy[column] = df_noisy[column] + noise
                
                # Arredondar para manter formato original
                if df_noisy[column].dtype == 'int64':
                    df_noisy[column] = df_noisy[column].round().astype(int)
                else:
                    df_noisy[column] = df_noisy[column].round(2)
        
        print(f"Ruído adicionado nas colunas: {columns_to_add_noise}")
        
        return df_noisy
    
    def data_masking(self, df, columns_to_mask):
        """
        Técnica de Mascaramento de Dados
        Substitui parte dos dados por caracteres de mascaramento
        
        Args:
            df (pd.DataFrame): Dataset original
            columns_to_mask (dict): Dicionário com colunas e regras de mascaramento
            
        Returns:
            pd.DataFrame: Dataset com mascaramento aplicado
        """
        print("Implementando Mascaramento de Dados")
        
        df_masked = df.copy()
        
        for column, mask_rules in columns_to_mask.items():
            if column in df_masked.columns:
                if mask_rules['type'] == 'email':
                    # Mascarar email: manter primeiro caractere e domínio
                    df_masked[column] = df_masked[column].apply(
                        lambda x: re.sub(r'(.{1}).*@', r'\1***@', str(x))
                    )
                
                elif mask_rules['type'] == 'phone':
                    # Mascarar telefone: manter apenas últimos 4 dígitos
                    df_masked[column] = df_masked[column].apply(
                        lambda x: '***-****-' + str(x)[-4:] if len(str(x)) >= 4 else str(x)
                    )
                
                elif mask_rules['type'] == 'cpf':
                    # Mascarar CPF: manter apenas primeiros 3 e últimos 2 dígitos
                    df_masked[column] = df_masked[column].apply(
                        lambda x: str(x)[:3] + '***.***-' + str(x)[-2:] if len(str(x)) >= 5 else str(x)
                    )
        
        print("Mascaramento aplicado nas seguintes colunas:")
        for col, rules in columns_to_mask.items():
            print(f"- {col}: {rules['type']}")
        
        return df_masked
    
    def differential_privacy(self, df, columns_to_privatize, epsilon=1.0):
        """
        Técnica de Privacidade Diferencial
        Adiciona ruído calibrado para garantir privacidade diferencial
        
        Args:
            df (pd.DataFrame): Dataset original
            columns_to_privatize (list): Lista de colunas numéricas
            epsilon (float): Parâmetro de privacidade (menor = mais privacidade)
            
        Returns:
            pd.DataFrame: Dataset com privacidade diferencial
        """
        print(f"Implementando Privacidade Diferencial (ε={epsilon})")
        
        df_private = df.copy()
        
        for column in columns_to_privatize:
            if column in df_private.columns and df_private[column].dtype in ['int64', 'float64']:
                # Calcular sensibilidade (assumindo sensibilidade 1)
                sensitivity = 1.0
                
                # Calcular escala do ruído Laplace
                scale = sensitivity / epsilon
                
                # Adicionar ruído Laplace
                noise = np.random.laplace(0, scale, len(df_private))
                df_private[column] = df_private[column] + noise
                
                # Arredondar para manter formato original
                if df_private[column].dtype == 'int64':
                    df_private[column] = df_private[column].round().astype(int)
                else:
                    df_private[column] = df_private[column].round(2)
        
        print(f"Privacidade diferencial aplicada nas colunas: {columns_to_privatize}")
        
        return df_private

def demonstrate_anonymization_techniques():
    """
    Demonstra as principais técnicas de anonimização
    """
    print("=== DEMONSTRAÇÃO DE TÉCNICAS DE ANONIMIZAÇÃO ===\n")
    
    # Carregar dados de exemplo
    try:
        df = pd.read_csv('dados_sensiveis_original.csv')
        print(f"Dataset carregado: {len(df)} registros, {len(df.columns)} colunas\n")
    except FileNotFoundError:
        print("Arquivo de dados não encontrado. Execute primeiro o sample_data_generator.py")
        return
    
    # Inicializar anonimizador
    anonymizer = DataAnonymizer()
    
    # 1. K-Anonimidade
    print("1. K-ANONIMIDADE")
    print("-" * 50)
    quasi_identifiers = ['idade', 'cidade', 'estado']
    df_k_anon = anonymizer.k_anonymity(df, quasi_identifiers, k=3)
    df_k_anon.to_csv('dados_k_anonimidade.csv', index=False, encoding='utf-8')
    print("Arquivo salvo: dados_k_anonimidade.csv\n")
    
    # 2. Generalização
    print("2. GENERALIZAÇÃO")
    print("-" * 50)
    generalization_rules = {
        'idade': {'type': 'age_ranges'},
        'salario': {'type': 'salary_ranges'},
        'cidade': {'type': 'location_generalization'},
        'endereco': {'type': 'location_generalization'}
    }
    df_generalized = anonymizer.generalization(df, generalization_rules)
    df_generalized.to_csv('dados_generalizados.csv', index=False, encoding='utf-8')
    print("Arquivo salvo: dados_generalizados.csv\n")
    
    # 3. Supressão
    print("3. SUPRESSÃO")
    print("-" * 50)
    columns_to_suppress = ['nome_completo', 'cpf', 'rg', 'numero_cartao']
    df_suppressed = anonymizer.suppression(df, columns_to_suppress)
    df_suppressed.to_csv('dados_suprimidos.csv', index=False, encoding='utf-8')
    print("Arquivo salvo: dados_suprimidos.csv\n")
    
    # 4. Pseudoanonimização
    print("4. PSEUDOANONIMIZAÇÃO")
    print("-" * 50)
    columns_to_pseudonymize = ['email', 'telefone']
    df_pseudonymized = anonymizer.pseudonymization(df, columns_to_pseudonymize)
    df_pseudonymized.to_csv('dados_pseudoanonimizados.csv', index=False, encoding='utf-8')
    print("Arquivo salvo: dados_pseudoanonimizados.csv\n")
    
    # 5. Mascaramento
    print("5. MASCARAMENTO")
    print("-" * 50)
    masking_rules = {
        'email': {'type': 'email'},
        'telefone': {'type': 'phone'},
        'cpf': {'type': 'cpf'}
    }
    df_masked = anonymizer.data_masking(df, masking_rules)
    df_masked.to_csv('dados_mascarados.csv', index=False, encoding='utf-8')
    print("Arquivo salvo: dados_mascarados.csv\n")
    
    # 6. Adição de Ruído
    print("6. ADIÇÃO DE RUÍDO")
    print("-" * 50)
    columns_to_add_noise = ['salario', 'renda_familiar', 'score_credito']
    df_noisy = anonymizer.noise_addition(df, columns_to_add_noise, noise_level=0.05)
    df_noisy.to_csv('dados_com_ruido.csv', index=False, encoding='utf-8')
    print("Arquivo salvo: dados_com_ruido.csv\n")
    
    # 7. Privacidade Diferencial
    print("7. PRIVACIDADE DIFERENCIAL")
    print("-" * 50)
    columns_to_privatize = ['salario', 'renda_familiar']
    df_differential = anonymizer.differential_privacy(df, columns_to_privatize, epsilon=1.0)
    df_differential.to_csv('dados_privacidade_diferencial.csv', index=False, encoding='utf-8')
    print("Arquivo salvo: dados_privacidade_diferencial.csv\n")
    
    print("=== DEMONSTRAÇÃO CONCLUÍDA ===")
    print("Todos os arquivos foram salvos com sucesso!")

if __name__ == "__main__":
    demonstrate_anonymization_techniques()
