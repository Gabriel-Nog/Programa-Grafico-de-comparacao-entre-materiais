from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Csv file
def read_and_process_csv(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        print("Colunas no DataFrame:", df.columns)  # Adicione esta linha para verificar os nomes das colunas
        
        required_columns = ['Massa Específica (g/cm³)', 'Módulo de elasticidade(Gpa)']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Coluna {col} não encontrada no arquivo CSV")
        
        df = df.dropna(subset=required_columns)
        df['Massa Específica (g/cm³)'] = df['Massa Específica (g/cm³)'].str.replace(',', '.').astype(float)
        df['Módulo de elasticidade(Gpa)'] = df['Módulo de elasticidade(Gpa)'].astype(float)
        df['Coeficiente de Poisson'] = df['Coeficiente de Poisson'].str.replace(',', '.').astype(float)
        df['Coeficiente de expansão térmica(10^-6 °C^-1)'] = df['Coeficiente de expansão térmica(10^-6 °C^-1)'].str.replace(',', '.').astype(float)
        df['Calor específico J/kg.K'] = df['Calor específico J/kg.K'].astype(float)
        df['Densidade'] = df['Densidade'].astype(float)
        return df
    except Exception as e:
        print(f"Erro ao ler e processar o arquivo CSV: {e}")
        return None
      
        # //plot_coeficiente_poisson
def plot_coeficiente_poisson(df, materials_list):
    if materials_list[0] == '' and materials_list[1] == '':
        try:
            top_8 = df.nlargest(8, 'Coeficiente de Poisson')
            materials = top_8['Material']
            coeficiente_poisson = top_8['Coeficiente de Poisson']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, coeficiente_poisson, color='salmon')
            plt.xlabel('Coeficiente de Poisson')
            plt.ylabel('Material')
            plt.title('Top 8 Maiores Coeficientes de Poisson dos Materiais')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_coeficiente.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Coeficiente de Poisson: {e}")
    else:
        try:
            df_filtered = df[df['Material'].isin(materials_list)]
            df_filtered = df_filtered.sort_values(by='Coeficiente de Poisson', ascending=False)
            materials = df_filtered['Material']
            coeficiente_poisson = df_filtered['Coeficiente de Poisson']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, coeficiente_poisson, color='salmon')
            plt.xlabel('Coeficiente de Poisson')
            plt.ylabel('Material')
            plt.title('Coeficientes de Poisson dos Materiais Selecionados')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_coeficiente.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Coeficiente de Poisson: {e}")

# //plot_coeficiente_expansao_termica
def plot_coeficiente_expansao_termica(df, materials_list):
    if materials_list[0] == '' and materials_list[1] == '':
        try:
            top_8 = df.nlargest(8, 'Coeficiente de expansão térmica(10^-6 °C^-1)')
            materials = top_8['Material']
            coeficiente_expansao_termica = top_8['Coeficiente de expansão térmica(10^-6 °C^-1)']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, coeficiente_expansao_termica, color='lightcoral')
            plt.xlabel('Coeficiente de expansão térmica(10^-6 °C^-1)')
            plt.ylabel('Material')
            plt.title('Top 8 Maiores Coeficientes de Expansão Térmica dos Materiais')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_expansao.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Coeficiente de Expansão Térmica: {e}")
    else:
        try:
            df_filtered = df[df['Material'].isin(materials_list)]
            df_filtered = df_filtered.sort_values(by='Coeficiente de expansão térmica(10^-6 °C^-1)', ascending=False)
            materials = df_filtered['Material']
            coeficiente_expansao_termica = df_filtered['Coeficiente de expansão térmica(10^-6 °C^-1)']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, coeficiente_expansao_termica, color='lightcoral')
            plt.xlabel('Coeficiente de expansão térmica(10^-6 °C^-1)')
            plt.ylabel('Material')
            plt.title('Coeficientes de Expansão Térmica dos Materiais Selecionados')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_expansao.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Coeficiente de Expansão Térmica: {e}")

# //plot_calor_especifico
def plot_calor_especifico(df, materials_list):
    if materials_list[0] == '' and materials_list[1] == '':
        try:
            top_8 = df.nlargest(8, 'Calor específico J/kg.K')
            materials = top_8['Material']
            calor_especifico = top_8['Calor específico J/kg.K']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, calor_especifico, color='gold')
            plt.xlabel('Calor específico J/kg.K')
            plt.ylabel('Material')
            plt.title('Top 8 Maiores Calores Específicos dos Materiais')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_calor.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Calor Específico: {e}")
    else:
        try:
            df_filtered = df[df['Material'].isin(materials_list)]
            df_filtered = df_filtered.sort_values(by='Calor específico J/kg.K', ascending=False)
            materials = df_filtered['Material']
            calor_especifico = df_filtered['Calor específico J/kg.K']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, calor_especifico, color='gold')
            plt.xlabel('Calor específico J/kg.K')
            plt.ylabel('Material')
            plt.title('Calores Específicos dos Materiais Selecionados')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_calor.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Calor Específico: {e}")
# //plot_densidade
def plot_densidade(df, materials_list):
    if materials_list[0] == '' and materials_list[1] == '':
        try:
            top_8 = df.nlargest(8, 'Densidade')
            materials = top_8['Material']
            densidade = top_8['Densidade']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, densidade, color='plum')
            plt.xlabel('Densidade')
            plt.ylabel('Material')
            plt.title('Top 8 Maiores Densidades dos Materiais')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_densidade.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Densidade: {e}")
    else:
        try:
            df_filtered = df[df['Material'].isin(materials_list)]
            df_filtered = df_filtered.sort_values(by='Densidade', ascending=False)
            materials = df_filtered['Material']
            densidade = df_filtered['Densidade']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, densidade, color='plum')
            plt.xlabel('Densidade')
            plt.ylabel('Material')
            plt.title('Densidades dos Materiais Selecionados')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_densidade.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Densidade: {e}")

        

# //plot_massa_especifica
def plot_massa_especifica(df, materials_list):
    if materials_list[0] == '' and materials_list[1] == '':
        try:
            top_8 = df.nlargest(8, 'Massa Específica (g/cm³)')
            materials = top_8['Material']
            massa_especifica = top_8['Massa Específica (g/cm³)']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, massa_especifica, color='skyblue')
            plt.xlabel('Massa Específica (g/cm³)')
            plt.ylabel('Material')
            plt.title('Top 8 Maiores Massas Específicas dos Materiais')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_massa.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Massa Específica: {e}")
    else:
        try:
            df_filtered = df[df['Material'].isin(materials_list)]
            df_filtered = df_filtered.sort_values(by='Massa Específica (g/cm³)', ascending=False)
            materials = df_filtered['Material']
            massa_especifica = df_filtered['Massa Específica (g/cm³)']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, massa_especifica, color='skyblue')
            plt.xlabel('Massa Específica (g/cm³)')
            plt.ylabel('Material')
            plt.title('Massas Específicas dos Materiais Selecionados')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_massa.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Massa Específica: {e}")
# //plot_modulo_elasticidade
def plot_modulo_elasticidade(df, materials_list):
    if materials_list[0] == '' and materials_list[1] == '':
        try:
            top_8 = df.nlargest(8, 'Módulo de elasticidade(Gpa)')
            materials = top_8['Material']
            modulo_elasticidade = top_8['Módulo de elasticidade(Gpa)']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, modulo_elasticidade, color='lightgreen')
            plt.xlabel('Módulo de elasticidade(Gpa)')
            plt.ylabel('Material')
            plt.title('Top 8 Maiores Módulos de Elasticidade dos Materiais')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_modulo.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Módulo de Elasticidade: {e}")
    else:
        try:
            df_filtered = df[df['Material'].isin(materials_list)]
            df_filtered = df_filtered.sort_values(by='Módulo de elasticidade(Gpa)', ascending=False)
            materials = df_filtered['Material']
            modulo_elasticidade = df_filtered['Módulo de elasticidade(Gpa)']
            
            plt.figure(figsize=(10, 8))
            plt.barh(materials, modulo_elasticidade, color='lightgreen')
            plt.xlabel('Módulo de elasticidade(Gpa)')
            plt.ylabel('Material')
            plt.title('Módulos de Elasticidade dos Materiais Selecionados')
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig('static/images/graph_modulo.png')
            plt.close()
        except Exception as e:
            print(f"Erro ao plotar Módulo de Elasticidade: {e}")       

    

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate-graph', methods=['POST'])
def generate_graph():
    #Lista de materiais
    materials_list = []
    i = 1

    # Loop para pegar todos os elementos até que não haja mais entradas
    while f'elemento{i}' in request.form:
        materials_list.append(request.form[f'elemento{i}'])    
        i += 1
    
    selected_options = request.form.getlist('options')
    df = read_and_process_csv('BaseDeDados.csv')
    options = []
    for option in selected_options:
        options.append(option)
    
    if df is not None:
        if not selected_options:
            return render_template('form.html', error="Nenhuma opção foi selecionada. Por favor, selecione pelo menos uma opção.")
        
        if 'massa' in selected_options:
            plot_massa_especifica(df, materials_list)
        if 'modulo' in selected_options:
            plot_modulo_elasticidade(df, materials_list)
        if 'coeficiente' in selected_options:
            plot_coeficiente_poisson(df, materials_list)
        if 'expansao' in selected_options:
            plot_coeficiente_expansao_termica(df, materials_list)
        if 'calor' in selected_options:
            plot_calor_especifico(df, materials_list)
        if 'densidade' in selected_options:
            plot_densidade(df, materials_list)
    
    return render_template('view.html', selected_options=options, materials_list=materials_list)

if __name__ == '__main__':
    app.run(debug=True)