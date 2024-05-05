import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from data_loader import resumen_df

# Obtener las opciones para el Dropdown 'departamento-dropdown'
departamento_options = [{'label': departamento, 'value': departamento} for departamento in resumen_df['DEPARTAMENTO'].unique() if departamento]

# Agregar opción adicional para seleccionar todos los departamentos
departamento_options.insert(0, {'label': 'Seleccionar todos los departamentos', 'value': 'todos'})

# Obtener los años disponibles en el DataFrame
available_years = resumen_df['FECHA_REGISTRO'].dt.year.unique()

# Establecer el tema de los gráficos
colors = {
    'background': '#F9F9F9',  # Cambiar el fondo a un color claro
    'text': '#000000'
}

# Cambiar la tipografía a "Roboto"
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Roboto&display=swap']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.title = "Dashboard de Inversión Pública del Perú - DEMO"

# Define el mensaje de bienvenida
welcome_message = html.Div(
    id='welcome-message',
    children=[
        html.Div(
            id='welcome-content',
            children=[
                html.H2('¡Bienvenido al Dashboard de Inversión Pública del Perú - DEMO!', style={'color': '#333333', 'fontFamily': 'Poppins, sans-serif'}),
                html.P('Explora y analiza datos sobre inversión pública en el Perú a través de tres gráficos principales:', style={'color': '#333333', 'fontFamily': 'Roboto', 'fontSize': '16px'}),
                html.Ul([ 
                    html.Li([html.Strong('Evolución Financiera:'), ' Visualiza la evolución de la inversión a lo largo del tiempo.']),
                    html.Li([html.Strong('Distribución de Inversiones por Sector y Entidad:'), ' Observa cómo se distribuyen las inversiones en diferentes sectores y entidades.']), 
                    html.Li([html.Strong('Comparación de Avance Físico por Entidad:'), ' Compara el avance físico de las inversiones entre diferentes entidades.'])
                ], style={'color': '#333333', 'fontFamily': 'Roboto', 'fontSize': '16px'}),
                html.P('Desarrollado por Data Count AI y programado por Fabian Sagua.', style={'color': '#333333', 'fontFamily': 'Roboto', 'fontSize': '16px'}),
                html.Button('Cerrar', id='close-welcome-button', n_clicks=0, style={'margin-top': '10px'})
            ],
            style={'background-color': 'rgba(240, 240, 240, 0.9)', 'padding': '20px', 'border-radius': '10px', 'position': 'fixed', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)', 'z-index': '1000'}
        )
    ]
)

# Define el layout de la aplicación
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '30px'}, children=[
    
    welcome_message,

    html.Img(src='/assets/Logo.png', style={'height': '100px', 'width': 'auto', 'top': '20px', 'left': '20px'}),  # Agregar el logo y fijarlo en la parte superior izquierda

    html.H1("Dashboard de Inversión Pública del Perú - DEMO", style={'textAlign': 'left', 'color': colors['text'], 'fontFamily': 'Poppins, sans-serif'}),

    html.P("Este dashboard proporciona un resumen de las inversiones del Banco de Inversiones del Perú desde el año 2001 hasta el mes de abril del 2024. Incluye información detallada sobre el estado de las inversiones, información financiera como Devengados, Presupuesto Institucional de Apertura (PIA), Presupuesto Institucional Modificado (PIM), costo actualizado, avance físico, montos programados de las inversiones, estado situacional, programas, subprograma, entre otros. Este panel de visualización es una versión demo, desarrollada con la finalidad de permitir a los usuarios explorar y comprender mejor los datos de inversión pública del Perú.", style={'textAlign': 'left', 'color': colors['text'], 'fontFamily': 'Roboto', 'fontSize': '16px'}),

    html.Div([
        html.Label('Seleccionar rango de años:', style={'font-family': 'Roboto', 'font-size': '18px'}),
        dcc.RangeSlider(
            id='year-range-slider',
            min=min(available_years),
            max=max(available_years),
            step=1,
            marks={str(year): str(year) for year in available_years},
            value=[2023, 2024],  # Años por defecto
        ),
    ], style={'margin-bottom': '30px'}),

    html.Div([
        html.Label('Filtrar por Sector:', style={'font-family': 'Roboto', 'font-size': '18px'}),
        dcc.Dropdown(
            id='sector-dropdown',
            options=[{'label': sector, 'value': sector} for sector in resumen_df['SECTOR'].unique()],
            value=['GOBIERNOS LOCALES'],  # Valor predeterminado
            multi=True,  # Permitir selección múltiple
            style={'width': '80%'}
        ),
    ], style={'margin-bottom': '30px'}),

    html.Div([
        html.Label('Filtrar por Departamento:', style={'font-family': 'Roboto', 'font-size': '18px'}),
        dcc.Dropdown(
            id='departamento-dropdown',
            options=departamento_options,
            value=['TACNA'],  # Valor predeterminado: seleccionar todos los departamentos
            multi=True,  # Permitir selección múltiple
            style={'width': '80%'}
        ),
    ], style={'margin-bottom': '30px'}),

    dcc.Graph(id='evolucion-financiera', style={'height': '400px', 'margin-bottom': '30px'}),
    dcc.Graph(id='distribucion-inversiones', style={'height': '400px', 'margin-bottom': '30px'}),
    dcc.Graph(id='avance-fisico', style={'height': '400px', 'margin-bottom': '30px'})
])

# Define el callback para cerrar el mensaje de bienvenida
@app.callback(
    Output('welcome-message', 'style'),
    [Input('close-welcome-button', 'n_clicks')]
)
def close_welcome_message(n_clicks):
    if n_clicks > 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

# Callback para actualizar los gráficos con los datos filtrados
@app.callback(
    [Output('evolucion-financiera', 'figure'),
     Output('distribucion-inversiones', 'figure'),
     Output('avance-fisico', 'figure')],
    [Input('sector-dropdown', 'value'),
     Input('departamento-dropdown', 'value'),
     Input('year-range-slider', 'value')]
)
def update_graphs(sector_value, departamento_value, year_range):
    # Filtrar el DataFrame según los valores seleccionados
    if 'todos' in departamento_value:
        # Si se seleccionan todos los departamentos, no se filtra por departamento
        filtered_df = resumen_df[resumen_df['SECTOR'].isin(sector_value)]
    else:
        filtered_df = resumen_df[(resumen_df['SECTOR'].isin(sector_value)) & 
                                 (resumen_df['DEPARTAMENTO'].isin(departamento_value))]

    # Filtrar por rango de años
    filtered_df = filtered_df[filtered_df['FECHA_REGISTRO'].dt.year.between(year_range[0], year_range[1])]

    # Verificar si el DataFrame filtrado está vacío
    if filtered_df.empty:
        # Devolver gráficos vacíos o mensajes de error
        empty_fig = px.scatter()  # Gráfico vacío
        return empty_fig, empty_fig, empty_fig

    # Gráfico de evolución financiera a lo largo del tiempo
    fig1 = px.line(filtered_df, x='FECHA_REGISTRO', y=['MONTO_VIABLE', 'COSTO_ACTUALIZADO'], color='ENTIDAD',
                   title='Evolución Financiera a lo largo del Tiempo',
                   template='plotly_white', labels={'value': 'Monto (SOLES)', 'FECHA_REGISTRO': 'Fecha'},
                   color_discrete_sequence=px.colors.qualitative.Plotly)

    # Gráfico de distribución de inversiones por sector y entidad (Treemap)
    fig2 = px.treemap(filtered_df, path=['SECTOR', 'ENTIDAD'], values='MONTO_VIABLE',
                      title='Distribución de Inversiones por Sector y Entidad',
                      color='MONTO_VIABLE', color_continuous_scale='RdBu',
                      labels={'MONTO_VIABLE': 'Monto (SOLES)', 'SECTOR': 'Sector', 'ENTIDAD': 'Entidad'})

    # Gráfico de comparación de avance físico por entidad (Gráfico de barras horizontales)
    fig3 = px.bar(filtered_df, y='ENTIDAD', x='AVANCE_FISICO',
                  title='Comparación de Avance Físico por Entidad',
                  template='plotly_white', labels={'AVANCE_FISICO': 'Avance Físico', 'ENTIDAD': 'Entidad'},
                  color_discrete_sequence=px.colors.qualitative.Plotly, orientation='h')

    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='0.0.0.0', dev_tools_ui=False, dev_tools_props_check=False)

