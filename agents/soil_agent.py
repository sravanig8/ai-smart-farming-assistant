"""
Soil Analysis Agent module.

Analyzes soil moisture data and provides intelligent recommendations.
"""
from typing import Dict, Literal


class SoilAnalysisAgent:
    """
    Intelligent agent for analyzing soil conditions based on moisture levels.
    
    Classifies soil as Dry, Optimal, or Overwatered and provides recommendations.
    """
    
    # Soil moisture thresholds (in percentage)
    DRY_THRESHOLD = 30
    OPTIMAL_MIN = 30
    OPTIMAL_MAX = 60
    OVERWATERED_THRESHOLD = 60
    
    # Classification types
    SOIL_STATES = {
        'dry': 'Dry',
        'optimal': 'Optimal',
        'overwatered': 'Overwatered'
    }
    
    def __init__(self, soil_moisture: float):
        """
        Initialize the soil analysis agent.
        
        Args:
            soil_moisture: Soil moisture value (0-100 percentage)
            
        Raises:
            ValueError: If soil_moisture is not in valid range (0-100)
        """
        if not isinstance(soil_moisture, (int, float)):
            raise ValueError(f"Soil moisture must be numeric, got {type(soil_moisture)}")
        
        if not (0 <= soil_moisture <= 100):
            raise ValueError(f"Soil moisture must be between 0 and 100, got {soil_moisture}")
        
        self.soil_moisture = soil_moisture
    
    def analyze(self) -> Dict:
        """
        Analyze soil moisture and return classification with recommendations.
        
        Returns:
            Dictionary containing:
            {
                'soil_moisture': float,           # Input soil moisture value
                'classification': str,            # Dry, Optimal, or Overwatered
                'recommendation': str,            # Action recommendation
                'urgency': str,                   # Low, Medium, High
                'status': bool                    # True (analysis successful)
            }
        """
        classification = self._classify_soil()
        recommendation = self._get_recommendation(classification)
        urgency = self._determine_urgency(classification)
        
        return {
            'soil_moisture': self.soil_moisture,
            'classification': classification,
            'recommendation': recommendation,
            'urgency': urgency,
            'status': True
        }
    
    def _classify_soil(self) -> Literal['Dry', 'Optimal', 'Overwatered']:
        """
        Classify soil condition based on moisture percentage.
        
        Returns:
            String classification: 'Dry', 'Optimal', or 'Overwatered'
        """
        if self.soil_moisture < self.DRY_THRESHOLD:
            return self.SOIL_STATES['dry']
        elif self.OPTIMAL_MIN <= self.soil_moisture <= self.OPTIMAL_MAX:
            return self.SOIL_STATES['optimal']
        else:
            return self.SOIL_STATES['overwatered']
    
    def _get_recommendation(self, classification: str) -> str:
        """
        Get actionable recommendation based on soil classification.
        
        Args:
            classification: Soil classification (Dry, Optimal, Overwatered)
            
        Returns:
            Recommendation string for the farmer
        """
        recommendations = {
            'Dry': (
                f"⚠️ IRRIGATION NEEDED: Soil moisture is at {self.soil_moisture}%. "
                "Water your crops immediately. Increase irrigation frequency to prevent crop stress."
            ),
            'Optimal': (
                f"✅ CONDITIONS NORMAL: Soil moisture is at {self.soil_moisture}%. "
                "Maintain current irrigation schedule. Crops are in ideal growing conditions."
            ),
            'Overwatered': (
                f"⚠️ REDUCE WATERING: Soil moisture is at {self.soil_moisture}%. "
                "Stop irrigation for now to prevent waterlogging and root rot. "
                "Improve drainage if possible."
            )
        }
        return recommendations.get(classification, "Unknown condition")
    
    def _determine_urgency(self, classification: str) -> Literal['Low', 'Medium', 'High']:
        """
        Determine urgency level for farmer action.
        
        Args:
            classification: Soil classification (Dry, Optimal, Overwatered)
            
        Returns:
            Urgency level: 'Low', 'Medium', or 'High'
        """
        if classification == 'Optimal':
            return 'Low'
        elif classification == 'Dry':
            # Higher urgency if extremely dry
            if self.soil_moisture < 15:
                return 'High'
            return 'Medium'
        else:  # Overwatered
            # Higher urgency if severely overwatered
            if self.soil_moisture > 80:
                return 'High'
            return 'Medium'
