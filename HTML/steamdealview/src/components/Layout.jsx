import { Outlet } from 'react-router-dom';

const Layout = () => {
  return (
    // 전체 텍스트 색상을 회색톤으로 변경 (text-gray-300)
    <div className="min-h-screen bg-gray-950 text-gray-300"> 
      <header className="bg-gray-800 p-4 shadow-xl border-b border-gray-700">
        <div className="container mx-auto">
          {/* 제목 색상을 덜 자극적인 Gray 100으로 변경 */}
          <h1 className="text-4xl font-extrabold text-gray-100 tracking-wider">
            STEAM DEALS VIEWER
          </h1>
        </div>
      </header>
      <main className="container mx-auto p-4 sm:p-6 lg:p-8">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;