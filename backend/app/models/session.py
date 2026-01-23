import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, Enum as SQLEnum
import enum

from app.core.database import Base


class InterviewPhase(str, enum.Enum):
    SETUP = "setup"
    ANALYZING = "analyzing"
    INTRO = "intro"
    QUESTIONS = "questions"
    FOLLOWUP = "followup"
    EVALUATION = "evaluation"
    FEEDBACK = "feedback"
    COMPLETED = "completed"


class Seniority(str, enum.Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Input data
    resume_text = Column(Text, nullable=True)
    job_description = Column(Text, nullable=True)
    role = Column(String(255), nullable=True)

    # Resume analysis results
    detected_seniority = Column(SQLEnum(Seniority), nullable=True)
    strengths = Column(JSON, default=list)  # List of strengths
    gaps = Column(JSON, default=list)  # List of skill gaps
    focus_areas = Column(JSON, default=list)  # Focus areas for interview

    # Interview state
    status = Column(String(50), default="created")  # created, active, completed, cancelled
    current_phase = Column(SQLEnum(InterviewPhase), default=InterviewPhase.SETUP)

    # Timing
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    duration_minutes = Column(String(10), default="35")  # Target duration

    # Scoring
    scores = Column(JSON, default=dict)  # {"technical": 0, "design": 0, "communication": 0}

    # Questions and answers history
    qa_history = Column(JSON, default=list)  # [{question, answer, score, feedback}]

    # Final feedback
    final_report = Column(Text, nullable=True)
    recommendation = Column(String(50), nullable=True)  # Hire, Borderline, No-Hire
    skill_roadmap = Column(JSON, default=list)  # Learning roadmap

    # Memory opt-in
    memory_opt_in = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
