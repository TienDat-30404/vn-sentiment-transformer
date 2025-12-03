"""
Trợ lý Phân loại Cảm xúc Tiếng Việt sử dụng Transformer
Sinh viên: Đặng Tiến Đạt
Thời gian: 06/12/2025
"""

import streamlit as st
import torch
from transformers import pipeline 
import warnings
import pandas as pd
import plotly.express as px

from database import (
    init_database, save_sentiment, get_all_sentiments, 
    get_statistics, clear_database
)
from nlp_processor import analyze_sentiment_vietnamese

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Phân loại Cảm xúc Tiếng Việt",
    page_icon="💬",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 12px;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .sentiment-positive {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .sentiment-negative {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .sentiment-neutral {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ========================== TẢI MÔ HÌNH ==========================
@st.cache_resource
def load_sentiment_pipeline():
    model_name = "wonrax/phobert-base-vietnamese-sentiment"
    
    try:
        st.info(f"Đang tải mô hình Transformer: {model_name}. Quá trình này có thể mất vài phút lần đầu.")
        sentiment_pipeline = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)
        st.success("Tải mô hình Transformer thành công!")
        return sentiment_pipeline
    except Exception as e:
        st.error(f"Lỗi tải mô hình Transformer: {e}.")
        return None

sentiment_pipeline = load_sentiment_pipeline()

# ========================== LOGIC CHÍNH ==========================
def main():
    init_database()
    st.title("💬 Trợ lý Phân loại Cảm xúc Tiếng Việt (Sử dụng Transformer)")
    st.subheader(f"Sinh viên: Đặng Tiến Đạt (3122560011) - Thời gian: 06/12/2025")

    if sentiment_pipeline is None:
        st.error("Ứng dụng không thể chạy do lỗi tải mô hình Transformer.")
        return

    tab1, tab2, tab3 = st.tabs(["Phân tích", "Thống kê", "Lịch sử"])

    with tab1:
        st.header("Nhập nội dung để phân loại cảm xúc")
        user_input = st.text_area("Nhập câu Tiếng Việt:", value="Hôm nay tôi rất vui", height=100, max_chars=50)

        if st.button("Phân loại cảm xúc"):
            if 5 <= len(user_input) <= 50:
                result = analyze_sentiment_vietnamese(user_input, sentiment_pipeline)
                
                save_sentiment(user_input, result["label"], result["score"])
                
                st.subheader("✅ Kết quả Phân loại")
                
                if result["label"] == "POSITIVE":
                    display_label = "POSITIVE"
                    css_class = "sentiment-positive"
                elif result["label"] == "NEGATIVE":
                    display_label = "NEGATIVE"
                    css_class = "sentiment-negative"
                else:
                    display_label = "NEUTRAL"
                    css_class = "sentiment-neutral"

                st.markdown(f"""
                <div class="{css_class}">
                    <h3>Text: {user_input}</h3>
                    <h3>Sentiment: {display_label}</h3>
                    <p>Độ tin cậy: {result["score"]*100:.2f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
            elif len(user_input) < 5:
                st.warning("Văn bản quá ngắn. Vui lòng nhập tối thiểu 5 ký tự.")
            else: 
                 st.warning("Văn bản quá dài. Vui lòng nhập tối đa 50 ký tự.")


    with tab2:
        st.header("Thống kê Phân bố Cảm xúc")
        
        stats = get_statistics() 
        if stats:
            stats_df = pd.DataFrame(list(stats.items()), columns=['Cảm xúc', 'Số lượng'])
            all_labels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
            for label in all_labels:
                if label not in stats_df['Cảm xúc'].values:
                    stats_df.loc[len(stats_df)] = [label, 0]
            
            stats_df['Tên hiển thị'] = stats_df['Cảm xúc'].replace({
                'POSITIVE': 'Tích cực',
                'NEGATIVE': 'Tiêu cực',
                'NEUTRAL': 'Trung tính'
            })
            
            fig = px.pie(
                stats_df, values='Số lượng', names='Tên hiển thị', 
                title='Phân bố Cảm xúc trong Lịch sử',
                color_discrete_map={'Tích cực':'#28a745', 'Tiêu cực':'#dc3545', 'Trung tính':'#ffc107'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Chưa có dữ liệu phân loại nào để thống kê.")

    with tab3:
        st.header("Lịch sử phân loại (50 mục gần nhất)")
        
        history_df = get_all_sentiments() 
        
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("Xóa toàn bộ lịch sử", type="primary"):
                clear_database() 
                st.experimental_rerun()
                
        if not history_df.empty:
            history_df['confidence'] = (history_df['confidence'] * 100).round(2).astype(str) + '%'
            history_df['sentiment'] = history_df['sentiment'].replace({
                'POSITIVE': 'Tích cực', 'NEGATIVE': 'Tiêu cực', 'NEUTRAL': 'Trung tính'
            })
            history_df = history_df.rename(columns={
                'timestamp': 'Thời gian', 'text': 'Văn bản', 'sentiment': 'Cảm xúc', 'confidence': 'Độ tin cậy'
            })
            st.dataframe(history_df[['Thời gian', 'Văn bản', 'Cảm xúc', 'Độ tin cậy']], use_container_width=True, hide_index=True)
        else:
            st.info("Lịch sử phân loại trống.")

if __name__ == "__main__":
    try:
        _ = torch.rand(1)
        main()
    except ImportError:
        st.error("Lỗi: Không tìm thấy thư viện PyTorch. Vui lòng chạy lệnh: `pip install torch`")
    except Exception as e:
        st.error(f"Lỗi không xác định khi khởi chạy: {e}")