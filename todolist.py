from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String())
    deadline = Column(Date, default=datetime.today())

    def __init__(self, task, deadline):
        self.task = task
        self.deadline = deadline

    def __repr__(self):
        return self.task, self.deadline


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def add_task():
    task_to_add = input("Enter task\n")
    deadline_to_add = input("Enter deadline\n")
    new_row = Table(task=task_to_add, deadline=datetime.strptime(deadline_to_add, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()
    print("\nThe task has been added!")


def today_tasks():
    if session.query(Table):
        count = 1
        print(f"Today {datetime.strftime(datetime.today(), '%-d %b')}:")
        if session.query(Table.deadline).first() == datetime.strftime(datetime.today(), '%Y-%m-%d'):
            for tasks in session.query(Table).filter(Table.deadline == datetime.strftime(datetime.today(), '%Y-%m-%d')):
                print(f"{count}. {tasks.task}")
                count += 1
        else:
            print("Nothing to do!\n")


def week_tasks():
    res = [i[0] for i in session.query(Table.deadline).order_by(Table.deadline).distinct().all()]
    list_of_weekday = []
    for day in range(7):
        list_of_weekday.append(datetime.date(datetime.today()) + timedelta(days=day))
        print(
            f"\n{datetime.strftime(datetime.today() + timedelta(days=day), '%A')} {datetime.strftime(datetime.today() + timedelta(days=day), '%-d %b')}:")
        if list_of_weekday[day] in res:
            rows = session.query(Table).filter(
                Table.deadline == datetime.strftime(datetime.today() + timedelta(days=day), '%Y-%m-%d'))
            count_task = 1
            for tasks in rows:
                print(f"{count_task}. {tasks.task}")
                count_task += 1
        else:
            print("Nothing to do!")


def all_tasks():
    result = session.query(Table).order_by(Table.deadline).all()
    count_task = 1
    print('All tasks:')
    for row in result:
        print(
            f"{count_task}. {row.task}. {datetime.strftime(row.deadline, '%-d %b')}")
        count_task += 1


def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    print('Missed tasks:')
    count_task = 1
    if session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all():
        for row in rows:
            print(f"{count_task}. {row.task}. {datetime.strftime(row.deadline, '%-d %b')}")
            count_task += 1
    else:
        print("Nothing is missed!")


def delete_task():
    rows = session.query(Table).filter(Table.deadline).order_by(Table.deadline).all()
    rows_for_delete = []
    if rows:
        count_task = 1
        for row in rows:
            print(f"{count_task}. {row.task}. {datetime.strftime(row.deadline, '%-d %b')}")
            count_task += 1
            rows_for_delete.append(row)
        delete_item = int(input('Choose the number of the task you want to delete: '))
        session.delete(rows_for_delete[-delete_item + 1])
        session.commit()
        print('The task has been deleted!')
    else:
        print('Nothing to delete')


def menu():
    menu_string = ("\n1) Today's tasks\n"
                   "2) Week's tasks\n"
                   "3) All tasks\n"
                   "4) Missed tasks\n"
                   "5) Add task\n"
                   "6) Delete task\n"
                   "0) Exit\n")
    while True:
        choice = int(input(menu_string))
        if choice == 1:
            today_tasks()
        elif choice == 2:
            week_tasks()
        elif choice == 3:
            all_tasks()
        elif choice == 4:
            missed_tasks()
        elif choice == 5:
            add_task()
        elif choice == 6:
            delete_task()
        elif choice == 0:
            print("Bye!")
            break


if __name__ == "__main__":
    menu()
