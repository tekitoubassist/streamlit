from operator import index
import streamlit as st
import datetime
import calendar
import pandas as pd
import numpy as np

KINlist = ("赤い龍", "白い風", "青い夜", "黄色い種",
            "赤い蛇", "白い世界の橋渡し", "青い手", "黄色い星",
            "赤い月", "白い犬", "青い猿", "黄色い人",
            "赤い空歩く人", "白い魔法使い", "青い鷲", "黄色い戦士",
            "赤い地球", "白い鏡", "青い嵐", "黄色い太陽") #(KINnum - 1) % 20
#KINlist2 = KINlist[(KINnum - 1) // 13 * 13 % 20]
#KINlist3 = f"音{KINnum % 13 + 1}"

STRINGS_LENGTH = 30

def test_app_init():
    st.set_page_config(
        page_title = "ツォルキン計算",
        layout = "wide",
        initial_sidebar_state = "expanded"
    )
    if "count" not in st.session_state:
        st.session_state.count = 2
    if "AD" not in st.session_state:
        st.session_state.AD = ""
    if "KIN" not in st.session_state:
        st.session_state.KIN = ""
    if "birth" not in st.session_state:
        st.session_state.birth = 1

def Get_KIN_num(st_year: int, st_month: int, st_day: int):
    first_date = datetime.date.min
    specified_date = datetime.date(st_year, st_month, st_day)
    AD_date_diff = specified_date - first_date
    KIN_date_diff = AD_date_diff.days
    for i in range(st_year - 1):
        if calendar.isleap(i + 1) == True:
            KIN_date_diff -= 1
    if (calendar.isleap(st_year) == True) and (st_month >= 3):
        KIN_date_diff -= 1
    KIN_num = (KIN_date_diff + 78) % 260
    if KIN_num == 0:
        KIN_num = 260
    return KIN_num

def ADtoKIN_calc(st_year: int, st_month: int, st_day: int, *KIN_data_sel: tuple):
    KIN_num = Get_KIN_num(st_year, st_month, st_day)

    KIN_data = []
    KIN_result = []

    KIN_math = (KIN_num - 1) % 20 + 1
    sound_num = (KIN_num - 1) % 13 + 1
    if len(KIN_data_sel) == 0 or "KIN" in KIN_data_sel: #KIN
        add_KIN_info = ""
        black_KIN_num = [1, 20, 22, 39, 43, 50, 51, 58, 64, 69, 72, 77, 85, 88, 93, 96, 106, 107, 108,
                        109, 110, 111, 112, 113, 114, 115, 146, 147, 148, 149, 150, 151, 152, 153, 154,
                        155, 165, 168, 173, 176, 184, 189, 192, 197, 203, 210, 211, 218, 222, 239, 241, 260]
        if KIN_num % 19 == 0:
            add_KIN_info += " (絶対拡張KIN)"
        if KIN_math in [10, 15, 20]:
            if sound_num in [3, 4, 10, 11]:
                add_KIN_info += " (極性KIN)"
        if KIN_num in black_KIN_num:
            add_KIN_info += " (黒KIN)"
        KIN_data.append("KIN")
        KIN_result.append((str)(KIN_num) + add_KIN_info)
    if len(KIN_data_sel) == 0 or "SC" in KIN_data_sel: #SC
        KIN_data.append("SC")
        KIN_result.append(KINlist[KIN_math - 1].ljust(STRINGS_LENGTH - len(KINlist[KIN_math - 1])))
    if len(KIN_data_sel) == 0 or "WS" in KIN_data_sel: #WS
        KIN_data.append("WS")
        KIN_result.append(KINlist[(KIN_num - 1) // 13 * 13 % 20].ljust(STRINGS_LENGTH - len(KINlist[(KIN_num - 1) // 13 * 13 % 20])))
    if len(KIN_data_sel) == 0 or "銀河の音" in KIN_data_sel: #銀河の音
        KIN_data.append("銀河の音")
        KIN_result.append(f"音{sound_num}".ljust(STRINGS_LENGTH - len(f"音{sound_num}")))
    if len(KIN_data_sel) == 0 or "5つの城" in KIN_data_sel: #5つの城
        KIN_castle_info = ""
        KIN_castle_num = (KIN_num - 1) // 52
        if KIN_castle_num == 0:
            KIN_castle_info = "回転の赤い東の城"
        elif KIN_castle_num == 1:
            KIN_castle_info = "交差の白い北の城"
        elif KIN_castle_num == 2:
            KIN_castle_info = "燃える青い西の城"
        elif KIN_castle_num == 3:
            KIN_castle_info = "与える黄色い南の城"
        else:
            KIN_castle_info = "魅惑の緑の中央の城"
        KIN_data.append("5つの城")
        KIN_result.append(KIN_castle_info.ljust(STRINGS_LENGTH - len(KIN_castle_info)))
    if len(KIN_data_sel) == 0 or "反対KIN" in KIN_data_sel: #反対KIN
        KIN_data.append("反対KIN")
        KIN_result.append(KINlist[(KIN_math + 9) % 20].ljust(STRINGS_LENGTH - len(KINlist[(KIN_math + 9) % 20])))
    if len(KIN_data_sel) == 0 or "類似KIN" in KIN_data_sel: #類似KIN
        KIN_data.append("類似KIN")
        KIN_result.append(KINlist[(38 - KIN_math) % 20].ljust(STRINGS_LENGTH - len(KINlist[(38 - KIN_math) % 20])))
    if len(KIN_data_sel) == 0 or "神秘KIN" in KIN_data_sel: #神秘KIN
        KIN_data.append("神秘KIN")
        KIN_result.append(KINlist[20 - KIN_math].ljust(STRINGS_LENGTH - len(KINlist[20 - KIN_math])))
    if len(KIN_data_sel) == 0 or "ガイドKIN" in KIN_data_sel: #ガイドKIN
        guide_sel = sound_num % 5
        if guide_sel == 1:
            guide_num = KIN_math - 1
            reverse_guide_num = KIN_math - 1
        elif guide_sel == 2:
            guide_num = (KIN_math + 11) % 20
            reverse_guide_num = (KIN_math + 7) % 20
        elif guide_sel == 3:
            guide_num = (KIN_math + 3) % 20
            reverse_guide_num = (KIN_math + 15) % 20
        elif guide_sel == 4:
            guide_num = (KIN_math + 15) % 20
            reverse_guide_num = (KIN_math + 3) % 20
        else:
            guide_num = (KIN_math + 7) % 20
            reverse_guide_num = (KIN_math + 11) % 20
        KIN_data.append("ガイドKIN")
        KIN_result.append(KINlist[guide_num].ljust(STRINGS_LENGTH - len(KINlist[guide_num])))
    if len(KIN_data_sel) == 0 or "逆ガイドKIN" in KIN_data_sel: #逆ガイドKIN
        KIN_data.append("逆ガイドKIN")
        KIN_result.append(KINlist[reverse_guide_num].ljust(STRINGS_LENGTH - len(KINlist[reverse_guide_num])))
    if len(KIN_data_sel) == 0 or "鏡KIN" in KIN_data_sel: #鏡KIN
        KIN_data.append("鏡KIN")
        KIN_result.append(f"{261 - KIN_num} (WS : {KINlist[(28 - KIN_math) % 20]})".ljust(STRINGS_LENGTH - len(f"{261 - KIN_num} (WS : {KINlist[(28 - KIN_math) % 20]})")))

    # return pd.DataFrame({"結果": KIN_result}, index=KIN_data)
    return pd.DataFrame({"内容": KIN_data, "結果": KIN_result})

def Calc_inc():
    if st.session_state.count < 4:
        st.session_state.count += 1

def Cacl_dec():
    if st.session_state.count > 1:
        st.session_state.count -= 1

def Calc_reset():
    st.session_state.count = 2

def test_calc(test, i):
    test = i
    st.write(test)

def test_app():
    test_app_init()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("カレンダーを増やす", on_click=Calc_inc)
    with col2:
        st.button("カレンダーを減らす", on_click=Cacl_dec)
    with col3:
        st.button("リセット", on_click=Calc_reset)
    st.write("カレンダーの数 : ", st.session_state.count)
    st_year = [1980] * st.session_state.count
    st_month = [1] * st.session_state.count
    st_day = [1] * st.session_state.count
    max_day = [31] * st.session_state.count

    #カレンダーの数を表示
    title_col = st.columns(st.session_state.count)
    for i in range(st.session_state.count):
        with title_col[i]:
            st.title(f"カレンダー{i + 1}")
    #入力欄を表示
    input_col = st.columns(3 * st.session_state.count)
    for i in range(st.session_state.count):
        with input_col[i * 3]:
            st_year[i] = int(st.number_input(f"年{i + 1}", min_value=1, max_value=9999, value=1980))
        with input_col[i * 3 + 1]:
            st_month[i] = int(st.number_input(f"月{i + 1}", min_value=1, max_value=12, value=1))
        with input_col[i * 3 + 2]:
            _, max_day[i] = calendar.monthrange(st_year[i], st_month[i])
            st_day[i] = int(st.number_input(f"日{i + 1}", min_value=1, max_value=max_day[i], value=1))
    #計算結果を表示
    output_col = st.columns(st.session_state.count)
    for i in range(st.session_state.count):
        st.session_state.birth = f"{st_year[i]}年{st_month[i]}月{st_day[i]}日"
        st.session_state.KIN = ADtoKIN_calc(st_year[i], st_month[i], st_day[i])
        st.session_state.KIN.index = st.session_state.KIN["内容"]
        st.session_state.KIN = st.session_state.KIN.drop(columns="内容")
        with output_col[i]:
            st.subheader(st.session_state.birth)
            st.table(st.session_state.KIN)
            #起承転結
            KIN_story_list = []
            KIN_story = ["起", "承", "転", "結"]
            KIN_num = (Get_KIN_num(st_year[i], st_month[i], st_day[i]) - 1) % 20
            for _i in range(4):
                if "赤い" in KINlist[KIN_num]:
                    KIN_story_list.append(KINlist[KIN_num])
                    KIN_num = (KIN_num + 5) % 20
                    KIN_story_list.append(KINlist[KIN_num])
                    KIN_num = (KIN_num + 5) % 20
                    KIN_story_list.append(KINlist[KIN_num])
                    KIN_num = (KIN_num + 5) % 20
                    KIN_story_list.append(KINlist[KIN_num])
                    break
                else:
                    KIN_num = (KIN_num + 5) % 20
            KIN_story_df = pd.DataFrame({"起承転結": KIN_story_list}, index=KIN_story)
            st.table(KIN_story_df)
            #個人KIN年表
            personal_KIN_list_df = pd.DataFrame(np.arange(315).reshape(105, 3))
            # personal_KIN_list_df = pd.DataFrame()
            personal_KIN_date = []
            for j in range(105):
                personal_KIN_df = ADtoKIN_calc(st_year[i] + j, st_month[i], st_day[i], "SC", "WS", "銀河の音")
                personal_KIN_list = personal_KIN_df["結果"].tolist()
                personal_KIN_date.append(f"{st_year[i] + j}年{st_month[i]}月{st_day[i]}日")
                personal_KIN_list_df.loc[j] = personal_KIN_list
            personal_KIN_list_df.index = personal_KIN_date
            personal_KIN_list_df.columns = ["SC", "WS", "銀河の音"]
            st.dataframe(personal_KIN_list_df)

if __name__ == "__main__":
    test_app()

# streamlit run (このファイルの名前).py