"""
ConsultancyBot Package
Dynamic, reusable consultancy automation system for InnovLead Canada Inc.

This package provides a complete consultancy workflow:
- Dynamic competitor research (any industry)
- Funding opportunity analysis
- Strategic proposal generation
- Template-based document generation
"""

from .bot import ConsultancyBot
from .competitor_research import CompetitorResearcher
from .proposal_generator import ProposalGenerator

__version__ = "1.0.0"
__all__ = ["ConsultancyBot", "CompetitorResearcher", "ProposalGenerator"]
