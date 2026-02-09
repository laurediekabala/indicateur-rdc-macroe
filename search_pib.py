import pdfplumber

chemin_pdf = "e:\\BCC\\rapport_annuel_2023.pdf"

with pdfplumber.open(chemin_pdf) as pdf:
    print("Recherche du tableau PIB dans le PDF...\n")
    
    pages_with_pib = []
    
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text = page.extract_text()
        
        if text and "PIB" in text.upper():
            pages_with_pib.append(i + 1)
            print(f"✓ Page {i+1} contient 'PIB'")
    
    if pages_with_pib:
        print(f"\n📍 Tableau PIB trouve aux pages: {pages_with_pib}")
        
        # Afficher le contenu de la première page contenant PIB
        first_page = pages_with_pib[0]
        page = pdf.pages[first_page - 1]
        text = page.extract_text()
        
        print(f"\n{'='*70}")
        print(f"Contenu de la PAGE {first_page}:")
        print(f"{'='*70}\n")
        print(text[:2000])  # Premier 2000 caractères
        
    else:
        print("❌ Aucune page contenant 'PIB' trouvée")
