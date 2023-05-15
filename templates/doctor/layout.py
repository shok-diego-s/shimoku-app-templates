from shimoku_api_python import Client
import pandas as pd
import numpy as np

def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(f"data/{name}")

def median_life(shimoku: Client, menu_path: str, order: int):

    data = read_csv("vida_media.csv")

    next_order=order

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

    shimoku.plt.stacked_horizontal_barchart(
        data=data,
        menu_path=menu_path,
        order=next_order,
        x="categoria",
        rows_size=2,
        cols_size=8,
    )
    next_order+=1

    shimoku.plt.indicator(
        data={
            "description": "meses",
            "title": "Tiempo Promedio para Todos: ",
            "value": 12,
            "color": "grey",
        },
        menu_path=menu_path,
        order=next_order,
        cols_size=4,
        value="value",
        header="title",
        footer="description",
        color="color",
    )
    next_order+=1

    return next_order

def age_group(shimoku: Client, menu_path: str, order: int):
    data = read_csv("age_group.csv")

    next_order=order

    shimoku.plt.bar(
        # Half of the data, to display every label
        data=data[:8],
        x="X",
        y=["Median Life"],
        title="Vida media de Usuarios por Grupo de Edad",
        order=next_order,
        menu_path=menu_path,
        rows_size=2,
        x_axis_name="Age range & Activation code",
        y_axis_name="Median Life (Months)",
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
    order+=median_life(shimoku,menu_path,order)
    order+=age_group(shimoku,menu_path,order)
    order+=cohort_activation(shimoku,menu_path,order)
    order+=client_life_cohorts(shimoku,menu_path,order)
    order+=client_num_bycode(shimoku,menu_path,order)
