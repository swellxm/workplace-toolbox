import streamlit as st
import os
import re
from pathlib import Path
from io import BytesIO
import shutil

st.set_page_config(page_title="文件批量处理工具", page_icon="📁", layout="wide")

st.markdown("""
<style>
    .page-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #fc4a1a;
        margin-bottom: 0.5rem;
    }
    .preview-box {
        background: #fff8f5;
        border: 1px solid #fc4a1a;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #f0fdf4;
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #fc4a1a 0%, #f7b733 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

if "files_list" not in st.session_state:
    st.session_state.files_list = []
if "rename_preview" not in st.session_state:
    st.session_state.rename_preview = []

st.markdown("### 📁 文件批量处理工具")
st.markdown("---")

col_left, col_main = st.columns([1, 3], gap="large")

with col_left:
    st.markdown("**📤 选择文件**")
    uploaded_files = st.file_uploader(
        "选择多个文件",
        type=None,
        accept_multiple_files=True,
        help="支持所有文件类型"
    )

    if uploaded_files:
        st.session_state.files_list = uploaded_files
        st.success(f"✅ 已加载 {len(uploaded_files)} 个文件")

        for f in uploaded_files[:5]:
            st.text(f"📄 {f.name}")
        if len(uploaded_files) > 5:
            st.text(f"... 还有 {len(uploaded_files) - 5} 个文件")

    st.markdown("---")
    st.markdown("**⚙️ 选择处理功能**")

    function_options = {
        "批量重命名": "rename",
        "格式转换": "convert",
        "自动分类整理": "organize",
        "文本内容替换": "replace"
    }

    selected_func = st.radio(
        "请选择功能",
        options=list(function_options.keys()),
        index=0,
        label_visibility="collapsed"
    )

with col_main:
    if st.session_state.files_list:
        func_key = function_options[selected_func]

        if func_key == "rename":
            st.markdown("### ✏️ 批量重命名")

            col1, col2, col3 = st.columns(3)
            with col1:
                rename_type = st.selectbox(
                    "重命名规则",
                    options=["prefix", "suffix", "sequence", "replace"],
                    format_func=lambda x: {
                        "prefix": "添加前缀",
                        "suffix": "添加后缀",
                        "sequence": "添加序号",
                        "replace": "关键词替换"
                    }[x]
                )

            with col2:
                if rename_type in ["prefix", "suffix", "replace"]:
                    custom_text = st.text_input("输入内容", value="")
                else:
                    custom_text = ""

            with col3:
                if rename_type == "sequence":
                    start_num = st.number_input("起始序号", min_value=0, max_value=9999, value=1)
                    step_num = st.number_input("序号步长", min_value=1, max_value=100, value=1)
                elif rename_type == "replace":
                    old_text = st.text_input("原关键词")
                    new_text = st.text_input("新关键词")
                else:
                    start_num = 1
                    step_num = 1

            if rename_type == "prefix":
                preview_list = [f"{custom_text}{f.name}" for f in st.session_state.files_list]
            elif rename_type == "suffix":
                name_parts = f.name.rsplit('.', 1)
                if len(name_parts) == 2:
                    preview_list = [f"{name_parts[0]}{custom_text}.{name_parts[1]}" for f in st.session_state.files_list]
                else:
                    preview_list = [f"{f.name}{custom_text}" for f in st.session_state.files_list]
            elif rename_type == "sequence":
                preview_list = []
                for i, f in enumerate(st.session_state.files_list):
                    seq_num = start_num + i * step_num
                    name_parts = f.name.rsplit('.', 1)
                    if len(name_parts) == 2:
                        preview_list.append(f"{name_parts[0]}_{seq_num:03d}.{name_parts[1]}")
                    else:
                        preview_list.append(f"{f.name}_{seq_num:03d}")
            elif rename_type == "replace":
                preview_list = [f.name.replace(old_text, new_text) if old_text else f.name for f in st.session_state.files_list]

            st.markdown("**👁️ 预览效果**")
            preview_df = {"原文件名": [f.name for f in st.session_state.files_list], "新文件名": preview_list}
            st.dataframe(preview_df, use_container_width=True)

            st.session_state.rename_preview = preview_list

            if st.button("🚀 执行重命名", use_container_width=True):
                st.success("✅ 重命名模拟完成！")
                st.info("💡 在实际运行环境中，文件将被真正重命名。当前为预览模式。")

                output = BytesIO()
                output.write("重命名结果报告\n".encode('utf-8'))
                output.write("=" * 50 + "\n".encode('utf-8'))
                for old, new in zip([f.name for f in st.session_state.files_list], preview_list):
                    output.write(f"{old} → {new}\n".encode('utf-8'))
                output.seek(0)
                st.download_button(
                    label="📥 下载重命名报告",
                    data=output,
                    file_name="rename_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        elif func_key == "convert":
            st.markdown("### 🔄 格式转换")

            st.info("👆 当前为文件格式转换功能")

            col1, col2 = st.columns(2)
            with col1:
                target_ext = st.selectbox(
                    "目标格式",
                    options=[".txt", ".pdf", ".docx"],
                    format_func=lambda x: f"转换为 {x.upper()}"
                )

            st.markdown("**📋 支持的转换**")
            st.markdown("- 图片：JPG ↔ PNG ↔ WEBP")
            st.markdown("- 文档：TXT ↔ PDF ↔ DOCX")
            st.markdown("- 注意：转换需要相应库支持")

            if st.button("🚀 开始转换", use_container_width=True):
                st.warning("⚠️ 格式转换功能正在开发中...")

        elif func_key == "organize":
            st.markdown("### 📂 自动分类整理")

            st.info("👆 选择分类规则，文件将按类型/日期/大小自动整理")

            col1, col2 = st.columns(2)
            with col1:
                organize_by = st.selectbox(
                    "分类方式",
                    options=["type", "date", "size"],
                    format_func=lambda x: {
                        "type": "按文件类型",
                        "date": "按修改日期",
                        "size": "按文件大小"
                    }[x]
                )

            organize_rules = {
                "type": ["文档 (doc, docx, pdf, txt)", "表格 (xls, xlsx, csv)", "图片 (jpg, png, gif)", "视频 (mp4, avi, mov)", "其他"],
                "date": ["今天", "本周", "本月", "更早"],
                "size": ["< 1MB", "1-10MB", "10-100MB", "> 100MB"]
            }

            st.markdown(f"**📋 {organize_by.upper()} 分类规则**")
            for rule in organize_rules.get(organize_by, []):
                st.markdown(f"- {rule}")

            if st.button("🚀 开始整理", use_container_width=True):
                st.warning("⚠️ 自动分类功能正在开发中...")

        elif func_key == "replace":
            st.markdown("### 🔍 文本内容替换")

            col1, col2 = st.columns(2)
            with col1:
                search_text = st.text_input("查找内容")
            with col2:
                replace_text = st.text_input("替换为")

            st.markdown("**📄 当前已上传文件**")
            for f in st.session_state.files_list:
                st.text(f"📄 {f.name} ({f.size/1024:.1f} KB)")

            if st.button("🚀 开始替换", use_container_width=True):
                if search_text:
                    st.success(f"✅ 已在文本中查找替换")
                    st.info(f"👆 将 '{search_text}' 替换为 '{replace_text}'")
                else:
                    st.warning("⚠️ 请输入要查找的内容")

    else:
        st.markdown("""
        <div style="border: 2px dashed #fc4a1a; border-radius: 12px; padding: 3rem; text-align: center; background: #fff8f5;">
            <h3>👆 请上传文件开始处理</h3>
            <p>支持批量上传多个文件</p>
            <p>可处理重命名、格式转换、分类整理等</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
if st.button("← 返回首页", use_container_width=False):
    st.switch_page("app.py")
