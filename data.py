#streamlit run data.py    体现代码的复用
#核心是 “主程序只做‘调用 + 优化 + 展示’，stepxx.py 只做‘核心逻辑 + 返回原始结果’
import streamlit as st
import step1  # 关键：导入step1模块，无需拷贝step1的代码
import pandas as pd

step1_code='''
# -*- coding: utf-8 -*-
#1.读取“申万行业分类.xlsx”表，字段如下所示：
# 行业名称	股票代码	股票名称
# 获得“家用电器”行业的所有上市公司股票代码和股票简称
# 结果用序列Fs来表示，其中index为股票代码、值为股票简称
def return_values():
    # 读取Excel文件
    import pandas as pd
    A = pd.read_excel('申万行业分类.xlsx')
    
    # 筛选出“家用电器”行业的记录
    # 注意：确保字段名与Excel中的实际列名一致，如果有空格或其他字符需要对应调整
    home_appliance = A[A['行业名称'] == '家用电器']
    
    # 构建指定格式的序列：index为股票代码，值为股票名称
    Fs = pd.Series(
        data=home_appliance['股票名称'].values,  # 序列的值为股票名称
        index=home_appliance['股票代码'].values   # 序列的索引为股票代码
    )
        
    return Fs

'''
st.set_page_config(
            page_title="46_杨炎梅",  # 页面标题
            layout='wide',
        )

with st.sidebar:
     st.subheader('请选择实验')
     List=['1.申万家用电器行业股票代码获取',
           '2.申万家用电器行业股票财务指标数据获取',
           '3.申万家用电器行业股票财务指标数据处理',
           '4.申万家用电器行业股票财务指标数据主成分分析',
           '5.申万家用电器行业股票日交易数据获取',
           '6.申万家用电器行业股票交易指数的构造',
           '7.计算沪深300指数2014-2017年的年涨跌幅指标',
           '8.计算获得沪深300指数2016年收盘指数的关键转折点',
           '9.计算沪深300指数2016年10、20、30、60日收盘指数移动平均值',
           '10.计算沪深300指数2016年现价指标']
     nm=st.selectbox(" ",List)

if nm=='申万家用电器行业股票代码获取':
   st.subheader('作品提交要求')
   st.markdown('1.页面标题采用“学号后两位_姓名命名')
   st.markdown('2.List选择列表为10个实验名称')
   st.markdown('3.各关卡的通过代码，建议通过文件函数直接读取stepxx.py这个文件，不用直接拷贝到程序文件')
   st.markdown('4.各实验关卡的结果，要优化其展示结果，比如第1关的返回结果为序列，需要调整为数据框方便展示，比如5、6、8、9实验关卡，不仅要返回数据，还要将数据进行可视化绘图')
   st.markdown('5.优化结果展示的代码，也在界面展示，显示为优化的程序代码')
   st.subheader('代码')
   st.code(step1_code,language='python')
   st.subheader('结果')
   r=step1.return_values()
   st.dataframe(pd.DataFrame({'股票代码':list(r.index),'股票简称':r.values}))
   
   # 2. 展示 step1.py 的核心代码（关键：直接读取文件，不手动拷贝）
   st.subheader('核心代码（step1.py）')
   try:
        # 读取step1.py文件的内容
        with open('step1.py', 'r', encoding='utf-8') as f:
            step1_code = f.read()
        st.code(step1_code, language='python')  # 语法高亮展示代码
   except FileNotFoundError:
        st.error('未找到step1.py文件，请确保该文件与主程序在同一文件夹下')
    
    # 3. 调用step1的核心函数，获取原始结果（序列）
   st.subheader('实验结果（优化后展示）')
   try:
        # 主程序不写核心逻辑，直接调用step1.return_values()
        original_series = step1.return_values()  # 原始结果：pd.Series
        
        # 4. 结果优化（主程序负责，序列转DataFrame
        # 将序列的index（股票代码）和values（股票名称）转为DataFrame的两列
        optimized_df = pd.DataFrame({
            '股票代码': original_series.index.astype(str).str.zfill(6),  # 股票代码转6位字符串（补前导0）
            '股票简称': original_series.values
        }).reset_index(drop=True)  # 重置索引，避免重复
        
        # 5. 展示优化后的结果（用st.dataframe，支持排序、筛选）
        st.dataframe(optimized_df, use_container_width=True)
        
        # 额外：展示结果统计信息（提升用户体验）
        st.success(f'✅ 共查询到 {len(optimized_df)} 只家用电器行业股票')
        
        # 6. 展示“结果优化的代码”（按要求显示优化逻辑）
        st.subheader('结果优化代码')
        optimize_code = '''
# 原始结果：index为股票代码、值为股票名称的pd.Series
original_series = step1.return_values()

# 优化逻辑：序列转DataFrame，股票代码补全为6位字符串
optimized_df = pd.DataFrame({
    '股票代码': original_series.index.astype(str).str.zfill(6),  # 避免0开头股票代码被截断
    '股票简称': original_series.values
}).reset_index(drop=True)
        '''
        st.code(optimize_code, language='python')
    
   except Exception as e:
        st.error(f'❌ 实验运行失败：{str(e)}')

# 后续实验（2-10关）按此逻辑扩展：
# elif selected_experiment == '申万家用电器行业股票财务指标数据获取':
#     import step2
#     st.subheader('核心代码（step2.py）')
#     读取step2.py代码并展示
#     调用step2.xxx()获取原始财务数据
#     主程序优化结果（如筛选、去重）
#     展示优化后的DataFrame
# 
# elif selected_experiment == '申万家用电器行业股票财务指标数据处理':
#     import step3
#     ... 以此类推
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
    