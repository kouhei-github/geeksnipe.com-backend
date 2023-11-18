from config.index import Base
from sqlalchemy import Integer, String, Column, ForeignKey, BIGINT, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

class CompanyStack(Base):
    # テーブル名
    __tablename__ = 'company_stacks'

    # 個々のカラムを定義
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    stack_id = Column(Integer, ForeignKey('stacks.id'))
    company = relationship('Company', back_populates='companies')
    stack = relationship('Stack', back_populates='stacks')


class Company(Base):
    """
    Lineテーブルクラス
    """

    # テーブル名
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), comment="会社名")
    offer_name = Column(String(100), comment="申込者名")
    email = Column(String(100), comment="メールアドレス")
    url = Column(String(100), comment="企業HP")
    phone = Column(String(100), comment="電話番号")
    display_status = Column(Integer, comment="掲載ステータス")
    where_we_know = Column(Integer, comment="どこで知ったか")
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    child = relationship("User", uselist=False, back_populates="companies")
    stacks = relationship(
        'Stack',
        secondary=CompanyStack.__tablename__,
        back_populates='companies'

        # 中間テーブル
    )



class Stack(Base):
    """
    Lineテーブルクラス
    """

    # テーブル名
    __tablename__ = 'stacks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), comment="言語・フレームワーク")
    companies = relationship(
        'Company',
        secondary=CompanyStack.__tablename__,
        # 中間テーブル
        back_populates='stacks'
    )
