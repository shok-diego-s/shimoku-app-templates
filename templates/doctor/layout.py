from shimoku_api_python import Client
import pandas as pd
import numpy as np
import math

from utils import meses

def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(f"data/{name}")

def get_df_gender(gender: str, data: pd.DataFrame):
    return data.query(f"Genero == '{gender}'")


def median_life(shimoku: Client, menu_path: str, order: int, data: pd.DataFrame):

    next_order=order

    def get_kpis(gender: str):
        df = get_df_gender(gender, data)

        return {
            'count': df.shape[0],
            'monthavg': df['Vida Media'].mean(),
        }

    kpis_men = get_kpis('Hombre')
    kpis_women = get_kpis('Mujer')

    shimoku.plt.html(
        html=shimoku.html_components.beautiful_indicator(
            title= "Vida media de clientes",
            href="https://shimoku.io/1-vida-media-de-clientes",
            background_url="https://images.unsplash.com/photo-1628771065518-0d82f1938462?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80",
        ),
        menu_path=menu_path,
        order=next_order,
        rows_size=1,
        cols_size=12,
    )
    next_order+=1

    shimoku.plt.html(
        html=shimoku.html_components.panel(
            text=f"Meses transcurridos entre alta-baja. Para cada usuario se calculan sus meses de vida (desde alta hasta la baja, si hay, si no desde alta hasta hoy), se suman todos y se divide por el número total de usuarios. Fecha máxima del conjunto de datos:",
            href="",
            symbol_name="Panorama",
        ),
        menu_path=menu_path,
        order=next_order,
        rows_size=1,
        cols_size=12,
    )
    next_order+=1

    common_params = {
        'value': "value",
        'header':"title",
        'footer':"description",
        'color': "color",
        'cols_size':3,
        'rows_size':1,
        'menu_path': menu_path,
    }

    hash_sy = "(#)"
    shimoku.plt.indicator(
        data={
            "description": "",
            "title": f"Hombres {hash_sy}",
            "value": kpis_men['count'],
            "color": "grey",
        },
        order=next_order,
        **common_params,
    )
    next_order+=1

    one_dec = "{:.1f}"
    shimoku.plt.indicator(
        data={
            "description": "meses",
            "title": "Tiempo promedio Hombres",
            "value": one_dec.format(kpis_men['monthavg']),
            "color": "grey",
        },
        order=next_order,
        **common_params,
    )
    next_order+=1

    shimoku.plt.indicator(
        data={
            "description": "",
            "title": f"Mujeres {hash_sy}",
            "value": kpis_women['count'],
            "color": "grey",
        },
        order=next_order,
        **common_params,
    )
    next_order+=1

    shimoku.plt.indicator(
        data={
            "description": "meses",
            "title": "Tiempo promedio Mujeres",
            "value": one_dec.format(kpis_women['monthavg']),
            "color": "grey",
        },
        order=next_order,
        **common_params,
    )
    next_order+=1


    return next_order

def age_scatter_chart(shimoku: Client, menu_path: str, order: int, data: pd.DataFrame):
    next_order=order

    cols = ['Edad', 'Vida Media']
    df_men = get_df_gender('Hombre', data)[cols]
    df_women = get_df_gender('Mujer', data)[cols]
    series_data_men = df_men.values.tolist()
    series_data_women = df_women.values.tolist()

    def getMarkLine(df, color: str):
        return {
            'silent': True,
            'symbol': 'none',
            'lineStyle': {
                'color': f"var(--chart-{color})",
                'type': 'solid',
                'width': 0.5,
            },
            'data': [
                {
                    'yAxis': df['Vida Media'].mean(),
                },
            ],
        }

    options = {
        'legend': {},
        'toolbox': {
            'feature': {
                'dataView': { 'show': True, 'readOnly': False },
                'magicType': { 'show': True, 'type': ['line', 'bar'] },
                'restore': { 'show': True },
                'saveAsImage': { 'show': True },
                'dataZoom': { 'show': True },
            }
        },
        'xAxis': {
            'name': 'Edad',
            'nameLocation': 'center',
            'nameGap': 50,
        },
        'yAxis': {
            'name': 'Videa Promedio del Cliente (Meses)',
            'nameLocation': 'center',
            'nameGap': 50,
        },
        'series': [
            {
                'symbolSize': 10,
                'data': series_data_men,
                'name': 'Hombre',
                'type': 'scatter',
                'itemStyle': {
                    'color': 'var(--chart-C1)',
                },
                'markLine': getMarkLine(df_men, 'C1')
            },
            {
                'symbolSize': 10,
                'data': series_data_women,
                'name': 'Mujer',
                'type': 'scatter',
                'itemStyle': {
                    'color': 'var(--chart-C8)',
                },
                'markLine': getMarkLine(df_women, 'C8')
            }
        ]
    }

    shimoku.plt.free_echarts(
        data=data[:1], # dummy,
        order=order,
        menu_path=menu_path,
        options=options,
    )

    next_order+=1

    return next_order

def age_group(shimoku: Client, menu_path: str, order: int):
    data = read_csv("age_group_radar.csv")

    next_order=order

    cols = list(data.columns)
    data = data.to_dict('records')

    # data = [{'name': 'Mujer', '16-25': 9, '26-35': 5, '36-45': 9, }, {'name': 'Hombre', '16-25': 1, '26-35': 2, '36-45': 5}]
    shimoku.plt.radar(
        data=data,
        # x='name',
        # y=['16-25', '26-35', '36-45']
        x=cols[0],
        y=cols[1:-1],
        order=next_order,
        menu_path=menu_path,
        cols_size=8,
        rows_size=2,
    )

    next_order+=1

    return next_order


def cohort_activation(shimoku: Client, menu_path: str, order: int):
    data = read_csv("cohort_activation.csv")
    columns = list(data.columns)

    next_order=order

    shimoku.plt.bar(
        data=data,
        order=next_order,
        menu_path=menu_path,
        x=columns[0],
        y=columns[1:-1],
        x_axis_name="Cohorts & Activation code",
        y_axis_name="Median Life (Months)",
    )

    next_order+=1

    return next_order

def heatmap_ocurrency(shimoku: Client, menu_path: str, order: int):
    data = read_csv("heatmap.csv")

    next_order=order

    series_data = data.values.tolist()
    options = {
        'title': {
            'top': 30,
            'text': "Número de ocurrencias de Altas",
            'subtext': "Por día de semana",
        },
        'tooltip': {},
        'visualMap': {
            'min': 0,
            'max': 60,
            'calculable': True,

            'orient': 'horizontal',
            'left': 'center',
            'top': 65
        },
        'calendar': {
            'top': 140,
            'left': 100,
            'right': 30,
            'cellSize': ['auto', 20],
            'range': ['2023-01', '2023-05'],
            'dayLabel': {
                'nameMap': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            },
            'monthLabel': {
                'nameMap': ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio",
                          "Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
            },
            'itemStyle': {
                'borderWidth': 0.5
            },
            'yearLabel': { 'show': False }
        },
        'series': {
            'type': 'heatmap',
            'coordinateSystem': 'calendar',
            'data': series_data,

        }
    }
    next_order+=1

    shimoku.plt.free_echarts(
        data=data[:1], # dummy
        options=options,
        order=next_order,
        menu_path=menu_path,
        rows_size=2,
    )
    return next_order

def client_num_byage(shimoku: Client, menu_path: str, order: int):
    data = read_csv("client_num_byage.csv")
    next_order=order

    columns = list(data.columns)

    dataset = data.values.tolist()
    dataset.insert(0, columns)
    options = {
        'title': {
            'text': 'Número de clientes por edad y género en el último mes (EOP)',
        },
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {
                'type': 'cross',
                'crossStyle': {
                    'color': '#999'
                }
            }
        },
        'toolbox': {
            'feature': {
                'dataView': { 'show': True, 'readOnly': False },
                'magicType': { 'show': True, 'type': ['line', 'bar'] },
                'restore': { 'show': True },
                'saveAsImage': { 'show': True }
            }
        },
        'legend': {
            'data': columns[1:-1],
        },
        'xAxis': {
            'type': 'category',
            'name': 'Rango de edad',
            'nameLocation': 'center',
            'nameGap': 40,
            'axisPointer': {
                'type': 'shadow'
            },
        },
        'yAxis': {
            'name': 'Nro clientes',
            'nameLocation': 'center',
            'nameGap': 50,
        },
        'series': [
            {
                'name': columns[1:][0],
                'type': 'bar',
            },
            {
                'name': columns[1:][1],
                'type': 'bar',
            },
            {
                'name': columns[1:][2],
                'type': 'line',
            }
        ]
    }

    shimoku.plt.free_echarts(
        data=data, # dummy
        options=options,
        order=next_order,
        sort={
            'field': 'sort_values',
            'direction': 'asc',
        },
        menu_path=menu_path,
    )

    next_order+=1

    return next_order

def client_num_bycode(shimoku: Client, menu_path: str, order: int, data: pd.DataFrame):

    next_order=order

    cols = ["Suscrito en", "Codigo"]

    dfa = data.groupby(cols).size().reset_index(name='count')

    dfb = dfa.pivot(
        index=cols[0], columns=cols[1], values='count'
    ).reset_index()

    dfb.fillna(0, inplace=True)

    # Order by month name
    dfb[cols[0]] = pd.Categorical(
        dfb[cols[0]], categories=meses, ordered=True
    )

    dfb.sort_values(cols[0], inplace=True)

    shimoku.plt.stacked_barchart(
        data=dfb,
        order=next_order,
        x=cols[0],
        show_values=list(dfb.columns[1:]),
        menu_path=menu_path,
        x_axis_name="Mes del año actual",
        y_axis_name='Proporcion de \nClientes por mes',
        calculate_percentages=True,
        # option_modifications={
        #     'yAxis': {
        #         'name': 'Proporcion de Clientes por mes',
        #         'nameLocation': 'center',
        #         'nameGap': 50,
        #     }
        # },
    )

    next_order+=1

    return next_order

def sunburst_chart(shimoku: Client, menu_path: str, order: int, data: pd.DataFrame):
    next_order=order

    shimoku.plt.html(
        order=next_order,
        menu_path=menu_path,
        html=shimoku.html_components.create_h1_title_with_modal(
            title="Proporciones jerárquicas",
            subtitle="",
            text_color='var(--color-white)',
            background_color='var(--color-primary)',
            modal_title='Proporciones jerárquicas',
            modal_text="""
            Este gráfico muestra por niveles las proporciones por,
            Rango de Edad, \n
            Rango de Vida Media, \n
            Y como se distribuye el uso de los códigos de activación entre los rangos de vida media
            """,
        )
    )
    next_order+=1

    def make_range(col: str):
        min_val = math.floor(data[col].min())
        max_val = math.ceil(data[col].max())
        range_size = math.floor( (max_val - min_val) / 4) # 
        val_ranges = [( val, val + (range_size - 1) ) for val in range(min_val, max_val, range_size)]

        return val_ranges

    age_ranges = make_range('Edad')
    life_ranges = make_range('Vida Media')

    codes = data['Codigo'].unique()
    sun_data = []
    for min_age, max_age in age_ranges[:4]:
        df_age = data.query(f"Edad >={min_age} & Edad <= {max_age}")
        age_range_count = df_age.shape[0]
        lvl_one = {
            'name': f"{min_age} - {max_age}",
            'value': age_range_count,
            'children': []
        }

        for code in list(codes)[:4]:
            df_code = df_age.query(f"Codigo == '{code}'")
            lvl_two = {
                'name': code,
                'value': df_code.shape[0],
                'children': []
            }

            # Rename column so it can be used in query method
            df_code = df_code.rename(columns={'Vida Media': 'vida_media'})

            for min_life, max_life in life_ranges[:4]:
                df_life = df_code.query(f"vida_media >={min_life} & vida_media <= {max_life}")
                lvl_three = {
                    'name': f"{min_life} - {max_life}",
                    'value': df_life.shape[0],
                }

                lvl_two['children'].append(lvl_three)

            lvl_one['children'].append(lvl_two)

        sun_data.append(lvl_one)


    shimoku.plt.sunburst(
        data=sun_data,
        children='children',
        value='value',
        name='xAxis',
        order=next_order,
        menu_path=menu_path,
        rows_size=5,
        cols_size=12,
    )

    next_order+=1

    return next_order

def plot_dashboard(shimoku: Client, menu_path: str):
    order=0
    alt_menu='V2'

    data=read_csv('main.csv')

    order+=sunburst_chart(shimoku,alt_menu,order,data)

    # order+=median_life(shimoku,alt_menu,order, data)
    # order+=age_scatter_chart(shimoku,alt_menu,order, data)
    # order+=heatmap_ocurrency(shimoku,alt_menu,order)
    # order+=client_num_bycode(shimoku,alt_menu,order, data)
    # order+=sunburst_chart(shimoku,alt_menu,order,data)


    # Possibly delete
    # order+=age_group(shimoku,alt_menu,order)
    # order+=cohort_activation(shimoku,alt_menu,order)
    # order+=client_life_cohorts(shimoku,alt_menu,order)
    # order+=client_num_byage(shimoku,alt_menu,order)
