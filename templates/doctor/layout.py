from shimoku_api_python import Client
import pandas as pd
import numpy as np

def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(f"data/{name}")

def median_life(shimoku: Client, menu_path: str, order: int, data: pd.DataFrame):

    next_order=order

    def get_kpis(gender: str):
        df = data.query(f"Genero == '{gender}'")

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

    # df = data.copy()
    # df['Edad'] = data['Edad'].round(2)

    shimoku.plt.scatter(
        data=data,
        x='Edad',
        y=['Edad','Vida Media'],
        order=order,
        menu_path=menu_path,
        option_modifications={
            'optionModifications': {
                'markLine': {
                    'silent': True,
                    'symbol': 'none',
                    'lineStyle': {
                        'color': 'red',
                        'type': 'solid',
                        'width': 2,
                    },
                    'data': [
                        {
                            'yAxis': data['Vida Media'].mean(),
                        },
                    ],
                }
            }
        }
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
def client_life_cohorts(shimoku: Client, menu_path: str, order: int):
    data = read_csv("client_life_cohorts.csv")

    next_order=order
    shimoku.plt.html(
        html=shimoku.html_components.panel(
            href="",
            text="El analisis por cohortes permite visualizar datos por grupos, normalmente según dos ejes "
            "temporales. El eje vertical representa el mes de suscripción del usuario, es la variable "
            "que define los cohortes.\n El eje horizontal representa la cantidada de meses despues del mes "
            "del eje vertical. Este mes puede ser el de la baja del usuario, o el mes en el que han tenido/"
            "puntuado una consulta, de esta manera se puede ver la información relativa a cuantos meses "
            "han pasado después del alta. Un caso muy claro es el mapa de vida de clientes en el que se "
            "puede ver como la vida en meses de los clientes crece igual que el eje horizontal.\n",
            symbol_name="insights",
        ),
        menu_path=menu_path,
        order=next_order,
        rows_size=1,
        cols_size=12,
    )
    next_order+=1

    data = data.to_dict('records')

    shimoku.plt.heatmap(
        data=data,
        order=next_order,
        menu_path=menu_path,
        title='Client life by cohorts',
        x='xAxis', y='yAxis', value='value',
        x_axis_name='Unsubscribed at',
        y_axis_name='Subscribed At',
    )
    next_order+=1

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

def client_num_bycode(shimoku: Client, menu_path: str, order: int):

    data = read_csv("client_num_bycode.csv")
    next_order=order

    columns = list(data.columns)

    shimoku.plt.stacked_area_chart(
        data=data,
        order=next_order,
        menu_path=menu_path,
        x=columns[0], # month
        show_values=columns[1:-1], # activation_codes
        x_axis_name="Month of the current year",
        y_axis_name='Clients per month',
        #calculate_percentages=True,
    )

    next_order+=1

    return next_order

def plot_dashboard(shimoku: Client, menu_path: str):
    order=0
    alt_menu='V2'

    data=read_csv('main.csv')
    order+=median_life(shimoku,alt_menu,order, data)
    order+=age_scatter_chart(shimoku,alt_menu,order, data)


    # order+=age_group(shimoku,alt_menu,order)
    # order+=cohort_activation(shimoku,alt_menu,order)
    # order+=client_life_cohorts(shimoku,alt_menu,order)
    # order+=client_num_byage(shimoku,alt_menu,order)
    # order+=client_num_bycode(shimoku,alt_menu,order)
