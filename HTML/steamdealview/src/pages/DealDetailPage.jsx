// src/pages/DealDetailPage.jsx

import { useQuery , useQueryClient , useMutation } from '@tanstack/react-query';
import { useParams, Link, useNavigate  } from 'react-router-dom';
import React, { useState } from 'react';

// ----------------------------------------------------
// 1. 상세 API 호출 함수 정의
// ----------------------------------------------------
const fetchDealDetail = async (id) => {
  const response = await fetch(`http://localhost:8080/api/deals/${id}`);
  
  if (!response.ok) {
    // 404 Not Found도 여기서 처리 가능
    throw new Error('해당 ID의 게임 정보를 찾을 수 없습니다.');
  }
  return response.json();
};
const updateDeal = async ({ id, dealData }) => {
    const response = await fetch(`http://localhost:8080/api/deals/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dealData),
    });
    if (!response.ok) {
        throw new Error('게임 정보 수정에 실패했습니다.');
    }
    return response.json();
};
const deleteDeal = async (id) => {
    const response = await fetch(`http://localhost:8080/api/deals/${id}`, {
        method: 'DELETE',
    });
    if (response.status === 404) {
        throw new Error('이미 존재하지 않는 게임입니다.');
    }
    if (!response.ok && response.status !== 204) {
        throw new Error('게임 삭제에 실패했습니다.');
    }
    // 204 No Content는 본문이 없으므로 빈 객체 반환
    return {}; 
};
const DealDetailPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    
    // 수정 상태를 관리하는 State (U 기능 추가)
    const [isEditing, setIsEditing] = useState(false); 

    // 기존 데이터 쿼리
    const { data: deal, isLoading, isError, error } = useQuery({
        queryKey: ['deal', id],
        queryFn: () => fetchDealDetail(id),
        enabled: !!id,
    });

    const updateMutation = useMutation({
        mutationFn: updateDeal,
        onSuccess: (updatedData) => {
            // 상세 쿼리 데이터만 갱신 (목록 쿼리는 놔둠)
            queryClient.setQueryData(['deal', id], updatedData); 
            setIsEditing(false); // 수정 모드 종료
            alert('게임 정보가 성공적으로 수정되었습니다.');
        },
        onError: (e) => alert(`수정 실패: ${e.message}`),
    });

    const deleteMutation = useMutation({
        mutationFn: deleteDeal,
        onSuccess: () => {
            // 'deals' 목록 쿼리를 무효화하여 리스트를 새로고침
            queryClient.invalidateQueries({ queryKey: ['deals'] });
            alert('게임 딜이 성공적으로 삭제되었습니다.');
            navigate('/'); // 삭제 후 목록 페이지로 이동
        },
        onError: (e) => alert(`삭제 실패: ${e.message}`),
    });

    const handleDelete = () => {
        if (window.confirm('정말로 이 게임 딜을 삭제하시겠습니까?')) {
            deleteMutation.mutate(id); // 삭제 요청 실행
        }
    };

  if (isLoading) {
    return (
      <div className="text-center p-8 text-gray-400">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-red-500 mx-auto"></div>
        <p className="mt-4 text-lg">상세 정보 로딩 중...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="text-center p-8 text-red-400">
        <p className="font-bold text-xl">🚨 오류: {error.message}</p>
        <Link to="/" className="text-blue-400 underline mt-4 block">
          목록으로 돌아가기
        </Link>
      </div>
    );
  }

  if (!deal) {
      return <div>데이터를 찾을 수 없습니다.</div>;
  }

  // ----------------------------------------------------
  // 3. 상세 정보 렌더링
  // ----------------------------------------------------
  return (
    // 배경색을 bg-gray-800 유지 (Layout의 bg-gray-950과 대비되어 중앙 컨텐츠 강조)
    <div className="bg-gray-800 p-8 rounded-xl shadow-2xl max-w-4xl mx-auto border border-gray-700">
        <Link to="/" className="text-red-400 hover:text-red-300 transition block mb-6">
            &larr; 할인 목록으로 돌아가기
        </Link>

        {/* -------------------- 수정 폼 (isEditing = true) -------------------- */}
            {isEditing ? (
                // ... UpdateForm 호출 유지
                <UpdateForm 
                    deal={deal} 
                    onUpdate={(data) => updateMutation.mutate({ id, dealData: data })}
                    onCancel={() => setIsEditing(false)}
                />
            ) : (
            /* -------------------- 상세 보기 (isEditing = false) -------------------- */
                <>
                    {/* 제목을 text-gray-100으로 변경 */}
                    <h1 className="text-4xl font-extrabold mb-4 text-gray-100">{deal.title}</h1>
                    {/* 이미지 영역 유지 */}
                    <div className="w-full h-64 mb-6 overflow-hidden rounded-lg">
                        <img 
                            src={deal.imageUrl} 
                            alt={deal.title} 
                            className="w-full h-full object-cover" 
                        />
                    </div>
                    {/* 장르 텍스트 색상을 text-gray-300으로 변경 */}
                    <p className="text-lg text-gray-300 mb-6">장르: {deal.genre}</p>
                    
                    <div className="mb-8 p-6 bg-gray-900 rounded-lg border border-red-900">
                        <p className="text-2xl font-bold text-red-500 mb-2">
                            🔥 {deal.discountPercent}% 할인 중!
                        </p>
                        <div className="flex justify-between items-end">
                            <div>
                                <p className="text-sm text-gray-500 line-through">
                                    정가: ${deal.originalPrice}
                                </p>
                                <p className="text-4xl font-black text-green-400">
                                    할인가: ${deal.discountPrice}
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <h2 className="text-2xl font-semibold mt-8 mb-3 border-b border-gray-700 pb-1">게임 설명</h2>
                    {/* 설명 텍스트 색상을 text-gray-300으로 변경 */}
                    <p className="text-gray-300 leading-relaxed whitespace-pre-wrap">
                        {deal.description}
                    </p>
                    
                    {/* 수정 및 삭제 버튼 유지 */}
                    <div className="mt-8 flex justify-end space-x-4">
                        <button 
                            onClick={() => setIsEditing(true)} 
                            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition w-full md:w-auto">
                            ✏️ 정보 수정하기
                        </button>
                        <button 
                            onClick={handleDelete} 
                            className="bg-red-700 hover:bg-red-800 text-white font-bold py-2 px-4 rounded transition w-full md:w-auto">
                            🗑️ 삭제하기
                        </button>
                    </div>
                </>
            )}
    </div>
    );
};

const UpdateForm = ({ deal, onUpdate, onCancel }) => {

    const [formData, setFormData] = useState({
        title: deal.title, 
        originalPrice: deal.originalPrice, 
        // discountPrice 제거, discountPercent로 초기화
        discountPercent: deal.discountPercent, 
        genre: deal.genre, 
        description: deal.description,
        imageUrl: deal.imageUrl || '' // null 대신 빈 문자열로 초기화하여 에러 방지
    });

    const handleChange = (e) => {
        const { name, value, type } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'number' ? parseFloat(value) : value,
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        
        // --- 🚨 계산 로직 변경: 할인가(discountPrice) 자동 계산 🚨 ---
        const originalPrice = formData.originalPrice;
        const discountPercent = formData.discountPercent;
        
        // 할인가 = 정가 * (1 - 할인율/100)
        const discountPrice = originalPrice * (1 - discountPercent / 100);

        onUpdate({ 
            ...formData, 
            discountPrice: discountPrice.toFixed(2), // 소수점 둘째 자리까지 반올림
            discountPercent: discountPercent
        });
    };

    // 할인가 미리보기 계산
    const calculatedDiscountPrice = formData.originalPrice > 0 && formData.discountPercent >= 0 
        ? (formData.originalPrice * (1 - formData.discountPercent / 100)).toFixed(2)
        : deal.discountPrice.toFixed(2); // 초기값은 기존 할인가 사용

    return (
        <div className="bg-gray-700 p-6 sm:p-8 rounded-xl border-2 border-yellow-500/50"> 
            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                
                <input name="title" value={formData.title} onChange={handleChange} placeholder="게임 제목" required className="p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-yellow-500 col-span-2" />
                <input name="genre" value={formData.genre} onChange={handleChange} placeholder="장르" required className="p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-yellow-500" />
                <input name="imageUrl" value={formData.imageUrl} onChange={handleChange} placeholder="이미지 URL" className="p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-yellow-500" />
                
                <div className="md:col-span-2 grid grid-cols-3 gap-4 sm:gap-6 border-t pt-4 border-gray-700 items-center">
                    <input name="originalPrice" type="number" value={formData.originalPrice} onChange={handleChange} placeholder="정가 ($)" required 
                           className="p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-green-500" min="0" step="0.01" />

                    <input name="discountPercent" type="number" value={formData.discountPercent} onChange={handleChange} placeholder="할인율 (%)" required 
                           className="p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-green-500" min="0" max="100" />
                    
                    <p className="text-lg font-bold text-center text-green-400">
                      할인가: ${calculatedDiscountPrice}
                    </p>
                </div>

                <textarea name="description" value={formData.description} onChange={handleChange} placeholder="게임 설명" required rows="4" className="md:col-span-2 p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-yellow-500"></textarea>

                <div className="md:col-span-2 flex justify-end space-x-3 mt-4">
                </div>
            </form>
        </div>
    );
};

export default DealDetailPage;