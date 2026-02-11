import os
import json
import re
import sys
import io
import contextlib
import warnings
from typing import Optional, List, Any, Tuple
from PIL import Image
import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from google import genai
from google.genai import types
from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)

def code_interpret(e2b_code_interpreter: Sandbox, code: str) -> Tuple[Optional[List[Any]], str]:
    with st.spinner('Executing code in E2B sandbox...'):
        exec = e2b_code_interpreter.run_code(code)
        
        stdout_output = exec.logs.stdout
        stderr_output = exec.logs.stderr

        if stderr_output:
            print(f"[Sandbox Error] {''.join(stderr_output)}", file=sys.stderr)
            
        return exec.results, "\n".join(stdout_output)

def match_code_blocks(llm_response: str) -> str:
    match = pattern.search(llm_response)
    if match:
        code = match.group(1)
        return code
    return ""

def chat_with_llm(e2b_code_interpreter: Sandbox, user_message: str, dataset_path: str) -> Tuple[Optional[List[Any]], str, str]:
    # Clearer instructions to ensure the AI knows which columns exist
    try:
        df_sample = pd.read_csv(dataset_path, nrows=2)
        columns_list = df_sample.columns.tolist()
    except:
        columns_list = []

    system_prompt = f"""You are a Senior AI Data Scientist. Follow the 'Agentic Pipeline':
1. VALIDATION | 2. PREPROCESSING | 3. ANOMALY DETECTION | 4. VISUALIZATION

IMPORTANT:
- Dataset location: '{dataset_path}'
- Actual Columns: {columns_list}
- First, write a brief human-readable plan in your response.
- Then, write a Python code block using ```python...```.
- Inside the code, use `print()` for the 'Data Health Report' and 'Cleaning Log'.
- Ensure you use the correct column names from the provided list: {columns_list}."""

    with st.spinner('Applying Agentic Pipeline logic...'):
        try:
            client = genai.Client(api_key=st.session_state.google_api_key)
            
            response = client.models.generate_content(
                model=st.session_state.model_name,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt
                )
            )
            response_text = response.text
            
            python_code = match_code_blocks(response_text)
            
            if python_code:
                code_results, code_stdout = code_interpret(e2b_code_interpreter, python_code)
                return code_results, response_text, code_stdout
            else:
                st.warning(f"Failed to match any Python code in model's response")
                return None, response_text, ""
        except Exception as e:
            if "429" in str(e) or "ResourceExhausted" in str(e):
                st.error("🚫 **Quota Exceeded:** You've hit the Gemini API rate limit. Please wait a few seconds.")
            else:
                st.error(f"An error occurred: {e}")
            return None, "", ""

def upload_dataset(code_interpreter: Sandbox, uploaded_file) -> str:
    dataset_path = f"./{uploaded_file.name}"
    
    try:
        code_interpreter.files.write(dataset_path, uploaded_file.getvalue())
        return dataset_path
    except Exception as error:
        st.error(f"Error during file upload: {error}")
        raise error


def main():
    """Main Streamlit application with Golden Pipeline UI."""
    st.set_page_config(
        page_title="Agentic Data Sanitizer | Agentic Pipeline",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for a premium look
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            background-color: #2563eb;
            color: white;
            font-weight: bold;
            border: none;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #1d4ed8;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        .report-section {
            background-color: white;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #2563eb;
            margin-bottom: 1rem;
        }
        h1 {
            color: #1e293b;
            font-weight: 800 !important;
        }
        pre {
            background-color: #f1f5f9;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🛡️ Agentic Data Sanitizer")
    st.caption("Engineered with the Agentic Pipeline Architecture: Audit > Clean > Detect > Visualize")
    st.markdown("---")

    # Initialize session state variables
    if 'google_api_key' not in st.session_state:
        st.session_state.google_api_key = os.getenv("GOOGLE_API_KEY", "")
    if 'e2b_api_key' not in st.session_state:
        st.session_state.e2b_api_key = os.getenv("E2B_API_KEY", "")
    if 'query_input' not in st.session_state:
        st.session_state.query_input = ""
    
    st.session_state.model_name = 'gemini-2.5-flash'

    with st.sidebar:
        st.header("⚙️ Control Panel")
        with st.expander("🔑 Credentials", expanded=False):
            st.session_state.google_api_key = st.text_input("Gemini API Key", value=st.session_state.google_api_key, type="password")
            st.session_state.e2b_api_key = st.text_input("E2B API Key", value=st.session_state.e2b_api_key, type="password")
        
        st.divider()
        st.info("💡 Pro Tip: Upload any 'dirty' dataset with missing values or inconsistent formatting to see the Agentic Pipeline in action.")

    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.subheader("📁 Dataset Source")
        uploaded_file = st.file_uploader("Upload CSV", type="csv")
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success(f"Loaded: {uploaded_file.name}")
            
            with st.expander("🔍 Raw Data Preview"):
                st.dataframe(df.head(5), use_container_width=True)

    with col2:
        st.subheader("💬 AI Analyst")
        
        if uploaded_file is not None:
            # Dynamic Recommendations based on columns
            cols = df.columns.tolist()
            recs = ["🛡️ Perform a full data health audit"]
            
            if any(c in str(cols).lower() for c in ['date', 'time', 'year', 'month']):
                recs.append("📈 Analyze temporal trends and growth")
            if any(c in str(cols).lower() for c in ['sales', 'revenue', 'price', 'amount']):
                recs.append("💰 Identify revenue anomalies and outliers")
            if any(c in str(cols).lower() for c in ['category', 'region', 'type', 'group']):
                recs.append("🍕 Show distribution across categories")
            
            st.markdown("##### 💡 AI Recommendations")
            # Display recommendations as small buttons
            rec_cols = st.columns(len(recs))
            for i, rec in enumerate(recs):
                if rec_cols[i].button(rec, use_container_width=True, key=f"rec_{i}"):
                    st.session_state.query_input = rec.split(" ", 1)[1] # Remove emoji
                    st.rerun()

        query = st.text_area("Type your custom instructions...", 
                           value=st.session_state.query_input,
                           placeholder="Ex: Compare sales by region and show me a heatmap.",
                           height=150)
        
        analyze_btn = st.button("🚀 Execute Agentic Pipeline")

    if uploaded_file and analyze_btn:
        final_query = query
        
        if not st.session_state.google_api_key or not st.session_state.e2b_api_key:
            st.error("Missing API Keys! Configure in sidebar.")
        else:
            with Sandbox(api_key=st.session_state.e2b_api_key) as code_interpreter:
                dataset_path = upload_dataset(code_interpreter, uploaded_file)
                code_results, llm_response, code_stdout = chat_with_llm(code_interpreter, final_query, dataset_path)
                
                if llm_response:
                    st.markdown("---")
                    
                    # AI's textual reasoning
                    text_report = pattern.sub("", llm_response).strip()
                    
                    tab_audit, tab_viz, tab_raw = st.tabs(["📋 Data Audit & Cleaning", "📊 Intelligent Visuals", "🤖 AI Insight"])
                    
                    with tab_audit:
                        if text_report:
                            st.markdown(f"### 🚩 Analyst Strategy\n{text_report}")
                        
                        if code_stdout:
                            st.markdown("### 🛠️ Execution Log")
                            # Extract health score if present for a nice metric
                            if "Health Score:" in code_stdout:
                                try:
                                    score = code_stdout.split("Health Score:")[1].split("%")[0].strip()
                                    st.metric("Data Health Score", f"{score}%")
                                except:
                                    pass
                            st.code(code_stdout, language="markdown")
                        
                    with tab_viz:
                        if code_results:
                            st.write("### 📈 Intelligent Visualizations")
                            for result in code_results:
                                if hasattr(result, 'png') and result.png:
                                    png_data = base64.b64decode(result.png)
                                    st.image(Image.open(BytesIO(png_data)), use_container_width=True)
                                elif hasattr(result, 'figure'):
                                    st.pyplot(result.figure, use_container_width=True)
                                elif isinstance(result, (pd.DataFrame, pd.Series)):
                                    st.dataframe(result, use_container_width=True)
                        else:
                            st.warning("No visual artifacts generated. The agent prioritized a structural audit. Try asking for a 'plot' or 'trend' specifically.")

                    with tab_raw:
                        st.info("Full System Trace and Technical Output:")
                        st.code(llm_response, language="markdown")

    # Professional Footer
    st.markdown("""
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: white;
            color: #64748b;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            border-top: 1px solid #e2e8f0;
            z-index: 100;
        }
        </style>
        <div class="footer">
            Built with ❤️ by <b>Aravind S Gudi</b> | Agentic Pipeline v1.0
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
