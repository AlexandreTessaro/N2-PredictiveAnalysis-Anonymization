# Anonimização de Dados - Conformidade com LGPD

## 📋 Descrição do Projeto

Este projeto implementa técnicas de anonimização de dados pessoais em conformidade com a **Lei Geral de Proteção de Dados Pessoais (LGPD)** do Brasil. O objetivo é demonstrar como utilizar dados sensíveis em análises, predições e classificações sem desrespeitar a legislação de proteção de dados.

## 🎯 Objetivos

- Implementar técnicas de anonimização de dados conforme LGPD
- Demonstrar o trade-off entre utilidade dos dados e privacidade
- Fornecer ferramentas práticas para proteção de dados pessoais
- Gerar visualizações comparativas das técnicas aplicadas

## 🔧 Técnicas Implementadas

### 1. **K-Anonimidade**
- **Descrição**: Garante que cada registro seja indistinguível de pelo menos k-1 outros registros
- **Aplicação**: Agrupamento de registros baseado em atributos quasi-identificadores
- **Parâmetros**: k=3 (mínimo de 3 registros por grupo)

### 2. **L-Diversidade**
- **Descrição**: Garante que cada grupo tenha pelo menos l valores distintos para o atributo sensível
- **Aplicação**: Diversificação de valores sensíveis dentro dos grupos
- **Parâmetros**: l=2 (mínimo de 2 valores distintos)

### 3. **Generalização**
- **Descrição**: Substitui valores específicos por categorias mais amplas
- **Aplicação**: 
  - Idade → Faixas etárias (18-25, 26-35, etc.)
  - Salário → Faixas salariais (Baixo, Médio, Alto, etc.)
  - Localização → Cidade anonimizada

### 4. **Supressão**
- **Descrição**: Remove completamente atributos identificadores diretos
- **Aplicação**: Eliminação de campos como CPF, RG, nome completo
- **Benefício**: Redução máxima de risco de reidentificação

### 5. **Pseudoanonimização**
- **Descrição**: Substitui identificadores por pseudônimos usando hash
- **Aplicação**: Email e telefone → Hash SHA-256
- **Benefício**: Mantém utilidade para análises agregadas

### 6. **Mascaramento de Dados**
- **Descrição**: Substitui parte dos dados por caracteres de mascaramento
- **Aplicação**:
  - Email: `j***@exemplo.com`
  - Telefone: `***-****-1234`
  - CPF: `123***.***-45`

### 7. **Adição de Ruído**
- **Descrição**: Adiciona ruído aleatório aos dados numéricos
- **Aplicação**: Salário, renda familiar, score de crédito
- **Parâmetros**: Ruído gaussiano com 5% de desvio padrão

### 8. **Privacidade Diferencial**
- **Descrição**: Adiciona ruído calibrado para garantir privacidade diferencial
- **Aplicação**: Dados numéricos sensíveis
- **Parâmetros**: ε=1.0 (parâmetro de privacidade)

## 📁 Estrutura do Projeto

```
N2-PredictiveAnalysis/
├── requirements.txt                 # Dependências do projeto
├── sample_data_generator.py        # Gerador de dados sensíveis
├── anonymization_techniques.py     # Implementação das técnicas
├── demo_anonymization.py          # Demonstração completa
├── README.md                      # Documentação do projeto
└── dados_sensiveis_original.csv   # Dataset de exemplo (gerado)
```

## 🚀 Como Executar

### 1. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 2. Geração de Dados de Exemplo

```bash
python sample_data_generator.py
```

### 3. Execução da Demonstração Completa

```bash
python demo_anonymization.py
```

### 4. Execução Individual das Técnicas

```bash
python anonymization_techniques.py
```

## 📊 Saídas Geradas

### Arquivos CSV
- `dados_sensiveis_original.csv` - Dataset original com dados sensíveis
- `dados_k_anonimidade.csv` - Dataset com K-anonimidade aplicada
- `dados_generalizados.csv` - Dataset com generalização aplicada
- `dados_suprimidos.csv` - Dataset com supressão aplicada
- `dados_pseudoanonimizados.csv` - Dataset com pseudoanonimização aplicada
- `dados_mascarados.csv` - Dataset com mascaramento aplicado
- `dados_com_ruido.csv` - Dataset com adição de ruído
- `dados_privacidade_diferencial.csv` - Dataset com privacidade diferencial

### Visualizações
- `comparacao_anonimizacao.png` - Gráficos comparativos das técnicas
- `utilidade_vs_privacidade.png` - Trade-off utilidade vs privacidade

## 📈 Análise de Resultados

### Métricas de Privacidade
- **K-Anonimidade**: Medida pelo número mínimo de registros por grupo
- **L-Diversidade**: Medida pela diversidade de valores sensíveis
- **Supressão**: Medida pela porcentagem de atributos removidos

### Métricas de Utilidade
- **Correlação**: Mantida entre variáveis numéricas
- **Distribuição**: Preservada para análises estatísticas
- **Agregação**: Possível para análises de tendências

### Trade-off Utilidade vs Privacidade
- **Alta Utilidade, Baixa Privacidade**: Pseudoanonimização
- **Alta Privacidade, Baixa Utilidade**: Supressão
- **Equilíbrio**: Generalização + K-anonimidade

## 🔒 Conformidade com LGPD

### Princípios Aplicados
1. **Finalidade**: Dados anonimizados para análise estatística
2. **Adequação**: Técnicas adequadas ao propósito
3. **Necessidade**: Mínimo necessário para análise
4. **Transparência**: Processo documentado e auditável
5. **Segurança**: Proteção contra reidentificação

### Direitos dos Titulares
- **Anonimização**: Dados não podem ser reidentificados
- **Portabilidade**: Dados anonimizados podem ser transferidos
- **Eliminação**: Dados originais podem ser eliminados após anonimização

## 🛠️ Ferramentas Utilizadas

### Bibliotecas Python
- **pandas**: Manipulação de dados
- **numpy**: Operações numéricas
- **anonymization-library**: Técnicas de anonimização
- **faker**: Geração de dados sintéticos
- **matplotlib/seaborn**: Visualizações

### Técnicas de Anonimização
- **ARX**: Framework de anonimização (referência)
- **IBM Guardian**: Solução empresarial (referência)
- **Google TensorFlow Privacy**: Privacidade diferencial (referência)

## 📚 Referências

### Legislação
- [Lei Geral de Proteção de Dados Pessoais (LGPD)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [Resolução ANPD nº 1/2023](https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/resolucao-anpd-n-1-de-2023.pdf)

### Técnicas de Anonimização
- Samarati, P., & Sweeney, L. (1998). Protecting privacy when disclosing information: k-anonymity and its enforcement through generalization and suppression.
- Machanavajjhala, A., et al. (2007). l-diversity: Privacy beyond k-anonymity.
- Dwork, C. (2006). Differential privacy.

### Ferramentas
- [ARX Data Anonymization Tool](https://arx.deidentifier.org/)
- [IBM Guardian](https://www.ibm.com/security/data-privacy)
- [TensorFlow Privacy](https://github.com/tensorflow/privacy)

## 👥 Autores

- **Luiz Carlos Camargo** - Professor Orientador
- **Equipe de Desenvolvimento** - Implementação das técnicas

## 📅 Cronograma

- **Desenvolvimento**: Outubro 2024
- **Apresentação**: 27/10/2024
- **Entrega**: Teams (por um dos membros da dupla)

## ⚠️ Considerações Importantes

### Limitações
- Dados sintéticos para demonstração
- Técnicas aplicadas em ambiente controlado
- Necessária validação para dados reais

### Recomendações
- Avaliar trade-off utilidade vs privacidade
- Considerar contexto específico da aplicação
- Implementar auditoria e monitoramento
- Revisar periodicamente as técnicas aplicadas

## 📞 Suporte

Para dúvidas ou sugestões sobre o projeto, entre em contato através do Teams da disciplina.

---

**⚠️ Aviso Legal**: Este projeto é para fins educacionais e de demonstração. Para aplicação em dados reais, consulte especialistas em proteção de dados e legislação aplicável.
