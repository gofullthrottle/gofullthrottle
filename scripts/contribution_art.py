#!/usr/bin/env python3
"""
GitHub Contribution Art Generator
Creates contribution patterns to spell words in your GitHub contribution graph
"""
import json
from datetime import datetime, timedelta

class ContributionArt:
    def __init__(self):
        # Letter patterns for 7x5 grid (height x width)
        self.letters = {
            'P': [
                "████ ",
                "█   █",
                "████ ",
                "█    ",
                "█    "
            ],
            'A': [
                " ███ ",
                "█   █",
                "█████",
                "█   █",
                "█   █"
            ],
            'N': [
                "█   █",
                "██  █",
                "█ █ █",
                "█  ██",
                "█   █"
            ],
            'G': [
                " ████",
                "█    ",
                "█ ███",
                "█   █",
                " ████"
            ],
            'E': [
                "█████",
                "█    ",
                "████ ",
                "█    ",
                "█████"
            ],
            'M': [
                "█   █",
                "██ ██",
                "█ █ █",
                "█   █",
                "█   █"
            ],
            'C': [
                " ████",
                "█    ",
                "█    ",
                "█    ",
                " ████"
            ],
            'R': [
                "████ ",
                "█   █",
                "████ ",
                "█  █ ",
                "█   █"
            ],
            'Y': [
                "█   █",
                "█   █",
                " ███ ",
                "  █  ",
                "  █  "
            ],
            'T': [
                "█████",
                "  █  ",
                "  █  ",
                "  █  ",
                "  █  "
            ],
            'O': [
                " ███ ",
                "█   █",
                "█   █",
                "█   █",
                " ███ "
            ],
            'I': [
                "█████",
                "  █  ",
                "  █  ",
                "  █  ",
                "█████"
            ],
            '.': [
                "     ",
                "     ",
                "     ",
                "     ",
                "  █  "
            ],
            'L': [
                "█    ",
                "█    ",
                "█    ",
                "█    ",
                "█████"
            ],
            'V': [
                "█   █",
                "█   █",
                "█   █",
                " █ █ ",
                "  █  "
            ],
            '5': [
                "█████",
                "█    ",
                "████ ",
                "    █",
                "████ "
            ],
            ' ': [
                "     ",
                "     ",
                "     ",
                "     ",
                "     "
            ]
        }
    
    def get_word_pattern(self, word):
        """Generate pattern for a word"""
        word = word.upper()
        patterns = []
        
        for char in word:
            if char in self.letters:
                patterns.append(self.letters[char])
            else:
                patterns.append(self.letters[' '])  # Default to space
        
        # Combine patterns horizontally
        combined = []
        for row in range(5):  # 5 rows per letter
            line = ""
            for pattern in patterns:
                line += pattern[row] + " "  # Add space between letters
            combined.append(line.rstrip())
        
        return combined
    
    def generate_dates(self, pattern, start_year):
        """Generate commit dates based on pattern"""
        dates = []
        
        # GitHub contribution graph starts on Sunday
        # Find the first Sunday of the year
        start_date = datetime(start_year, 1, 1)
        days_until_sunday = (6 - start_date.weekday()) % 7
        first_sunday = start_date + timedelta(days=days_until_sunday)
        
        for week in range(len(pattern[0])):  # Width of pattern
            for day in range(5):  # Only weekdays for pattern (Mon-Fri)
                if day < len(pattern) and week < len(pattern[day]):
                    if pattern[day][week] == '█':
                        commit_date = first_sunday + timedelta(weeks=week, days=day+1)
                        if commit_date.year == start_year:
                            dates.append(commit_date.strftime('%Y-%m-%d'))
        
        return dates
    
    def create_art_plan(self):
        """Create the complete art plan for all years"""
        plan = {
            2019: self.generate_dates(self.get_word_pattern("PANGEAM"), 2019),
            2020: self.generate_dates(self.get_word_pattern("PANGEAM"), 2020),
            2021: self.generate_dates(self.get_word_pattern("PANGEAM"), 2021),
            2022: self.generate_dates(self.get_word_pattern("CRYPTO"), 2022),
            2023: self.generate_dates(self.get_word_pattern("A.I."), 2023),
            2024: self.generate_dates(self.get_word_pattern("AGENTIC"), 2024),
            2025: self.generate_dates(self.get_word_pattern("LEVEL 5"), 2025)
        }
        
        return plan
    
    def save_plan(self, filename="contribution_plan.json"):
        """Save the contribution plan to a file"""
        plan = self.create_art_plan()
        
        with open(filename, 'w') as f:
            json.dump(plan, f, indent=2)
        
        print(f"Contribution art plan saved to {filename}")
        
        # Print summary
        for year, dates in plan.items():
            word = {
                2019: "PANGEAM", 2020: "PANGEAM", 2021: "PANGEAM",
                2022: "CRYPTO", 2023: "A.I.", 2024: "AGENTIC", 2025: "LEVEL 5"
            }[year]
            print(f"{year}: {word} - {len(dates)} commit dates")
    
    def preview_pattern(self, word):
        """Preview how a word will look"""
        pattern = self.get_word_pattern(word)
        print(f"\nPreview of '{word}':")
        print("-" * len(pattern[0]))
        for line in pattern:
            print(line.replace('█', '●').replace(' ', '·'))
        print("-" * len(pattern[0]))

if __name__ == "__main__":
    art = ContributionArt()
    
    # Preview all words
    words = ["PANGEAM", "CRYPTO", "A.I.", "AGENTIC", "LEVEL 5"]
    for word in words:
        art.preview_pattern(word)
    
    # Generate and save the plan
    art.save_plan()