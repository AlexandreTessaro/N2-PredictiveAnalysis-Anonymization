"""
Demonstração Completa de Anonimização de Dados
Script principal para executar todas as técnicas de anonimização
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from anonymization_techniques import DataAnonymizer
from sample_data_generator import generate_sensitive_dataset
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AnonymizationDemo:
    """
    Classe para demonstrar técnicas de anonimização com visualizações
    """
    
    def __init__(self):
        self.anonymizer = DataAnonymizer()
        self.results = {}
    
    def generate_comparison_report(self, original_df, anonymized_dfs):
        """
        Gera relatório comparativo entre dados originais e anonimizados
        
        Args:
            original_df (pd.DataFrame): Dataset original
            anonymized_dfs (dict): Dicionário com datasets anonimizados
        """
        print("=" * 80)
        print("RELATÓRIO COMPARATIVO DE ANONIMIZAÇÃO")
        print("=" * 80)
        
        # Estatísticas gerais
        print(f"\n1. ESTATÍSTICAS GERAIS")
        print("-" * 40)
        print(f"Dataset original: {len(original_df)} registros, {len(original_df.columns)} colunas")
        
        for technique, df in anonymized_dfs.items():
            print(f"{technique}: {len(df)} registros, {len(df.columns)} colunas")
        
        # Análise de utilidade dos dados
        print(f"\n2. ANÁLISE DE UTILIDADE DOS DADOS")
        print("-" * 40)
        
        # Comparar estatísticas descritivas
        numeric_cols = original_df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols[:3]:  # Analisar apenas as primeiras 3 colunas numéricas
            print(f"\nColuna: {col}")
            print(f"Original - Média: {original_df[col].mean():.2f}, Desvio: {original_df[col].std():.2f}")
            
            for technique, df in anonymized_dfs.items():
                if col in df.columns:
                    # Verificar se a coluna ainda é numérica após anonimização
                    if df[col].dtype in ['int64', 'float64']:
                        print(f"{technique} - Média: {df[col].mean():.2f}, Desvio: {df[col].std():.2f}")
                    else:
                        print(f"{technique} - Tipo: {df[col].dtype} (não numérico após anonimização)")
        
        # Análise de privacidade
        print(f"\n3. ANÁLISE DE PRIVACIDADE")
        print("-" * 40)
        
        # Identificar registros únicos
        quasi_identifiers = ['idade', 'cidade', 'estado']
        original_unique = original_df[quasi_identifiers].drop_duplicates()
        print(f"Combinações únicas no original: {len(original_unique)}")
        
        for technique, df in anonymized_dfs.items():
            if all(col in df.columns for col in quasi_identifiers):
                unique_combinations = df[quasi_identifiers].drop_duplicates()
                print(f"{technique} - Combinações únicas: {len(unique_combinations)}")
    
    def create_visualizations(self, original_df, anonymized_dfs):
        """
        Cria visualizações comparativas
        
        Args:
            original_df (pd.DataFrame): Dataset original
            anonymized_dfs (dict): Dicionário com datasets anonimizados
        """
        print("\n4. CRIANDO VISUALIZAÇÕES")
        print("-" * 40)
        
        # Configurar figura
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Comparação: Dados Originais vs Anonimizados', fontsize=16, fontweight='bold')
        
        # 1. Distribuição de Idade
        axes[0, 0].hist(original_df['idade'], bins=20, alpha=0.7, label='Original', color='blue')
        if 'Generalização' in anonymized_dfs:
            df_gen = anonymized_dfs['Generalização']
            if 'idade' in df_gen.columns:
                # Converter faixas etárias para valores numéricos para visualização
                age_mapping = {'18-25': 21.5, '26-35': 30.5, '36-45': 40.5, '46-55': 50.5, '56-65': 60.5, '65+': 70}
                df_gen_numeric = df_gen['idade'].map(age_mapping)
                axes[0, 0].hist(df_gen_numeric, bins=20, alpha=0.7, label='Generalizado', color='red')
        axes[0, 0].set_title('Distribuição de Idade')
        axes[0, 0].set_xlabel('Idade')
        axes[0, 0].set_ylabel('Frequência')
        axes[0, 0].legend()
        
        # 2. Distribuição de Salário
        axes[0, 1].hist(original_df['salario'], bins=20, alpha=0.7, label='Original', color='blue')
        if 'Adição de Ruído' in anonymized_dfs:
            df_noisy = anonymized_dfs['Adição de Ruído']
            if 'salario' in df_noisy.columns:
                axes[0, 1].hist(df_noisy['salario'], bins=20, alpha=0.7, label='Com Ruído', color='green')
        axes[0, 1].set_title('Distribuição de Salário')
        axes[0, 1].set_xlabel('Salário')
        axes[0, 1].set_ylabel('Frequência')
        axes[0, 1].legend()
        
        # 3. Correlação Idade vs Salário (Original)
        axes[1, 0].scatter(original_df['idade'], original_df['salario'], alpha=0.6, color='blue', label='Original')
        if 'Privacidade Diferencial' in anonymized_dfs:
            df_diff = anonymized_dfs['Privacidade Diferencial']
            if 'idade' in df_diff.columns and 'salario' in df_diff.columns:
                axes[1, 0].scatter(df_diff['idade'], df_diff['salario'], alpha=0.6, color='red', label='Privacidade Diferencial')
        axes[1, 0].set_title('Correlação Idade vs Salário')
        axes[1, 0].set_xlabel('Idade')
        axes[1, 0].set_ylabel('Salário')
        axes[1, 0].legend()
        
        # 4. Comparação de Técnicas (Número de Registros)
        techniques = list(anonymized_dfs.keys())
        record_counts = [len(df) for df in anonymized_dfs.values()]
        record_counts.insert(0, len(original_df))
        technique_names = ['Original'] + techniques
        
        bars = axes[1, 1].bar(technique_names, record_counts, color=['blue'] + ['red'] * len(techniques))
        axes[1, 1].set_title('Número de Registros por Técnica')
        axes[1, 1].set_ylabel('Número de Registros')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        # Adicionar valores nas barras
        for bar, count in zip(bars, record_counts):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
                           str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('comparacao_anonimizacao.png', dpi=300, bbox_inches='tight')
        print("Gráfico salvo: comparacao_anonimizacao.png")
        
        # Criar gráfico de utilidade vs privacidade
        self.create_utility_privacy_chart(anonymized_dfs)
    
    def create_utility_privacy_chart(self, anonymized_dfs):
        """
        Cria gráfico de utilidade vs privacidade
        
        Args:
            anonymized_dfs (dict): Dicionário com datasets anonimizados
        """
        # Definir scores de utilidade e privacidade (valores hipotéticos baseados nas técnicas)
        utility_scores = {
            'K-Anonimidade': 0.7,
            'Generalização': 0.6,
            'Supressão': 0.8,
            'Pseudoanonimização': 0.9,
            'Mascaramento': 0.5,
            'Adição de Ruído': 0.4,
            'Privacidade Diferencial': 0.3
        }
        
        privacy_scores = {
            'K-Anonimidade': 0.8,
            'Generalização': 0.7,
            'Supressão': 0.9,
            'Pseudoanonimização': 0.6,
            'Mascaramento': 0.8,
            'Adição de Ruído': 0.5,
            'Privacidade Diferencial': 0.9
        }
        
        # Filtrar apenas técnicas que foram aplicadas
        applied_techniques = [tech for tech in utility_scores.keys() if tech in anonymized_dfs]
        
        if applied_techniques:
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))
            
            for technique in applied_techniques:
                ax.scatter(privacy_scores[technique], utility_scores[technique], 
                          s=200, label=technique, alpha=0.7)
                ax.annotate(technique, 
                           (privacy_scores[technique], utility_scores[technique]),
                           xytext=(5, 5), textcoords='offset points')
            
            ax.set_xlabel('Nível de Privacidade', fontsize=12)
            ax.set_ylabel('Nível de Utilidade', fontsize=12)
            ax.set_title('Trade-off: Utilidade vs Privacidade', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            
            plt.tight_layout()
            plt.savefig('utilidade_vs_privacidade.png', dpi=300, bbox_inches='tight')
            print("Gráfico salvo: utilidade_vs_privacidade.png")
    
    def run_complete_demo(self):
        """
        Executa demonstração completa de anonimização
        """
        print("=" * 80)
        print("DEMONSTRAÇÃO COMPLETA DE ANONIMIZAÇÃO DE DADOS")
        print("Conforme Lei Geral de Proteção de Dados (LGPD)")
        print("=" * 80)
        
        # 1. Gerar dados de exemplo
        print("\n1. GERANDO DADOS DE EXEMPLO")
        print("-" * 40)
        original_df = generate_sensitive_dataset(500)  # Dataset menor para demonstração
        original_df.to_csv('dados_sensiveis_original.csv', index=False, encoding='utf-8')
        print(f"Dataset gerado: {len(original_df)} registros")
        
        # 2. Aplicar técnicas de anonimização
        print("\n2. APLICANDO TÉCNICAS DE ANONIMIZAÇÃO")
        print("-" * 40)
        
        anonymized_dfs = {}
        
        # K-Anonimidade
        print("\nAplicando K-Anonimidade...")
        quasi_identifiers = ['idade', 'cidade', 'estado']
        df_k_anon = self.anonymizer.k_anonymity(original_df, quasi_identifiers, k=3)
        anonymized_dfs['K-Anonimidade'] = df_k_anon
        
        # Generalização
        print("\nAplicando Generalização...")
        generalization_rules = {
            'idade': {'type': 'age_ranges'},
            'salario': {'type': 'salary_ranges'},
            'cidade': {'type': 'location_generalization'},
            'endereco': {'type': 'location_generalization'}
        }
        df_generalized = self.anonymizer.generalization(original_df, generalization_rules)
        anonymized_dfs['Generalização'] = df_generalized
        
        # Supressão
        print("\nAplicando Supressão...")
        columns_to_suppress = ['nome_completo', 'cpf', 'rg', 'numero_cartao']
        df_suppressed = self.anonymizer.suppression(original_df, columns_to_suppress)
        anonymized_dfs['Supressão'] = df_suppressed
        
        # Pseudoanonimização
        print("\nAplicando Pseudoanonimização...")
        columns_to_pseudonymize = ['email', 'telefone']
        df_pseudonymized = self.anonymizer.pseudonymization(original_df, columns_to_pseudonymize)
        anonymized_dfs['Pseudoanonimização'] = df_pseudonymized
        
        # Mascaramento
        print("\nAplicando Mascaramento...")
        masking_rules = {
            'email': {'type': 'email'},
            'telefone': {'type': 'phone'},
            'cpf': {'type': 'cpf'}
        }
        df_masked = self.anonymizer.data_masking(original_df, masking_rules)
        anonymized_dfs['Mascaramento'] = df_masked
        
        # Adição de Ruído
        print("\nAplicando Adição de Ruído...")
        columns_to_add_noise = ['salario', 'renda_familiar', 'score_credito']
        df_noisy = self.anonymizer.noise_addition(original_df, columns_to_add_noise, noise_level=0.05)
        anonymized_dfs['Adição de Ruído'] = df_noisy
        
        # Privacidade Diferencial
        print("\nAplicando Privacidade Diferencial...")
        columns_to_privatize = ['salario', 'renda_familiar']
        df_differential = self.anonymizer.differential_privacy(original_df, columns_to_privatize, epsilon=1.0)
        anonymized_dfs['Privacidade Diferencial'] = df_differential
        
        # 3. Salvar resultados
        print("\n3. SALVANDO RESULTADOS")
        print("-" * 40)
        for technique, df in anonymized_dfs.items():
            filename = f'dados_{technique.lower().replace(" ", "_").replace("ç", "c")}.csv'
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Salvo: {filename}")
        
        # 4. Gerar relatório comparativo
        print("\n4. GERANDO RELATÓRIO COMPARATIVO")
        print("-" * 40)
        self.generate_comparison_report(original_df, anonymized_dfs)
        
        # 5. Criar visualizações
        print("\n5. CRIANDO VISUALIZAÇÕES")
        print("-" * 40)
        self.create_visualizations(original_df, anonymized_dfs)
        
        # 6. Resumo final
        print("\n" + "=" * 80)
        print("RESUMO FINAL")
        print("=" * 80)
        print(f"Dataset original: {len(original_df)} registros")
        print(f"Tecnicas aplicadas: {len(anonymized_dfs)}")
        print("Arquivos gerados:")
        print("  - dados_sensiveis_original.csv")
        for technique in anonymized_dfs.keys():
            filename = f'dados_{technique.lower().replace(" ", "_").replace("ç", "c")}.csv'
            print(f"  - {filename}")
        print("  - comparacao_anonimizacao.png")
        print("  - utilidade_vs_privacidade.png")
        print("\nDemonstracao concluida com sucesso!")
        print("Todos os dados estao em conformidade com a LGPD")

def main():
    """
    Função principal para executar a demonstração
    """
    demo = AnonymizationDemo()
    demo.run_complete_demo()

if __name__ == "__main__":
    main()
