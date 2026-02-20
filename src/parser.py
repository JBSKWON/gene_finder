import io
import Bio.SeqIO
from snapgene_reader import snapgene_file_to_dict

def parse_fasta(file_bytes):
    """
    BioPython을 이용하여 fasta 파일을 파싱합니다.
    Description(헤더) 혹은 ID를 유전자/시퀀스 이름의 목록으로 반환합니다.
    """
    text = file_bytes.decode('utf-8')
    records = Bio.SeqIO.parse(io.StringIO(text), "fasta")
    
    gene_names = []
    for record in records:
        # Fasta의 description (예: >GeneName description text)
        if record.description:
            gene_names.append(record.description)
        elif record.id:
            gene_names.append(record.id)
        elif record.name:
            gene_names.append(record.name)
            
    return gene_names

def parse_dna(file_bytes):
    """
    snapgene_reader를 이용하여 .dna (SnapGene 바이너리) 파일을 파싱합니다.
    파일 내부에 마킹된 Feature (주석)들의 이름(name)을 반환합니다.
    """
    try:
        # snapgene_reader는 dict나 tmp 파일로 변환하여 처리
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(delete=False, suffix='.dna') as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        
        data = snapgene_file_to_dict(tmp_path)
        os.remove(tmp_path)
        
    except Exception as e:
        print(f"Error parsing .dna file: {e}")
        return []
        
    gene_names = []
    features = data.get('features', [])
    for feature in features:
        # Feature 안에 name이라는 속성이 일반적임
        name = feature.get('name', '')
        if name:
            gene_names.append(name)
            
    return gene_names

def extract_genes_from_file(uploaded_file):
    """
    Streamlit의 UploadedFile 객체를 받아, 확장자에 맞는 파싱을 수행하고
    추출된 유전자(Feature) 이름 리스트를 반환합니다.
    """
    file_name = uploaded_file.name.lower()
    file_bytes = uploaded_file.read()
    
    if file_name.endswith('.fasta') or file_name.endswith('.fa'):
        return parse_fasta(file_bytes)
    elif file_name.endswith('.dna'):
        return parse_dna(file_bytes)
    else:
        return []
