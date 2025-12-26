"""
AI-CARE Lung ePRO System
智慧肺癌術後照護系統

📱 完整功能手機友善版
三軍總醫院 數位醫學中心
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ============================================
# 頁面設定
# ============================================
st.set_page_config(
    page_title="AI-CARE Lung",
    page_icon="🫁",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# 手機友善 CSS（完整版）
# ============================================
st.markdown("""
<style>
    /* 隱藏預設元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 手機字體 */
    html, body {
        font-size: 16px;
        -webkit-text-size-adjust: 100%;
    }
    
    /* 按鈕 */
    .stButton > button {
        width: 100%;
        padding: 14px 20px;
        font-size: 15px;
        border-radius: 12px;
        min-height: 50px;
    }
    
    /* 輸入框 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 16px;
        padding: 14px;
        border-radius: 12px;
    }
    
    /* Tabs 樣式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        font-size: 14px;
    }
    
    /* 卡片 */
    .card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    
    .card-green {
        background: linear-gradient(135deg, #ecfdf5, #d1fae5);
        border: 1px solid #a7f3d0;
    }
    
    .card-blue {
        background: linear-gradient(135deg, #eff6ff, #dbeafe);
        border: 1px solid #bfdbfe;
    }
    
    .card-purple {
        background: linear-gradient(135deg, #f5f3ff, #ede9fe);
        border: 1px solid #c4b5fd;
    }
    
    /* 警示卡片 */
    .alert-red {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border-left: 4px solid #ef4444;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .alert-yellow {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        border-left: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .alert-green {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border-left: 4px solid #22c55e;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    /* 聊天氣泡 */
    .chat-ai {
        background: #f1f5f9;
        border-radius: 18px 18px 18px 4px;
        padding: 14px 18px;
        margin: 8px 0;
        font-size: 15px;
        line-height: 1.6;
    }
    
    .chat-user {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border-radius: 18px 18px 4px 18px;
        padding: 14px 18px;
        margin: 8px 0;
        font-size: 15px;
        line-height: 1.6;
    }
    
    /* 統計數字 */
    .stat-big {
        font-size: 28px;
        font-weight: 700;
        line-height: 1.2;
    }
    
    /* 進度條 */
    .progress-bg {
        background: #e2e8f0;
        border-radius: 8px;
        height: 10px;
        overflow: hidden;
        margin: 8px 0;
    }
    
    .progress-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.3s ease;
    }
    
    /* 病人清單項目 */
    .patient-item {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border-left: 4px solid;
    }
    
    /* 手機適配 */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            display: none;
        }
        .main .block-container {
            padding: 1rem;
            padding-bottom: 20px;
        }
    }
    
    /* Plotly 圖表手機適配 */
    .js-plotly-plot {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# Session State
# ============================================
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "ai", "content": "您好！我是您的健康小助手 🌱\n\n今天感覺怎麼樣呢？", "time": "09:00"}
    ]

if 'page' not in st.session_state:
    st.session_state.page = "patient"

if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = None

# ============================================
# 完整模擬數據
# ============================================
PATIENTS = [
    {"id": "P001", "name": "王大明", "age": 68, "surgery": "右上肺葉切除", "day": 14, "compliance": 92, "status": "alert", "last_report": "10:30", "phone": "0912-345-678"},
    {"id": "P002", "name": "李小華", "age": 55, "surgery": "左下肺葉切除", "day": 21, "compliance": 85, "status": "warning", "last_report": "09:15", "phone": "0923-456-789"},
    {"id": "P003", "name": "陳美玲", "age": 72, "surgery": "右中肺葉切除", "day": 7, "compliance": 78, "status": "overdue", "last_report": "昨天", "phone": "0934-567-890"},
    {"id": "P004", "name": "張志明", "age": 61, "surgery": "肺節切除", "day": 30, "compliance": 95, "status": "normal", "last_report": "08:45", "phone": "0945-678-901"},
    {"id": "P005", "name": "林淑芬", "age": 58, "surgery": "左上肺葉切除", "day": 45, "compliance": 88, "status": "normal", "last_report": "昨天", "phone": "0956-789-012"},
]

ALERTS = [
    {"id": 1, "patient": "王大明", "level": "red", "symptom": "呼吸困難", "score": 8, "time": "10 分鐘前", "phone": "0912-345-678", "status": "pending"},
    {"id": 2, "patient": "李小華", "level": "yellow", "symptom": "疲勞", "score": 5, "time": "30 分鐘前", "phone": "0923-456-789", "status": "pending"},
    {"id": 3, "patient": "陳美玲", "level": "yellow", "symptom": "胸痛", "score": 4, "time": "1 小時前", "phone": "0934-567-890", "status": "contacted"},
    {"id": 4, "patient": "張志明", "level": "green", "symptom": "輕微咳嗽", "score": 2, "time": "2 小時前", "phone": "0945-678-901", "status": "resolved"},
]

INTERVENTION_RECORDS = [
    {"patient": "王大明", "type": "電話", "content": "呼吸困難症狀評估，建議使用噘嘴式呼吸，若持續加重需回診。病人表示了解。", "time": "今天 10:45", "duration": "8分鐘", "referral": None},
    {"patient": "李小華", "type": "LINE", "content": "提醒今日回報，病人表示下午會填寫。", "time": "今天 09:30", "duration": "2分鐘", "referral": None},
    {"patient": "陳美玲", "type": "電話", "content": "評估後轉介營養諮詢，體重持續下降。已預約營養師門診。", "time": "昨天 15:20", "duration": "12分鐘", "referral": "營養諮詢"},
]

SCHEDULE = [
    {"time": "08:00-10:00", "task": "檢視系統數據，主動聯繫未完成者", "status": "done", "detail": "已完成 12 位聯繫"},
    {"time": "10:00-12:00", "task": "處理紅色/黃色警示患者", "status": "current", "detail": "進行中 - 待處理 4 件"},
    {"time": "13:00-15:00", "task": "執行轉介、與醫療團隊溝通", "status": "upcoming", "detail": "營養 2 件、緩和 1 件"},
    {"time": "15:00-17:00", "task": "數據輸入、個案管理日誌", "status": "upcoming", "detail": ""},
]

COMPLIANCE_DATA = pd.DataFrame({
    '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
    'AI-ePRO': [82, 85, 78, 88, 91, 86],
    '傳統ePRO': [65, 62, 58, 55, 52, 48]
})

# ============================================
# 輔助函數
# ============================================
def simulate_ai_response(user_input):
    user_input = user_input.lower() if user_input else ""
    
    if any(word in user_input for word in ['悶', '喘', '呼吸']):
        return "了解，胸口悶悶的感覺。\n\n請問用 0-10 分來評估，0 分是完全不悶，10 分是非常悶，您覺得大概幾分呢？\n\n（可以用下方滑桿選擇）"
    elif any(word in user_input for word in ['累', '疲', '沒力']):
        return "謝謝您告訴我。疲勞感是術後常見的症狀。\n\n請問這個疲勞感，如果用 0-10 分來評估，您覺得大概幾分呢？"
    elif any(word in user_input for word in ['痛', '疼']):
        return "了解您有疼痛的感覺。\n\n請問：\n1. 疼痛的位置在哪裡？\n2. 用 0-10 分評估，大概幾分？\n3. 是持續痛還是間歇性的？"
    elif any(word in user_input for word in ['咳', '痰']):
        return "好的，關於咳嗽的問題。\n\n請問：\n1. 有沒有痰？\n2. 痰的顏色是？（白/黃/綠/帶血）\n3. 咳嗽嚴重程度 0-10 分？"
    elif any(word in user_input for word in ['不錯', '好', '還好', '👍']):
        return "太好了！很高興聽到您感覺不錯 😊\n\n為了完整記錄，想再確認一下：\n• 有沒有任何疼痛感？\n• 呼吸是否順暢？\n• 睡眠品質如何？"
    elif user_input.replace('分', '').replace('點', '.').replace('。', '').strip().replace('.', '', 1).isdigit():
        try:
            score = float(user_input.replace('分', '').replace('點', '.').replace('。', '').strip())
            score = int(score)
        except:
            score = 5
            
        if score >= 7:
            return f"收到，您評估為 {score} 分，這個分數較高。\n\n⚠️ 我已經通知您的個案管理師，她會在 30 分鐘內與您電話聯繫。\n\n在等待期間，您可以：\n• 找個舒適的姿勢休息\n• 試著做噘嘴式呼吸\n• 如果感覺更不舒服，請直接撥打緊急電話"
        elif score >= 4:
            return f"收到，您評估為 {score} 分。\n\n💡 小建議：\n• 噘嘴式呼吸：鼻子吸氣 2 秒，噘嘴慢慢吐氣 4 秒\n• 姿勢調整：稍微前傾坐著可能會舒服一些\n• 適度活動：短距離散步有助於改善\n\n個管師會在今天稍後關心您的狀況。"
        else:
            return f"收到，您評估為 {score} 分，這是很好的狀況！\n\n✅ 今日症狀回報已完成\n\n繼續保持，記得：\n• 每天按時服藥\n• 適度活動\n• 充足休息\n\n明天見！🌟"
    else:
        return "謝謝您的回覆。\n\n能否再詳細描述一下您的感受呢？例如：\n• 有沒有疼痛？\n• 呼吸是否順暢？\n• 有沒有咳嗽？"

def get_status_style(status):
    styles = {
        "alert": {"color": "#dc2626", "bg": "#fef2f2", "icon": "🔴", "border": "#ef4444"},
        "warning": {"color": "#d97706", "bg": "#fffbeb", "icon": "🟡", "border": "#f59e0b"},
        "overdue": {"color": "#7c3aed", "bg": "#f5f3ff", "icon": "⏰", "border": "#8b5cf6"},
        "normal": {"color": "#16a34a", "bg": "#f0fdf4", "icon": "✅", "border": "#22c55e"}
    }
    return styles.get(status, styles["normal"])

def get_alert_style(level):
    styles = {
        "red": {"color": "#dc2626", "bg": "#fef2f2", "badge": "#ef4444"},
        "yellow": {"color": "#d97706", "bg": "#fffbeb", "badge": "#f59e0b"},
        "green": {"color": "#16a34a", "bg": "#f0fdf4", "badge": "#22c55e"}
    }
    return styles.get(level, styles["green"])

# ============================================
# 頂部導航
# ============================================
def render_nav():
    # Logo
    st.markdown("""
    <div style="text-align: center; padding: 8px 0 16px 0;">
        <span style="font-size: 28px;">🫁</span>
        <span style="font-size: 18px; font-weight: 700; color: #1e293b; margin-left: 8px;">AI-CARE Lung</span>
        <span style="font-size: 11px; color: #64748b; margin-left: 8px;">Demo</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 導航按鈕
    cols = st.columns(3)
    
    pages = [
        ("patient", "👤 病人端", "#10b981"),
        ("manager", "👩‍⚕️ 個管師", "#3b82f6"),
        ("data", "📊 資料中心", "#8b5cf6")
    ]
    
    for col, (page_id, label, color) in zip(cols, pages):
        is_active = st.session_state.page == page_id
        if col.button(
            label, 
            key=f"nav_{page_id}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = page_id
            st.rerun()

# ============================================
# 病人端介面（完整版）
# ============================================
def render_patient():
    # 頂部資訊卡
    st.markdown("""
    <div style="background: linear-gradient(135deg, #10b981, #059669); border-radius: 20px; padding: 24px; color: white; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p style="opacity: 0.9; margin: 0 0 4px 0; font-size: 14px;">早安，王先生</p>
                <h2 style="margin: 0; font-size: 20px; font-weight: 600;">今日健康回報</h2>
            </div>
            <div style="font-size: 32px;">🌤️</div>
        </div>
        <div style="background: rgba(255,255,255,0.15); border-radius: 14px; padding: 16px; margin-top: 16px;">
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div>
                    <div style="font-size: 24px; font-weight: 700;">75%</div>
                    <div style="font-size: 12px; opacity: 0.9;">本週完成率</div>
                </div>
                <div style="width: 1px; background: rgba(255,255,255,0.3);"></div>
                <div>
                    <div style="font-size: 24px; font-weight: 700;">12</div>
                    <div style="font-size: 12px; opacity: 0.9;">連續天數 🎉</div>
                </div>
                <div style="width: 1px; background: rgba(255,255,255,0.3);"></div>
                <div>
                    <div style="font-size: 24px; font-weight: 700;">D+14</div>
                    <div style="font-size: 12px; opacity: 0.9;">術後天數</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["💬 對話回報", "📊 歷史紀錄", "📚 衛教專區"])
    
    with tab1:
        # 聊天記錄
        st.markdown("#### 與健康小助手對話")
        
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history[-6:]:
                if msg["role"] == "ai":
                    st.markdown(f"""
                    <div style="display: flex; gap: 10px; margin-bottom: 12px;">
                        <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #10b981, #059669); display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 16px;">🤖</div>
                        <div>
                            <div style="font-size: 11px; color: #64748b; margin-bottom: 4px;">健康小助手 · {msg['time']}</div>
                            <div class="chat-ai">{msg['content'].replace(chr(10), '<br>')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
                        <div style="text-align: right;">
                            <div style="font-size: 11px; color: #64748b; margin-bottom: 4px;">{msg['time']}</div>
                            <div class="chat-user">{msg['content']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 快速回覆
        st.markdown("**快速回覆**")
        col1, col2 = st.columns(2)
        
        quick_replies = [
            ("😊 還不錯", "還不錯 👍"),
            ("😓 有點累", "有點累"),
            ("😮‍💨 胸口悶", "胸口悶悶的"),
            ("😣 有點痛", "有點痛")
        ]
        
        for i, (label, content) in enumerate(quick_replies):
            col = col1 if i % 2 == 0 else col2
            if col.button(label, key=f"quick_{i}", use_container_width=True):
                now = datetime.now().strftime("%H:%M")
                st.session_state.chat_history.append({"role": "user", "content": content, "time": now})
                st.session_state.chat_history.append({"role": "ai", "content": simulate_ai_response(content), "time": now})
                st.rerun()
        
        # 症狀評分
        st.markdown("---")
        st.markdown("**症狀評分（0-10 分）**")
        
        score = st.slider("選擇不適程度", 0, 10, 0, key="symptom_score")
        
        if score <= 3:
            color, label, emoji = "#22c55e", "輕微", "🟢"
        elif score <= 6:
            color, label, emoji = "#f59e0b", "中度", "🟡"
        else:
            color, label, emoji = "#ef4444", "嚴重", "🔴"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 16px; background: {color}15; border-radius: 12px; margin: 8px 0;">
            <span style="font-size: 32px;">{emoji}</span>
            <p style="color: {color}; font-weight: 600; font-size: 16px; margin: 8px 0 0 0;">{label} ({score}/10)</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"📤 提交評分 ({score}分)", use_container_width=True, type="primary"):
            now = datetime.now().strftime("%H:%M")
            st.session_state.chat_history.append({"role": "user", "content": f"{score}分", "time": now})
            st.session_state.chat_history.append({"role": "ai", "content": simulate_ai_response(str(score)), "time": now})
            st.rerun()
        
        # 文字輸入
        st.markdown("---")
        user_input = st.text_input("或輸入您的感受：", placeholder="例如：今天覺得有點喘...", key="user_text_input")
        
        if st.button("📤 送出", use_container_width=True):
            if user_input:
                now = datetime.now().strftime("%H:%M")
                st.session_state.chat_history.append({"role": "user", "content": user_input, "time": now})
                st.session_state.chat_history.append({"role": "ai", "content": simulate_ai_response(user_input), "time": now})
                st.rerun()
    
    with tab2:
        st.markdown("#### 📈 症狀趨勢")
        
        # 模擬過去7天數據
        dates = [(datetime.now() - timedelta(days=i)).strftime("%m/%d") for i in range(6, -1, -1)]
        scores = [3, 2, 4, 3, 5, 3, 2]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=scores,
            mode='lines+markers',
            line=dict(color='#10b981', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="日期",
            yaxis_title="症狀分數",
            yaxis=dict(range=[0, 10])
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 歷史記錄
        st.markdown("#### 📋 回報記錄")
        
        history = [
            {"date": "今天 09:30", "symptoms": "輕微疲勞", "score": 2, "status": "正常"},
            {"date": "昨天 10:15", "symptoms": "胸悶", "score": 3, "status": "正常"},
            {"date": "12/24 08:45", "symptoms": "呼吸順暢", "score": 1, "status": "良好"},
            {"date": "12/23 09:00", "symptoms": "輕微咳嗽", "score": 3, "status": "正常"},
        ]
        
        for h in history:
            color = "#22c55e" if h["score"] <= 3 else "#f59e0b" if h["score"] <= 6 else "#ef4444"
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 14px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 12px; color: #64748b;">{h['date']}</div>
                    <div style="font-weight: 500; color: #1e293b;">{h['symptoms']}</div>
                </div>
                <div style="background: {color}20; color: {color}; padding: 4px 12px; border-radius: 8px; font-weight: 600;">
                    {h['score']}分
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("#### 📚 衛教資源")
        
        # 衛教卡片
        edu_items = [
            {"icon": "🫁", "title": "噘嘴式呼吸", "desc": "改善呼吸困難的技巧", "tag": "呼吸訓練"},
            {"icon": "🚶", "title": "術後活動指引", "desc": "循序漸進恢復活動", "tag": "運動"},
            {"icon": "🍎", "title": "營養補充建議", "desc": "促進傷口癒合的飲食", "tag": "營養"},
            {"icon": "💊", "title": "藥物注意事項", "desc": "止痛藥與其他用藥", "tag": "用藥"},
            {"icon": "😴", "title": "睡眠姿勢", "desc": "術後舒適的睡姿", "tag": "休息"},
            {"icon": "🚨", "title": "警示症狀", "desc": "何時需要立即就醫", "tag": "重要"},
        ]
        
        for item in edu_items:
            tag_color = "#ef4444" if item["tag"] == "重要" else "#3b82f6"
            st.markdown(f"""
            <div style="background: white; border-radius: 14px; padding: 16px; margin-bottom: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); display: flex; align-items: center; gap: 14px;">
                <div style="font-size: 32px;">{item['icon']}</div>
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                        <span style="font-weight: 600; color: #1e293b;">{item['title']}</span>
                        <span style="background: {tag_color}15; color: {tag_color}; padding: 2px 8px; border-radius: 6px; font-size: 11px;">{item['tag']}</span>
                    </div>
                    <div style="font-size: 13px; color: #64748b;">{item['desc']}</div>
                </div>
                <div style="color: #94a3b8;">▶</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 今日小知識
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fef3c7, #fef9c3); border: 1px solid #fcd34d; border-radius: 16px; padding: 20px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                <span style="font-size: 24px;">💡</span>
                <span style="font-weight: 600; color: #92400e; font-size: 16px;">今日小知識</span>
            </div>
            <p style="color: #78350f; font-size: 14px; line-height: 1.6; margin: 0;">
                <strong>噘嘴式呼吸練習</strong><br>
                1. 用鼻子慢慢吸氣 2 秒<br>
                2. 噘起嘴巴，像吹蠟燭一樣<br>
                3. 慢慢吐氣 4 秒<br><br>
                每天練習 5 次，可以幫助改善肺功能！
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # 緊急聯繫（固定在底部）
    st.markdown("---")
    if st.button("🚨 緊急聯繫個管師", use_container_width=True, type="secondary"):
        st.error("📞 正在撥打個管師專線：0912-345-678")

# ============================================
# 個管師端介面（完整版）
# ============================================
def render_manager():
    # 統計摘要
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3b82f6, #2563eb); border-radius: 20px; padding: 20px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0 0 16px 0; font-size: 18px;">👩‍⚕️ 今日工作台</h3>
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="font-size: 28px; font-weight: 700;">2</div>
                <div style="font-size: 12px; opacity: 0.9;">🔴 紅色</div>
            </div>
            <div>
                <div style="font-size: 28px; font-weight: 700;">5</div>
                <div style="font-size: 12px; opacity: 0.9;">🟡 黃色</div>
            </div>
            <div>
                <div style="font-size: 28px; font-weight: 700;">3</div>
                <div style="font-size: 12px; opacity: 0.9;">⏰ 逾期</div>
            </div>
            <div>
                <div style="font-size: 28px; font-weight: 700;">32</div>
                <div style="font-size: 12px; opacity: 0.9;">✅ 正常</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚠️ 警示", "📋 個案", "📝 紀錄", "📅 排程", "📊 統計"])
    
    with tab1:
        st.markdown("#### 即時警示")
        st.caption("🔴 30分鐘內處理 | 🟡 當日處理")
        
        for alert in ALERTS:
            style = get_alert_style(alert["level"])
            status_label = {"pending": "待處理", "contacted": "聯繫中", "resolved": "已處理"}
            
            st.markdown(f"""
            <div class="alert-{alert['level']}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 40px; height: 40px; border-radius: 10px; background: {style['badge']}; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px;">{alert['score']}</div>
                        <div>
                            <div style="font-weight: 600; color: {style['color']};">{alert['patient']}</div>
                            <div style="font-size: 12px; color: #64748b;">{alert['symptom']}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 11px; color: #64748b;">{alert['time']}</div>
                        <div style="font-size: 11px; color: {style['color']};">{status_label[alert['status']]}</div>
                    </div>
                </div>
                <div style="font-size: 12px; color: #64748b;">📱 {alert['phone']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if alert["status"] == "pending":
                col1, col2 = st.columns(2)
                col1.button(f"📞 電聯", key=f"call_{alert['id']}", use_container_width=True)
                col2.button(f"📋 詳情", key=f"detail_{alert['id']}", use_container_width=True)
    
    with tab2:
        st.markdown("#### 我的個案")
        
        # 搜尋
        search = st.text_input("🔍 搜尋病人", placeholder="姓名或病歷號...")
        
        for p in PATIENTS:
            if search and search not in p["name"] and search not in p["id"]:
                continue
                
            style = get_status_style(p["status"])
            
            with st.expander(f"{style['icon']} {p['name']} ({p['id']}) - D+{p['day']}"):
                col1, col2 = st.columns(2)
                col1.write(f"**年齡**：{p['age']} 歲")
                col2.write(f"**手術**：{p['surgery']}")
                
                col1, col2 = st.columns(2)
                col1.write(f"**順從度**：{p['compliance']}%")
                col2.write(f"**最後回報**：{p['last_report']}")
                
                st.progress(p['compliance'] / 100)
                
                col1, col2, col3 = st.columns(3)
                col1.button("📞 電話", key=f"p_call_{p['id']}", use_container_width=True)
                col2.button("💬 LINE", key=f"p_line_{p['id']}", use_container_width=True)
                col3.button("📝 紀錄", key=f"p_record_{p['id']}", use_container_width=True)
    
    with tab3:
        st.markdown("#### 介入紀錄")
        
        # 新增紀錄表單
        with st.form("new_record"):
            st.markdown("**新增紀錄**")
            
            col1, col2 = st.columns(2)
            patient = col1.selectbox("病人", ["選擇..."] + [p["name"] for p in PATIENTS])
            method = col2.selectbox("方式", ["電話", "LINE", "簡訊", "門診"])
            
            content = st.text_area("紀錄內容", placeholder="輸入聯繫紀錄...")
            
            col1, col2 = st.columns(2)
            need_referral = col1.checkbox("需要轉介")
            if need_referral:
                referral = col2.selectbox("轉介", ["緩和醫療", "營養", "復健", "心理"])
            
            if st.form_submit_button("💾 儲存紀錄", use_container_width=True):
                st.success("✅ 紀錄已儲存！")
        
        st.markdown("---")
        st.markdown("**最近紀錄**")
        
        for record in INTERVENTION_RECORDS:
            referral_tag = f'<span style="background: #fce7f3; color: #be185d; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-left: 4px;">→{record["referral"]}</span>' if record["referral"] else ""
            
            st.markdown(f"""
            <div style="background: white; border-radius: 12px; padding: 14px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>
                        <span style="font-weight: 600;">{record['patient']}</span>
                        <span style="background: #e0f2fe; color: #0369a1; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-left: 4px;">{record['type']}</span>
                        <span style="background: #f1f5f9; color: #64748b; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin-left: 4px;">{record['duration']}</span>
                        {referral_tag}
                    </div>
                    <span style="font-size: 11px; color: #94a3b8;">{record['time']}</span>
                </div>
                <p style="margin: 0; font-size: 13px; color: #475569; line-height: 1.5;">{record['content']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("#### 今日排程")
        
        for item in SCHEDULE:
            if item["status"] == "done":
                bg, border, icon = "#f0fdf4", "#bbf7d0", "✅"
            elif item["status"] == "current":
                bg, border, icon = "#eff6ff", "#bfdbfe", "▶️"
            else:
                bg, border, icon = "#f8fafc", "#e2e8f0", "⏳"
            
            st.markdown(f"""
            <div style="background: {bg}; border: 1px solid {border}; border-radius: 12px; padding: 14px; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 20px;">{icon}</span>
                    <div>
                        <div style="font-size: 12px; color: #64748b;">{item['time']}</div>
                        <div style="font-weight: 500; color: #1e293b;">{item['task']}</div>
                        {f'<div style="font-size: 12px; color: #64748b; margin-top: 2px;">{item["detail"]}</div>' if item["detail"] else ""}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("#### 工作統計")
        
        # 今日數據
        col1, col2 = st.columns(2)
        col1.metric("今日聯繫", "12 次", "+3")
        col2.metric("平均通話", "4.5 分鐘", "-0.5")
        
        col1, col2 = st.columns(2)
        col1.metric("警示處理", "8 件", "+2")
        col2.metric("轉介完成", "3 件", "+1")
        
        st.markdown("---")
        st.markdown("**本週工作量**")
        
        # 工作量圖表
        days = ['一', '二', '三', '四', '五']
        contacts = [10, 12, 8, 15, 12]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=days, y=contacts, marker_color='#3b82f6'))
        fig.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=20, b=40),
            xaxis_title="星期",
            yaxis_title="聯繫次數"
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# 資料中心介面（完整版）
# ============================================
def render_data():
    # 頂部統計
    st.markdown("""
    <div style="background: linear-gradient(135deg, #8b5cf6, #7c3aed); border-radius: 20px; padding: 20px; color: white; margin-bottom: 20px;">
        <h3 style="margin: 0 0 16px 0; font-size: 18px;">📊 研究數據總覽</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; text-align: center;">
            <div style="background: rgba(255,255,255,0.15); border-radius: 12px; padding: 12px;">
                <div style="font-size: 24px; font-weight: 700;">127</div>
                <div style="font-size: 11px; opacity: 0.9;">總收案 /150</div>
            </div>
            <div style="background: rgba(255,255,255,0.15); border-radius: 12px; padding: 12px;">
                <div style="font-size: 24px; font-weight: 700;">78.5%</div>
                <div style="font-size: 11px; opacity: 0.9;">完成率</div>
            </div>
            <div style="background: rgba(255,255,255,0.15); border-radius: 12px; padding: 12px;">
                <div style="font-size: 24px; font-weight: 700;">85.2%</div>
                <div style="font-size: 11px; opacity: 0.9;">AI組</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 總覽", "🏆 品質", "📋 順從度", "💾 匯出"])
    
    with tab1:
        st.markdown("#### 收案進度")
        
        groups = [
            ("組別A (AI-ePRO)", 45, 50, "#8b5cf6"),
            ("組別B (傳統ePRO)", 42, 50, "#3b82f6"),
            ("組別C (常規照護)", 40, 50, "#64748b"),
        ]
        
        for name, current, target, color in groups:
            pct = current / target * 100
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                    <span style="font-size: 13px; color: #1e293b;">{name}</span>
                    <span style="font-size: 13px; font-weight: 600; color: {color};">{current}/{target} ({pct:.0f}%)</span>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {pct}%; background: {color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 研究時程")
        
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 6px; overflow-x: auto; padding: 8px 0;">
            <div style="background: #22c55e; color: white; padding: 10px 14px; border-radius: 8px; font-size: 12px; white-space: nowrap;">✓ Y1</div>
            <div style="color: #22c55e; font-size: 12px;">→</div>
            <div style="background: #8b5cf6; color: white; padding: 10px 14px; border-radius: 8px; font-size: 12px; white-space: nowrap;">▶ Y2 RCT</div>
            <div style="color: #94a3b8; font-size: 12px;">→</div>
            <div style="background: #e2e8f0; color: #64748b; padding: 10px 14px; border-radius: 8px; font-size: 12px; white-space: nowrap;">Y3 多中心</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 順從度趨勢")
        
        fig = px.line(COMPLIANCE_DATA, x='月份', y=['AI-ePRO', '傳統ePRO'],
                     color_discrete_map={'AI-ePRO': '#8b5cf6', '傳統ePRO': '#94a3b8'})
        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=20, b=40),
            legend_title_text='',
            yaxis_title='完成率 (%)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### 品質指標達成")
        
        quality_metrics = [
            {"name": "緩和轉介率", "indicator": "#4", "current": 68, "target": 60, "trend": "+28%", "good": True},
            {"name": "30天死亡率", "indicator": "#6", "current": 1.2, "target": 2, "trend": "-52%", "good": True},
            {"name": "完治率", "indicator": "#9", "current": 82, "target": 75, "trend": "+17%", "good": True},
            {"name": "個管收案率", "indicator": "#5", "current": 95, "target": 90, "trend": "+27%", "good": True},
        ]
        
        for m in quality_metrics:
            color = "#22c55e" if m["good"] else "#f59e0b"
            st.markdown(f"""
            <div style="background: white; border-radius: 14px; padding: 16px; margin-bottom: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>
                        <span style="background: #f5f3ff; color: #7c3aed; padding: 2px 8px; border-radius: 4px; font-size: 10px;">指標{m['indicator']}</span>
                        <span style="font-weight: 600; color: #1e293b; margin-left: 8px;">{m['name']}</span>
                    </div>
                    <span style="background: {color}20; color: {color}; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;">{m['trend']}</span>
                </div>
                <div style="display: flex; align-items: baseline; gap: 8px;">
                    <span style="font-size: 28px; font-weight: 700; color: #1e293b;">{m['current']}{'%' if m['current'] > 10 else '%'}</span>
                    <span style="font-size: 13px; color: #64748b;">目標 {m['target']}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 🏆 品質認證進度")
        
        cert = [
            ("📊 管理面", 3, 4),
            ("💉 照護面", 12, 15),
            ("📈 成效面", 7, 9),
        ]
        
        for label, done, total in cert:
            pct = done / total * 100
            st.markdown(f"""
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>{label}</span>
                    <span style="font-weight: 600;">{done}/{total}</span>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {pct}%; background: #8b5cf6;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("#### 各時段完成率")
        
        periods = [
            ("住院期間", 95),
            ("出院後 1 個月", 88),
            ("出院後 2-3 個月", 75),
            ("出院後 4-6 個月", 68),
            ("出院後 7-12 個月", 62),
        ]
        
        for period, rate in periods:
            color = "#22c55e" if rate >= 80 else "#f59e0b" if rate >= 60 else "#ef4444"
            st.markdown(f"""
            <div style="margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-size: 13px; color: #1e293b;">{period}</span>
                    <span style="font-size: 13px; font-weight: 600; color: {color};">{rate}%</span>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {rate}%; background: {color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 順從度影響因子")
        
        factors = [
            ("年齡 ≥65 歲", -15, False),
            ("大學以上學歷", 12, True),
            ("有主要照顧者", 18, True),
            ("智慧型手機經驗 ≥3年", 22, True),
            ("基線焦慮 (GAD-7≥10)", -8, False),
        ]
        
        for factor, impact, positive in factors:
            color = "#16a34a" if positive else "#dc2626"
            bg = "#f0fdf4" if positive else "#fef2f2"
            sign = "+" if impact > 0 else ""
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 14px; background: {bg}; border-radius: 10px; margin-bottom: 8px;">
                <span style="font-size: 13px; color: #1e293b;">{factor}</span>
                <span style="font-weight: 600; color: {color};">{sign}{impact}%</span>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("#### 數據匯出")
        
        formats = [
            ("📊 SPSS", ".sav"),
            ("📈 R", ".rds"),
            ("📉 SAS", ".sas7bdat"),
            ("📄 CSV", ".csv"),
            ("📗 Excel", ".xlsx"),
            ("🔗 REDCap", "同步"),
        ]
        
        col1, col2 = st.columns(2)
        for i, (name, ext) in enumerate(formats):
            col = col1 if i % 2 == 0 else col2
            col.button(f"{name} {ext}", key=f"export_{i}", use_container_width=True)
        
        st.markdown("---")
        st.markdown("**匯出選項**")
        
        col1, col2 = st.columns(2)
        col1.checkbox("去識別化處理", value=True)
        col2.checkbox("包含數據字典", value=True)
        
        col1, col2 = st.columns(2)
        col1.checkbox("僅完成追蹤者")
        col2.checkbox("包含稽核軌跡")
        
        if st.button("📦 產生匯出檔案", use_container_width=True, type="primary"):
            st.success("✅ 檔案產生中，請稍候...")

# ============================================
# 主程式
# ============================================
def main():
    render_nav()
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.page == "patient":
        render_patient()
    elif st.session_state.page == "manager":
        render_manager()
    elif st.session_state.page == "data":
        render_data()
    
    # Footer
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 16px; color: #94a3b8; font-size: 11px;">
        AI-CARE Lung Trial | 三軍總醫院 數位醫學中心 © 2024
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
