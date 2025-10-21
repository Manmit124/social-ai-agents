# Python Learning Guide - From Node.js to Python Backend

## 🎯 Purpose
This guide explains all Python concepts used in this project, especially for developers coming from Node.js/JavaScript background.

---

## Table of Contents
1. [Python vs Node.js: Key Differences](#python-vs-nodejs-key-differences)
2. [Why `__init__.py` Files?](#why-__init__py-files)
3. [Python Imports Explained](#python-imports-explained)
4. [Type Hints & TypedDict](#type-hints--typeddict)
5. [Async/Await in Python](#asyncawait-in-python)
6. [Decorators Explained](#decorators-explained)
7. [Classes vs Functions](#classes-vs-functions)
8. [Error Handling](#error-handling)
9. [Environment Variables](#environment-variables)
10. [Virtual Environments](#virtual-environments)
11. [Python Project Structure](#python-project-structure)
12. [Common Patterns Used](#common-patterns-used)

---

## Python vs Node.js: Key Differences

### Side-by-Side Comparison

| Feature | Node.js | Python |
|---------|---------|--------|
| **Package Manager** | npm/yarn | pip |
| **Package File** | `package.json` | `requirements.txt` |
| **Module System** | `require()` / `import` | `import` / `from` |
| **Async** | Promises, async/await | async/await (similar!) |
| **Classes** | ES6 classes | Python classes |
| **Type Safety** | TypeScript (optional) | Type hints (optional) |
| **Environment** | `.env` + dotenv | `.env` + python-dotenv |
| **Virtual Env** | `node_modules/` | `venv/` |
| **Web Framework** | Express.js | FastAPI / Flask |
| **String Format** | Template literals `` `${var}` `` | f-strings `f"{var}"` |

### Example: Hello World API

**Node.js (Express)**:
```javascript
const express = require('express');
const app = express();

app.get('/hello', (req, res) => {
  res.json({ message: 'Hello World' });
});

app.listen(8000);
```

**Python (FastAPI)**:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/hello')
async def hello():
    return {"message": "Hello World"}

# Run with: uvicorn main:app --reload
```

---

## Why `__init__.py` Files?

### 🤔 The Question
In Node.js, you can just create folders and import files. Why does Python need `__init__.py` in every folder?

### 📚 The Answer

**In Node.js**:
```
src/
  utils/
    helper.js      ← Can import directly
```
```javascript
// Works automatically
const helper = require('./utils/helper');
```

**In Python**:
```
backend/
  utils/
    __init__.py    ← Makes it a "package"
    helper.py
```
```python
# Now you can import
from utils import helper
```

### What `__init__.py` Does

1. **Marks Directory as Package**
   - Without it: Python treats folder as regular directory
   - With it: Python treats folder as importable package

2. **Package Initialization**
   - Runs when package is first imported
   - Can initialize package-level variables
   - Can control what gets exported

3. **Cleaner Imports**
   - Without `__init__.py`: `from agent.tools.twitter_tool import validate_tweet`
   - With `__init__.py`: `from agent.tools import validate_tweet`

### Example: Our Project

**File**: `backend/agent/tools/__init__.py`
```python
"""
Agent tools package
"""

from .twitter_tool import (
    get_twitter_constraints,
    validate_twitter_content,
)

__all__ = [
    "get_twitter_constraints",
    "validate_twitter_content",
]
```

**What This Does**:
```python
# Instead of this (ugly):
from agent.tools.twitter_tool import get_twitter_constraints

# You can do this (clean):
from agent.tools import get_twitter_constraints
```

### Can `__init__.py` Be Empty?

**Yes!** An empty `__init__.py` just marks the directory as a package:

```python
# backend/models/__init__.py
# (empty file - just marks 'models' as a package)
```

### Node.js Equivalent

Think of `__init__.py` like `index.js` in Node.js:

**Node.js**:
```javascript
// utils/index.js
export { helper } from './helper';
export { validator } from './validator';

// Now you can:
import { helper } from './utils';  // imports from index.js
```

**Python**:
```python
# utils/__init__.py
from .helper import helper_function
from .validator import validate_function

# Now you can:
from utils import helper_function
```

---

## Python Imports Explained

### Import Styles

#### 1. Import Module
```python
# Import entire module
import os

# Usage
os.getenv("API_KEY")
```
**Node.js equivalent**:
```javascript
const os = require('os');
os.platform();
```

#### 2. Import Specific Items
```python
# Import specific functions/classes
from os import getenv

# Usage (no prefix needed)
getenv("API_KEY")
```
**Node.js equivalent**:
```javascript
const { getenv } = require('os');
getenv("API_KEY");
```

#### 3. Import with Alias
```python
# Import with different name
from services.gemini_service import GeminiService as AI

# Usage
ai = AI()
```
**Node.js equivalent**:
```javascript
const AI = require('./services/gemini_service').GeminiService;
const ai = new AI();
```

#### 4. Import Everything (Not Recommended)
```python
from os import *  # Imports everything - avoid this!
```

### Relative vs Absolute Imports

**Absolute Import** (from project root):
```python
# From anywhere in project
from backend.agent.state import AgentState
from backend.services.gemini_service import GeminiService
```

**Relative Import** (from current location):
```python
# From backend/agent/nodes.py
from .state import AgentState           # Same directory
from ..services.gemini_service import GeminiService  # Parent directory
```

**Dots Meaning**:
- `.` = current directory (like `./` in Node.js)
- `..` = parent directory (like `../` in Node.js)
- `...` = grandparent directory (like `../../` in Node.js)

### Our Project Example

**File**: `backend/agent/nodes.py`
```python
# Relative imports (from same package)
from .state import AgentState
from .tools import validate_tweet_length

# Absolute imports (from other packages)
from services.gemini_service import GeminiService
```

---

## Type Hints & TypedDict

### 🤔 Coming from TypeScript?

Python's type hints are similar to TypeScript but **optional** and **not enforced at runtime**.

### Basic Type Hints

**TypeScript**:
```typescript
function greet(name: string): string {
  return `Hello ${name}`;
}

const age: number = 25;
const isActive: boolean = true;
```

**Python**:
```python
def greet(name: str) -> str:
    return f"Hello {name}"

age: int = 25
is_active: bool = True
```

### Type Hints for Collections

**Python**:
```python
from typing import List, Dict, Optional, Any

# List of strings
tags: List[str] = ["#AI", "#Tech"]

# Dictionary
user: Dict[str, Any] = {"name": "John", "age": 30}

# Optional (can be None)
error: Optional[str] = None

# Multiple types
result: str | None = None  # Python 3.10+
```

**TypeScript equivalent**:
```typescript
const tags: string[] = ["#AI", "#Tech"];
const user: { [key: string]: any } = { name: "John", age: 30 };
const error: string | null = null;
```

### TypedDict (Like TypeScript Interfaces)

**TypeScript**:
```typescript
interface User {
  name: string;
  age: number;
  email?: string;  // Optional
}

const user: User = {
  name: "John",
  age: 30
};
```

**Python**:
```python
from typing import TypedDict, Optional

class User(TypedDict):
    name: str
    age: int
    email: Optional[str]  # Optional

user: User = {
    "name": "John",
    "age": 30
}
```

### Our Project Example

**File**: `backend/agent/state.py`
```python
from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    """State schema for the tweet generation agent."""
    user_prompt: str                # Required
    platform: str                   # Required
    tweet_content: str              # Required
    hashtags: List[str]             # List of strings
    is_valid: bool                  # Boolean
    error: Optional[str]            # Can be None
    step: str                       # Required
```

**Why TypedDict?**
- Documents expected structure
- IDE autocomplete support
- Type checking with mypy (optional)
- Better than plain `Dict[str, Any]`

### Important: Types Are Not Enforced!

```python
def add(a: int, b: int) -> int:
    return a + b

# This works! No runtime error
result = add("hello", "world")  # Returns "helloworld"
```

Python type hints are for:
- **Documentation**
- **IDE support**
- **Static analysis tools** (mypy, pylance)

They don't prevent wrong types at runtime!

---

## Async/Await in Python

### Good News: Very Similar to JavaScript!

**JavaScript**:
```javascript
async function fetchData() {
  const response = await fetch('https://api.example.com');
  const data = await response.json();
  return data;
}
```

**Python**:
```python
async def fetch_data():
    response = await httpx.get('https://api.example.com')
    data = response.json()
    return data
```

### Key Differences

| Feature | JavaScript | Python |
|---------|-----------|--------|
| **Async function** | `async function` | `async def` |
| **Await** | `await promise` | `await coroutine` |
| **Event loop** | Built-in (Node.js) | Need to import `asyncio` |
| **HTTP library** | `fetch` (built-in) | `httpx` or `aiohttp` |

### Running Async Code

**JavaScript**:
```javascript
// Automatically runs in event loop
async function main() {
  await doSomething();
}

main();
```

**Python**:
```python
import asyncio

async def main():
    await do_something()

# Need to explicitly run in event loop
asyncio.run(main())
```

### Our Project Example

**File**: `backend/agent/nodes.py`
```python
async def generate_node(state: AgentState) -> AgentState:
    """
    Async function - can use 'await'
    """
    gemini_service = get_gemini_service()
    
    # Await async call
    tweet_content = await gemini_service.generate_tweet(
        state["user_prompt"], 
        state["platform"]
    )
    
    state["tweet_content"] = tweet_content
    return state
```

### Mixing Sync and Async

**Problem**: Some libraries are synchronous (blocking)

**Solution**: Run sync code in thread pool

```python
import asyncio

# Synchronous function (blocks)
def sync_function():
    return "result"

# Run it in async context
async def async_wrapper():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, sync_function)
    return result
```

**Our Project Example** (`services/gemini_service.py`):
```python
async def generate_tweet(self, user_prompt: str) -> str:
    # Gemini client is synchronous, so run in executor
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None,
        lambda: self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
    )
    return response.text
```

---

## Decorators Explained

### 🤔 What Are Decorators?

Decorators are functions that modify other functions. Think of them as "wrappers" or "higher-order functions".

**Node.js equivalent**: Higher-order functions or middleware

### Basic Decorator

**Python**:
```python
def uppercase_decorator(func):
    def wrapper():
        result = func()
        return result.upper()
    return wrapper

@uppercase_decorator
def greet():
    return "hello world"

print(greet())  # Output: "HELLO WORLD"
```

**Node.js equivalent**:
```javascript
function uppercaseDecorator(func) {
  return function() {
    const result = func();
    return result.toUpperCase();
  };
}

const greet = uppercaseDecorator(() => "hello world");
console.log(greet());  // Output: "HELLO WORLD"
```

### The `@` Symbol

```python
@decorator
def function():
    pass

# Is the same as:
def function():
    pass
function = decorator(function)
```

### FastAPI Route Decorators

**Our Project** (`backend/main.py`):
```python
@app.post("/api/generate")
async def generate_content(request: GenerateRequest):
    return {"success": True}
```

**What `@app.post()` does**:
1. Registers the function as a route handler
2. Maps POST requests to `/api/generate`
3. Handles request/response serialization
4. Adds to OpenAPI documentation

**Express.js equivalent**:
```javascript
app.post('/api/generate', async (req, res) => {
  res.json({ success: true });
});
```

### Common Decorators in Our Project

#### 1. Route Decorators
```python
@app.get("/api/history")      # GET request
@app.post("/api/generate")    # POST request
@app.delete("/api/post/{id}") # DELETE request
```

#### 2. Dependency Injection
```python
from fastapi import Depends

@app.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user)):
    # user_id is automatically injected
    return {"user_id": user_id}
```

**What `Depends()` does**:
- Calls `get_current_user()` before route handler
- Passes result as parameter
- Like middleware in Express.js

#### 3. Property Decorator
```python
class User:
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        return self._name.upper()

user = User("john")
print(user.name)  # Calls method like a property (no parentheses)
```

---

## Classes vs Functions

### When to Use Classes

**Use Classes When**:
- You need to maintain state
- You have related methods
- You need initialization logic

**Use Functions When**:
- Simple, stateless operations
- One-off tasks
- Pure functions

### Class Example

**Our Project** (`services/gemini_service.py`):
```python
class GeminiService:
    def __init__(self, api_key: str = None):
        """
        Constructor - runs when instance is created
        Like constructor() in JavaScript
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client()
        self.model_name = "gemini-2.0-flash-exp"
    
    async def generate_tweet(self, prompt: str) -> str:
        """
        Instance method - has access to self.client, self.model_name
        """
        response = await self.client.generate(prompt)
        return response.text

# Usage
service = GeminiService()
tweet = await service.generate_tweet("Hello")
```

**JavaScript equivalent**:
```javascript
class GeminiService {
  constructor(apiKey = null) {
    this.apiKey = apiKey || process.env.GEMINI_API_KEY;
    this.client = new genai.Client();
    this.modelName = "gemini-2.0-flash-exp";
  }
  
  async generateTweet(prompt) {
    const response = await this.client.generate(prompt);
    return response.text;
  }
}

const service = new GeminiService();
const tweet = await service.generateTweet("Hello");
```

### `self` Explained

**Python**:
```python
class Counter:
    def __init__(self):
        self.count = 0  # Instance variable
    
    def increment(self):
        self.count += 1  # Access via self
```

**JavaScript**:
```javascript
class Counter {
  constructor() {
    this.count = 0;  // Instance variable
  }
  
  increment() {
    this.count += 1;  // Access via this
  }
}
```

`self` in Python = `this` in JavaScript

### Static Methods vs Instance Methods

```python
class MathUtils:
    # Instance method (needs self)
    def add_to_value(self, x):
        return self.value + x
    
    # Static method (no self needed)
    @staticmethod
    def add(x, y):
        return x + y

# Static method - no instance needed
result = MathUtils.add(5, 3)

# Instance method - needs instance
utils = MathUtils()
utils.value = 10
result = utils.add_to_value(5)
```

---

## Error Handling

### Try/Except (Like Try/Catch)

**JavaScript**:
```javascript
try {
  const data = await fetchData();
  return data;
} catch (error) {
  console.error(error);
  throw new Error("Failed to fetch");
} finally {
  cleanup();
}
```

**Python**:
```python
try:
    data = await fetch_data()
    return data
except Exception as e:
    print(f"Error: {e}")
    raise Exception("Failed to fetch")
finally:
    cleanup()
```

### Specific Exception Types

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except ValueError:
    print("Invalid value")
except Exception as e:
    print(f"Other error: {e}")
```

### FastAPI Exception Handling

**Our Project** (`backend/main.py`):
```python
from fastapi import HTTPException

@app.post("/api/generate")
async def generate_content(request: GenerateRequest):
    # Validation error
    if not request.prompt:
        raise HTTPException(
            status_code=400,
            detail="Prompt is required"
        )
    
    # Authentication error
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    # Server error
    try:
        result = await generate()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
```

**Express.js equivalent**:
```javascript
app.post('/api/generate', async (req, res) => {
  if (!req.body.prompt) {
    return res.status(400).json({ error: "Prompt is required" });
  }
  
  if (!userId) {
    return res.status(401).json({ error: "Not authenticated" });
  }
  
  try {
    const result = await generate();
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

---

## Environment Variables

### Loading .env Files

**Node.js**:
```javascript
require('dotenv').config();
const apiKey = process.env.API_KEY;
```

**Python**:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
```

### Our Project Example

**File**: `backend/main.py`
```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access variables
supabase_url = os.getenv("SUPABASE_URL")
api_key = os.getenv("GEMINI_API_KEY")
port = int(os.getenv("PORT", 8000))  # Default value
```

### Environment File

**`.env`**:
```bash
SUPABASE_URL=https://xxx.supabase.co
GEMINI_API_KEY=AIzaSyxxx...
PORT=8000
```

---

## Virtual Environments

### 🤔 What's a Virtual Environment?

Like `node_modules` but for the entire Python environment.

**Node.js**:
- Each project has `node_modules/`
- Packages installed per project
- `package.json` defines dependencies

**Python**:
- Each project has `venv/`
- Packages installed in virtual environment
- `requirements.txt` defines dependencies

### Why Virtual Environments?

**Problem**: System-wide Python packages can conflict

```bash
# Project A needs requests==2.28.0
# Project B needs requests==2.31.0
# Can't have both installed globally!
```

**Solution**: Each project gets its own isolated environment

### Creating Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Now you're in the virtual environment
# Prompt shows: (venv) $

# Install packages (only in this environment)
pip install fastapi

# Deactivate when done
deactivate
```

### Requirements File

**`requirements.txt`** (like `package.json`):
```txt
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
supabase==2.0.3
```

```bash
# Install all dependencies
pip install -r requirements.txt

# Generate requirements.txt from current environment
pip freeze > requirements.txt
```

**Node.js equivalent**:
```bash
npm install              # = pip install -r requirements.txt
npm install fastapi      # = pip install fastapi
```

---

## Python Project Structure

### Typical Python Project

```
my-project/
├── venv/                    # Virtual environment (like node_modules)
├── src/                     # Source code
│   ├── __init__.py         # Makes 'src' a package
│   ├── main.py             # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   └── services/
│       ├── __init__.py
│       └── api.py
├── tests/                   # Tests
│   ├── __init__.py
│   └── test_api.py
├── .env                     # Environment variables
├── .gitignore              # Git ignore
├── requirements.txt        # Dependencies
└── README.md               # Documentation
```

### Our Project Structure

```
backend/
├── venv/                   # Virtual environment
├── agent/                  # AI agent package
│   ├── __init__.py        # Package marker
│   ├── state.py           # Agent state
│   ├── graph.py           # Agent workflow
│   ├── nodes.py           # Processing nodes
│   └── tools/             # Tools package
│       ├── __init__.py
│       └── twitter_tool.py
├── services/              # External services
│   ├── __init__.py
│   ├── gemini_service.py
│   └── supabase_service.py
├── main.py                # FastAPI app
├── requirements.txt       # Dependencies
└── .env                   # Environment variables
```

---

## Common Patterns Used

### 1. Singleton Pattern (Global Instance)

**Our Project** (`agent/nodes.py`):
```python
# Global variable
_gemini_service = None

def get_gemini_service():
    """
    Lazy initialization - create only when needed
    Reuse same instance (singleton pattern)
    """
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
```

**Why?**
- Create expensive objects once
- Reuse across multiple calls
- Save memory and initialization time

### 2. Dependency Injection

**Our Project** (`main.py`):
```python
from fastapi import Depends
from auth.supabase_auth import get_current_user

@app.get("/protected")
async def protected_route(user_id: str = Depends(get_current_user)):
    """
    user_id is automatically injected by FastAPI
    get_current_user() runs before this function
    """
    return {"user_id": user_id}
```

**How it works**:
1. FastAPI sees `Depends(get_current_user)`
2. Calls `get_current_user()` first
3. Passes result to `protected_route()`
4. Like middleware in Express.js

### 3. Context Manager (with statement)

```python
# Automatically closes file
with open("file.txt", "r") as f:
    content = f.read()
# File is automatically closed here

# Async version
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.com")
# Client is automatically closed
```

**Our Project** (`services/social/twitter_service.py`):
```python
async with httpx.AsyncClient() as client:
    response = await client.post(
        self.token_url,
        data=data
    )
# Client automatically cleaned up
```

### 4. List Comprehension

**Instead of**:
```python
# Traditional loop
hashtags = []
for word in text.split():
    if word.startswith('#'):
        hashtags.append(word)
```

**Use**:
```python
# List comprehension (more Pythonic)
hashtags = [word for word in text.split() if word.startswith('#')]
```

**Our Project** (`services/gemini_service.py`):
```python
# Parse hashtags from response
hashtags = [word for word in response.text.split() if word.startswith('#')]
```

### 5. F-Strings (String Formatting)

**Old way**:
```python
name = "John"
age = 30
message = "Hello, " + name + ". You are " + str(age) + " years old."
```

**Modern way (f-strings)**:
```python
name = "John"
age = 30
message = f"Hello, {name}. You are {age} years old."
```

**Our Project**:
```python
print(f"📝 User {user_id} - Received prompt for {platform}: {prompt}")
```

### 6. Dictionary `.get()` with Default

```python
# Instead of:
if "key" in dict:
    value = dict["key"]
else:
    value = "default"

# Use:
value = dict.get("key", "default")
```

**Our Project**:
```python
platform = state.get("platform", "twitter")  # Default to "twitter"
error = state.get("error", None)             # Default to None
```

### 7. Optional Parameters

```python
def greet(name: str, greeting: str = "Hello"):
    """
    greeting is optional, defaults to "Hello"
    """
    return f"{greeting}, {name}"

greet("John")              # Uses default: "Hello, John"
greet("John", "Hi")        # Custom: "Hi, John"
```

**Our Project** (`agent/graph.py`):
```python
async def run_agent(user_prompt: str, platform: str = "twitter"):
    """
    platform is optional, defaults to "twitter"
    """
    # ...
```

---

## Quick Reference: Python Syntax

### Variables
```python
# No const/let/var needed
name = "John"
age = 30
is_active = True
items = ["a", "b", "c"]
user = {"name": "John", "age": 30}
```

### Functions
```python
# Regular function
def add(a, b):
    return a + b

# Async function
async def fetch_data():
    return await api.get()

# Lambda (arrow function)
square = lambda x: x ** 2
```

### Conditionals
```python
if age > 18:
    print("Adult")
elif age > 13:
    print("Teen")
else:
    print("Child")

# Ternary operator
status = "adult" if age > 18 else "minor"
```

### Loops
```python
# For loop
for item in items:
    print(item)

# For loop with index
for i, item in enumerate(items):
    print(f"{i}: {item}")

# While loop
while count < 10:
    count += 1

# Dictionary loop
for key, value in user.items():
    print(f"{key}: {value}")
```

### None (null)
```python
value = None  # Like null in JavaScript

if value is None:
    print("No value")

if value:  # Falsy check
    print("Has value")
```

### Boolean Operators
```python
# and, or, not (not &&, ||, !)
if age > 18 and is_active:
    print("Active adult")

if age < 13 or age > 65:
    print("Special rate")

if not is_active:
    print("Inactive")
```

### String Methods
```python
text = "Hello World"

text.lower()           # "hello world"
text.upper()           # "HELLO WORLD"
text.strip()           # Remove whitespace
text.split()           # ["Hello", "World"]
text.startswith("H")   # True
text.endswith("d")     # True
text.replace("o", "0") # "Hell0 W0rld"
"#" in text            # False (contains check)
```

### List Methods
```python
items = [1, 2, 3]

items.append(4)        # Add to end
items.pop()            # Remove from end
items.insert(0, 0)     # Insert at index
items.remove(2)        # Remove specific value
len(items)             # Length
items[0]               # First item
items[-1]              # Last item
items[1:3]             # Slice [2, 3]
```

### Dictionary Methods
```python
user = {"name": "John", "age": 30}

user["name"]           # Get value
user.get("email", "")  # Get with default
user["email"] = "..."  # Set value
"name" in user         # Check key exists
user.keys()            # Get all keys
user.values()          # Get all values
user.items()           # Get key-value pairs
```

---

## Common Gotchas for Node.js Developers

### 1. Indentation Matters!

**JavaScript**: Uses `{}` for blocks
```javascript
if (true) {
  console.log("Hello");
  console.log("World");
}
```

**Python**: Uses indentation (4 spaces)
```python
if True:
    print("Hello")
    print("World")
```

❌ **Wrong**:
```python
if True:
print("Hello")  # IndentationError!
```

### 2. No Semicolons

```python
# No semicolons needed
name = "John"
age = 30
print(name)
```

### 3. True/False (Capital Letters)

```javascript
// JavaScript
const isActive = true;
const isDisabled = false;
```

```python
# Python
is_active = True   # Capital T
is_disabled = False  # Capital F
```

### 4. `None` not `null`

```javascript
const value = null;
```

```python
value = None  # Capital N
```

### 5. String Concatenation

```javascript
// JavaScript
const message = "Hello " + name + "!";
const message = `Hello ${name}!`;
```

```python
# Python
message = "Hello " + name + "!"
message = f"Hello {name}!"  # f-string (preferred)
```

### 6. Array vs List

```javascript
// JavaScript
const items = [1, 2, 3];
items.push(4);
```

```python
# Python
items = [1, 2, 3]
items.append(4)  # Not push!
```

### 7. Object vs Dictionary

```javascript
// JavaScript
const user = {
  name: "John",
  age: 30
};
console.log(user.name);
```

```python
# Python
user = {
    "name": "John",  # Quotes required!
    "age": 30
}
print(user["name"])  # Brackets, not dot!
```

### 8. `===` vs `==`

```javascript
// JavaScript
if (value === 5) { }  // Strict equality
if (value == 5) { }   // Loose equality
```

```python
# Python
if value == 5:  # Only one ==
    pass

# For identity check (like ===)
if value is 5:
    pass
```

---

## Running Python Code

### Running a Script

```bash
# Run Python file
python main.py

# Run with Python 3 explicitly
python3 main.py
```

### Running FastAPI

```bash
# Development (auto-reload)
uvicorn main:app --reload --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Python REPL (Like Node REPL)

```bash
# Start Python interactive shell
python

>>> print("Hello")
Hello
>>> exit()
```

---

## Debugging Tips

### Print Debugging

```python
# Simple print
print("Debug:", variable)

# F-string with type
print(f"Value: {value}, Type: {type(value)}")

# Pretty print (for complex objects)
from pprint import pprint
pprint(complex_dict)
```

### Using Debugger

```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or in Python 3.7+
breakpoint()
```

### Logging (Better than print)

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

---

## Resources for Learning More

### Official Documentation
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Type Hints Guide](https://docs.python.org/3/library/typing.html)

### For Node.js Developers
- [Python for JavaScript Developers](https://www.valentinog.com/blog/python-for-js/)
- [FastAPI vs Express](https://fastapi.tiangolo.com/alternatives/)

### Practice
- [Python Exercises](https://www.w3schools.com/python/python_exercises.asp)
- [Real Python Tutorials](https://realpython.com/)

---

## Summary: Key Takeaways

1. **`__init__.py`** - Makes directories importable packages (like `index.js`)
2. **Type Hints** - Optional, for documentation (like TypeScript)
3. **Async/Await** - Very similar to JavaScript
4. **Decorators** - Functions that modify functions (like `@app.get()`)
5. **Classes** - Use `self` instead of `this`
6. **Virtual Environments** - Like `node_modules` but for Python
7. **Indentation** - Matters! Use 4 spaces
8. **F-Strings** - Modern string formatting: `f"Hello {name}"`
9. **None** - Python's `null`
10. **True/False** - Capital letters

---

## Next Steps

1. ✅ Read this guide
2. ✅ Review the backend code with new understanding
3. ✅ Try modifying existing endpoints
4. ✅ Create a new endpoint from scratch
5. ✅ Experiment with type hints
6. ✅ Practice async/await patterns
7. ✅ Build a small FastAPI project

You're now ready to work with Python backends! 🚀

