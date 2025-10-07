"""
Gerador de Dados Sensíveis para Demonstração de Anonimização
Simula um dataset com informações pessoais sensíveis conforme LGPD
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Configurar Faker para português brasileiro
fake = Faker('pt_BR')

def generate_sensitive_dataset(n_records=1000):
    """
    Gera um dataset com dados sensíveis para demonstração de técnicas de anonimização
    
    Args:
        n_records (int): Número de registros a serem gerados
        
    Returns:
        pd.DataFrame: Dataset com dados sensíveis
    """
    
    data = []
    
    for _ in range(n_records):
        # Dados pessoais básicos
        nome_completo = fake.name()
        cpf = fake.cpf()
        rg = fake.rg()
        email = fake.email()
        telefone = fake.phone_number()
        
        # Endereço
        endereco = fake.address()
        cidade = fake.city()
        estado = fake.state()
        cep = fake.postcode()
        
        # Dados demográficos
        data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80)
        idade = (datetime.now().date() - data_nascimento).days // 365
        
        # Dados profissionais
        profissao = fake.job()
        empresa = fake.company()
        salario = random.randint(3000, 50000)
        
        # Dados médicos (hipotéticos)
        altura = round(random.uniform(1.50, 2.00), 2)
        peso = round(random.uniform(50, 120), 1)
        imc = round(peso / (altura ** 2), 1)
        
        # Dados financeiros
        renda_familiar = random.randint(5000, 100000)
        numero_cartao = fake.credit_card_number()
        
        # Dados de comportamento (hipotéticos)
        score_credito = random.randint(300, 850)
        tempo_cliente = random.randint(0, 20)
        
        record = {
            'id': len(data) + 1,
            'nome_completo': nome_completo,
            'cpf': cpf,
            'rg': rg,
            'email': email,
            'telefone': telefone,
            'endereco': endereco,
            'cidade': cidade,
            'estado': estado,
            'cep': cep,
            'data_nascimento': data_nascimento,
            'idade': idade,
            'profissao': profissao,
            'empresa': empresa,
            'salario': salario,
            'altura': altura,
            'peso': peso,
            'imc': imc,
            'renda_familiar': renda_familiar,
            'numero_cartao': numero_cartao,
            'score_credito': score_credito,
            'tempo_cliente': tempo_cliente,
            'data_cadastro': fake.date_time_between(start_date='-5y', end_date='now')
        }
        
        data.append(record)
    
    return pd.DataFrame(data)

def save_sample_data():
    """Gera e salva o dataset de exemplo"""
    print("Gerando dataset com dados sensíveis...")
    df = generate_sensitive_dataset(1000)
    
    # Salvar dataset original
    df.to_csv('dados_sensiveis_original.csv', index=False, encoding='utf-8')
    
    print(f"Dataset gerado com {len(df)} registros")
    print("Arquivo salvo: dados_sensiveis_original.csv")
    
    # Mostrar estatísticas básicas
    print("\nEstatísticas do Dataset:")
    print(f"- Total de registros: {len(df)}")
    print(f"- Colunas: {len(df.columns)}")
    print(f"- Dados faltantes: {df.isnull().sum().sum()}")
    
    return df

if __name__ == "__main__":
    df = save_sample_data()
    print("\nPrimeiras 5 linhas do dataset:")
    print(df.head())
