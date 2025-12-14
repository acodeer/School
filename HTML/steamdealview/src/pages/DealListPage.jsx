import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import DealForm from '../components/DealForm.jsx';

// ----------------------------------------------------
// 1. API 호출 함수 정의
// ----------------------------------------------------
const fetchDeals = async () => {
  const response = await fetch('http://localhost:8080/api/deals');
  
  if (!response.ok) {
    throw new Error('할인 목록을 불러오는 데 실패했습니다.');
  }
  return response.json();
};

const DealListPage = () => {
  const { data: deals, isLoading, isError, error } = useQuery({
    queryKey: ['deals'],
    queryFn: fetchDeals,
  });

  if (isLoading) {
    return (
      <div className="text-center p-8 text-gray-400">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-red-500 mx-auto"></div>
        <p className="mt-4 text-lg">데이터 로딩 중...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="text-center p-8 text-red-400 border border-red-700 bg-red-950 rounded">
        <p className="font-bold text-xl">🚨 API 호출 에러 🚨</p>
        <p className="mt-2 text-sm">{error.message}</p>
      </div>
    );
  }

  return (
    <div>
      <DealForm />
      {/* 제목 색상을 Gray 100으로 변경 */}
      <h2 className="text-3xl font-extrabold mb-8 text-gray-100 border-b border-red-900 pb-2"> 
        Steam 오늘의 핫딜 🔥
      </h2>
      <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
    {deals && deals.map((deal) => (
        <Link key={deal.id} to={`/deals/${deal.id}`} className="block">
            <div className="bg-gray-800 p-3 sm:p-4 rounded-lg shadow-2xl hover:bg-gray-700 transition duration-300 transform hover:scale-[1.02] border border-gray-700 h-full flex flex-col justify-between">
              
                {/* 이미지 */}
                {deal.imageUrl && (
                    <div className="w-full h-24 overflow-hidden rounded-md mb-3">
                        <img 
                            src={deal.imageUrl} 
                            alt={deal.title} 
                            className="w-full h-full object-cover" 
                        />
                    </div>
                )}
                
                {/* 할인율 표시  */}
                <p className="bg-green-600 text-xs sm:text-sm font-bold w-fit px-2 sm:px-3 py-0.5 sm:py-1 rounded-full mb-2">
                    -{deal.discountPercent}% 할인
                </p>
                
                {/* 제목 */}
                <h3 className="text-sm sm:text-lg font-bold truncate text-gray-100 mb-1 leading-snug">
                    {deal.title}
                </h3>
                
                {/* 가격 정보 */}
                <div className="mt-auto pt-2">
                    <p className="text-xs text-gray-500 line-through">
                        ${deal.originalPrice}
                    </p>
                    <p className="text-lg sm:text-xl font-extrabold text-green-400">
                        ${deal.discountPrice}
                    </p>
                </div>
            </div>
        </Link>
        ))}
      </div>
      {deals && deals.length === 0 && (
        <p className="text-center text-gray-500 mt-10 text-xl">
          현재 할인 중인 게임이 없습니다.
        </p>
      )}
    </div>
  );
};

export default DealListPage;