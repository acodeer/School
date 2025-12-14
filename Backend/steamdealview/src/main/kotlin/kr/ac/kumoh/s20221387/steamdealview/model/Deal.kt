package kr.ac.kumoh.s20221387.steamdealview.model

import org.springframework.data.annotation.Id
import org.springframework.data.mongodb.core.mapping.Document

@Document(collection = "deals") // MongoDB의 'deals' 컬렉션에 매핑
data class Deal(
    @Id // MongoDB의 ObjectId를 매핑. String으로 사용합니다.
    val id: String? = null,
    val title: String,          // 제목
    val originalPrice: Double,  // 정가
    val discountPrice: Double,  // 할인가
    val discountPercent: Int,   // 할인율 (%)
    val genre: String,          // 장르
    val description: String,     // 상세 설명
    val imageUrl: String? = null      // TODO 이미지
)