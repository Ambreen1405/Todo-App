'use client'

import { useState, useEffect } from 'react'
import { v4 as uuidv4 } from 'uuid'
import { Todo } from '@/types/todo'

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState('')
  const [editDescription, setEditDescription] = useState('')

  // Load todos from localStorage on component mount
  useEffect(() => {
    const savedTodos = localStorage.getItem('todos')
    if (savedTodos) {
      setTodos(JSON.parse(savedTodos, (key, value) => {
        if (key === 'createdAt') return new Date(value)
        return value
      }))
    }
  }, [])

  // Save todos to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('todos', JSON.stringify(todos))
  }, [todos])

  const addTodo = () => {
    if (!title.trim()) return

    const newTodo: Todo = {
      id: uuidv4(),
      title: title.trim(),
      description: description.trim(),
      completed: false,
      createdAt: new Date(),
    }

    setTodos([newTodo, ...todos])
    setTitle('')
    setDescription('')
  }

  const deleteTodo = (id: string) => {
    setTodos(todos.filter(todo => todo.id !== id))
  }

  const toggleComplete = (id: string) => {
    setTodos(
      todos.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    )
  }

  const startEditing = (todo: Todo) => {
    setEditingId(todo.id)
    setEditTitle(todo.title)
    setEditDescription(todo.description)
  }

  const saveEdit = () => {
    if (!editTitle.trim() || !editingId) return

    setTodos(
      todos.map(todo =>
        todo.id === editingId
          ? { ...todo, title: editTitle.trim(), description: editDescription.trim() }
          : todo
      )
    )

    setEditingId(null)
    setEditTitle('')
    setEditDescription('')
  }

  const cancelEdit = () => {
    setEditingId(null)
    setEditTitle('')
    setEditDescription('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-50 via-blue-50 to-indigo-100 py-12 px-4 sm:px-6">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Todo App</h1>
          <p className="text-gray-600">Manage your tasks efficiently</p>
        </div>

        {/* Add Todo Form */}
        <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-xl p-6 mb-8 border border-gray-100 transition-all duration-300 hover:shadow-2xl">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Add New Task</h2>
          <div className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                Title
              </label>
              <input
                type="text"
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:shadow-md"
                placeholder="Enter task title..."
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 hover:shadow-md"
                placeholder="Enter task description..."
                rows={2}
              />
            </div>
            <button
              onClick={addTodo}
              className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg active:scale-95"
            >
              Add Task
            </button>
          </div>
        </div>

        {/* Todo List */}
        <div className="bg-gradient-to-br from-white to-gray-50 rounded-2xl shadow-xl p-6 border border-gray-100 transition-all duration-300 hover:shadow-2xl">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Tasks</h2>

          {todos.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500">No tasks yet. Add a task to get started!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {todos.map((todo) => (
                <div
                  key={todo.id}
                  className={`p-4 rounded-xl border transition-all duration-300 transform hover:scale-[1.02] hover:shadow-lg ${
                    todo.completed
                      ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200'
                      : 'bg-gradient-to-r from-white to-gray-50 border-gray-200'
                  }`}
                >
                  {editingId === todo.id ? (
                    // Edit Mode
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="w-full px-3 py-1 border border-gray-300 rounded-lg mb-2 transition-all duration-200 hover:shadow-md"
                        placeholder="Edit title..."
                      />
                      <textarea
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                        className="w-full px-3 py-1 border border-gray-300 rounded-lg mb-2 transition-all duration-200 hover:shadow-md"
                        placeholder="Edit description..."
                        rows={2}
                      />
                      <div className="flex space-x-2">
                        <button
                          onClick={saveEdit}
                          className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-3 py-1 rounded-lg text-sm transition-all duration-300 transform hover:scale-105 active:scale-95"
                        >
                          Save
                        </button>
                        <button
                          onClick={cancelEdit}
                          className="bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white px-3 py-1 rounded-lg text-sm transition-all duration-300 transform hover:scale-105 active:scale-95"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    // Display Mode
                    <div>
                      <div className="flex items-start">
                        <input
                          type="checkbox"
                          checked={todo.completed}
                          onChange={() => toggleComplete(todo.id)}
                          className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer transition-transform duration-200 hover:scale-110"
                        />
                        <div className="ml-3 flex-1">
                          <h3
                            className={`font-medium ${
                              todo.completed
                                ? 'text-gray-500 line-through'
                                : 'text-gray-800'
                            }`}
                          >
                            {todo.title}
                          </h3>
                          {todo.description && (
                            <p
                              className={`mt-1 text-sm ${
                                todo.completed
                                  ? 'text-gray-400 line-through'
                                  : 'text-gray-600'
                              }`}
                            >
                              {todo.description}
                            </p>
                          )}
                          <p className="text-xs text-gray-500 mt-2">
                            Created: {todo.createdAt.toLocaleDateString()}
                          </p>
                        </div>
                        <div className="flex space-x-2">
                          <button
                            onClick={() => startEditing(todo)}
                            className="text-blue-600 hover:text-blue-800 transition-all duration-200 transform hover:scale-110 hover:bg-blue-100 p-1 rounded-full"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              className="h-5 w-5"
                              viewBox="0 0 20 20"
                              fill="currentColor"
                            >
                              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                            </svg>
                          </button>
                          <button
                            onClick={() => deleteTodo(todo.id)}
                            className="text-red-600 hover:text-red-800 transition-all duration-200 transform hover:scale-110 hover:bg-red-100 p-1 rounded-full"
                          >
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              className="h-5 w-5"
                              viewBox="0 0 20 20"
                              fill="currentColor"
                            >
                              <path
                                fillRule="evenodd"
                                d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
                                clipRule="evenodd"
                              />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gradient-to-br from-blue-100 to-indigo-100 rounded-xl shadow-lg p-6 text-center transition-all duration-300 transform hover:scale-105 hover:shadow-xl">
            <p className="text-3xl font-bold text-gray-800">{todos.length}</p>
            <p className="text-gray-600 mt-2">Total Tasks</p>
          </div>
          <div className="bg-gradient-to-br from-green-100 to-emerald-100 rounded-xl shadow-lg p-6 text-center transition-all duration-300 transform hover:scale-105 hover:shadow-xl">
            <p className="text-3xl font-bold text-green-700">
              {todos.filter(todo => todo.completed).length}
            </p>
            <p className="text-gray-600 mt-2">Completed</p>
          </div>
          <div className="bg-gradient-to-br from-amber-100 to-orange-100 rounded-xl shadow-lg p-6 text-center transition-all duration-300 transform hover:scale-105 hover:shadow-xl">
            <p className="text-3xl font-bold text-amber-700">
              {todos.filter(todo => !todo.completed).length}
            </p>
            <p className="text-gray-600 mt-2">Pending</p>
          </div>
        </div>
      </div>
    </div>
  )
}