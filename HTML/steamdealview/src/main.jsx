import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

// 1. React Router
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

// 2. TanStack Query
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// 페이지 컴포넌트 임포트 (아래에서 정의할 예정)
import DealListPage from './pages/DealListPage.jsx';
import DealDetailPage from './pages/DealDetailPage.jsx';
import Layout from './components/Layout.jsx';

// 쿼리 클라이언트 생성
const queryClient = new QueryClient();

// 라우터 설정
const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />, // 전체 레이아웃을 잡아줄 컴포넌트
    children: [
      {
        path: '/',
        element: <DealListPage />, // 할인 목록 페이지
      },
      {
        path: 'deals/:id',
        element: <DealDetailPage />, // 상세 정보 페이지
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* QueryClientProvider로 앱 전체를 감싸서 Query 사용 가능하게 함 */}
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
);