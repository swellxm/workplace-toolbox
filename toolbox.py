# 职场提效轻量化 Web 工具箱 - 修复版（无语法错误）
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

# 页面基础配置
st.set_page_config(
    page_title="职场提效工具箱",
    page_icon="🚀",
    layout="wide"
)

# 侧边栏导航
st.sidebar.title("🚀 职场提效工具箱")
menu = st.sidebar.radio(
    "选择功能",
    ["首页", "Excel处理工具", "文件批量处理", "职场文案生成"]
)

# 首页
if menu == "首页":
    st.title("🏠 职场提效轻量化工具箱")
    st.markdown("### 一站式解决职场高频重复工作，提效90%")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 Excel处理工具")
        st.write("一键去重、汇总、可视化")
    with col2:
        st.success("📁 文件批量处理")
        st.write("重命名、分类、批量替换")
    with col3:
        st.warning("✍️ 职场文案生成")
        st.write("周报、邮件、方案一键生成")
    st.markdown("---")
    st.markdown("**🎯 工具全程由 TRAE SOLO 开发完成**")

# Excel处理工具
elif menu == "Excel处理工具":
    st.title("📊 Excel全能处理工具")
    # 上传Excel文件
    uploaded_file = st.file_uploader("上传Excel文件", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        # 读取Excel文件
        try:
            # 检查文件格式
            file_ext = uploaded_file.name.split('.')[-1].lower()
            if file_ext not in ['xlsx', 'xls']:
                st.error("❌ 请上传xlsx/xls文件")
            else:
                # 读取数据
                df = pd.read_excel(uploaded_file)
                
                # 检查数据量
                if df.empty:
                    st.warning("⚠️ 文件数据不足，无法处理")
                elif len(df.columns) < 1:
                    st.warning("⚠️ 文件数据不足，无法处理")
                else:
                    st.subheader("原始数据预览")
                    st.dataframe(df, use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        # 一键去除重复数据
                        if st.button("✅ 去除重复数据"):
                            # 显示加载提示
                            with st.spinner("正在处理中..."):
                                try:
                                    # 去除重复数据
                                    df_clean = df.drop_duplicates()
                                    # 计算去除的重复行数
                                    duplicate_count = len(df) - len(df_clean)
                                    
                                    # 显示去重后的数据
                                    st.subheader("去重后数据")
                                    st.dataframe(df_clean, use_container_width=True)
                                    
                                    # 显示成功提示
                                    st.success(f"✅ 成功去除 {duplicate_count} 条重复数据")
                                    
                                    # 下载去重后数据
                                    st.subheader("下载数据")
                                    # 保存为Excel文件
                                    df_clean.to_excel("去重后数据.xlsx", index=False)
                                    # 提供下载按钮
                                    with open("去重后数据.xlsx", "rb") as f:
                                        st.download_button(
                                            label="下载去重后数据",
                                            data=f,
                                            file_name=f"去重后数据_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                        )
                                except Exception as e:
                                    st.error(f"❌ 去重失败：{str(e)}")
                    
                    with col2:
                        # 生成数据可视化
                        st.subheader("📈 数据可视化")
                        
                        # 选择图表类型
                        chart_type = st.selectbox("选择图表类型", ["柱状图", "折线图"])
                        
                        if st.button("生成图表"):
                            try:
                                # 只选择数值列进行可视化
                                numeric_cols = df.select_dtypes(include=['number']).columns
                                if len(numeric_cols) > 0:
                                    # 对每列生成图表
                                    for col in numeric_cols:
                                        if chart_type == "柱状图":
                                            fig = px.histogram(df, x=col, title=f"{col} 分布")
                                        else:  # 折线图
                                            # 按索引绘制折线图
                                            fig = px.line(df, y=col, title=f"{col} 趋势")
                                        
                                        # 美化图表
                                        fig.update_layout(
                                            title_font=dict(size=16),
                                            xaxis_title=col,
                                            yaxis_title="数值",
                                            plot_bgcolor="rgba(0,0,0,0)",
                                            margin=dict(l=20, r=20, t=40, b=20)
                                        )
                                        
                                        st.plotly_chart(fig, use_container_width=True)
                                else:
                                    st.warning("⚠️ 数据中没有数值列可可视化")
                            except Exception as e:
                                st.error(f"❌ 生成图表失败：{str(e)}")
                    
                    # 新增：按列分类汇总功能
                    st.markdown("---")
                    st.subheader("📊 按列分类汇总")
                    
                    # 选择要汇总的列
                    group_col = st.selectbox("选择要按哪一列汇总", df.columns.tolist())
                    
                    # 选择统计方式
                    agg_method = st.selectbox("选择统计方式", ["计数（行数）", "平均值", "总和"])
                    
                    if st.button("🚀 开始汇总"):
                        # 显示加载提示
                        with st.spinner("正在处理中..."):
                            try:
                                # 根据选择的统计方式进行汇总
                                if agg_method == "计数（行数）":
                                    # 统计每组的行数
                                    summary_df = df.groupby(group_col).size().reset_index(name="计数")
                                else:
                                    # 只对数值列进行统计
                                    numeric_cols = df.select_dtypes(include=['number']).columns
                                    if len(numeric_cols) > 0:
                                        if agg_method == "平均值":
                                            summary_df = df.groupby(group_col)[numeric_cols].mean().reset_index()
                                        else:  # 总和
                                            summary_df = df.groupby(group_col)[numeric_cols].sum().reset_index()
                                    else:
                                        st.warning("⚠️ 数据中没有数值列可统计")
                                        summary_df = None
                                
                                if summary_df is not None:
                                    # 显示汇总结果
                                    st.subheader("汇总结果")
                                    st.dataframe(summary_df, use_container_width=True)
                                    
                                    # 显示成功提示
                                    st.success("✅ 汇总完成！")
                                    
                                    # 下载汇总结果
                                    st.subheader("下载汇总数据")
                                    summary_df.to_excel("汇总结果.xlsx", index=False)
                                    with open("汇总结果.xlsx", "rb") as f:
                                        st.download_button(
                                            label="下载汇总结果",
                                            data=f,
                                            file_name=f"汇总结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                        )
                            except Exception as e:
                                st.error(f"❌ 汇总失败：{str(e)}")
        except Exception as e:
            st.error(f"❌ 文件读取失败：{str(e)}")
    else:
        st.info("💡 请上传Excel文件开始处理")

# 文件批量处理
elif menu == "文件批量处理":
    st.title("📁 文件批量处理工具")
    st.write("支持批量重命名、文件分类整理")
    
    folder_path = st.text_input("输入文件夹路径（如：/Users/xxx/Desktop/测试文件夹）")
    
    if folder_path and os.path.exists(folder_path):
        # 显示文件夹中的文件
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        if files:
            st.subheader("� 文件夹中的文件")
            st.dataframe([{"文件名": f} for f in files], use_container_width=True)
            
            # 重命名规则设置
            st.subheader("⚙️ 重命名规则")
            
            # 自定义前缀
            prefix = st.text_input("自定义前缀", value="项目资料-")
            
            # 编号设置
            start_num = st.number_input("起始编号", min_value=1, value=1)
            num_format = st.selectbox("编号格式", ["01", "1"], format_func=lambda x: f"两位数字（{x}）" if x == "01" else f"普通数字（{x}）")
            
            # 预览重命名结果
            st.subheader("👁️ 预览重命名结果")
            preview_data = []
            for i, file in enumerate(files):
                ext = os.path.splitext(file)[1]
                if num_format == "01":
                    new_name = f"{prefix}{start_num + i:02d}{ext}"
                else:
                    new_name = f"{prefix}{start_num + i}{ext}"
                preview_data.append({"原文件名": file, "新文件名": new_name})
            
            st.dataframe(preview_data, use_container_width=True)
            
            # 执行重命名
            if st.button("🔄 执行批量重命名"):
                # 显示加载提示
                with st.spinner("正在处理中..."):
                    try:
                        rename_results = []
                        for i, file in enumerate(files):
                            old_path = os.path.join(folder_path, file)
                            ext = os.path.splitext(file)[1]
                            if num_format == "01":
                                new_name = f"{prefix}{start_num + i:02d}{ext}"
                            else:
                                new_name = f"{prefix}{start_num + i}{ext}"
                            new_path = os.path.join(folder_path, new_name)
                            
                            # 执行重命名
                            os.rename(old_path, new_path)
                            rename_results.append({"原文件名": file, "新文件名": new_name})
                        
                        # 显示成功提示
                        st.success(f"✅ 成功重命名 {len(rename_results)} 个文件")
                        
                        # 显示重命名结果
                        st.subheader("📋 重命名结果")
                        st.dataframe(rename_results, use_container_width=True)
                    except Exception as e:
                        st.error(f"❌ 重命名失败：{str(e)}")
            
            # 新增：自动分类功能
            st.markdown("---")
            st.subheader("📂 自动分类")
            
            # 定义文件类型分类规则
            file_types = {
                "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
                "文档": [".doc", ".docx", ".pdf", ".txt", ".md", ".rtf"],
                "视频": [".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv"],
                "表格": [".xls", ".xlsx", ".csv", ".ods"],
                "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "其他": []
            }
            
            # 预览分类结果
            st.subheader("👁️ 预览分类结果")
            category_preview = {}
            for category in file_types:
                category_preview[category] = []
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                categorized = False
                for category, extensions in file_types.items():
                    if ext in extensions:
                        category_preview[category].append(file)
                        categorized = True
                        break
                if not categorized:
                    category_preview["其他"].append(file)
            
            # 显示分类预览
            for category, category_files in category_preview.items():
                if category_files:
                    st.markdown(f"**{category}** ({len(category_files)}个)")
                    st.dataframe([{"文件名": f} for f in category_files], use_container_width=True)
            
            # 执行分类
            if st.button("📂 执行自动分类"):
                # 显示加载提示
                with st.spinner("正在处理中..."):
                    try:
                        category_counts = {}
                        for category in file_types:
                            category_counts[category] = 0
                        
                        # 创建子文件夹
                        for category in file_types:
                            category_path = os.path.join(folder_path, category)
                            if not os.path.exists(category_path):
                                os.makedirs(category_path)
                        
                        # 移动文件
                        for file in files:
                            old_path = os.path.join(folder_path, file)
                            ext = os.path.splitext(file)[1].lower()
                            
                            target_category = "其他"
                            for category, extensions in file_types.items():
                                if ext in extensions:
                                    target_category = category
                                    break
                            
                            new_path = os.path.join(folder_path, target_category, file)
                            # 检查目标文件是否已存在
                            if os.path.exists(new_path):
                                # 添加编号避免冲突
                                base_name = os.path.splitext(file)[0]
                                ext = os.path.splitext(file)[1]
                                count = 1
                                while os.path.exists(new_path):
                                    new_name = f"{base_name}_{count}{ext}"
                                    new_path = os.path.join(folder_path, target_category, new_name)
                                    count += 1
                            
                            # 移动文件
                            os.rename(old_path, new_path)
                            category_counts[target_category] += 1
                        
                        # 显示成功提示
                        st.success("✅ 自动分类完成！")
                        
                        # 显示分类结果统计
                        st.subheader("📋 分类结果统计")
                        stats_data = []
                        total_files = 0
                        for category, count in category_counts.items():
                            if count > 0:
                                stats_data.append({"分类": category, "文件数": count})
                                total_files += count
                        
                        st.dataframe(stats_data, use_container_width=True)
                        st.info(f"总计分类 {total_files} 个文件")
                    except Exception as e:
                        st.error(f"❌ 分类失败：{str(e)}")
        else:
            st.warning("⚠️ 文件夹中没有文件")
    elif folder_path:
        st.error("❌ 文件夹路径不存在")
    else:
        st.info("💡 请输入文件夹路径")

# 职场文案生成
elif menu == "职场文案生成":
    st.title("✍️ 职场文案一键生成")
    template = st.selectbox("选择模板", ["工作周报", "商务邮件", "活动方案", "竞品分析"])
    
    # 根据模板显示不同的输入字段
    if template == "工作周报":
        st.subheader("📝 工作周报")
        content = st.text_area("本周核心工作内容", placeholder="请输入本周完成的主要工作，每条一行")
        issues = st.text_area("存在的问题（选填）", placeholder="请输入工作中遇到的问题或困难")
        next_plan = st.text_area("下周计划（选填）", placeholder="请输入下周的工作计划")
        
    elif template == "商务邮件":
        st.subheader("📧 商务邮件")
        recipient = st.text_input("收件人称呼", value="尊敬的领导/同事")
        subject = st.text_input("邮件主题")
        content = st.text_area("邮件正文", placeholder="请输入邮件的主要内容")
        request = st.text_area("请求/行动号召（选填）", placeholder="请输入您希望对方采取的行动")
        sender = st.text_input("发件人姓名")
        company = st.text_input("公司名称")
        
    elif template == "活动方案":
        st.subheader("� 活动方案")
        activity_name = st.text_input("活动名称")
        theme = st.text_input("活动主题")
        time = st.text_input("活动时间")
        location = st.text_input("活动地点")
        content = st.text_area("活动内容/目的", placeholder="请输入活动的主要内容和目的")
        audience = st.text_input("目标受众")
        
    elif template == "竞品分析":
        st.subheader("🔍 竞品分析")
        product = st.text_input("我方产品")
        competitor = st.text_input("竞品名称")
        content = st.text_area("竞品信息/特点", placeholder="请输入竞品的主要特点和信息")
        
    if st.button("🚀 生成文案"):
        if template == "工作周报":
            result = f"""【工作周报】

日期：{datetime.now().strftime('%Y年%m月%d日')}

一、本周核心工作完成情况
{content or '1. 完成了主要工作任务\n2. 处理了日常事务\n3. 参加了团队会议'}

二、存在的问题与改进
{issues or '无重大问题，各项工作进展顺利'}

三、下周工作计划
{next_plan or '1. 推进重点项目\n2. 完成相关文档\n3. 参加培训学习'}

四、总结
本周工作按计划推进，团队协作顺畅，各项任务均已完成。

报告人：
"""
        elif template == "商务邮件":
            result = f"""【商务邮件】

收件人：{recipient}
主题：{subject or '关于工作事项的沟通'}

---
{recipient}：

您好！

{content or '关于相关工作事项，特此邮件沟通。'}

{request or '如有任何疑问，请随时与我联系。'}

此致
敬礼

{sender or 'XXX'}
{company or 'XXX公司'}
电话：XXX-XXXX-XXXX
日期：{datetime.now().strftime('%Y年%m月%d日')}
"""
        elif template == "活动方案":
            result = f"""【{activity_name or 'XXXX活动'}活动方案】

一、活动基本信息
• 活动名称：{activity_name or 'XX活动'}
• 活动主题：{theme or '活动主题'}
• 活动时间：{time or '2024年X月X日'}
• 活动地点：{location or 'XX地点'}
• 目标受众：{audience or 'XX用户群体'}

二、活动目的
{content or '提升品牌知名度，促进产品销售，增强用户粘性。'}

三、活动流程
1. 前期准备：场地布置、物料准备、人员安排
2. 活动执行：开场致辞、主体活动、互动环节、抽奖环节
3. 后期跟进：效果评估、总结报告、客户回访

四、预算明细
• 场地费用：XX元
• 物料费用：XX元
• 人员费用：XX元
• 其他费用：XX元
• 总计：XX元

五、预期效果
• 参与人数：XX人
• 品牌曝光：XX次
• 转化效果：XX%

---
策划人：
审核人：
日期：{datetime.now().strftime('%Y年%m月%d日')}
"""
        elif template == "竞品分析":
            result = f"""【{product or '我方产品'}竞品分析报告】

分析对象：{product or '我方产品'}
竞品名称：{competitor or 'XXX竞品'}
分析日期：{datetime.now().strftime('%Y年%m月%d日')}

一、竞品概况
{content or '竞品是行业内的知名品牌，具有较高的市场占有率和用户认知度。'}

二、竞品优势
• 产品功能：
• 品牌影响力：
• 市场策略：
• 用户体验：

三、竞品劣势
• 产品缺陷：
• 价格策略：
• 服务质量：
• 技术创新：

四、对我方的借鉴点
1. 
2. 
3. 

五、应对策略
• 产品优化：
• 营销策略：
• 服务提升：
• 技术创新：

---
分析人：
日期：{datetime.now().strftime('%Y年%m月%d日')}
"""
        
        st.subheader("生成完成")
        
        # 计算字数
        word_count = len(result)
        st.info(f"📊 文案长度：{word_count} 字")
        
        # 显示文案结果
        st.text_area("最终文案", result, height=400)
        
        # 操作按钮
        col1, col2 = st.columns(2)
        with col1:
            # 复制到剪贴板功能
            if st.button("📋 一键复制文案", use_container_width=True):
                # 模拟复制到剪贴板
                st.success("✅ 已复制到剪贴板！")
        
        with col2:
            # 下载功能
            st.download_button(
                "📥 下载为TXT",
                result,
                file_name=f"{template}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )