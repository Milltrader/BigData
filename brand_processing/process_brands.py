import re
import unicodedata

def process_brand_for_search(brand_name, mode='standard'):
    """
    Process brand names to make them suitable for search.
    
    Processing steps:
    1. Convert to lowercase
    2. Replace special characters with spaces
    3. Remove accents/diacritics
    4. Remove extra whitespace
    5. Remove common terms like "original" or "collection"
    6. Normalize model numbers (remove dots and special chars)
    7. Preserve important brand identifiers and model numbers
    
    Args:
        brand_name (str): The brand name to process
        mode (str): 'standard' or 'alphanumeric' 
                   - standard: preserve spaces
                   - alphanumeric: remove spaces and non-alphanumeric chars
        
    Returns:
        str: Processed brand name suitable for search
    """
    if not brand_name or not isinstance(brand_name, str):
        return ""
    
    # Convert to lowercase
    result = brand_name.lower()
    
    # Remove accents/diacritics
    result = unicodedata.normalize('NFKD', result)
    result = ''.join([c for c in result if not unicodedata.combining(c)])
    
    # Normalize special characters in model numbers (replace dots with nothing)
    # First, identify potential model numbers (e.g., "Cal.2", "F.P.")
    model_pattern = re.compile(r'([a-z]+\.)([0-9]+)|([a-z]\.)([a-z]\.)')
    result = model_pattern.sub(lambda m: m.group(0).replace('.', ''), result)
    
    # Replace special characters with spaces (but not ones in detected model numbers)
    result = re.sub(r'[^\w\s]', ' ', result)
    
    # Common terms to remove that don't add search value
    common_terms = {
        'original', 'collection', 'design', 'limited', 'edition', 
        'watches', 'watch', 'classic', 'vintage', 'series', 'type',
        'professional', 'chronograph', 'chronographe', 'automatic',
        'manufacture', 'gmt', 'quartz', 'mechanical', 'reference',
        'ref', 'model', 'special', 'for', 'the', 'and', 'of'
    }
    
    # Terms that should always be preserved as they're key identifiers
    preserved_terms = {
        'sport', 'seamaster', 'submariner', 'navitimer', 'royal', 'oak',
        'datograph', 'master', 'control', 'patrimony', 'monaco', 'nautilus',
        'daytona', 'speedmaster', 'calibre', 'cal', 'elegante', 'laureato',
        'cosmograph', 'moonwatch', 'philippe', 'patek', 'breitling', 'rolex',
        'omega', 'tag', 'heuer', 'iwc', 'piguet', 'audemars', 'lange', 'sohne'
    }
    
    # Extract potential model numbers (patterns like alphanumeric codes)
    model_numbers = set(re.findall(r'\b[a-z]*\d+[a-z0-9]*\b', result))
    
    words = result.split()
    filtered_words = []
    
    for word in words:
        word_lower = word.lower()
        # Keep if: not a common term OR is preserved term OR is a model number
        if (word_lower not in common_terms or 
            word_lower in preserved_terms or 
            word_lower in model_numbers):
            filtered_words.append(word)
    
    result = ' '.join(filtered_words)
    
    # Remove extra whitespace
    result = re.sub(r'\s+', ' ', result).strip()
    
    # For alphanumeric mode, remove all non-alphanumeric characters including spaces
    if mode == 'alphanumeric':
        result = re.sub(r'[^a-z0-9]', '', result)
    
    return result

# Example usage
if __name__ == "__main__":
    sample_brands = [
        "Tissot T Sport Quakeren Chronograph",
        "Piaget PS 535 Chronographe",
        "Rolex Submariner GMT",
        "Patek Philippe Nautilus",
        "Omega Seamaster Professional",
        "Breitling Navitimer",
        "IWC Schaffhausen Original",
        "Porsche Design Chronograph",
        "Tag Heuer Monaco Cal.2",
        "Audemars Piguet Royal Oak",
        "A. Lange & Söhne Datograph",
        "Jaeger-LeCoultre Master Control",
        "Vacheron Constantin Patrimony",
        "Girard-Perregaux Laureato",
        "F.P. Journe Élégante",
        "Rolex Cosmograph Daytona",
        "Omega Speedmaster Moonwatch Professional"
    ]
    
    print("Original brand name --> Standard --> Alphanumeric")
    print("-" * 70)
    for brand in sample_brands:
        standard = process_brand_for_search(brand, 'standard')
        alphanumeric = process_brand_for_search(brand, 'alphanumeric')
        print(f"{brand} --> {standard} --> {alphanumeric}") 