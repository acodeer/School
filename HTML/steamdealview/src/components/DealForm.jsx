// src/components/DealForm.jsx (수정된 내용)

import { useMutation, useQueryClient } from '@tanstack/react-query';
import React, { useState } from 'react';

const createDeal = async (newDeal) => {
  const response = await fetch('http://localhost:8080/api/deals', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(newDeal),
  });
  if (!response.ok) {
    throw new Error('게임 등록에 실패했습니다.');
  }
  return response.json();
};

const DealForm = () => {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState({
    title: '', originalPrice: 0, discountPrice: 0, discountPercent: 0, genre: '', description: '', imageUrl: '' 
  });

  // useMutation 훅을 사용하여 POST 요청을 처리
  const mutation = useMutation({
    mutationFn: createDeal,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deals'] }); 
      setFormData({
        title: '', originalPrice: 0, discountPrice: 0, discountPercent: 0, genre: '', description: '', imageUrl: ''
      }); // 폼 초기화
      alert('새로운 게임 딜이 성공적으로 등록되었습니다!');
    },
    onError: (error) => {
      alert(`등록 실패: ${error.message}`);
    },
  });

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      // 숫자 입력은 숫자로 변환
      [name]: type === 'number' ? parseFloat(value) : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
   
    const originalPrice = formData.originalPrice;
    const discountPercent = formData.discountPercent;
    

    const discountPrice = originalPrice * (1 - discountPercent / 100);


    mutation.mutate({ 
        ...formData, 
        discountPrice: discountPrice.toFixed(2), 
        discountPercent: discountPercent 
    });
  };

  // 할인가 미리보기 계산
  const calculatedDiscountPrice = formData.originalPrice > 0 && formData.discountPercent >= 0 
    ? (formData.originalPrice * (1 - formData.discountPercent / 100)).toFixed(2)
    : '0.00';


  return (
        <div className="bg-gray-800 p-6 sm:p-8 rounded-2xl shadow-2xl border-2 border-red-800 mb-10">
            <h3 className="text-2xl sm:text-3xl font-extrabold mb-6 text-red-400 border-b border-red-900 pb-2">
                🎮 새로운 게임 할인 정보 등록
            </h3>
            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
                
                {/* 1. 게임 제목, 장르, 이미지 URL 입력 필드 (기존 스타일 유지) */}
                <input name="title" value={formData.title} onChange={handleChange} placeholder="* 게임 제목 (필수)" required 
                       className="p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-red-400 focus:ring-2 focus:ring-red-400 md:col-span-2" />
                
                <input name="genre" value={formData.genre} onChange={handleChange} placeholder="장르 (예: RPG, 전략)" required 
                       className="p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-red-400" />

                <input name="imageUrl" value={formData.imageUrl} onChange={handleChange} placeholder="이미지 URL (http://...)" 
                       className="p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-red-400" />
                
                {/* 4. 가격 입력 그룹: 명확한 레이블 및 설명 추가 */}
                <div className="md:col-span-2 grid grid-cols-3 gap-4 sm:gap-6 border-t pt-4 border-gray-700 items-start">
                    
                    {/* 정가 입력 필드 */}
                    <div className="flex flex-col space-y-1">
                        <label htmlFor="originalPrice" className="text-sm font-semibold text-gray-400">정가 (Original Price)</label>
                        <input id="originalPrice" name="originalPrice" type="number" value={formData.originalPrice} onChange={handleChange} placeholder="예: 59.99 ($)" required 
                            className="p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-green-400" min="0" step="0.01" />
                        <p className="text-xs text-gray-500">게임의 원래 가격을 입력합니다.</p>
                    </div>

                    {/* 할인율 입력 필드 */}
                    <div className="flex flex-col space-y-1">
                        <label htmlFor="discountPercent" className="text-sm font-semibold text-gray-400">할인율 (Discount %)</label>
                        <input id="discountPercent" name="discountPercent" type="number" value={formData.discountPercent} onChange={handleChange} placeholder="예: 40 (%)" required 
                            className="p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-green-400" min="0" max="100" />
                        <p className="text-xs text-gray-500">0에서 100 사이의 숫자를 입력합니다.</p>
                    </div>
                    
                    {/* 할인가 미리보기 (텍스트만) */}
                    <div className="flex flex-col space-y-1 self-center mt-5 p-3 rounded-lg bg-gray-900 border border-gray-700">
                        <label className="text-sm font-semibold text-gray-400">계산된 할인가</label>
                        <p className="text-xl font-bold text-center text-green-400">
                           ${calculatedDiscountPrice}
                        </p>
                    </div>
                </div>
                
                {/* 5. 설명 */}
                <textarea name="description" value={formData.description} onChange={handleChange} placeholder="* 게임에 대한 자세한 설명" required rows="4" 
                          className="md:col-span-2 p-3 rounded-lg bg-gray-900 text-gray-100 border border-gray-600 focus:border-red-400 transition"></textarea>

                {/* 6. 제출 버튼  */}
                <button type="submit" 
                        disabled={mutation.isPending}
                        className="md:col-span-2 mt-4 bg-red-600 hover:bg-red-700 text-white text-lg font-extrabold py-3 rounded-lg transition shadow-md disabled:bg-gray-500 disabled:cursor-not-allowed">
                    {mutation.isPending ? '⏳ 등록 처리 중...' : '🔥 지금 바로 할인 정보 등록'}
                </button>
            </form>
            {mutation.isError && <p className="md:col-span-2 text-red-300 text-center mt-3">❌ 등록 에러: {mutation.error.message}</p>}
        </div>
  );
};

export default DealForm;