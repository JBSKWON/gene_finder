import streamlit as st
import os
import sys

# src 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from parser import extract_genes_from_file
from search import filter_files

st.set_page_config(page_title="DNA & Fasta Finder", page_icon="🧬", layout="wide")

st.title("🧬 DNA & Fasta Finder")
st.markdown("여러 개의 `.dna` (SnapGene) 및 `.fasta` 파일을 업로드하고, 원하는 유전자 이름을 검색해 보세요.")

# 사이드바 혹은 메인 화면 구성
with st.sidebar:
    st.header("1. 파일 업로드")
    uploaded_files = st.file_uploader(
        "DNA / FASTA 파일을 끌어다 놓으세요. (여러 개 가능)", 
        type=['dna', 'fasta', 'fa'], 
        accept_multiple_files=True
    )
    
    st.markdown("---")
    st.markdown("💡 **Tip**: 파일은 한 번에 10~20개 정도 올리는 것을 권장합니다.")

st.header("2. 유전자 검색")
st.info("✨ **스마트 검색 지원**: 'Kanamycin', 'Kanamycin resistant' 처럼 풀네임을 검색해도 내부적으로 `KanR` 등의 약어를 포함해 함께 찾아줍니다! (대소문자 구분 없음)")
query = st.text_input("찾으려는 유전자 이름 (예: Kanamycin, GFP, AmpR 등)", "")

if uploaded_files:
    # 파싱 상태 표시를 위한 스피너
    with st.spinner("업로드된 파일들을 분석 중입니다..."):
        # 파싱 결과를 세션 스테이트에 캐싱 (성능 향상, 재파싱 방지)
        if "parsed_data" not in st.session_state or st.session_state.get("uploaded_files") != uploaded_files:
            parsed_data = []
            for file in uploaded_files:
                genes = extract_genes_from_file(file)
                parsed_data.append({
                    "file": file,
                    "genes": genes
                })
            st.session_state["parsed_data"] = parsed_data
            st.session_state["uploaded_files"] = uploaded_files

    if query:
        st.subheader("🔍 검색 결과")
        # 검색 로직 실행
        results = filter_files(query, st.session_state["parsed_data"])
        
        if results:
            st.success(f"총 {len(results)}개의 파일에서 '{query}'를 찾았습니다!")
            
            for res in results:
                with st.expander(f"📄 {res['file'].name}", expanded=True):
                    # 매칭된 유전자 하이라이트 표시
                    matched_str = ", ".join(res['matched_genes'])
                    st.markdown(f"**🔬 발견된 유전자 (매칭됨):** `{matched_str}`")
                    
                    if len(res['all_genes']) > 0:
                        st.caption(f"*이 파일에 포함된 전체 Feature 개수: {len(res['all_genes'])}개*")
        else:
            st.warning(f"업로드된 파일 중 '{query}'를 포함하는 파일이 없습니다.")
            
else:
    st.info("👈 왼쪽 사이드바에서 먼저 파일을 업로드해 주세요.")
