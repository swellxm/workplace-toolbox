import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Excel全能处理工具", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .page-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #11998e;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #666;
        margin-bottom: 2rem;
    }
    .upload-zone {
        border: 2px dashed #11998e;
        border-radius: 12px;
        padding: 3rem;
        text-align: center;
        background: #f0fdfb;
    }
    .result-box {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

if "df" not in st.session_state:
    st.session_state.df = None
if "processed_df" not in st.session_state:
    st.session_state.processed_df = None

st.markdown("### 📊 Excel 全能处理工具")
st.markdown("---")

col_left, col_main = st.columns([1, 3], gap="large")

with col_left:
    st.markdown("**📤 上传文件**")
    uploaded_file = st.file_uploader(
        "选择 Excel 文件",
        type=['xlsx', 'xls', 'csv'],
        help="支持 .xlsx, .xls, .csv 格式"
    )

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            st.success(f"✅ 已加载: {uploaded_file.name}")
            st.info(f"📊 数据规模: {df.shape[0]} 行 × {df.shape[1]} 列")
        except Exception as e:
            st.error(f"❌ 读取失败: {str(e)}")

    st.markdown("---")
    st.markdown("**⚙️ 选择处理功能**")

    function_options = {
        "一键去重": "dedup",
        "分类汇总": "summary",
        "数据可视化": "chart",
        "表格拆分": "split",
        "表格合并": "merge",
        "格式转换": "convert"
    }

    selected_func = st.radio(
        "请选择功能",
        options=list(function_options.keys()),
        index=0,
        label_visibility="collapsed"
    )

with col_main:
    if st.session_state.df is not None:
        df = st.session_state.df

        st.markdown("**📋 数据预览（前20行）**")
        st.dataframe(df.head(20), use_container_width=True, height=300)

        func_key = function_options[selected_func]

        if func_key == "dedup":
            st.markdown("---")
            st.markdown("### 🗑️ 一键去重")

            col1, col2 = st.columns(2)
            with col1:
                keep_option = st.selectbox(
                    "重复时保留",
                    options=["first", "last"],
                    format_func=lambda x: "保留首次出现" if x == "first" else "保留最后出现"
                )

            if st.button("🚀 开始去重", use_container_width=True):
                processed_df = df.drop_duplicates(keep=keep_option)
                st.session_state.processed_df = processed_df

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("原始行数", df.shape[0])
                with col2:
                    st.metric("去重后行数", processed_df.shape[0])

                removed = df.shape[0] - processed_df.shape[0]
                if removed > 0:
                    st.success(f"✅ 已删除 {removed} 条重复数据")
                else:
                    st.info("📋 数据中没有重复行")

        elif func_key == "summary":
            st.markdown("---")
            st.markdown("### 📈 分类汇总")

            col1, col2, col3 = st.columns(3)
            with col1:
                group_col = st.selectbox("分组字段", options=df.columns.tolist())

            with col2:
                value_col = st.selectbox("汇总字段", options=df.select_dtypes(include=['number']).columns.tolist())

            with col3:
                agg_func = st.selectbox(
                    "汇总方式",
                    options=["sum", "count", "mean", "max", "min"],
                    format_func=lambda x: {"sum": "求和", "count": "计数", "mean": "平均值", "max": "最大值", "min": "最小值"}[x]
                )

            if st.button("🚀 生成汇总", use_container_width=True):
                summary_df = df.groupby(group_col)[value_col].agg(agg_func).reset_index()
                summary_df.columns = [group_col, f"{value_col}_{agg_func}"]
                st.session_state.processed_df = summary_df
                st.dataframe(summary_df, use_container_width=True)

        elif func_key == "chart":
            st.markdown("---")
            st.markdown("### 📊 数据可视化")

            col1, col2 = st.columns(2)
            with col1:
                chart_type = st.selectbox("图表类型", options=["bar", "line", "pie"], format_func=lambda x: {"bar": "柱状图", "line": "折线图", "pie": "饼图"}[x])

            with col2:
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                if numeric_cols:
                    value_col = st.selectbox("数值字段", options=numeric_cols)

            if chart_type in ["bar", "line"]:
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                if categorical_cols:
                    category_col = st.selectbox("分类字段", options=categorical_cols)

                    if st.button("🚀 生成图表", use_container_width=True):
                        if chart_type == "bar":
                            fig = px.bar(df, x=category_col, y=value_col, title=f"{category_col} - {value_col} 柱状图")
                        else:
                            fig = px.line(df, x=category_col, y=value_col, title=f"{category_col} - {value_col} 折线图", markers=True)

                        st.plotly_chart(fig, use_container_width=True)
                        st.session_state.processed_df = df

            elif chart_type == "pie":
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                if categorical_cols and numeric_cols:
                    category_col = st.selectbox("分类字段", options=categorical_cols)

                    if st.button("🚀 生成图表", use_container_width=True):
                        fig = px.pie(df, names=category_col, values=value_col, title=f"{category_col} 占比分布")
                        st.plotly_chart(fig, use_container_width=True)
                        st.session_state.processed_df = df

        elif func_key == "split":
            st.markdown("---")
            st.markdown("### ✂️ 表格拆分")

            col1, col2 = st.columns(2)
            with col1:
                split_col = st.selectbox("按此列拆分", options=df.columns.tolist())

            with col2:
                split_mode = st.selectbox("拆分方式", options=["by_value", "by_count"], format_func=lambda x: {"by_value": "按列值分组", "by_count": "均分行数"}[x])

            if split_mode == "by_count":
                rows_per_file = st.number_input("每个文件行数", min_value=10, max_value=10000, value=100)
            else:
                rows_per_file = None

            if st.button("🚀 开始拆分", use_container_width=True):
                if split_mode == "by_value":
                    unique_values = df[split_col].unique()
                    st.success(f"📋 将拆分为 {len(unique_values)} 个文件")

                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        for value in unique_values:
                            subset = df[df[split_col] == value]
                            sheet_name = str(value)[:31]
                            subset.to_excel(writer, sheet_name=sheet_name, index=False)

                    output.seek(0)
                    st.download_button(
                        label="📥 下载拆分后的Excel",
                        data=output,
                        file_name="拆分结果.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                else:
                    n_splits = len(df) // rows_per_file + (1 if len(df) % rows_per_file else 0)
                    st.success(f"📋 将拆分为 {n_splits} 个文件")

                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        for i in range(n_splits):
                            start_idx = i * rows_per_file
                            end_idx = min((i + 1) * rows_per_file, len(df))
                            subset = df.iloc[start_idx:end_idx]
                            subset.to_excel(writer, sheet_name=f"第{i+1}页", index=False)

                    output.seek(0)
                    st.download_button(
                        label="📥 下载拆分后的Excel",
                        data=output,
                        file_name="拆分结果.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

        elif func_key == "merge":
            st.markdown("---")
            st.markdown("### 🔗 表格合并")

            st.info("👆 请在上方上传多个Excel文件进行合并（当前仅支持单文件预览）")

            if st.button("🚀 合并文件", use_container_width=True, disabled=True):
                pass

        elif func_key == "convert":
            st.markdown("---")
            st.markdown("### 🔄 格式转换")

            col1, col2 = st.columns(2)
            with col1:
                target_format = st.selectbox("目标格式", options=["xlsx", "csv"], format_func=lambda x: f"转换为 {x.upper()}")

            if st.button("🚀 开始转换", use_container_width=True):
                output = BytesIO()

                if target_format == "csv":
                    df.to_csv(output, index=False, encoding='utf-8-sig')
                    output.seek(0)
                    st.download_button(
                        label="📥 下载 CSV 文件",
                        data=output,
                        file_name="转换结果.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    df.to_excel(output, index=False, engine='openpyxl')
                    output.seek(0)
                    st.download_button(
                        label="📥 下载 Excel 文件",
                        data=output,
                        file_name="转换结果.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

        if st.session_state.processed_df is not None and func_key not in ["chart", "merge"]:
            st.markdown("---")
            st.markdown("### 📥 下载结果")

            result_df = st.session_state.processed_df

            col1, col2 = st.columns(2)
            with col1:
                output = BytesIO()
                result_df.to_excel(output, index=False, engine='openpyxl')
                output.seek(0)
                st.download_button(
                    label="📥 下载为 Excel",
                    data=output,
                    file_name="处理结果.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            with col2:
                output_csv = BytesIO()
                result_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
                output_csv.seek(0)
                st.download_button(
                    label="📥 下载为 CSV",
                    data=output_csv,
                    file_name="处理结果.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    else:
        st.markdown("""
        <div class="upload-zone">
            <h3>👆 请上传 Excel 文件开始处理</h3>
            <p>支持 .xlsx, .xls, .csv 格式</p>
            <p>文件大小建议不超过 50MB</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
if st.button("← 返回首页", use_container_width=False):
    st.switch_page("app.py")
