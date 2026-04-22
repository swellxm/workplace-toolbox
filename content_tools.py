import streamlit as st
from datetime import datetime

st.set_page_config(page_title="职场文案全能生成工具", page_icon="📝", layout="wide")

st.markdown("""
<style>
    .page-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #4facfe;
        margin-bottom: 0.5rem;
    }
    .template-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        cursor: pointer;
        transition: transform 0.2s;
        text-align: center;
        height: 100%;
    }
    .template-card:hover {
        transform: scale(1.02);
    }
    .result-box {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        border-left: 4px solid #4facfe;
    }
    .copy-btn {
        background: #4facfe;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""

def generate_weekly_report(data):
    template = f"""【{data.get('week', '本')}周工作总结】

姓名：{data.get('name', 'XXX')}
部门：{data.get('department', 'XXX')}
日期：{data.get('date', datetime.now().strftime('%Y-%m-%d'))}

一、本周工作完成情况

{data.get('completed', '1. \n2. \n3. ')}

二、工作成果与亮点

{data.get('achievements', '• \n• \n• ')}

三、存在问题与改进

{data.get('issues', '• \n• ')}

四、下周工作计划

{data.get('next_week', '1. \n2. \n3. ')}

五、个人感悟

{data.get('reflection', '本周工作充实有序，团队协作顺畅...')}

---
报告人：{data.get('name', 'XXX')}
提交日期：{datetime.now().strftime('%Y-%m-%d')}
"""
    return template

def generate_monthly_report(data):
    projects_text = data.get('projects', '''项目一：[项目名称]
- 进展情况：
- 完成度：%
- 下月计划：

项目二：[项目名称]
- 进展情况：
- 完成度：%
- 下月计划：
''')
    next_month_text = data.get('next_month', '''目标一：
关键举措：
完成时间：

目标二：
关键举措：
完成时间：
''')
    template = f"""【{data.get('month', datetime.now().strftime('%Y年%m月'))}月度工作总结】

姓名：{data.get('name', 'XXX')}
部门：{data.get('department', 'XXX')}
职位：{data.get('position', 'XXX')}

一、本月主要工作

{data.get('main_work', '1. \n2. \n3. \n4. \n5. ')}

二、重点项目进展

{projects_text}

三、业绩数据

• KPI完成情况：{data.get('kpi', '...')}
• 关键指标达成：{data.get('metrics', '...')}

四、能力提升

{data.get('improvement', '• \n• \n• ')}

五、团队协作

{data.get('teamwork', '• \n• ')}

六、下月工作规划

{next_month_text}

七、所需支持

{data.get('support', '• \n• ')}

---
报告人：{data.get('name', 'XXX')}
提交日期：{datetime.now().strftime('%Y-%m-%d')}
"""
    return template

def generate_competitor_analysis(data):
    template = f"""【竞品分析报告】

分析对象：{data.get('product', 'XXX产品')}
竞品名称：{data.get('competitor', 'XXX竞品')}
分析日期：{datetime.now().strftime('%Y-%m-%d')}
分析师：{data.get('analyst', 'XXX')}

一、竞品概况

{data.get('overview', '''• 公司背景：
• 市场份额：
• 核心优势：
''')}

二、产品功能对比

| 功能模块 | 我方产品 | 竞品 | 差异分析 |
|---------|---------|------|---------|
| 功能1 | ✓ | ✓/✗ | |
| 功能2 | ✓ | ✓/✗ | |
| 功能3 | ✓ | ✓/✗ | |

三、定价策略

{data.get('pricing', '''• 竞品定价：
• 收费模式：
• 价格优势：
''')}

四、用户评价

{data.get('reviews', '''• 正面评价：
• 负面评价：
• 用户痛点：
''')}

五、营销策略

{data.get('marketing', '''• 推广渠道：
• 品牌定位：
• 活动策略：
''')}

六、SWOT分析

• S（优势）：{data.get('strengths', '')}
• W（劣势）：{data.get('weaknesses', '')}
• O（机会）：{data.get('opportunities', '')}
• T（威胁）：{data.get('threats', '')}

七、启示与建议

{data.get('suggestions', '''1.
2.
3.
''')}

---
报告人：{data.get('analyst', 'XXX')}
"""
    return template

def generate_activity_plan(data):
    team_text = data.get('team', '''总负责人：
执行组：
物料组：
宣传组：
客服组：
''')
    schedule_text = data.get('schedule', '''08:00 - 09:00  签到
09:00 - 09:30  开场
09:30 - 11:30  主体活动
11:30 - 12:00  抽奖/合影
12:00 - 14:00  午餐
''')
    template = f"""【{data.get('activity_name', 'XXXX活动')}活动策划方案】

一、活动基本信息

• 活动名称：{data.get('activity_name', '')}
• 活动主题：{data.get('theme', '')}
• 活动时间：{data.get('time', '')}
• 活动地点：{data.get('location', '')}
• 参与对象：{data.get('audience', '')}
• 预计人数：{data.get('expected_num', '')}人

二、活动背景与目的

{data.get('background', '''活动背景：
活动的市场需求或发展趋势...

活动目的：
1.
2.
3.
''')}

三、活动内容

{data.get('content', '''主活动：
•

互动环节：
•
•

奖品设置：
• 一等奖：
• 二等奖：
• 三等奖：
''')}

四、宣传推广

{data.get('promotion', '''推广渠道：
• 线上：
• 线下：

推广时间：
• 预热期：
• 爆发期：

预算：
''')}

五、人员分工

{team_text}

六、预算明细

| 项目 | 单价 | 数量 | 金额 |
|------|------|------|------|
| | | | |
| 合计 | | | |

七、风险预案

• 风险1： 预案：
• 风险2： 预案：

八、活动流程

{schedule_text}

九、效果评估

• 评估指标：
• 数据收集方式：
• 预期效果：

---
策划人：
审核人：
日期：
"""
    return template

def generate_business_email(data):
    closing_map = {"此致 敬礼": "此致\n敬礼", "顺颂商祺": "顺颂商祺", "祝好": "祝好", "Best Regards": "Best Regards"}
    closing_text = closing_map.get(data.get('closing', '此致 敬礼'), data.get('closing', '此致 敬礼'))
    template = f"""【商务邮件】

收件人：{data.get('recipient', 'xxx@company.com')}
抄送：{data.get('cc', '')}
主题：{data.get('subject', '')}

---
{data.get('recipient_name', '尊敬的')} {data.get('title', '')}：

{data.get('greeting', '您好！')}

{data.get('body', '''''')}

{data.get('request', '''''')}

{closing_text}

{data.get('sender_name', 'XXX')}
{data.get('company', 'XXX公司')}
{data.get('phone', '电话：XXX-XXXX-XXXX')}
"""
    return template

def generate_job_report(data):
    reflection_text = data.get('reflection', '''（一）存在的不足
1.
2.

（二）原因分析
1.
2.
''')
    future_text = data.get('future_plan', '''（一）下阶段目标
• 目标1：
• 目标2：
• 目标3：

（二）具体举措
• 举措1：
• 举措2：

（三）所需支持
• 支持1：
• 支持2：
''')
    template = f"""【述职报告】

述职人：{data.get('name', 'XXX')}
部门：{data.get('department', 'XXX')}
职位：{data.get('position', 'XXX')}
述职周期：{data.get('period', '2024年X月-X月')}

一、岗位职责认知

{data.get('responsibilities', '''本人在职岗位为...，主要职责包括：
1.
2.
3.
''')}

二、工作业绩展示

{data.get('achievements', '''（一）核心业绩

1. 业绩一：
   - 完成情况：
   - 数据量化：
   - 亮点总结：

2. 业绩二：
   - 完成情况：
   - 数据量化：
   - 亮点总结：

3. 业绩三：
   - 完成情况：
   - 数据量化：
   - 亮点总结：

（二）重点项目

项目名称：
项目目标：
本人贡献：
项目成果：
''')}

三、能力提升

{data.get('improvement', '''（一）专业能力
•

（二）管理能力
•

（三）学习成长
• 参加的培训：
• 获得的证书：
• 阅读的书籍：
''')}

四、团队协作

{data.get('teamwork', '''• 带领团队完成...
• 协助兄弟部门...
• 培养下属...
''')}

五、问题反思

{reflection_text}

六、未来规划

{future_text}

七、个人感悟

{data.get('feelings', '''''')}

---
述职人：{data.get('name', 'XXX')}
日期：{datetime.now().strftime('%Y-%m-%d')}
"""
    return template

template_functions = {
    "周报": generate_weekly_report,
    "月报": generate_monthly_report,
    "竞品分析": generate_competitor_analysis,
    "活动方案": generate_activity_plan,
    "商务邮件": generate_business_email,
    "述职报告": generate_job_report
}

st.markdown("### 📝 职场文案全能生成工具")
st.markdown("---")

col_left, col_main = st.columns([1, 3], gap="large")

with col_left:
    st.markdown("**📋 选择文案类型**")

    template_types = ["周报", "月报", "竞品分析", "活动方案", "商务邮件", "述职报告"]
    selected_template = st.selectbox("文案模板", options=template_types)

    st.markdown("---")
    st.markdown("**🎨 输出风格**")
    style = st.selectbox(
        "选择风格",
        options=["简洁专业", "详细全面", "活泼轻松"],
        label_visibility="collapsed"
    )

with col_main:
    st.markdown(f"**📝 {selected_template}**")

    if selected_template == "周报":
        with st.form("weekly_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("姓名", placeholder="请输入姓名")
                department = st.text_input("部门", placeholder="请输入部门")
            with col2:
                week = st.text_input("周期", placeholder="如：2024年第15周")
                date = st.date_input("提交日期")

            completed = st.text_area("本周完成工作（每条一行）", height=100, placeholder="1. 完成了XX项目\n2. 完成了XX报告\n3. ...")
            achievements = st.text_area("工作成果与亮点", height=80, placeholder="• 业绩提升20%\n• 获得客户好评\n• ...")
            issues = st.text_area("存在问题", height=60, placeholder="• XX项目进度延误\n• ...")
            next_week = st.text_area("下周工作计划", height=80, placeholder="1. 推进XX项目\n2. 完成XX报告\n3. ...")
            reflection = st.text_area("个人感悟", height=60, placeholder="本周工作...")

            submitted = st.form_submit_button("🚀 生成周报", use_container_width=True)

            if submitted:
                data = {
                    "name": name, "department": department, "week": week,
                    "date": date.strftime('%Y-%m-%d'), "completed": completed,
                    "achievements": achievements, "issues": issues,
                    "next_week": next_week, "reflection": reflection
                }
                st.session_state.generated_content = generate_weekly_report(data)

    elif selected_template == "月报":
        with st.form("monthly_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("姓名", placeholder="请输入姓名")
                department = st.text_input("部门", placeholder="请输入部门")
            with col2:
                position = st.text_input("职位", placeholder="请输入职位")
                month = st.text_input("月份", placeholder="如：2024年03月")

            main_work = st.text_area("本月主要工作", height=120, placeholder="1.\n2.\n3.")
            projects = st.text_area("重点项目进展", height=120, placeholder="项目一：\n- 进展情况：\n...")
            kpi = st.text_input("KPI完成情况")
            metrics = st.text_area("关键指标达成", height=60)
            improvement = st.text_area("能力提升", height=60)
            teamwork = st.text_area("团队协作", height=60)
            next_month = st.text_area("下月工作规划", height=100)
            support = st.text_area("所需支持", height=60)

            submitted = st.form_submit_button("🚀 生成月报", use_container_width=True)

            if submitted:
                data = {
                    "name": name, "department": department, "position": position,
                    "month": month, "main_work": main_work, "projects": projects,
                    "kpi": kpi, "metrics": metrics, "improvement": improvement,
                    "teamwork": teamwork, "next_month": next_month, "support": support
                }
                st.session_state.generated_content = generate_monthly_report(data)

    elif selected_template == "竞品分析":
        with st.form("competitor_form"):
            col1, col2 = st.columns(2)
            with col1:
                product = st.text_input("我方产品", placeholder="产品名称")
                competitor = st.text_input("竞品名称", placeholder="竞品名称")
            with col2:
                analyst = st.text_input("分析师", placeholder="您的姓名")
                date = st.date_input("分析日期")

            overview = st.text_area("竞品概况", height=80)
            pricing = st.text_area("定价策略", height=80)
            reviews = st.text_area("用户评价", height=80)
            marketing = st.text_area("营销策略", height=80)
            col_swot1, col_swot2 = st.columns(2)
            with col_swot1:
                strengths = st.text_input("优势 S")
                weaknesses = st.text_input("劣势 W")
            with col_swot2:
                opportunities = st.text_input("机会 O")
                threats = st.text_input("威胁 T")
            suggestions = st.text_area("启示与建议", height=80)

            submitted = st.form_submit_button("🚀 生成分析报告", use_container_width=True)

            if submitted:
                data = {
                    "product": product, "competitor": competitor,
                    "analyst": analyst, "date": date.strftime('%Y-%m-%d'),
                    "overview": overview, "pricing": pricing, "reviews": reviews,
                    "marketing": marketing, "strengths": strengths,
                    "weaknesses": weaknesses, "opportunities": opportunities,
                    "threats": threats, "suggestions": suggestions
                }
                st.session_state.generated_content = generate_competitor_analysis(data)

    elif selected_template == "活动方案":
        with st.form("activity_form"):
            col1, col2 = st.columns(2)
            with col1:
                activity_name = st.text_input("活动名称", placeholder="XX活动")
                theme = st.text_input("活动主题", placeholder="活动主题")
            with col2:
                time = st.text_input("活动时间", placeholder="2024年X月X日")
                location = st.text_input("活动地点", placeholder="XX地点")

            audience = st.text_input("参与对象", placeholder="XX用户群体")
            expected_num = st.number_input("预计人数", min_value=1, value=100)
            background = st.text_area("活动背景与目的", height=100)
            content = st.text_area("活动内容", height=100)
            promotion = st.text_area("宣传推广", height=80)
            team = st.text_area("人员分工", height=80)
            schedule = st.text_area("活动流程", height=100)

            submitted = st.form_submit_button("🚀 生成活动方案", use_container_width=True)

            if submitted:
                data = {
                    "activity_name": activity_name, "theme": theme,
                    "time": time, "location": location, "audience": audience,
                    "expected_num": expected_num, "background": background,
                    "content": content, "promotion": promotion,
                    "team": team, "schedule": schedule
                }
                st.session_state.generated_content = generate_activity_plan(data)

    elif selected_template == "商务邮件":
        with st.form("email_form"):
            col1, col2 = st.columns(2)
            with col1:
                recipient = st.text_input("收件人邮箱", placeholder="xxx@company.com")
                recipient_name = st.text_input("收件人姓名", placeholder="张总")
            with col2:
                title = st.text_input("收件人职位", placeholder="总监")
                subject = st.text_input("邮件主题", placeholder="关于XX项目的沟通")

            cc = st.text_input("抄送（选填）", placeholder="xxx@company.com")
            greeting = st.selectbox("称呼", ["您好！", "尊敬的张总：", "各位领导：", "同事们："])
            body = st.text_area("邮件正文", height=120, placeholder="邮件主要内容...")
            request = st.text_area("请求/行动号召", height=80, placeholder="烦请XX，谢谢！")
            closing = st.selectbox("结尾", ["此致 敬礼", "顺颂商祺", "祝好", "Best Regards"])
            sender_name = st.text_input("发件人姓名")
            company = st.text_input("公司名称")
            phone = st.text_input("联系电话")

            submitted = st.form_submit_button("🚀 生成邮件", use_container_width=True)

            if submitted:
                data = {
                    "recipient": recipient, "recipient_name": recipient_name,
                    "title": title, "subject": subject, "cc": cc,
                    "greeting": greeting, "body": body, "request": request,
                    "closing": closing, "sender_name": sender_name,
                    "company": company, "phone": phone, "email": ""
                }
                st.session_state.generated_content = generate_business_email(data)

    elif selected_template == "述职报告":
        with st.form("report_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("述职人姓名", placeholder="您的姓名")
                department = st.text_input("部门", placeholder="所属部门")
            with col2:
                position = st.text_input("职位", placeholder="当前职位")
                period = st.text_input("述职周期", placeholder="2024年X月-X月")

            responsibilities = st.text_area("岗位职责认知", height=80)
            achievements = st.text_area("工作业绩展示", height=150)
            improvement = st.text_area("能力提升", height=80)
            teamwork = st.text_area("团队协作", height=60)
            reflection = st.text_area("问题反思", height=100)
            future_plan = st.text_area("未来规划", height=120)
            feelings = st.text_area("个人感悟", height=60)

            submitted = st.form_submit_button("🚀 生成述职报告", use_container_width=True)

            if submitted:
                data = {
                    "name": name, "department": department, "position": position,
                    "period": period, "responsibilities": responsibilities,
                    "achievements": achievements, "improvement": improvement,
                    "teamwork": teamwork, "reflection": reflection,
                    "future_plan": future_plan, "feelings": feelings
                }
                st.session_state.generated_content = generate_job_report(data)

if st.session_state.generated_content:
    st.markdown("---")
    st.markdown("### 📋 生成结果")

    st.text_area(
        "文案内容",
        value=st.session_state.generated_content,
        height=400,
        key="result_display"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📋 复制到剪贴板", use_container_width=True)
    with col2:
        st.download_button(
            "📥 下载为TXT",
            st.session_state.generated_content,
            file_name=f"{selected_template}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col3:
        if st.button("🔄 重新生成", use_container_width=True):
            st.session_state.generated_content = ""

st.markdown("---")
if st.button("← 返回首页", use_container_width=False):
    st.switch_page("app.py")
