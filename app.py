import streamlit as st
from social_media_generator import SocialMediaPostGenerator
from datetime import datetime

# Set page config
st.set_page_config(page_title="AI Social Media Post Generator", page_icon="✨", layout="centered")

# Custom CSS for better readability
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    .stMarkdown {
        color: #FFFFFF;
    }
    .post-container {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #3E3E3E;
        color: #FFFFFF;
        margin: 10px 0;
    }
    .suggestion-container {
        background-color: #262730;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #3E3E3E;
        margin: 5px 0;
    }
    .history-container {
        background-color: #262730;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #3E3E3E;
        margin: 5px 0;
        cursor: pointer;
    }
    .history-container:hover {
        background-color: #2E3338;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSelectbox, .stTextInput {
        background-color: #262730;
        color: #FFFFFF;
    }
    .metadata {
        color: #888;
        font-size: 0.8em;
        margin-top: 5px;
    }
    .tiktok-post {
        font-family: 'TikTok Font', sans-serif;
        line-height: 1.5;
    }
    .hashtags {
        color: #25F4EE;
        font-size: 0.9em;
        margin-top: 10px;
    }
    .language-badge {
        background-color: #4CAF50;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        margin-left: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generator' not in st.session_state:
    st.session_state.generator = SocialMediaPostGenerator()
if 'show_history' not in st.session_state:
    st.session_state.show_history = False

# Title and description
st.title("✨ AI Social Media Post Generator")
st.markdown("""
Generate scroll-stopping, emotionally resonant social media posts in seconds. Powered by OpenRouter AI.
""")

# Tabs for generation and history
tab1, tab2 = st.tabs(["Generate Post", "History"])

with tab1:
    # Input form
    with st.form("post_form"):
        col1, col2 = st.columns(2)
        with col1:
            topic = st.text_input("Topic", "self-doubt")
            length = st.selectbox("Length", ["short", "medium", "long"], index=1)
        with col2:
            platform = st.selectbox("Platform", ["TikTok", "Facebook", "Instagram", "LinkedIn", "Twitter"], index=0)
            tone = st.selectbox("Tone", ["Inspirational", "Urgent", "Emotional", "Empathetic", "Professional", "Friendly", "Casual"], index=0)
        
        # Language selection
        language = st.selectbox("Language", ["EN", "BM"], index=0, help="EN: English, BM: Bahasa Malaysia")
        
        submitted = st.form_submit_button("✨ Generate Post")

    # Generate and display results
    if submitted:
        with st.spinner("✨ Generating your post..."):
            try:
                result = st.session_state.generator.generate_post(topic, length, platform, tone, language)
                
                st.markdown(f"### 📝 Generated Post <span class='language-badge'>{language}</span>", unsafe_allow_html=True)
                post_class = "tiktok-post" if platform == "TikTok" else ""
                st.markdown(f"""
                <div class="post-container {post_class}">
                {result['content'].replace('\n', '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                st.subheader("🖼️ Image Suggestions")
                for i, suggestion in enumerate(result['image_suggestions'], 1):
                    st.markdown(f"""
                    <div class="suggestion-container">
                    <strong>{i}.</strong> {suggestion}
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating post: {str(e)}")

with tab2:
    st.subheader("📚 Generated Posts History")
    
    # Get history
    history = st.session_state.generator.get_history()
    
    if not history:
        st.info("No posts generated yet. Start creating some posts!")
    else:
        # Add clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.generator.clear_history()
            st.rerun()
        
        # Display history
        for post in reversed(history):
            timestamp = datetime.fromisoformat(post['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            metadata = post['metadata']
            post_class = "tiktok-post" if metadata['platform'] == "TikTok" else ""
            
            st.markdown(f"""
            <div class="history-container {post_class}">
                <div>{post['content'].replace('\n', '<br>')}</div>
                <div class="metadata">
                    Topic: {metadata['topic']} | Platform: {metadata['platform']} | 
                    Length: {metadata['length']} | Tone: {metadata['tone']} | 
                    Language: {metadata.get('language', 'EN')} | Generated: {timestamp}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
---
<div style='text-align: center; color: #666;'>
Made with ❤️ using OpenRouter AI and Streamlit
</div>
""", unsafe_allow_html=True) 