package kr.ac.kumoh.s20221387.steamdealview.controller


import kr.ac.kumoh.s20221387.steamdealview.model.Deal
import kr.ac.kumoh.s20221387.steamdealview.repository.DealRepository
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

@RestController
@RequestMapping("/api/deals") // 기본 경로 설정

class DealController(
    // 생성자 주입 (Kotlin에서 권장되는 방식)
    private val dealRepository: DealRepository
) {

    // UC-BE-01: 전체 할인 게임 조회 (GET /api/deals)
    @GetMapping
    fun getAllDeals(): List<Deal> {
        // findAll()은 자동으로 List<Deal>을 반환합니다.
        return dealRepository.findAll()
    }

    // UC-BE-02: 특정 할인 게임 상세 조회 (GET /api/deals/{id})
    @GetMapping("/{id}")
    fun getDealById(@PathVariable id: String): ResponseEntity<Deal> {
        val deal = dealRepository.findById(id)

        // Optional<Deal>을 처리하여 데이터가 존재하면 200 OK, 없으면 404 Not Found를 반환
        return if (deal.isPresent) {
            ResponseEntity.ok(deal.get())
        } else {
            ResponseEntity.notFound().build()
        }
    }
    @PostMapping // HTTP POST 요청 처리
    fun createDeal(@RequestBody deal: Deal): ResponseEntity<Deal> {
        val savedDeal = dealRepository.save(deal)
        return ResponseEntity.status(201).body(savedDeal)
    }
    @PutMapping("/{id}") // HTTP PUT 요청 처리
    fun updateDeal(@PathVariable id: String, @RequestBody updatedDeal: Deal): ResponseEntity<Deal> {
        return dealRepository.findById(id).map { existingDeal ->
            val dealToUpdate = existingDeal.copy(
                title = updatedDeal.title,
                originalPrice = updatedDeal.originalPrice,
                discountPrice = updatedDeal.discountPrice,
                discountPercent = updatedDeal.discountPercent,
                genre = updatedDeal.genre,
                description = updatedDeal.description,
                imageUrl = updatedDeal.imageUrl // <-- 이미지 URL 필드 추가
            )
            val savedDeal = dealRepository.save(dealToUpdate)
            ResponseEntity.ok(savedDeal)
        }.orElse(ResponseEntity.notFound().build())
    }
    @DeleteMapping("/{id}") // HTTP DELETE 요청 처리
    fun deleteDeal(@PathVariable id: String): ResponseEntity<Void> {
        // 1. 해당 ID의 Deal이 존재하는지 확인
        return if (dealRepository.existsById(id)) {
            // 2. 존재하면 삭제
            dealRepository.deleteById(id)
            // 3. 204 No Content 반환 (성공적으로 삭제되었으나 반환할 내용이 없음)
            ResponseEntity.noContent().build()
        } else {
            // 4. 없으면 404 Not Found 반환
            ResponseEntity.notFound().build()
        }
    }
}