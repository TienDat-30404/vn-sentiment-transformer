import streamlit as st
from underthesea import text_normalize

# Từ điển thay thế cho tiền xử lý Tiếng Việt
REPLACEMENTS = {
    'rat': 'rất', 'qua': 'quá', 'chua': 'chưa', 'toi': 'tôi', 'hom': 'hôm',
    'nay': 'nay', 'do': 'đó', 'day': 'đây', 'buon': 'buồn', 'vui': 'vui',
    'ghe': 'ghê', 'lam': 'lắm', 'thich': 'thích', 'khong': 'không', 
    'cung': 'cũng', 'binh' : 'bình', 'thuong' : 'thường', 'do' : 'dở',
    'mai': 'mai'
}

# Ánh xạ nhãn Transformer về POSITIVE/NEUTRAL/NEGATIVE
LABEL_MAPPING = {
    'POS': 'POSITIVE', 'NEG': 'NEGATIVE', 'NEU': 'NEUTRAL',
    'LABEL_1': 'POSITIVE', 'LABEL_0': 'NEGATIVE', 'LABEL_2': 'NEUTRAL',
}


def normalize_and_add_diacritics(text):
    """Chuẩn hóa văn bản (thêm dấu, xử lý viết tắt)"""
    try:
        text = text_normalize(text) 
    except NameError:
        pass 

    text_lower = text.lower()
    words = text_lower.split()
    processed_words = [REPLACEMENTS.get(word, word) for word in words]
    
    return ' '.join(processed_words)

def analyze_sentiment_vietnamese(text, sentiment_pipeline):
    processed_text = normalize_and_add_diacritics(text) 
    
    #Kiểm tra đầu vào (5 <= độ dài <= 50)
    if len(processed_text) < 5 or len(processed_text) > 50:
        return {"label": "NEUTRAL", "score": 0.50}
    
  
    try:
        results = sentiment_pipeline(processed_text)
    except Exception as e:
        st.error(f"Lỗi khi chạy pipeline Transformer: {e}")
        return {"label": "NEUTRAL", "score": 0.50}

    # Xử lý kết quả đầu ra
    result = results[0]
    raw_label = result['label'].upper()
    label = LABEL_MAPPING.get(raw_label, 'NEUTRAL')
    confidence = result['score'] 
    
    if confidence < 0.5:
        return {"label": "NEUTRAL", "score": 0.50}

    return {"label": label, "score": confidence}