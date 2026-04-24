from sqlalchemy import Column, Integer, Float, Enum, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"
    FAILED = "failed"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    contract = relationship("Contract", back_populates="payments")

class EscrowAccount(Base):
    __tablename__ = "escrow_accounts"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    is_released = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())