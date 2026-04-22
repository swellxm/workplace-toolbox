import streamlit as st

st.set_page_config(
    page_title="职场提效工具箱",
    page_icon="🧰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        padding: 1rem 0;
        color: #1f77b4;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .tool-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        transition: transform 0.3s ease;
        cursor: pointer;
        height: 100%;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .tool-card:hover {
        transform: translateY(-5px);
    }
    .tool-card.excel {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .tool-card.file {
        background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
    }
    .tool-card.content {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .tool-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    .tool-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .tool-desc {
        font-size: 0.95rem;
        opacity: 0.9;
    }
    .tool-features {
        text-align: left;
        margin-top: 1rem;
        font-size: 0.85rem;
        opacity: 0.85;
    }
    .tool-features li {
        margin: 0.3rem 0;
    }
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #888;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🧰 职场提效工具箱</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">面向全行业职场人的轻量化提效工具，零门槛、3秒出结果</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="tool-card excel">
        <div class="tool-icon">📊</div>
        <div class="tool-title">Excel 全能处理</div>
        <div class="tool-desc">一键完成专业数据处理</div>
        <ul class="tool-features">
            <li>✓ 去重 / 分类汇总</li>
            <li>✓ 数据可视化图表</li>
            <li>✓ 表格拆分 / 合并</li>
            <li>✓ 格式转换 (xlsx/csv)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("立即使用", key="excel_btn", use_container_width=True):
        st.switch_page("pages/excel_tools.py")

with col2:
    st.markdown("""
    <div class="tool-card file">
        <div class="tool-icon">📁</div>
        <div class="tool-title">文件批量处理</div>
        <div class="tool-desc">告别繁琐的文件整理工作</div>
        <ul class="tool-features">
            <li>✓ 批量重命名</li>
            <li>✓ 格式转换</li>
            <li>✓ 自动分类整理</li>
            <li>✓ 文本内容替换</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("立即使用", key="file_btn", use_container_width=True):
        st.switch_page("pages/file_tools.py")

with col3:
    st.markdown("""
    <div class="tool-card content">
        <div class="tool-icon">📝</div>
        <div class="tool-title">职场文案生成</div>
        <div class="tool-desc">智能生成专业工作文案</div>
        <ul class="tool-features">
            <li>✓ 周报 / 月报</li>
            <li>✓ 竞品分析 / 活动方案</li>
            <li>✓ 商务邮件</li>
            <li>✓ 述职报告</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("立即使用", key="content_btn", use_container_width=True):
        st.switch_page("pages/content_tools.py")

st.markdown("""
<div class="footer">
    <p>💡 数据仅本地处理，不上传服务器，安全放心</p>
    <p>© 2024 职场提效工具箱 | 让重复工作自动化</p>
</div>
""", unsafe_allow_html=True)
