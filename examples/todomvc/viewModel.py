from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from ex4nicegui import to_ref, ref_computed, deep_ref, Ref


@dataclass
class TodoItem:
    id: datetime
    title: str
    completed: bool = False


_T_todos = List[TodoItem]


class filters:
    @staticmethod
    def active(todos: _T_todos):
        return [todo for todo in todos if not todo.completed]

    @staticmethod
    def completed(todos: _T_todos):
        return [todo for todo in todos if todo.completed]

    @staticmethod
    def all(todos: _T_todos):
        return todos


@dataclass
class State:
    todos: Ref[_T_todos] = field(default_factory=lambda: deep_ref([]))
    filter_do = to_ref("all")

    @ref_computed
    def filtered_todos(self) -> _T_todos:
        return getattr(filters, self.filter_do.value)(self.todos.value)

    @ref_computed
    def active_count(self):
        return len(filters.active(self.todos.value))

    @ref_computed
    def completed_count(self):
        return len(filters.completed(self.todos.value))

    @ref_computed
    def total_count(self):
        return len(self.todos.value)

    @ref_computed
    def completion_ratio(self):
        if self.total_count.value == 0:
            return 0.0
        return round(self.completed_count.value / self.total_count.value, 2)

    # methods
    def add_todo(self, title):
        if title:
            self.todos.value.append(TodoItem(datetime.now(), title))

    def remove_todo(self, todo: TodoItem):
        self.todos.value.remove(todo)

    def remove_completed_todos(self):
        for todo in [todo for todo in self.todos.value if todo.completed]:
            self.remove_todo(todo)

    def all_checks(self):
        for todo in self.todos.value:
            todo.completed = True

    def all_unchecks(self):
        for todo in self.todos.value:
            todo.completed = not todo.completed
