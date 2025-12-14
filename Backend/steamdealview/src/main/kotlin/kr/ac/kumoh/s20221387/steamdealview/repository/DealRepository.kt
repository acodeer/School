package kr.ac.kumoh.s20221387.steamdealview.repository

import kr.ac.kumoh.s20221387.steamdealview.model.Deal
import org.springframework.data.mongodb.repository.MongoRepository
import org.springframework.stereotype.Repository

@Repository
// <대상 모델 클래스, ID 타입>을 지정합니다.
interface DealRepository : MongoRepository<Deal, String> {
    // CRUD 메서드(findAll, findById 등)가 자동으로 제공됩니다.
}