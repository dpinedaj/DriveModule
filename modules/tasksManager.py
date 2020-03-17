
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm.exc import NoResultFound

from .db_session import session
from modules import Base

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from libraries.constants import Constants as cts



class TaskManager(Base):

    __tablename__ = 'tasks_manager'
    
    id = Column(String)
    title = Column(String)
    source = Column(String)
    destroy = Column(String)
    fails = Column(Boolean)
    processing = Column(Boolean)
    error = Column(String)

    @classmethod
    def next(cls):
        query = """
            UPDATE %s SET
                processing = true
            WHERE id = (
                SELECT id   
                FROM %s
                WHERE processing = false
                AND 
                (
                    fails = false
                )
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            )
            RETURNING *
        """ % (cls.__tablename__, cls.__tablename__)

        try:
            rs = session.execute(query).fetchone()
            session.commit()

            if rs:
                result = session.query(TaskManager).filter_by(id=rs['id']).one()
            else:
                result = None
        except NoResultFound:
            print('No task to update')
        
        return result
        

    def destroy(self):
        try:
            session.delete(self)
            session.commit()
        except Exception as ex:
            print(str(ex))

    def failed(self, message):
        self.processing = False
        self.fails = True
        self.error = message
        
        session.add(self)
        session.commit()

    def __repr__(self):
        return "%s(id=%s, fn=%s, proc=%s, fail=%s, error=%s)" % (
            self.__class__.__name__,
            self.id,
            self.file_name,
            self.processing,
            self.fails,
            self.error
        )