import base64
import zlib
import urllib.request
import os

mermaid_code = """flowchart TD
    A([User Input: Hindi / Hinglish SMS]) --> B[Data Cleaning & Preprocessing]
    B --> C[Feature Extraction TF-IDF]
    
    C --> M1[Linear SVM]
    C --> M2[Random Forest]
    C --> M3[Naive Bayes]
    C --> M4[Logistic Regression]
    
    M1 --> S{Evaluate & Select Best}
    M2 --> S
    M3 --> S
    M4 --> S
    
    S --> D[Deployed Model]
    D --> E{Classification Result}
    E -->|Spam| F([Spam Message])
    E -->|Ham| G([Legitimate Message])

    classDef default fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
"""

def generate_mermaid_image():
    compressed = zlib.compress(mermaid_code.encode('utf-8'), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    
    url = f"https://kroki.io/mermaid/png/{encoded}"
    output_path = r"c:\NLP PROJECT\architecture_diagram.png"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    print(f"Downloading image from {url}...")
    with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
        out_file.write(response.read())
    print(f"Image saved to: {output_path}")

if __name__ == "__main__":
    generate_mermaid_image()
