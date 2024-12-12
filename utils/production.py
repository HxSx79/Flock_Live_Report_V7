from datetime import datetime
from typing import Dict, List
from .bom_reader import BOMReader

class ProductionTracker:
    def __init__(self):
        self.bom_reader = BOMReader()
        self.line1_data = {
            'part': {
                'program': '',
                'number': '',
                'description': '',
                'name': ''  # Kept for backward compatibility
            },
            'production': {'quantity': 0, 'delta': 0, 'pph': 0},
            'scrap': {'total': 0, 'rate': 0}
        }
        self.line2_data = {
            'part': {
                'program': '',
                'number': '',
                'description': '',
                'name': ''  # Kept for backward compatibility
            },
            'production': {'quantity': 0, 'delta': 0, 'pph': 0},
            'scrap': {'total': 0, 'rate': 0}
        }
        self.totals = {
            'quantity': 0,
            'delta': 0,
            'scrap': 0,
            'scrapRate': 0
        }
        self.production_details = []

    def update_part_info(self, line_number: int, class_name: str) -> None:
        """Update part information based on detected class name"""
        part_info = self.bom_reader.get_part_info(class_name)
        line_data = self.line1_data if line_number == 1 else self.line2_data
        
        line_data['part'].update({
            'program': part_info['program'],
            'number': part_info['part_number'],
            'description': part_info['description'],
            'name': part_info['description']  # Kept for backward compatibility
        })

    def update_line_data(self, line_number: int, detections: List[Dict]) -> None:
        # Update production data based on detections
        for detection in detections:
            class_name = detection.get('class_name')
            if class_name:
                self.update_part_info(line_number, class_name)

    def get_all_data(self) -> Dict:
        return {
            'line1_part': self.line1_data['part'],
            'line1_production': self.line1_data['production'],
            'line1_scrap': self.line1_data['scrap'],
            'line2_part': self.line2_data['part'],
            'line2_production': self.line2_data['production'],
            'line2_scrap': self.line2_data['scrap'],
            'total_quantity': self.totals['quantity'],
            'total_delta': self.totals['delta'],
            'total_scrap': self.totals['scrap'],
            'average_scrap_rate': self.totals['scrapRate']
        }