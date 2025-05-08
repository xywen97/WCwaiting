import streamlit as st
import time
import numpy as np
from toilet_sim import ToiletSimStep

st.title("男女厕所排队仿真与可视化")

# 添加时间随机性控制
st.sidebar.header("时间随机性设置")
enable_time_variation = st.sidebar.checkbox("启用时间随机性", value=False)
time_variation_std = st.sidebar.slider("时间波动标准差（秒）", 1, 30, 5, disabled=not enable_time_variation)

params = {
    'n_male': st.slider('男厕坑位数', 1, 10, 3),
    'n_female': st.slider('女厕坑位数', 1, 10, 3),
    'arrival_interval': st.slider('平均到达间隔（秒）', 5, 60, 20),
    'female_ratio': st.slider('女性比例', 0.1, 0.9, 0.5),
    'male_pee_time': st.slider('男小便平均时间（秒）', 10, 120, 20),
    'male_poop_time': st.slider('男大便平均时间（秒）', 30, 1800, 60),
    'male_poop_prob': st.slider('男大便概率', 0.05, 0.3, 0.1),
    'female_pee_time': st.slider('女小便平均时间（秒）', 20, 300, 40),
    'female_poop_time': st.slider('女大便平均时间（秒）', 60, 1800, 90),
    'female_poop_prob': st.slider('女大便概率', 0.05, 0.3, 0.1),
    'sim_time': st.slider('仿真总时长（秒）', 600, 18000, 3600),
    'enable_time_variation': enable_time_variation,
    'time_variation_std': time_variation_std
}

if st.button('开始仿真'):
    sim = ToiletSimStep(params['n_male'], params['n_female'], params)
    status_placeholder = st.empty()
    queue_placeholder = st.empty()
    while not sim.finished:
        sim.step()
        status = sim.get_status()
        # 显示坑位状态
        with status_placeholder.container():
            st.write(f"当前时间: {status['now']:.1f} 秒")
            st.write("男厕坑位状态：")
            cols = st.columns(params['n_male'])
            for i, s in enumerate(status['male_status']):
                cols[i].write("占用" if s else "空闲")
            st.write("女厕坑位状态：")
            cols = st.columns(params['n_female'])
            for i, s in enumerate(status['female_status']):
                cols[i].write("占用" if s else "空闲")
        # 显示队伍长度
        with queue_placeholder.container():
            st.metric("男厕排队人数", status['male_queue_len'])
            st.metric("女厕排队人数", status['female_queue_len'])
        time.sleep(0.05)
    st.success("仿真结束！") 