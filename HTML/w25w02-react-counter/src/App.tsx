import './App.css'
import { useState } from 'react'

function App() {
  const [count, setCount] = useState(1)
  const plusOne = (prev: number) => prev + 1
  return (
    <>
      <h1>카운터 : {count}</h1>
      <button
        onClick={() => {
          setCount(plusOne)
          setCount(plusOne)
          setCount(plusOne)
          setCount(plusOne)
          setCount(plusOne)
        }}
      >
        증가
      </button>
    </>
  )
}

export default App
