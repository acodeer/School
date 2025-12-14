package kr.ac.kumoh.s20221387.steamdealview.config

import org.springframework.context.annotation.Configuration
import org.springframework.web.servlet.config.annotation.CorsRegistry
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer

@Configuration // Spring 설정 파일임을 명시
class WebConfig : WebMvcConfigurer {

    override fun addCorsMappings(registry: CorsRegistry) {
        // 프론트엔드 개발 서버 주소(http://localhost:5173)에서 오는 모든 요청 허용
        registry.addMapping("/api/**") // '/api'로 시작하는 모든 경로에 적용
            .allowedOrigins("http://localhost:5173") // React 개발 서버 출처
            .allowedMethods("GET", "POST", "PUT", "DELETE") // 모든 CRUD 메서드 허용
            .allowedHeaders("*") // 모든 헤더 허용
    }
}