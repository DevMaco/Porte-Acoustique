"""
Génération de l'image hero pour porte-acoustique.com
via l'API Google Gemini (Imagen 3).

Installation :
    pip install google-genai pillow

Usage :
    python generate_hero.py --api-key YOUR_GEMINI_API_KEY
    python generate_hero.py --api-key YOUR_GEMINI_API_KEY --prompt-style photo
"""

import argparse
import base64
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Prompts disponibles
# ---------------------------------------------------------------------------

PROMPTS = {
    "technique": (
        "Technical product photography of a premium acoustic soundproof door, "
        "white modern door with clean lines, shown from a slight 3/4 angle, "
        "professional studio lighting, white background, "
        "the door is open at 30 degrees showing its thick multi-layer cross-section edge (50mm thick), "
        "visible internal acoustic layers, rubber perimeter seal highlighted in orange, "
        "high-end chrome lever handle, "
        "subtle dimension callout lines with measurements in millimeters, "
        "minimalist technical blueprint aesthetic with warm white tones, "
        "ultra sharp product shot, commercial photography quality, 4k, clean"
    ),
    "photo": (
        "Professional product photo of a premium acoustic door installed in a modern hallway, "
        "sleek white door, modern interior, soft studio lighting, "
        "slightly open to reveal thick 50mm acoustic core with multiple layers visible in cross-section, "
        "orange rubber perimeter seal visible at the edge, "
        "high-end chrome handle, very clean and professional look, "
        "warm neutral background, architectural photography, "
        "high resolution, commercial quality"
    ),
    "render": (
        "3D render of an acoustic soundproof door, "
        "white minimalist design, professional product render, "
        "neutral studio background gradient from light grey to white, "
        "door shown at 3/4 angle slightly open, "
        "thick 50mm door edge visible showing acoustic multi-layer construction, "
        "orange acoustic perimeter gasket seal visible, "
        "brushed chrome handle and hinges, "
        "subtle shadow, professional CGI render, ultra realistic, 4k"
    ),
}

# ---------------------------------------------------------------------------
# Génération
# ---------------------------------------------------------------------------

def generate_image(api_key: str, style: str, output_path: Path) -> None:
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("ERREUR: Installe le SDK d'abord :  pip install google-genai")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    prompt = PROMPTS.get(style, PROMPTS["technique"])
    print(f"Generation en cours (style: {style}) ...")
    print(f"    Prompt : {prompt[:80]}...\n")

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    image_data = None
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_data = part.inline_data.data
            break

    if not image_data:
        print("ERREUR: Aucune image generee. Verifie ta cle API et les quotas.")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_data)
    print(f"OK - Image sauvegardee : {output_path}")
    print(f"    Taille : {len(image_data) / 1024:.0f} Ko")


def update_hero_css(image_path: str) -> None:
    """Affiche la ligne CSS à copier dans style.css pour utiliser l'image."""
    rel = image_path.replace("\\", "/")
    print(f"\nPour utiliser l'image dans le hero, ajoute dans css/style.css :")
    print(f"""
.home-hero {{
    background-image: url('../{rel}');
    background-size: cover;
    background-position: center;
}}
""")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Génère l'image hero via Gemini Imagen 3")
    parser.add_argument("--api-key", default="AIzaSyD6L7qvEUDvwkfORHnIkm06XO4UinzLWbA", help="Clé API Google Gemini (AIza…)")
    parser.add_argument(
        "--style",
        choices=list(PROMPTS.keys()),
        default="technique",
        help="Style de l'image (défaut: technique)",
    )
    parser.add_argument(
        "--output",
        default="images/hero-door.jpg",
        help="Chemin de sortie (défaut: images/hero-door.jpg)",
    )
    args = parser.parse_args()

    output_path = Path(__file__).parent / args.output
    generate_image(args.api_key, args.style, output_path)
    update_hero_css(args.output)


if __name__ == "__main__":
    main()
