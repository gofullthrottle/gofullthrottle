#!/usr/bin/env python3
"""
Generate custom SVG animations for GitHub profile
"""
import xml.etree.ElementTree as ET
from datetime import datetime

def create_neural_network_svg():
    """Create animated neural network SVG"""
    svg = ET.Element('svg', {
        'width': '800',
        'height': '400',
        'xmlns': 'http://www.w3.org/2000/svg',
        'style': 'background: #0d1117;'
    })
    
    # Add animated neural network nodes
    nodes = [
        (100, 100), (200, 150), (300, 100), (400, 200),
        (500, 150), (600, 100), (700, 180), (150, 250),
        (250, 300), (350, 250), (450, 300), (550, 250),
        (650, 300)
    ]
    
    # Create connections
    for i, (x1, y1) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes):
            if i != j and abs(x1 - x2) < 200 and abs(y1 - y2) < 150:
                line = ET.SubElement(svg, 'line', {
                    'x1': str(x1), 'y1': str(y1),
                    'x2': str(x2), 'y2': str(y2),
                    'stroke': '#00ff88',
                    'stroke-width': '1',
                    'opacity': '0.3'
                })
                
                # Add pulse animation
                animate = ET.SubElement(line, 'animate', {
                    'attributeName': 'opacity',
                    'values': '0.1;0.8;0.1',
                    'dur': f'{2 + i * 0.1}s',
                    'repeatCount': 'indefinite'
                })
    
    # Create nodes
    for i, (x, y) in enumerate(nodes):
        circle = ET.SubElement(svg, 'circle', {
            'cx': str(x), 'cy': str(y), 'r': '8',
            'fill': '#00ff88',
            'stroke': '#ffffff',
            'stroke-width': '2'
        })
        
        # Add pulsing animation
        animate = ET.SubElement(circle, 'animate', {
            'attributeName': 'r',
            'values': '6;12;6',
            'dur': f'{1.5 + i * 0.05}s',
            'repeatCount': 'indefinite'
        })
    
    # Add title
    title = ET.SubElement(svg, 'text', {
        'x': '400', 'y': '50',
        'text-anchor': 'middle',
        'fill': '#ffffff',
        'font-family': 'Orbitron, monospace',
        'font-size': '24',
        'font-weight': 'bold'
    })
    title.text = 'NEURAL NETWORK ACTIVE'
    
    # Add glowing effect
    animate_glow = ET.SubElement(title, 'animate', {
        'attributeName': 'fill',
        'values': '#ffffff;#00ff88;#ffffff',
        'dur': '3s',
        'repeatCount': 'indefinite'
    })
    
    return ET.tostring(svg, encoding='unicode')

def create_data_stream_svg():
    """Create animated data stream SVG"""
    svg = ET.Element('svg', {
        'width': '800',
        'height': '200',
        'xmlns': 'http://www.w3.org/2000/svg',
        'style': 'background: #0d1117;'
    })
    
    # Create flowing data streams
    for i in range(10):
        y = 20 + i * 18
        
        # Create data blocks
        for j in range(20):
            rect = ET.SubElement(svg, 'rect', {
                'x': str(-50 + j * 60),
                'y': str(y),
                'width': '40',
                'height': '12',
                'fill': '#00ff88' if j % 3 == 0 else '#0066cc',
                'opacity': '0.7',
                'rx': '2'
            })
            
            # Add flowing animation
            animate = ET.SubElement(rect, 'animateTransform', {
                'attributeName': 'transform',
                'type': 'translate',
                'values': '-100 0;900 0;-100 0',
                'dur': f'{5 + i * 0.3}s',
                'repeatCount': 'indefinite'
            })
    
    # Add data labels
    labels = ['NEURAL DATA', 'BLOCKCHAIN SYNC', 'AI PROCESSING', 'QUANTUM BITS']
    for i, label in enumerate(labels):
        text = ET.SubElement(svg, 'text', {
            'x': '20', 'y': str(40 + i * 40),
            'fill': '#ffffff',
            'font-family': 'Courier New, monospace',
            'font-size': '12',
            'opacity': '0.8'
        })
        text.text = label
    
    return ET.tostring(svg, encoding='unicode')

def create_matrix_rain_svg():
    """Create Matrix-style digital rain SVG"""
    svg = ET.Element('svg', {
        'width': '800',
        'height': '600',
        'xmlns': 'http://www.w3.org/2000/svg',
        'style': 'background: #000000;'
    })
    
    # Matrix characters
    chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
    
    # Create falling character streams
    for i in range(50):
        x = i * 16
        
        # Create column of characters
        for j in range(40):
            char = chars[j % len(chars)]
            text = ET.SubElement(svg, 'text', {
                'x': str(x),
                'y': str(-j * 20),
                'fill': '#00ff41',
                'font-family': 'Courier New, monospace',
                'font-size': '14',
                'opacity': str(max(0.1, 1 - j * 0.02))
            })
            text.text = char
            
            # Add falling animation
            animate = ET.SubElement(text, 'animateTransform', {
                'attributeName': 'transform',
                'type': 'translate',
                'values': f'0 0;0 {800 + j * 20}',
                'dur': f'{3 + i * 0.1}s',
                'repeatCount': 'indefinite'
            })
    
    return ET.tostring(svg, encoding='unicode')

def save_animations():
    """Save all SVG animations to files"""
    animations = {
        'neural_network.svg': create_neural_network_svg(),
        'data_stream.svg': create_data_stream_svg(),
        'matrix_rain.svg': create_matrix_rain_svg()
    }
    
    for filename, svg_content in animations.items():
        with open(f'widgets/{filename}', 'w') as f:
            f.write(svg_content)
        print(f"Created {filename}")

if __name__ == "__main__":
    import os
    os.makedirs('widgets', exist_ok=True)
    save_animations()
    print("All SVG animations created successfully!")