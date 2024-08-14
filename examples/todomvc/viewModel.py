from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from ex4nicegui import rxui, Ref


class TodoItem(rxui.ViewModel):
    id: datetime
    title = rxui.var("")
    completed = rxui.var(False)

    def __init__(self, id: datetime, title: str):
        super().__init__()
        self.id = id
        self.title.value = title

    def switch_completed(self):
        self.completed.value = not self.completed.value


_T_todos = List[TodoItem]


class filters:
    @staticmethod
    def active(todos: _T_todos):
        return [todo for todo in todos if not todo.completed.value]

    @staticmethod
    def completed(todos: _T_todos):
        return [todo for todo in todos if todo.completed.value]

    @staticmethod
    def all(todos: _T_todos):
        return todos


class State(rxui.ViewModel):
    todos: Ref[List[TodoItem]] = rxui.var(lambda: [])
    filter_do = rxui.var("all")

    @rxui.cached_var
    def filtered_todos(self) -> _T_todos:
        return getattr(filters, self.filter_do.value)(self.todos.value)

    @rxui.cached_var
    def active_count(self):
        return len(filters.active(self.todos.value))

    @rxui.cached_var
    def completed_count(self):
        return len(filters.completed(self.todos.value))

    @rxui.cached_var
    def total_count(self):
        return len(self.todos.value)

    @rxui.cached_var
    def completion_ratio(self):
        if self.total_count() == 0:
            return 0.0
        return round(self.completed_count() / self.total_count(), 2)

    # methods
    def add_todo(self, title: str):
        if title:
            self.todos.value.append(TodoItem(datetime.now(), title))

    def remove_todo(self, todo: TodoItem):
        self.todos.value.remove(todo)

    def remove_completed_todos(self):
        for todo in [todo for todo in self.todos.value if todo.completed.value]:
            self.remove_todo(todo)

    def all_checks(self):
        for todo in self.todos.value:
            todo.completed.value = True

    def all_unchecks(self):
        for todo in self.todos.value:
            todo.completed.value = not todo.completed.value
