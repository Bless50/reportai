from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, JSON, ARRAY
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.db.base_class import Base

class Reference(Base):
    """
    Reference model for APA format citations.
    Supports various types of references (journal articles, books, websites, etc.)
    """
    __tablename__ = "references"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    report_id = Column(PostgresUUID(as_uuid=True), ForeignKey("reports.id"))
    
    # Basic citation info
    citation_key = Column(String, nullable=False)  # e.g., "Smith2023"
    reference_type = Column(String, nullable=False)  # article, book, website, etc.
    
    # Authors can be multiple
    authors = Column(ARRAY(String), nullable=False)  # ["Smith, J.", "Doe, J."]
    year = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    
    # Publication details
    journal = Column(String)  # For articles
    volume = Column(String)   # For articles/journals
    issue = Column(String)    # For articles/journals
    pages = Column(String)    # For articles/books
    
    # Book specific
    edition = Column(String)
    publisher = Column(String)
    publisher_location = Column(String)  # City, Country
    
    # Online sources
    doi = Column(String)      # Digital Object Identifier
    url = Column(String)      # Web address
    
    # Additional metadata
    in_text_citation = Column(String)  # Generated in-text citation format
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    report = relationship("Report", back_populates="references")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._generate_in_text_citation()

    def _generate_in_text_citation(self):
        """Generate the in-text citation format (e.g., 'Smith et al., 2020')"""
        if not self.authors or not self.year:
            return
        
        authors_text = self.authors[0].split(",")[0] if self.authors else "No Author"
        if len(self.authors) > 1:
            authors_text += " et al."
        self.in_text_citation = f"({authors_text}, {self.year})"

    @hybrid_property
    def formatted_apa(self):
        """Format the reference in APA style"""
        # Authors
        if not self.authors:
            authors_text = "No author"
        else:
            if len(self.authors) == 1:
                authors_text = self.authors[0]
            elif len(self.authors) == 2:
                authors_text = f"{self.authors[0]} & {self.authors[1]}"
            else:
                authors_text = ", ".join(self.authors[:-1]) + f", & {self.authors[-1]}"

        # Basic citation parts
        citation = f"{authors_text} ({self.year}). {self.title}"

        # Format based on reference type
        if self.reference_type == "article":
            # Journal article
            citation += f". {self.journal}"
            if self.volume:
                citation += f", {self.volume}"
                if self.issue:
                    citation += f"({self.issue})"
            if self.pages:
                citation += f", {self.pages}"
            citation += "."
            
        elif self.reference_type == "book":
            # Book
            if self.edition:
                citation += f" ({self.edition} ed.)"
            if self.publisher_location:
                citation += f". {self.publisher_location}"
            if self.publisher:
                citation += f": {self.publisher}"
            citation += "."
            
        elif self.reference_type == "website":
            # Website
            citation += f". Retrieved from {self.url}"

        # Add DOI if available
        if self.doi:
            citation += f" https://doi.org/{self.doi}"

        return citation
