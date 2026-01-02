import { NextRequest, NextResponse } from 'next/server'
import { Todo } from '@/types/todo'

// In-memory storage for todos (in a real app, you'd use a database)
let todos: Todo[] = []

export async function GET(request: NextRequest) {
  // Return all todos
  return NextResponse.json({ success: true, data: todos })
}

export async function POST(request: NextRequest) {
  try {
    const { title, description } = await request.json()
    if (!title) {
      return NextResponse.json({ success: false, error: 'Title is required' }, { status: 400 })
    }

    const newTodo: Todo = {
      id: Math.random().toString(36).substring(7),
      title,
      description: description || '',
      completed: false,
      createdAt: new Date(),
    }

    todos.push(newTodo)
    return NextResponse.json({ success: true, data: newTodo }, { status: 201 })
  } catch (error) {
    return NextResponse.json({ success: false, error: 'Invalid request body' }, { status: 400 })
  }
}

export async function PUT(request: NextRequest) {
  try {
    const { id, title, description, completed } = await request.json()
    const todoIndex = todos.findIndex(todo => todo.id === id)

    if (todoIndex === -1) {
      return NextResponse.json({ success: false, error: 'Todo not found' }, { status: 404 })
    }

    todos[todoIndex] = {
      ...todos[todoIndex],
      ...(title !== undefined && { title }),
      ...(description !== undefined && { description }),
      ...(completed !== undefined && { completed }),
    }

    return NextResponse.json({ success: true, data: todos[todoIndex] })
  } catch (error) {
    return NextResponse.json({ success: false, error: 'Invalid request body' }, { status: 400 })
  }
}

export async function DELETE(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')

  if (!id) {
    return NextResponse.json({ success: false, error: 'ID is required' }, { status: 400 })
  }

  const initialLength = todos.length
  todos = todos.filter(todo => todo.id !== id)

  if (todos.length === initialLength) {
    return NextResponse.json({ success: false, error: 'Todo not found' }, { status: 404 })
  }

  return NextResponse.json({ success: true, message: 'Todo deleted successfully' })
}