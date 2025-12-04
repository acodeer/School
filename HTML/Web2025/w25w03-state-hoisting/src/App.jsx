import './App.css'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

function App() {
  return (
    <>
    {/* // 1. <BrowserRouter>로 전체 앱을 감싸 라우팅 기능 활성화
    <BrowserRouter> */}
      <nav>
        {/* 2. <Link>를 사용하여 페이지 간 이동 링크 생성 */}
        <Link to="/">홈</Link> | <Link to="/about">소개</Link>
      </nav>

      {/* 3. <Routes>는 경로 정의(<Route>들)의 컨테이너 역할 */}
      <Routes>
        {/* 4. <Route>는 특정 path와 해당 path에서 렌더링할 element(컴포넌트)를 매핑 */}
        {/* path="/"일 때 <Home /> 컴포넌트 렌더링 */}
        <Route path="/" element={<Home />} />
        
        {/* path="/about"일 때 <About /> 컴포넌트 렌더링 */}
        <Route path="/about" element={<About />} />
      </Routes>
    {/* </BrowserRouter> */}
    </>
  )
}

function Home() {
  return <h2>홈 페이지</h2>;
}

const About = () => <h2>소개 페이지</h2>

export default App
