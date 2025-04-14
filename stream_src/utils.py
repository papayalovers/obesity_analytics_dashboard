import plotly.graph_objects as go
import streamlit as st
import plotly.figure_factory as ff
import random 
import plotly.express as px

###################
# LINEPLOT        #
###################
def plot_obesity_trend_by_age(data):
    '''
    Fungsi ini digunakan untuk membuat grafik garis (line plot) yang menggambarkan jumlah kasus obesitas berdasarkan usia. 
    Grafik ini menampilkan jumlah orang obesitas di setiap rentang usia, dengan posisi teks menunjukkan jumlah kasus obesitas di setiap titik.

    **Parameter**:
    - `data`: Data frame yang berisi data terkait obesitas, termasuk kolom "age" dan "class".

    **Hasil**:
    - Grafik garis yang menunjukkan tren kasus obesitas berdasarkan usia.
    '''
    df_obese = data[data["class"] == "Obesity"]

    # hitung jumlah orang obesitas di setiap usia
    obesity_by_age = df_obese["age"].value_counts().reset_index()
    obesity_by_age.columns = ["Age", "Obesity Cases"]
    obesity_by_age = obesity_by_age.sort_values("Age")  
    
    # membuat linechart
    fig = go.Figure([go.Scatter(
        x=obesity_by_age['Age'],
        y=obesity_by_age['Obesity Cases'],
        mode="lines+markers+text",
        marker=dict(color='#17BFCE', size=8),  
        line=dict(width=2, color='#22FFA7'), 
        name="Obesity Cases",
        text=obesity_by_age['Obesity Cases'],
        textposition='top center',
        textfont=dict(size=12, color='white')
    )])

    fig.update_layout(
        title={
            'text': "Obesity Cases by Age", 
            'x': 0.5, 
            'xanchor': 'center', 
            'font': {'size': 18}
        },
        xaxis_title="Age",
        yaxis_title="Number of Obesity Cases",
        width=700, 
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)',
    )

    st.plotly_chart(fig, use_container_width=True)
###################
# GAUGEPLOT       #
###################
def plot_gauge(
    indicator_number, 
    indicator_color, 
    indicator_suffix, 
    indicator_title, 
    max_bound
):
    '''
    Fungsi ini digunakan untuk menampilkan indikator berbentuk gauge untuk suatu metrik dengan nilai numerik. 
    Grafik ini menggambarkan indikator yang dinamis dengan warna dan label sesuai dengan nilai yang diberikan.

    **Parameter**:
    - `indicator_number`: Nilai indikator yang akan ditampilkan pada gauge.
    - `indicator_color`: Warna indikator yang digunakan pada gauge.
    - `indicator_suffix`: Suffix untuk menambahkan unit pengukuran pada indikator.
    - `indicator_title`: Judul indikator.
    - `max_bound`: Batas maksimum untuk sumbu gauge.

    **Hasil**:
    - Grafik gauge dengan indikator nilai numerik.
    '''
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font": {
                    "size": 30,  # Ukuran font
                    "color": indicator_color,  # Warna font sesuai dengan warna indikator
                }
            },
            gauge={
                "axis": {
                    "range": [0, max_bound],  # Rentang gauge
                    "tickwidth": 1,  # Ukuran tick pada sumbu
                },
                "bar": {"color": indicator_color},  # Warna bar sesuai indikator
            }
        )
    )

    fig.update_layout(
        xaxis_title=indicator_title.capitalize(),
        title={
            'text': f'{indicator_title.capitalize()}', 
            'x': 0.5, 
            'y': 1,
            'xanchor': 'center', 
            'font': {'size': 18}
        },        
        height=170,  
        margin=dict(l=10, r=10, t=50, b=10, pad=8), 
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)' 
    )

    st.plotly_chart(fig, use_container_width=True)
###################
# DISPLOT         #
###################
def distplot(hist_data, group_labels, title):
    '''
    Fungsi ini digunakan untuk menampilkan distribusi data menggunakan histogram atau distribusi probabilitas. 
    Jika ada lebih dari satu kelompok data, distribusi akan dipisahkan berdasarkan kategori yang diberikan.

    **Parameter**:
    - `hist_data`: Data historis yang akan digunakan untuk plotting distribusi.
    - `group_labels`: Label untuk masing-masing kelompok data yang ingin dipisahkan.
    - `title`: Judul grafik distribusi.

    **Hasil**:
    - Grafik distribusi probabilitas atau histogram untuk kelompok data yang diberikan.
    '''
    # Check if we are dealing with multiple groups or single data set
    if len(hist_data) == 1:
        # If only one group, just plot the data without any grouping
        fig = ff.create_distplot(hist_data, group_labels, show_rug=False)
    else:
        # If multiple groups, create distplot with grouping
        fig = ff.create_distplot(hist_data, group_labels, show_rug=False)

    # Update layout for the figure
    fig.update_layout(
        legend=dict(
            x=0.65,  # Position of the legend (0 - 1)
            y=0.95,  # Position of the legend (0 - 1)
        ),
        title={
            'text': f'{title} by Class' if len(hist_data) > 1 else title,
            'font': {'size': 18},
            'x': 0.5,
            'xanchor': 'center',
        },
        width=700, 
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title=title.capitalize(),
    )
    
    st.plotly_chart(fig, use_container_width=True)
###################
# BARPLOT         #
###################
def barplot(data, x, title, hue=None):
    '''
    Fungsi ini digunakan untuk membuat grafik batang (bar plot) untuk distribusi data. 
    Jika parameter `hue` diberikan, data akan dipisahkan berdasarkan kategori `hue`.

    **Parameter**:
    - `data`: Data frame yang berisi data untuk plot.
    - `x`: Kolom yang akan dihitung distribusinya.
    - `title`: Judul grafik.
    - `hue`: Kolom yang digunakan untuk memisahkan data berdasarkan kategori.

    **Hasil**:
    - Grafik batang yang menunjukkan distribusi data berdasarkan kategori atau secara keseluruhan.

    '''
    # jika hue = True, lakukan pemisahan data berdasarkan hue
    if hue:
        hue_values = data[hue].unique()  # ambil semua nilai unik dari kolom hue
        fig = go.Figure()

        colors = px.colors.qualitative.Pastel  # pilihan warna soft

        for hue_value in hue_values:
            # filter data berdasarkan hue_value
            filtered_data = data[data[hue] == hue_value]
            count_data = filtered_data[x].value_counts().reset_index()
            count_data.columns = [x, 'count']
            
            color = random.choice(colors)  # pilih warna secara acak dari Set2

            fig.add_trace(go.Bar(
                name=str(hue_value),
                x=count_data[x],
                y=count_data['count'],
                text=count_data['count'], 
                textposition='outside', 
                textfont=dict(size=12),
                marker_color=color 
            ))

        fig.update_layout(
            barmode='group',  
            xaxis_title=title.capitalize(),
            title={
                'text': f'{title.capitalize()} Distribution by {hue.capitalize()}' if hue else f'{x.capitalize()} Distribution',
                'x': 0.5, 'xanchor': 'center', 'font': {'size': 18}},
            width=700, 
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',  
            paper_bgcolor='rgba(0,0,0,0)' 
        )

    else:
        count_data = data[x].value_counts().reset_index()
        count_data.columns = [x, 'count']
        fig = go.Figure([go.Bar(
            x=count_data[x],
            y=count_data['count'],
            text=count_data['count'], 
            textposition='outside',  
            textfont=dict(size=12) 
        )])

        fig.update_layout(
            xaxis_title=title.capitalize(),
            title={
                'text': f'{title.capitalize()} Distribution', 
                'x': 0.5, 
                'xanchor': 'center', 
                'font': {'size': 18}
            },
            width=700, 
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',  
            paper_bgcolor='rgba(0,0,0,0)' 
        )

    st.plotly_chart(fig, use_container_width=True)
###################
# BARPLOT 2       #
###################
def probability_barplot(data, given_condition):
    '''
    Fungsi ini digunakan untuk menampilkan probabilitas terjadinya obesitas berdasarkan kondisi tertentu. 
    Grafik ini menunjukkan fitur yang paling umum dalam kategori obesitas atau probabilitas obesitas berdasarkan fitur tertentu.

    **Parameter**:
    - `data`: Data frame yang berisi data untuk analisis.
    - `given_condition`: Kondisi yang digunakan untuk analisis (misalnya, 'Obesity').

    **Hasil**:
    - Grafik batang yang menunjukkan probabilitas obesitas berdasarkan kondisi tertentu.
    '''
    if given_condition == 'Obesity':
        title_text = "Most Common Features in Obese Category"
        obesity_class = data[data['class'] == 'Obesity']
        result = {'Label': [], 'Total': []}

        temp_columns_n_category = []

        for col in obesity_class.describe(include='object').columns.drop('class'):
            category_count = obesity_class[col].value_counts()
            most_common_category = category_count.idxmax()
            highest_count = category_count.max()

            result['Label'].append(f"{col.replace('_', ' ').capitalize()} => {most_common_category}")
            result['Total'].append(highest_count)

            temp_columns_n_category.append([col, most_common_category])


        sorted_items = sorted(zip(result['Total'], result['Label']), reverse=True)
        result_sorted = {
            'label': [item[1] for item in sorted_items],
            'proportion': [item[0] for item in sorted_items]
        }

        fig = go.Figure([go.Bar(
            x=result_sorted['proportion'],
            y=result_sorted['label'],
            text=result_sorted['proportion'],
            textposition='outside',
            textfont=dict(size=12),
            orientation='h',
            marker_color=px.colors.qualitative.Set3_r  
        )])

    else:
        title_text = "Probability of Obesity Given Certain Conditions"

        result = {'Label': [], 'Probability': []}
        for col in data.describe(include='object').columns.drop('class'):
            for val in data[col].unique():
                given_cond = data[data[col]==val] #n(B)
                obese = given_cond[given_cond['class']=='Obesity'] #n(AnB)
                prob = len(obese) / len(given_cond) #P(A|B)
                result['Label'].append(f"{col.replace('_', ' ').capitalize()} => {val}")
                result['Probability'].append(prob)

        sorted_items = sorted(zip(result['Probability'], result['Label']), reverse=True)
        top_12 = sorted_items[:12]
        probs,labels = zip(*top_12)

        fig = go.Figure([go.Bar(
            x=probs,
            y=labels,
            text=[f"{p:.1%}" for p in probs],
            textposition='outside',
            textfont=dict(size=12),
            orientation='h',
            marker_color=px.colors.qualitative.Set3_r
        )])

    fig.update_layout(
        title={'text': title_text, 'x': 0.5, 'xanchor': 'center', 'font': {'size': 18}},
        yaxis=dict(autorange='reversed'),  
        height=600,  
        width=1000,  
        margin=dict(l=100, r=50, t=80, b=50),  
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')  
    )

    st.plotly_chart(fig, use_container_width=True)

###################
# INDICATORS      #
###################
def low_prob_indicator(data):
    '''
    Fungsi ini digunakan untuk menampilkan indikator risiko obesitas berdasarkan kategori dengan probabilitas rendah. 
    Fungsi ini mengidentifikasi kategori dengan probabilitas obesitas terendah dan menampilkan indikator dalam bentuk angka persentase.

    **Parameter**:
    - `data`: Data frame yang berisi data untuk analisis.

    **Hasil**:
    - Daftar indikator dengan probabilitas obesitas terendah, masing-masing ditampilkan dalam bentuk angka dan grafik indikator.

    '''
    result = []
    for col in data.describe(include='object').columns.drop('class'):
        for val in data[col].unique():
            given_cond = data[data[col]==val] #n(B)
            obese = given_cond[given_cond['class']=='Obesity'] #n(AnB)
            prob = len(obese) / len(given_cond) #P(A|B)
            result.append([col, val, prob])

    sorted_items = sorted(result, key=lambda x: x[-1], reverse=True)
    low_category = sorted_items[-3:]
    

    figures = []
    for items in low_category:
        cat1 = items[0].replace('_',' ')
        cat2 = items[1].lower()
        probability = round(items[2] * 100,2)

        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="number",
            value=probability,  
            title={
                "text": "<span style='font-size:1.5em;font-weight:bold;'>Risk of Obesity</span><br>"
                        f"<span style='font-size:1.2em;color:lightgray'>If {cat1} is {cat2}</span><br>",
                "align": "center"
            },
            number={"font": {"size": 45}, 'suffix':'%'},  
            domain={'x': [0, 1], 'y': [0, 0.8]}  
        ))

        fig.update_layout(
            font=dict(color='white'),  
            height=200,  
            width=320,
            margin=dict(l=20, r=20, t=30, b=20),  
            shapes=[  
                dict(
                    type="rect",
                    x0=0, y0=0, x1=1, y1=1,  
                    fillcolor="rgba(0, 0, 139, 0.4)",  
                    line=dict(color="lightgray", width=3),  
                    xref="paper", yref="paper",
                    layer="below" 
                )
            ]
        )

        figures.append([cat1, cat2, probability, fig])
    return figures

