from shimoku_api_python import Client
from importlib.metadata import version
import platform
import pandas as pd
import math
from page_header import page_header
from utils import meses


vida_tab_group = "vida_tab_group"

def read_csv(name: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(f"data/{name}", **kwargs)

def get_df_gender(gender: str, data: pd.DataFrame):
    return data.query(f"Genero == '{gender}'")

def logo_link(shimoku: Client, img_url: str, href: str, menu_path: str, order: int, width: str = '100%', **kwargs):
    img_tag = f"<img src=\"{img_url}\" style=\"width: {width};\">"
    # if width != '100%':
    #     img_tag = f"<img src={img_url} height=100 height={height} width={width}>"

    html = f"""
    <a href={href}>
        {img_tag}
    </a>
    """
    shimoku.plt.html(
        html,
        menu_path=menu_path,
        order=order,
        **kwargs,
    )

def make_cat_range(df: pd.DataFrame, col: str, range_size: int):
    """
    Make a category range from numerical column
    """
    min_val = math.floor(df[col].min())
    max_val = math.ceil(df[col].max())
    range_size = math.floor( (max_val - min_val) / range_size) #
    val_ranges = [( val, val + (range_size - 1) ) for val in range(min_val, max_val, range_size)]

    return val_ranges

def life_kpis(shimoku: Client, menu_path: str, order: int, data: pd.DataFrame):

    next_order=order

    def get_kpis(gender: str):
        df = get_df_gender(gender, data)

        return {
            'count': df.shape[0],
            'monthavg': df['Vida Media'].mean(),
        }

    kpis_men = get_kpis('Hombre')
    kpis_women = get_kpis('Mujer')

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
        'title': {
            'text': 'Vida media de los usuarios por edad y género'
        },
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
            'name': 'Vida Promedio del Cliente (Meses)',
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
                    'color': 'var(--chart-C2)',
                    # 'color': 'var(--chart-C8)',
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
        tabs_index=(vida_tab_group, 'Scatter'),
    )

    next_order+=1

    return next_order

def age_group_bar(shimoku: Client, menu_path: str, order: int, data: pd.DataFrame):
    """
    """
    next_order=order
    age_ranges = make_cat_range(data, 'Edad', range_size=8)
    df_age_dict = {'age_group': [], 'Hombre': [], 'Mujer': []}
    for min_age, max_age in age_ranges:
        query_res = data.query(f"Edad >= {min_age} & Edad <= {max_age}")

        df_age_dict['age_group'].append(f"{min_age}-{max_age}")

        df_men = query_res.query(f"Genero == 'Hombre'")
        df_women = query_res.query(f"Genero == 'Mujer'")

        df_age_dict['Hombre'].append(df_men['Vida Media'].median())
        df_age_dict['Mujer'].append(df_women['Vida Media'].median())

    df_age = pd.DataFrame(data=df_age_dict)

    df_age.fillna(0, inplace=True)

    shimoku.plt.bar(
        data=df_age.round(2),
        title="Vida media de los usuarios por edad y género",
        cols_size=12,
        rows_size=4,
        subtitle="Por edad y género",
        x="age_group",
        y=["Hombre", "Mujer"],
        y_axis_name="Vida promedio del cliente (Meses)",
        order=order,
        menu_path=menu_path,
        tabs_index=(vida_tab_group, "Bar"),
    )

    next_order+=1

    return next_order

def info_section(shimoku: Client, menu_path: str, order: int):

    next_order=order
    next_order+=page_header(
        shimoku,
        order=order,
        menu_path=menu_path,
        title="Estudio sobre altas y vida media de los usuarios de la aplicación",
        subtitle="Este dashboard demuestra el comportamiento de los usuarios que se han dado de alta a través de la aplicación. Detalla que tipo de código utilizaron para darse de alta, cuanto tiempo tardaron en hacerlo y que propiedades de la persona afectan este evento, como el género y la edad.",
        description=f"Para ver más detalle sobre como generar esta template o alguno de sus gráficos en concreto, te esperamos en el post de Medium y en el video de youtube que te hemos preparado. Dashboard creado con la versión {version('shimoku_api_python')} de la SDK y Python {platform.python_version()}",
        box={
            'background': "https://images.unsplash.com/photo-1628771065518-0d82f1938462?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80",
        },
        # url's to be defined later
        buttons={
            "button_github": {
                'button_url': "",
            },
            "button_medium": {
                "button_url": "",
            },
            "button_youtube": {
                "button_url": "",
            }
        },
    )
    return next_order

def heatmap_ocurrency(shimoku: Client, menu_path: str, order: int):
    data = read_csv("heatmap.csv", parse_dates=['date'])

    next_order=order

    series_values = data.values.tolist()
    series_data = [ {
        'name': value[0].strftime('%d, %b %Y'),
        'value': [str(value[0].date()), value[1]],
    } for value in series_values ]

    options = {
        'title': {
            'top': 30,
            'text': "Altas de usuarios",
            'subtext': "Por cada día del mes",
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
            'cellSize': ['auto', 40],
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
        rows_size=3,
    )
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

    shimoku.plt.stacked_area_chart(
        data=dfb,
        order=next_order,
        menu_path=menu_path,
        title="Códigos de alta usados",
        x=cols[0],
        show_values=list(dfb.columns[1:]),
        calculate_percentages=True,
        cols_size=12,
        rows_size=4,
        # option_modifications={
        #     'yAxis': {
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
            title='',
            subtitle="Género -> Edad -> Vida Media",
            text_color='var(--color-white)',
            background_color='var(--color-primary)',
            modal_title='Proporciones jerárquicas',
            modal_text="""
            Este gráfico muestra por niveles las proporciones por:
            Rango de Edad, \n
            Rango de Vida Media, \n
            y como se distribuye el uso de los códigos de activación entre los rangos de vida media.
            """,
        )
    )
    next_order+=1

    genders = data['Genero'].unique()

    age_ranges = make_cat_range(data, 'Edad', range_size=4)
    life_ranges = make_cat_range(data, 'Vida Media', range_size=4)

    sun_data = []

    # Rename column so it can be used in query method
    data.rename(columns={'Vida Media': 'vida_media'}, inplace=True)

    for gender in genders:
        df_g = get_df_gender(gender, data)
        lvl_one = {
            'name': gender,
            'value': df_g.shape[0],
            'children': []
        }

        for min_age, max_age in age_ranges:
            df_age = df_g.query(f"Edad >={min_age} & Edad <= {max_age}")
            age_range_count = df_age.shape[0]

            lvl_two = {
                'name': f"{min_age} - {max_age}",
                'value': age_range_count,
                'children': [],
            }

            for min_life, max_life in life_ranges:
                df_life = df_age.query(f"vida_media >={min_life} & vida_media <= {max_life}")

                lvl_three = {
                    'name': f"{min_life} - {max_life}",
                    'value': df_life.shape[0],
                    'children': [],
                }

                if df_life.shape[0] > 0:
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

def info_section_two(shimoku: Client, menu_path: str, order: int):
    next_order=order

    shimoku.plt.update_modal(
        menu_path=menu_path, modal_name='Test modal',
        open_by_default=False, width=90, height=90
    )
    shimoku.plt.add_tabs_group_to_modal(
        menu_path=menu_path, modal_name='Test modal', tabs_group_name='Test'
    )
    shimoku.plt.update_tabs_group_metadata(
        menu_path=menu_path, group_name='Test', order=1
    )

    modal_header = shimoku.html_components.create_h1_title_with_modal(
        title='Más información', subtitle='Para ver más detalle sobre como generar esta template o alguno de sus gráficos en concreto, te esperamos en el post de Medium y en el video que te hemos preparado',
        background_color='var(--chart-C1)'
    )

    shimoku.plt.html(
        html=modal_header, menu_path=menu_path, modal_name='Test modal', order=0
    )

    tabs_index=("Test", "Info")


    logo_link(
        shimoku,
        img_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Logo_of_YouTube_%282015-2017%29.svg/2560px-Logo_of_YouTube_%282015-2017%29.svg.png",
        order=2,
        menu_path=menu_path,
        tabs_index=tabs_index,
        cols_size=3,
        rows_size=1,
    )

    logo_link(
        shimoku,
        img_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Medium_%28website%29_logo.svg/798px-Medium_%28website%29_logo.svg.png?20210818085543",
        order=3,
        menu_path=menu_path,
        tabs_index=tabs_index,
        cols_size=6,
        rows_size=1,
    )
    # shimoku.plt.indicator(
    #     tabs_index=tabs_index, # delete
    #     menu_path=menu_path,
    #     order=2,
    #     color="color",
    #     background_image="background_image",
    #     footer="footer",
    #     value="value",
    #     header="header",
    #     align="align",
    #     target_path='targetPath',
    #     cols_size=3,
    #     data={
    #         "color": "warning",
    #         "background_image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Logo_of_YouTube_%282015-2017%29.svg/2560px-Logo_of_YouTube_%282015-2017%29.svg.png",
    #         "header": "",
    #         "footer": "",
    #         "value": "Youtube video",
    #         "align": "left",
    #         "targetPath": "https://youtube.com/",
    #     }
    # )

    # shimoku.plt.indicator(
    #     tabs_index=tabs_index, # delete
    #     menu_path=menu_path,
    #     order=3,
    #     color="color",
    #     background_image="background_image",
    #     footer="footer",
    #     value="value",
    #     header="header",
    #     align="align",
    #     target_path='targetPath',
    #     cols_size=3,
    #     data={
    #         "color": "warning",
    #         "background_image": "https://miro.medium.com/v2/resize:fit:1200/1*jfdwtvU6V6g99q3G7gq7dQ.png",
    #         "header": "",
    #         "footer": "",
    #         "value": "Medium post",
    #         "align": "left",
    #         "targetPath": "https://medium.com",
    #     }
    # )

    shimoku.plt.modal_button(
        menu_path=menu_path, order=0,
        modal_name_to_open='Test modal', label='Información'
    )

    return next_order+1

def configure_tabs(shimoku: Client, menu_path: str, order:int):
    """
    Set order and style of tabs
    """
    shimoku.plt.update_tabs_group_metadata(
        order=order,
        menu_path=menu_path,
        group_name=vida_tab_group,
        just_labels=True,
        sticky=False,
    )


def plot_dashboard(shimoku: Client, menu_path: str):
    order=0

    data=read_csv('main.csv')


    # menu_path="Option two"
    order=info_section(shimoku,menu_path,order)

    order+=life_kpis(shimoku,menu_path,order, data)

    tab_order=order
    # Increment one because of tabs
    order+=1
    # These two go in a tab
    order+=age_scatter_chart(shimoku,menu_path,order, data)
    order+=age_group_bar(shimoku,menu_path,order, data)
    configure_tabs(shimoku,menu_path,tab_order)
    order+=heatmap_ocurrency(shimoku,menu_path,order)
    order+=client_num_bycode(shimoku,menu_path,63, data)
    print(f"Order ====== {order}")
    order+=sunburst_chart(shimoku,menu_path,order,data)

