GENE_SYNONYMS = {
    # 항생제 내성 유전자 (Antibiotic Resistance)
    "kanr": ["kanamycin", "kanamycin resistant", "kanamycin resistance gene", "kan"],
    "ampr": ["ampicillin", "ampicillin resistant", "ampicillin resistance gene", "bla"],
    "cmr": ["chloramphenicol", "chloramphenicol resistant", "chloramphenicol resistance gene", "cat"],
    "tetr": ["tetracycline", "tetracycline resistant", "tetracycline resistance gene", "tet"],
    "specr": ["spectinomycin", "spectinomycin resistant", "spectinomycin resistance gene", "aada"],
    "zeor": ["zeocin", "zeocin resistant", "zeocin resistance gene", "ble"],
    "hygr": ["hygromycin", "hygromycin b", "hygromycin resistant", "hph"],
    "genr": ["gentamicin", "gentamicin resistant", "aacc1"],
    "neor": ["neomycin", "neomycin resistant"],
    "strr": ["streptomycin", "streptomycin resistant"],
    "eryr": ["erythromycin", "erythromycin resistant", "erm"],
    
    # 형광 단백질 (Fluorescent Proteins)
    "gfp": ["green fluorescent protein", "egfp"],
    "rfp": ["red fluorescent protein", "mcherry", "dsred"],
    "yfp": ["yellow fluorescent protein", "eyfp"],
    "cfp": ["cyan fluorescent protein", "ecfp"],
    
    # 선별 마커 및 기타 효소 (Selection Markers & Enzymes)
    "sacb": ["levansucrase", "sac b"],
    "ura3": ["orotidine 5-phosphate decarboxylase", "ura"],
    "leu2": ["beta-isopropylmalate dehydrogenase", "leu"],
    "his3": ["imidazoleglycerol-phosphate dehydratase", "his"],
    "trp1": ["phosphoribosylanthranilate isomerase", "trp"],
    "lacz": ["beta-galactosidase", "b-gal"],
    "lux": ["luciferase"],
    
    # 융합 태그 (Fusion Tags)
    "6xhis": ["his-tag", "polyhistidine", "his tag", "his6"],
    "gst": ["glutathione s-transferase"],
    "mbp": ["maltose binding protein", "maltose-binding protein"],
    "flag": ["flag-tag", "flag tag"],
    "myc": ["myc-tag", "myc tag"],
    "ha": ["ha-tag", "ha tag"]
}

def get_search_terms(query):
    """
    사용자의 query를 기반으로 매칭할 모든 동의어/약어 리스트를 반환합니다.
    """
    query_lower = query.lower().strip()
    search_terms = {query_lower}
    
    for short_name, synonyms in GENE_SYNONYMS.items():
        # 사용자가 풀네임의 일부를 검색했거나, 약어를 검색한 경우 서로를 동의어로 묶습니다.
        if query_lower == short_name or any(query_lower in syn for syn in synonyms) or any(syn in query_lower for syn in synonyms):
            search_terms.add(short_name)
            for syn in synonyms:
                search_terms.add(syn)
                
    return list(search_terms)

def filter_files(query, uploaded_files_with_genes):
    """
    업로드된 파일 목록(파일 객체 + 파싱된 유전자 리스트)을 받아,
    검색어(및 동의어)에 매칭되는 파일들만 필터링하여 반환합니다.
    """
    if not query:
        return []
        
    search_terms = get_search_terms(query)
    results = []
    
    for item in uploaded_files_with_genes:
        file_obj = item['file']
        gene_list = item['genes']
        
        matched_genes = []
        for gene in gene_list:
            gene_lower = gene.lower()
            # 추출한 여러 동의어 중 하나라도 gene 이름에 포함되어 있다면 매칭 성공 (대소문자 무시)
            if any(term in gene_lower for term in search_terms):
                matched_genes.append(gene)
        
        if matched_genes:
            results.append({
                "file": file_obj,
                "matched_genes": matched_genes,
                "all_genes": gene_list
            })
            
    return results
