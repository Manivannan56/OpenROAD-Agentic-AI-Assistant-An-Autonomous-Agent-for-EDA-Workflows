#!/usr/bin/env python3
"""
decision_engine.py
Decision Engine - Determines if goals met or retry needed
"""

class DecisionEngine:
    """Makes retry/success decisions based on metrics"""
    
    def __init__(self, constraints=None):
        """
        Initialize with constraints.
        
        Args:
            constraints: Dict of metric thresholds
        """
        self.constraints = constraints or {
            'wns_min': 0.0,
            'max_congestion': 90,
            'drc_violations': 0
        }
    
    def evaluate(self, metrics):
        """
        Evaluate if metrics meet constraints.
        
        Args:
            metrics: Dict of parsed metrics
            
        Returns:
            dict: Decision with status and issues
        """
        print(f"\n{'='*70}")
        print("DECISION ENGINE")
        print(f"{'='*70}")
        print(f"Metrics: {metrics}")
        print(f"Constraints: {self.constraints}")
        
        issues = []
        
        # Check timing
        wns = metrics.get('wns')
        if wns is not None and wns < self.constraints['wns_min']:
            issues.append({
                'type': 'timing',
                'metric': 'wns',
                'value': wns,
                'threshold': self.constraints['wns_min'],
                'message': f"Timing violation: WNS={wns}ns (need >={self.constraints['wns_min']})"
            })
        
        # Check congestion
        cong = metrics.get('max_congestion')
        if cong is not None and cong > self.constraints['max_congestion']:
            issues.append({
                'type': 'congestion',
                'metric': 'max_congestion',
                'value': cong,
                'threshold': self.constraints['max_congestion'],
                'message': f"High congestion: {cong}% (limit: {self.constraints['max_congestion']}%)"
            })
        
        # Check DRC
        drc = metrics.get('drc_violations', 0)
        if drc > self.constraints['drc_violations']:
            issues.append({
                'type': 'drc',
                'metric': 'drc_violations',
                'value': drc,
                'threshold': self.constraints['drc_violations'],
                'message': f"DRC violations: {drc} (need: 0)"
            })
        
        # Make decision
        if not issues:
            decision = {
                'status': 'success',
                'next_action': 'complete',
                'message': 'All constraints satisfied'
            }
            print("\n✓ Decision: SUCCESS")
        else:
            decision = {
                'status': 'retry',
                'next_action': 'replan',
                'issues': issues,
                'message': f'{len(issues)} constraint(s) violated'
            }
            print(f"\n✗ Decision: RETRY ({len(issues)} issues)")
            for issue in issues:
                print(f"  - {issue['message']}")
        
        return decision

