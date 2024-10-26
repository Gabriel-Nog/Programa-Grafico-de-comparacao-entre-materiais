from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)


# Csv file
def read_and_process_csv(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        print("Colunas no DataFrame:", df.columns
              )  # Adicione esta linha para verificar os nomes das colunas

        required_columns = [
            'Massa Específica (g/cm³)', 'Módulo de elasticidade(GPa)', 'Coeficiente de Poisson', 'Coeficiente de expansão térmica(10^-6°C^-1)', 'Calor específico (J/kg.K)',
            'Densidade (kg/m³)', 'Absorção óptica (m⁻¹)', 'Indução magnética (T)', 'Condutividade elétrica (S/m)'
        ]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Coluna {col} não encontrada no arquivo CSV")

        df = df.dropna(subset=required_columns)
        df['Massa Específica (g/cm³)'] = df[
            'Massa Específica (g/cm³)'].str.replace(',', '.').astype(float)
        df['Módulo de elasticidade(GPa)'] = df[
            'Módulo de elasticidade(GPa)'].astype(float)
        df['Coeficiente de Poisson'] = df[
            'Coeficiente de Poisson'].str.replace(',', '.').astype(float)
        df['Coeficiente de expansão térmica(10^-6°C^-1)'] = df[
            'Coeficiente de expansão térmica(10^-6°C^-1)'].str.replace(
                ',', '.').astype(float)
        df['Calor específico (J/kg.K)'] = df['Calor específico (J/kg.K)'].astype(
            float)
        df['Densidade (kg/m³)'] = df['Densidade (kg/m³)'].astype(float)
        df['Absorção óptica (m⁻¹)'] = df['Absorção óptica (m⁻¹)'].astype(float)
        df['Indução magnética (T)'] = df['Indução magnética (T)'].astype(float)
        df['Condutividade elétrica (S/m)'] = df['Condutividade elétrica (S/m)'].astype(float)
        return df
    except Exception as e:
        print(f"Erro ao ler e processar o arquivo CSV: {e}")
        return None

def multiplot(df, materials_list, x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    if materials_list[0] == '' and materials_list[1] == '':
        top_materials = df.nlargest(8, [x, y])
        material_top = top_materials['Material']
        materials_list = material_top.tolist()
    for material in materials_list:
        material_data = df[df['Material'] == material]
        if not material_data.empty:
            plt.plot([0, material_data[x].iloc[0]], [0, material_data[y].iloc[0]], marker='o', linestyle='-', label=material)
        else:
            print(f"Material {material} não encontrado no DataFrame.")
            
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    # Salvar o gráfico no diretório static/images
    plt.savefig('static/images/plot.png')
    plt.close()
   
@app.route('/')
def form():
    return render_template('form.html')


@app.route('/generate-graph', methods=['POST'])
def generate_graph():
    materials_list = []
    i = 1

    # Loop para pegar todos os elementos até que não haja mais entradas
    while f'elemento{i}' in request.form:
        materials_list.append(request.form[f'elemento{i}'])
        i += 1
    print("Materiais selecionados:", materials_list)
    axisX = request.form.get('axisX')
    axisY = request.form.get('axisY')
   
    df = read_and_process_csv('BaseDeDados.csv')
   

    print("Opções selecionadas:", axisX, axisY)
    if df is not None:
        if not len(axisX) > 0 or not len(axisY) > 0:
            return render_template(
                'form.html',
                error="Nenhuma opção foi selecionada. Por favor, selecione uma opção para X e para Y."
            )
        else:
            multiplot(df, materials_list, axisX, axisY, f'{axisY} x {axisX}',
                      axisX, axisY)
            return render_template('view.html')

if __name__ == '__main__':
    app.run(debug=True)
