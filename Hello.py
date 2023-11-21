# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    
        st.set_page_config(
        page_title="高齢者の運転免許返納",
        page_icon="🚗",
    )

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    st.title("Data visualization on driver's license return")

    st.header("Data", divider="gray")
    
    df = pd.read_csv("事故統計R3.csv")
    df = df.rename(columns={'発生場所緯度': 'lat', '発生場所経度': 'lon'})
    st.markdown("data : Accident Statistics in Fukuoka, 2021.")
    st.markdown('''Data Points: Each row seems to represent a distinct accident, with details about when and where it occurred, the nature of the accident, and the parties involved.  
                Accident Types: The '事故内容' column indicates the nature of the accident, with entries like "負傷" suggesting injuries.  
                Time and Location: The data includes specific times and geographic coordinates for each accident, which could be useful for spatial and temporal analysis.  
                Demographics: Age groups of the parties involved in the accidents are provided, which could be useful for demographic analysis.  
                Weather and Road Conditions: Information about the weather and road conditions at the time of each accident is included, which could be relevant for understanding the factors contributing to these incidents.''')
    st.dataframe(df)
    # Streamlitアプリケーションの設定
    ####年齢別事故の発生数####
    
    st.header('1. Number of accidents by age group', divider='gray')
    st.markdown('''Number of traffic accidents in Fukuoka Prefecture in 2021 by age group of the parties involved''')

    # 年齢層のカテゴリーをマッピング
    age_category_mapping = {
        '24歳以下': '24 and below',
        '25～34': '25-34',
        '35～44': '35-44',
        '45～54': '45-54',
        '55～64': '55-64',
        '65～74': '65-74',
        '75歳以上': '75 and above'
    }
    df['Age Group (Party A)'] = df['年齢（当事者A）'].map(age_category_mapping)

    # 年齢層ごとに事故件数を集計
    age_group_counts = df['Age Group (Party A)'].value_counts()

    # 可視化
    age_order = ['24 and below', '25-34', '35-44', '45-54', '55-64', '65-74', '75 and above']
    plt.figure(figsize=(10, 6))
    palette = sns.color_palette("coolwarm", len(age_order))
    sns.barplot(x=age_group_counts.index, y=age_group_counts.values, order=age_order, palette = palette)
    plt.title('Number of accidents by age group of parties involved in Fukuoka Prefecture')
    plt.xlabel('Age')
    plt.ylabel('Number of accidents')
    plt.xticks(rotation=45)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    ####年齢別事故率####
    st.header("2. Accident Rate as a Percentage of Licenses Held by Age Group", divider='gray')
    st.markdown('''Apart from accident statistics, we found the number of license holders living in Fukuoka Prefecture as of 2021 based on driver's license statistics published by the National Police Agency.  
                Based on this, we visualized how many license holders in each age group would have accidents in 2021. This is the graph.''')
    license_data = {
        'age_group': ['16-24', '25-34', '35-44', '45-54', '55-64', '65-74', 'over 75'],
        'license_count': [75608, 472998, 617440, 691151, 531731, 535771, 219221]
    }

    # DataFrameに変換
    license_df = pd.DataFrame(license_data)

    # 事故発生件数のデータ（事故統計からの集計）
    # ここでは事故データはすでに読み込まれていると仮定
    accident_counts = df['年齢（当事者A）'].value_counts()

    # 事故発生件数を年齢層に合わせて集計（例として、年齢層のラベルを合わせる）
    # 注意: 事故データの年齢層のラベルが異なる場合は、適宜調整が必要
    accident_counts_relabel = {
        '16-24': accident_counts.get('24歳以下', 0),
        '25-34': accident_counts.get('25～34', 0),
        '35-44': accident_counts.get('35～44', 0),
        '45-54': accident_counts.get('45～54', 0),
        '55-64': accident_counts.get('55～64', 0),
        '65-74': accident_counts.get('65～74', 0),
        'over 75': accident_counts.get('75歳以上', 0)
    }

    # 事故率の計算
    license_df['accident_count'] = license_df['age_group'].map(accident_counts_relabel)
    license_df['accident_rate'] = (license_df['accident_count'] / license_df['license_count']) * 100

    # 事故率の可視化
    plt.figure(figsize=(10, 6))
    plt.bar(license_df['age_group'], license_df['accident_rate'], color='orange')
    plt.title('Accident Rates by Age Group')
    plt.xlabel('Age group')
    plt.ylabel('Accident Rate（%）')
    
    st.pyplot()

    st.markdown('''Accidents caused by novice drivers appear as a higher percentage than those caused by elderly drivers. However, accidents by older drivers also appear to be more common than for other age groups.  
            The numbers alone were unclear, but the percentages suggest that first-time drivers and the elderly are causing more accidents.''')

    ###当事者年齢別重大事故の割合###
    st.header("Percentage of Serious Accidents by Age of Parties", divider="gray")
    st.text("How about SERIOUS accidents?")
    st.markdown('''Here, Accidents resulting in **fatalities** were defined as "serious accidents.''')

    from PIL import Image

    st.image('.Images/図1.png', caption='Age composition of parties involved in fatal accidents in 2021')

    st.markdown('''In 2021, there were 98 fatal accidents in Fukuoka Prefecture.  
                Seven of these, or 7%, were accidents involving persons aged 75 or older, and 24, or 25% of the total, if those aged 65 or older are included.  
                However, the 22% of those aged 55 to 64 is a figure that cannot be ignored. This graph shows that even if you are not elderly, you should not let your guard down.''')


    ######マッピング######
    st.header("Locations of traffic accidents in Fukuoka")
    st.markdown('''this is a map that shows locations of the accidents''')
    # 緯度経度データのみを抽出
    locations = df[['lat', 'lon']]
    locations = locations.dropna()  # NaN値を削除

    # マップにプロット
    st.map(locations, color='#ffa500', size=60)


    #####75歳以上の交通事故発生場所#####
    import pydeck as pdk
    #75歳以上の当事者を含む事故のデータ
    over_75_accidents = df[df['Age Group (Party A)'] == '75 and above']
    over_75_locations = over_75_accidents[['lat', 'lon']].dropna()
    # その他の事故のデータ
    other_accidents = df[df['Age Group (Party A)'] != '75 and above']
    other_locations = other_accidents[['lat', 'lon']].dropna()
    
    # Pydeckを用いて地図にプロット
    view_state = pdk.ViewState(latitude=df['lat'].mean(), longitude=df['lon'].mean(), zoom=10)
    layer1 = pdk.Layer(
        "ScatterplotLayer",
        other_locations,
        get_position='[lon, lat]',
        get_color='[255, 165, 0, 128]',
        get_radius=300,
    )
    layer2 = pdk.Layer(
        "ScatterplotLayer",
        over_75_locations,
        get_position='[lon, lat]',
        get_color='[200, 30, 0, 160,]',  
        get_radius=300,
    )
    st.markdown('''Red plot represents the accidents by people over 75''')
    st.pydeck_chart(pdk.Deck(map_style=None,layers=[layer1, layer2], initial_view_state=view_state))

    st.title('')







if __name__ == "__main__":
    run()
