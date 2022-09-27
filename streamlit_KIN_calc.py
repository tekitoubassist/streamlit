import streamlit as st
import datetime
import calendar
import pandas as pd

calc_KIN = 0

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
    if "range" not in st.session_state:
        st.session_state.range = 15

def ADtoKIN_calc(st_year: int, st_month: int, st_day: int, st_range: int):
    global calc_KIN
    KINlist = ["赤い龍", "白い風", "青い夜", "黄色い種",
                "赤い蛇", "白い世界の橋渡し", "青い手", "黄色い星",
                "赤い月", "白い犬", "青い猿", "黄色い人",
                "赤い空歩く人", "白い魔法使い", "青い鷲", "黄色い戦士",
                "赤い地球", "白い鏡", "青い嵐", "黄色い太陽"] #(KINnum - 1) % 20
    #KINlist2 = KINlist[(KINnum - 1) // 13 * 13 % 20]
    #KINlist3 = f"音{KINnum % 13 + 1}"

    KIN_data = []
    KIN_result = []
    AD_data = []
    AD_result = []

    first_date = datetime.date.min
    max_date = datetime.date.max
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
    calc_KIN = KIN_num
    KIN_math = (KIN_num - 1) % 20 + 1
    sound_num = (KIN_num - 1) % 13 + 1
    add_KIN_info = ""
    KIN_castle_info = ""
    KIN_castle_num = (KIN_num - 1) // 52
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
    KIN_result.append((str)(KIN_num) + add_KIN_info) #KIN
    KIN_data.append("SC")
    KIN_result.append(KINlist[KIN_math - 1]) #SC
    KIN_data.append("WS")
    KIN_result.append(KINlist[(KIN_num - 1) // 13 * 13 % 20]) #WS
    KIN_data.append("銀河の音")
    KIN_result.append(f"音{sound_num}") #銀河の音
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
    KIN_result.append(KIN_castle_info) #5つの城
    KIN_data.append("反対KIN")
    KIN_result.append(KINlist[(KIN_math + 9) % 20]) #反対KIN
    KIN_data.append("類似KIN")
    KIN_result.append(KINlist[(38 - KIN_math) % 20]) #類似KIN
    KIN_data.append("神秘KIN")
    KIN_result.append(KINlist[20 - KIN_math]) #神秘KIN
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
    KIN_result.append(KINlist[guide_num]) #ガイドKIN
    KIN_data.append("逆ガイドKIN")
    KIN_result.append(KINlist[reverse_guide_num]) #逆ガイドKIN
    KIN_data.append("鏡KIN")
    KIN_result.append(f"{261 - KIN_num} (WS : " + KINlist[(28 - KIN_math) % 20] + ")") #鏡KIN

    date_diff_cnt = KIN_date_diff
    date_cnt = specified_date
    for i in range(st_range + 1):
        if date_diff_cnt > 260:
            if i > 0:
                date_diff_cnt -= 260
                if calendar.isleap(date_cnt.year) == True:
                    if not((date_cnt.month >= 11) and ((date_cnt.month == 12) or (date_cnt.day >= 16))):
                        if date_cnt.month >= 3:
                            date_cnt -= datetime.timedelta(1)
                date_cnt -= datetime.timedelta(260)
                if date_diff_cnt <= 260:
                    break
        else:
            break

    specified_date_month = specified_date.month
    specified_date_day = specified_date.day
    date_cnt_year = date_cnt.year
    date_cnt_month = date_cnt.month
    date_cnt_day = date_cnt.day
    if specified_date == date_cnt:
        if calendar.isleap(f"     {date_cnt_year}     ") == True:
            if (date_cnt_month == 2) and (date_cnt_day == 29):
                AD_result.append(f"     {specified_date}     ")
                AD_data.append(" 誕生日 ")
                date_cnt += datetime.timedelta(1)
                AD_result.append(f"     {date_cnt}     ")
                AD_data.append(" 翌日 ")
            elif (date_cnt_month == 3) and (date_cnt_day == 1):
                AD_result.append(f"     {datetime.date(date_cnt_year, 2, 29)}     ")
                AD_data.append(" 前日 ")
                AD_result.append(f"     {specified_date}     ")
                AD_data.append(" 誕生日 ")
            else:
                AD_result.append(f"     {date_cnt}     ")
                AD_data.append(" 誕生日 ")
        else:
            AD_result.append(f"     {date_cnt}     ")
            AD_data.append(" 誕生日 ")
    else:
        if calendar.isleap(date_cnt_year) == True:
            if (date_cnt_month == 2) and (date_cnt_day == 29):
                AD_result.append(f"     {date_cnt}     ")
                AD_data.append(f" {- i}周期 ")
                date_cnt += datetime.timedelta(1)
            elif (date_cnt_month == 3) and (date_cnt_day == 1):
                AD_result.append(f"     {datetime.date(date_cnt_year, 2, 29)}     ")
                AD_data.append(f" {- i}周期 ")
        AD_result.append(f"     {date_cnt}     ")
        AD_data.append(f" {- i}周期 ")
    date_lim = max_date- date_cnt
    for j in range(st_range + i):
        if date_lim.days > 260:
            date_cnt += datetime.timedelta(260)
            date_cnt_year = date_cnt.year
            date_cnt_month = date_cnt.month
            date_cnt_day = date_cnt.day
            date_lim = max_date - date_cnt
            if (specified_date == date_cnt) or (specified_date == (date_cnt + datetime.timedelta(1))):
                if calendar.isleap(date_cnt_year) == True:
                    if (specified_date_month == 2) and (specified_date_day == 29):
                        AD_result.append(f"     {specified_date}     ")
                        AD_data.append(" 誕生日 ")
                        date_cnt += datetime.timedelta(1)
                        AD_result.append(f"     {date_cnt}     ")
                        AD_data.append(" 翌日 ")
                    elif specified_date_month >= 3:
                        if (specified_date_month == 3) and (specified_date_day == 1):
                            AD_result.append(f"     {date_cnt}     ")
                            AD_data.append(" 前日 ")
                            AD_result.append(f"     {specified_date}     ")
                            AD_data.append(" 誕生日 ")
                            date_cnt += datetime.timedelta(1)
                        else:
                            if not((date_cnt_month >= 11) and ((date_cnt_month == 12) or (date_cnt_day >= 16))):
                                date_cnt += datetime.timedelta(1)
                            AD_result.append(f"     {date_cnt}     ")
                            AD_data.append(" 誕生日 ")
                    else:
                        AD_result.append(f"     {date_cnt}     ")
                        AD_data.append(" 誕生日 ")
                else:
                    AD_result.append(f"     {date_cnt}     ")
                    AD_data.append(" 誕生日 ")
            else:
                if calendar.isleap(date_cnt_year) == True:
                    if (date_cnt_month == 2) and (date_cnt_day == 29):
                        AD_result.append(f"     {date_cnt}     ")
                        AD_data.append(f" {j - i + 1}周期 ")
                        date_cnt += datetime.timedelta(1)
                        AD_result.append(f"     {date_cnt}     ")
                        AD_data.append(f" {j - i + 1}周期 ")
                    elif date_cnt_month >= 3:
                        if (date_cnt_month == 3) and (date_cnt_day == 1):
                            AD_result.append(f"     {datetime.date(date_cnt_year, 2, 29)}     ")
                            AD_data.append(f" {j - i + 1}周期 ")
                            AD_result.append(f"     {date_cnt}     ")
                            AD_data.append(f" {j - i + 1}周期 ")
                            date_cnt += datetime.timedelta(1)
                        else:
                            if not((date_cnt_month >= 11) and ((date_cnt_month == 12) or (date_cnt_day >= 16))):
                                date_cnt += datetime.timedelta(1)
                            AD_result.append(f"     {date_cnt}     ")
                            AD_data.append(f" {j - i + 1}周期 ")
                    else:
                        AD_result.append(f"     {date_cnt}     ")
                        AD_data.append(f" {j - i + 1}周期 ")
                else:
                    AD_result.append(f"     {date_cnt}     ")
                    AD_data.append(f" {j - i + 1}周期 ")
        else:
            break

    KIN_df = pd.DataFrame({"結果": KIN_result}, index=KIN_data)
    st.session_state.KIN = KIN_df
    AD_df = pd.DataFrame({"日付": AD_result}, index=AD_data)
    st.session_state.AD = AD_df
    st.session_state.birth = f"{st_year}年{st_month}月{st_day}日生まれの人の計算結果"
    st.session_state.range = f"ツォルキン周期対応表(±{st_range}周期)"
    # KIN_list, AD_list = st.columns(2)
    # with KIN_list:
    #   st.subheader(f"{st_year}年{st_month}月{st_day}日生まれの人の計算結果")
    #   st.table(KIN_df)
    # with AD_list:
    #   st.subheader(f"ツォルキン周期対応表(±{st_range}周期)")
    #   st.dataframe(AD_df)

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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("カレンダーを増やす", on_click=Calc_inc)
    with col2:
        st.button("カレンダーを減らす", on_click=Cacl_dec)
    with col3:
        st.button("リセット", on_click=Calc_reset)
    with col4:
        st_range = int(st.number_input("範囲", min_value=1, max_value=4000, value=15))
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
    output_col = st.columns(2 * st.session_state.count)
    for i in range(st.session_state.count):
        ADtoKIN_calc(st_year[i], st_month[i], st_day[i], st_range)
        with output_col[i * 2]:
            # st.subheader(st.session_state.birth)
            st.table(st.session_state.KIN)
        with output_col[i * 2 + 1]:
            # st.subheader(st.session_state.range)
            st.dataframe(st.session_state.AD)

    # for i in range(st.session_state.count):
    #   st.title(f"カレンダー{i + 1}")
    #   input_year, input_month, input_day, input_range = st.columns(4)
    #   with input_year:
    #     st_year[i] = int(st.number_input("年", min_value=1, max_value=9999, value=1980))
    #   with input_month:
    #     st_month[i] = int(st.number_input("月", min_value=1, max_value=12, value=1))
    #   with input_day:
    #     _, max_day[i] = calendar.monthrange(st_year[i], st_month[i])
    #     st_day[i] = int(st.number_input("日", min_value=1, max_value=max_day[i], value=1))
    #   with input_range:
    #     st_range[i] = int(st.number_input("範囲", min_value=1, max_value=4000, value=15))
    #   ADtoKIN_calc(st_year[i], st_month[i], st_day[i], st_range[i])

if __name__ == "__main__":
    test_app()

# streamlit run streamlit_test.py