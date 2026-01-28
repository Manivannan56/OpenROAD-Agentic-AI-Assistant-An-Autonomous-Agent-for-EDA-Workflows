#!/usr/bin/env python3
"""
metrics_parser.py
Metrics Parser - Extracts metrics from OpenROAD reports
"""

import re
import json


class MetricsParser:
    """Parses OpenROAD report files"""
    
    def parse_timing(self, report_text):
        """
        Parse timing report.
        
        Args:
            report_text: Timing report content
            
        Returns:
            dict: Timing metrics
        """
        metrics = {}
        
        # WNS (Worst Negative Slack)
        wns_match = re.search(r'WNS:\s*([-\d.]+)', report_text)
        if wns_match:
            metrics['wns'] = float(wns_match.group(1))
        
        # TNS (Total Negative Slack)
        tns_match = re.search(r'TNS:\s*([-\d.]+)', report_text)
        if tns_match:
            metrics['tns'] = float(tns_match.group(1))
        
        # Violations
        viol_match = re.search(r'violations:\s*(\d+)', report_text, re.IGNORECASE)
        if viol_match:
            metrics['timing_violations'] = int(viol_match.group(1))
        
        return metrics
    
    def parse_congestion(self, report_text):
        """
        Parse congestion report.
        
        Args:
            report_text: Congestion report
            
        Returns:
            dict: Congestion metrics
        """
        metrics = {}
        
        # Max congestion
        max_match = re.search(r'Max:\s*(\d+)%', report_text)
        if max_match:
            metrics['max_congestion'] = int(max_match.group(1))
        
        # Average
        avg_match = re.search(r'Avg:\s*(\d+)%', report_text)
        if avg_match:
            metrics['avg_congestion'] = int(avg_match.group(1))
        
        return metrics
    
    def parse_drc(self, report_text):
        """
        Parse DRC report.
        
        Args:
            report_text: DRC report
            
        Returns:
            dict: DRC metrics
        """
        metrics = {}
        
        # Total violations
        viol_match = re.search(r'Violations:\s*(\d+)', report_text, re.IGNORECASE)
        if viol_match:
            metrics['drc_violations'] = int(viol_match.group(1))
        
        return metrics
    
    def parse_all(self, reports):
        """
        Parse all report types.
        
        Args:
            reports: Dict of {report_type: content}
            
        Returns:
            dict: All parsed metrics
        """
        all_metrics = {}
        
        if 'timing' in reports:
            all_metrics.update(self.parse_timing(reports['timing']))
        
        if 'congestion' in reports:
            all_metrics.update(self.parse_congestion(reports['congestion']))
        
        if 'drc' in reports:
            all_metrics.update(self.parse_drc(reports['drc']))
        
        return all_metrics


