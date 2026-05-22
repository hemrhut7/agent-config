import os
import sys
import argparse
from pdf2image import convert_from_path

def convert(pdf_path, output_dir, dpi=300, max_dim=None, fmt="png"):
    """
    Convert PDF pages to high-resolution images.
    
    Args:
        pdf_path: Path to the input PDF file.
        output_dir: Directory to save the converted images.
        dpi: Dots per inch for the conversion. Higher values mean higher resolution.
        max_dim: Optional maximum dimension (width or height). If set, images will be resized.
        fmt: Output format (e.g., "png", "jpeg").
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Converting {pdf_path} at {dpi} DPI...")
    images = convert_from_path(pdf_path, dpi=dpi)

    for i, image in enumerate(images):
        width, height = image.size
        if max_dim and (width > max_dim or height > max_dim):
            scale_factor = min(max_dim / width, max_dim / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = image.resize((new_width, new_height))
        
        image_path = os.path.join(output_dir, f"page_{i+1}.{fmt}")
        image.save(image_path)
        print(f"Saved page {i+1} as {image_path} (size: {image.size})")

    print(f"Successfully converted {len(images)} pages to {fmt.upper()} images in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF pages to high-resolution images.")
    parser.add_argument("pdf_path", help="Path to the input PDF file.")
    parser.add_argument("output_dir", help="Directory to save the converted images.")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for conversion (default: 300).")
    parser.add_argument("--max-dim", type=int, help="Optional maximum dimension for resizing.")
    parser.add_argument("--fmt", default="png", help="Output format (default: png).")

    args = parser.parse_args()
    convert(args.pdf_path, args.output_dir, dpi=args.dpi, max_dim=args.max_dim, fmt=args.fmt)
